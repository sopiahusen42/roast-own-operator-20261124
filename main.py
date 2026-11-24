"""Entry writer for the make.fun bounty "Roast Your Own Operator in One Line".

Emits exactly one line of at most 140 characters roasting the operator, plus a
single trailing newline, to entry.txt under $MAKEFUN_OUTPUT_DIR (default
/output). Standard library only and fully deterministic: no clock, no
randomness, identical bytes on every run.
"""

import os
import sys

ENTRY = "He renamed the folder final_FINAL_actually_final, then asked me to find the bug inside it. I found him instead."

MAX_CODE_POINTS = 140


def validate_entry(text, max_len=MAX_CODE_POINTS):
    """Return an error string if text is not a valid entry, else None."""
    if not isinstance(text, str):
        return "not a string"
    if not text.strip():
        return "blank after strip"
    if "\n" in text or "\r" in text:
        return "contains a line break; must be one line"
    if text != text.strip():
        return "leading or trailing whitespace"
    if not 1 <= len(text) <= max_len:
        return "length %d code points outside 1..%d" % (len(text), max_len)
    return None


def main():
    error = validate_entry(ENTRY)
    if error is not None:
        print("invalid entry: " + error, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")

    payload = ENTRY + chr(10)
    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(payload)

    with open(out_path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != payload:
        print("write verification failed: bytes on disk differ from entry", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
