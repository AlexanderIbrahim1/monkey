"""
This script takes the bytecode file that results from compiling monkey source code,
and runs it using a virtual machine.
"""

import argparse
import sys
from typing import Optional
from typing import Sequence

from pathlib import Path

from monkey.serialize.constants import MONKEY_BYTECODE_FILE_SUFFIX
from monkey.serialize.serialize import deserialize_bytecode
from monkey.compiler import Bytecode
import monkey.virtual_machine as vm


def run_virtual_machine(executable_file: Path | str) -> None:
    bytecode: Bytecode = deserialize_bytecode(executable_file)
    machine = vm.VirtualMachine(bytecode)
    vm.run(machine)


def main(argv: Optional[Sequence[str]] = None) -> int:
    usage_message = "usage: python execute.py <bytecode_file>"

    parser = argparse.ArgumentParser(usage=usage_message)
    parser.add_argument("bytecode_filename", type=str, help="compiled monkey bytecode file")

    args = parser.parse_args(argv)

    bytecode_filename = Path(args.bytecode_filename)
    if bytecode_filename.suffix != MONKEY_BYTECODE_FILE_SUFFIX:
        raise RuntimeError(
            f"This compiler requires the bytecode file to end in `{MONKEY_BYTECODE_FILE_SUFFIX}`."
        )

    run_virtual_machine(bytecode_filename)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
