"""
This script takes the compiled bytecode output from the compiler, and displays its contents
to users.
"""

import argparse
import sys
from typing import Optional
from typing import Sequence

from pathlib import Path

from monkey.serialize.constants import MONKEY_BYTECODE_FILE_SUFFIX
from monkey.serialize.serialize import deserialize_bytecode
from monkey.compiler import Bytecode
import monkey.code as code
import monkey.object as objs

DIVIDER_LINE_SIZE = 32
DIVIDER_LINE = "-" * DIVIDER_LINE_SIZE

INDEX_CONSTANT_SEPARATOR = ": "
CONSTANT_PADDING_SIZE = 5
INDEX_PADDING_SIZE = CONSTANT_PADDING_SIZE - len(INDEX_CONSTANT_SEPARATOR)
CONSTANT_PADDING = " " * CONSTANT_PADDING_SIZE


def main(argv: Optional[Sequence[str]] = None) -> int:
    usage_message = "usage: python display_bytecode.py <bytecode_file>"

    parser = argparse.ArgumentParser(usage=usage_message)
    parser.add_argument("bytecode_filename", type=str, help="compiled monkey bytecode file")

    args = parser.parse_args(argv)

    bytecode_filename = Path(args.bytecode_filename)
    if bytecode_filename.suffix != MONKEY_BYTECODE_FILE_SUFFIX:
        raise RuntimeError(
            f"This compiler requires the bytecode file to end in `{MONKEY_BYTECODE_FILE_SUFFIX}`."
        )

    bytecode: Bytecode = deserialize_bytecode(bytecode_filename)
    _pretty_print_bytecode(bytecode)

    return 0


def _pretty_print_bytecode(bytecode: Bytecode) -> None:
    print("INSTRUCTIONS")
    print(DIVIDER_LINE)
    print(code.instructions_to_string(bytecode.instructions))

    print("\nCONSTANTS")
    print(DIVIDER_LINE)
    for i, constant in enumerate(bytecode.constants):
        padded_constant_output = _padded_constant(constant, CONSTANT_PADDING)
        print(f"{i: <{INDEX_PADDING_SIZE}}{INDEX_CONSTANT_SEPARATOR}{padded_constant_output}")


def _padded_constant(constant: objs.Object, padding: str) -> str:
    output = str(constant)
    padded_output = output.replace("\n", f"\n{padding}")

    return padded_output


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
