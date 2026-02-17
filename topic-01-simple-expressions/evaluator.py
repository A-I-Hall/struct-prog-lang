import parser, tokenizer


def evaluate(ast):
    # evaluate the AST recursively. each node is a dict with `tag`.
    if ast["tag"] == "number":
        # base case: number nodes just return their value
        return ast["value"]
    elif ast["tag"] == "+":
        # add left and right
        return evaluate(ast["left"]) + evaluate(ast["right"])
    elif ast["tag"] == "-":
        # subtraction
        return evaluate(ast["left"]) - evaluate(ast["right"])
    elif ast["tag"] == "*":
        # multiplication
        return evaluate(ast["left"]) * evaluate(ast["right"])
    elif ast["tag"] == "/":
        # division (note: Python does float division)
        return evaluate(ast["left"]) / evaluate(ast["right"])
    elif ast["tag"] == "%":
        # modulo — follows Python semantics (remainder has sign of divisor)
        # if you want C-like behavior (remainder follows dividend), we can
        # change this to: a - int(a/b) * b
        return evaluate(ast["left"]) % evaluate(ast["right"])
    else:
        raise ValueError(f"Unknown AST node: {ast}")

def test_evaluate():
    print("test evaluate()")
    ast = {"tag": "number", "value": 3}
    assert evaluate(ast) == 3
    ast = {
        "tag": "+",
        "left": {"tag": "number", "value": 3},
        "right": {"tag": "number", "value": 4},
    }
    assert evaluate(ast) == 7
    ast = {
        "tag": "*",
        "left": {
            "tag": "+",
            "left": {"tag": "number", "value": 3},
            "right": {"tag": "number", "value": 4},
        },
        "right": {"tag": "number", "value": 5},
    }
    assert evaluate(ast) == 35
    tokens = tokenizer.tokenize("3*(4+5)")
    ast, tokens = parser.parse_expression(tokens)
    assert evaluate(ast) == 27
    tokens = tokenizer.tokenize("5%2")
    ast, tokens = parser.parse_expression(tokens)
    assert evaluate(ast) == 1

if __name__ == "__main__":
    test_evaluate()
    print("done.")
