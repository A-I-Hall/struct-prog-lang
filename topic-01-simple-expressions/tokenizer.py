import re
from pprint import pprint



patterns = [
    (r"\s+", "whitespace"),
    (r"\d+", "number"),
    (r"\+", "+"),
    (r"\-", "-"),
    (r"\/", "/"),
    (r"\*", "*"),
    (r"%", "%"),
    (r"\(", "("),
    (r"\)", ")"),
    (r".", "error"),
]

patterns = [(re.compile(p), tag) for p, tag in patterns]


def tokenize(characters):
    "Tokenize a string using the patterns above"
    tokens = []
    position = 0
    line = 1
    column = 1
    current_tag = None

    while position < len(characters):
        # try each pattern at the current position until one matches
        for pattern, tag in patterns:
            match = pattern.match(characters, position)
            if match:
                # found something - remember its tag
                current_tag = tag
                break
        assert match is not None
        value = match.group(0)

        # if nothing matched in our patterns (shouldn't happen because of '.'),
        # we raise a helpful exception mentioning the unexpected character.
        if current_tag == "error":
            raise Exception(f"Unexpected character: {value!r}")

        # skip whitespace tokens — they're not useful for parsing
        if tag != "whitespace":
            # build a token dict — numbers also carry their integer value
            token = {"tag": current_tag, "line": line, "column": column}
            if current_tag == "number":
                token["value"] = int(value)
            tokens.append(token)

        # advance position and update line/column
        for ch in value:
            if ch == "\n":
                line += 1
                column = 1
            else:
                column += 1
        position = match.end()

    # sentinel token marking end of input
    tokens.append({"tag": None, "line": line, "column": column})
    return tokens


def test_digits():
    print("test tokenize digits")
    t = tokenize("123")
    assert t[0]["tag"] == "number"
    assert t[0]["value"] == 123
    assert t[1]["tag"] is None
    t = tokenize("1")
    assert t[0]["tag"] == "number"
    assert t[0]["value"] == 1
    assert t[1]["tag"] is None


def test_operators():
    print("test tokenize operators")
    t = tokenize("+ - * / % ( )")
    tags = [tok["tag"] for tok in t]
    assert tags == ["+", "-", "*", "/", "%", "(", ")", None]


def test_expressions():
    print("test tokenize expressions")
    t = tokenize("1+222*3")
    assert t[0]["tag"] == "number" and t[0]["value"] == 1
    assert t[1]["tag"] == "+"
    assert t[2]["tag"] == "number" and t[2]["value"] == 222
    assert t[3]["tag"] == "*"
    assert t[4]["tag"] == "number" and t[4]["value"] == 3
    assert t[5]["tag"] is None


def test_whitespace():
    print("test tokenize whitespace")
    t = tokenize("1 +\t2  \n*    3")
    assert t[0]["tag"] == "number" and t[0]["value"] == 1
    assert t[1]["tag"] == "+"
    assert t[2]["tag"] == "number" and t[2]["value"] == 2
    assert t[3]["tag"] == "*"
    assert t[4]["tag"] == "number" and t[4]["value"] == 3
    assert t[5]["tag"] is None


def test_error():
    print("test tokenize error")
    try:
        t = tokenize("1@@@ +\t2  \n*    3")
    except Exception as e:
        assert str(e) == "Unexpected character: '@'"
        return
    assert Exception("Error did not happen.")


if __name__ == "__main__":
    test_digits()
    test_operators()
    test_expressions()
    test_whitespace()
    test_error()
    print("done.")
