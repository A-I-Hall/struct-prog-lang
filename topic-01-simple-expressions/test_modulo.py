from pprint import pprint
import os
import sys

# Friendly test file that shows AST + evaluator results so you can see
# what's happening step-by-step. Less formal comments all over, so it's
# easy to scan and follow during debugging.

# Make sure imports resolve when running from the repo root
sys.path.insert(0, os.path.dirname(__file__))

import tokenizer
import parser
import evaluator


# A small set of expressions to check common and edge cases for `%`
tests = [
    {"expr": "3+4"},
    {"expr": "3-5"},
    {"expr": "3*4+5"},
    {"expr": "10/4"},
    {"expr": "5%2"},
    {"expr": "4%2"},
    # negative-dividend examples so we can compare Python vs C-like behavior
    {"expr": "(0-3)%2", "c_left": "(0-3)", "c_right": "2"},
    {"expr": "(0-5+2)%3", "c_left": "(0-5+2)", "c_right": "3"},
    {"expr": "(0-7)%4", "c_left": "(0-7)", "c_right": "4"},
]


def almost_equal(a, b, tol=1e-9):
    # tiny helper to compare floats/int safely
    try:
        return abs(a - b) <= tol
    except Exception:
        return a == b


def compute_c_style_remainder(a, b):
    # C-like remainder (trunc toward zero): r = a - trunc(a/b) * b
    # This can be negative when a is negative, which differs from Python's `%`.
    return a - int(a / b) * b


def run_tests():
    passed = 0
    failed = 0
    print("Running tests — I'll print ASTs, results, and useful comparisons:\n")
    for t in tests:
        expr = t["expr"]
        print(f"Expression: {expr}")
        try:
            # tokenize and parse the expression
            toks = tokenizer.tokenize(expr)
            ast, rem = parser.parse_expression(toks)

            print("AST:")
            pprint(ast)  # show the tree so you can see precedence/structure

            # evaluate using the project evaluator
            result = evaluator.evaluate(ast)

            # Python's eval is what our evaluator currently mirrors for `%`
            expected_py = eval(expr)

            print(f"Result (evaluator): {result!r}")
            print(f"Expected (Python eval): {expected_py!r}")

            # show C-style remainder so you get the full picture for negatives
            if "c_left" in t and "c_right" in t:
                left_val = int(eval(t["c_left"]))
                right_val = int(eval(t["c_right"]))
                expected_c = compute_c_style_remainder(left_val, right_val)
                print(f"Expected (C-like remainder): {expected_c!r} (left={left_val}, right={right_val})")

            ok = almost_equal(result, expected_py)
            print("PASS" if ok else "FAIL")
            print("-")
            if ok:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            # show the exception; this helps track syntax/parse/runtime errors
            print(f"ERROR while testing {expr}: {e}")
            failed += 1
            print("-")

    print(f"Summary: passed={passed}, failed={failed}")


if __name__ == "__main__":
    run_tests()
