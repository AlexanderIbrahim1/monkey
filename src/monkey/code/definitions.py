import dataclasses

from monkey.code.code import Opcode
import monkey.code.opcodes as opcodes


@dataclasses.dataclass(frozen=True)
class OpcodeDefinition:
    name: str
    operand_widths: tuple[int, ...]  # number of bytes per operand


UNDEFINED_OPCODE = OpcodeDefinition("UNDEFINED", ())


OPCODE_DEFINITIONS: dict[Opcode, OpcodeDefinition] = {
    opcodes.OPCONSTANT: OpcodeDefinition("OPCONSTANT", (opcodes.OPCONSTANT_WIDTH,)),
    opcodes.OPPOP: OpcodeDefinition("OPPOP", ()),
    opcodes.OPADD: OpcodeDefinition("OPADD", ()),
    opcodes.OPSUB: OpcodeDefinition("OPSUB", ()),
    opcodes.OPMUL: OpcodeDefinition("OPMUL", ()),
    opcodes.OPDIV: OpcodeDefinition("OPDIV", ()),
    opcodes.OPTRUE: OpcodeDefinition("OPTRUE", ()),
    opcodes.OPFALSE: OpcodeDefinition("OPFALSE", ()),
    opcodes.OPEQUAL: OpcodeDefinition("OPEQUAL", ()),
    opcodes.OPNOTEQUAL: OpcodeDefinition("OPNOTEQUAL", ()),
    opcodes.OPGREATERTHAN: OpcodeDefinition("OPGREATERTHAN", ()),
    opcodes.OPMINUS: OpcodeDefinition("OPMINUS", ()),
    opcodes.OPBANG: OpcodeDefinition("OPBANG", ()),
    opcodes.OPJUMP: OpcodeDefinition("OPJUMP", (opcodes.OPJUMP_WIDTH,)),
    opcodes.OPJUMPWHENFALSE: OpcodeDefinition("OPJUMPWHENFALSE", (opcodes.OPJUMPWHENFALSE_WIDTH,)),
    opcodes.OPNULL: OpcodeDefinition("OPNULL", ()),
    opcodes.OPSETGLOBAL: OpcodeDefinition("OPSETGLOBAL", (opcodes.OPSETGLOBAL_WIDTH,)),
    opcodes.OPGETGLOBAL: OpcodeDefinition("OPGETGLOBAL", (opcodes.OPGETGLOBAL_WIDTH,)),
    opcodes.OPARRAY: OpcodeDefinition("OPARRAY", (opcodes.OPARRAY_WIDTH,)),
    opcodes.OPHASH: OpcodeDefinition("OPHASH", (opcodes.OPHASH_WIDTH,)),
}


def lookup_opcode_definition(opcode: Opcode) -> OpcodeDefinition:
    return OPCODE_DEFINITIONS.get(opcode, UNDEFINED_OPCODE)


def is_undefined(definition: OpcodeDefinition) -> bool:
    return definition == UNDEFINED_OPCODE
