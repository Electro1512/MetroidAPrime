import os
import struct
from typing import List
import zipfile
from worlds.Files import APContainer
import py_randomprime

from .MetroidPrimeInterface import GAMES, HUD_MESSAGE_DURATION


class MetroidPrimeContainer(APContainer):
    game: str = 'Metroid Prime'

    def __init__(self, config_json: str, outfile_name: str, output_directory: str,
                 player=None, player_name: str = "", server: str = ""):
        self.config_json = config_json
        self.config_path = "config.json"
        container_path = os.path.join(output_directory, outfile_name + ".apmp1")
        super().__init__(container_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        opened_zipfile.writestr(self.config_path, self.config_json)
        super().write_contents(opened_zipfile)


def construct_hud_message_patch(game_version: str) -> List[int]:
    from ppc_asm.assembler.ppc import addi, bl, li, lwz, r1, r3, r4, r5, r6, r31, stw, cmpwi, bne, mtspr, blr, lmw, r0, LR, stwu, mfspr, or_, lbz, stmw, stb, lis, r7, r9, nop, ori, GeneralRegister
    from ppc_asm import assembler
    symbols = py_randomprime.symbols_for_version(game_version)

    # UpdateHintState is 0x1BC in length, 111 instructions
    num_preserved_registers = 2
    num_required_instructions = 111
    instruction_size = 4
    block_size = 32
    patch_stack_length = 0x30 + (num_preserved_registers * instruction_size)
    instructions: List = [
        stwu(r1, -(patch_stack_length - instruction_size), r1),
        mfspr(r0, LR),
        stw(r0, patch_stack_length, r1),
        stmw(GeneralRegister(block_size - num_preserved_registers), patch_stack_length - instruction_size - num_preserved_registers * instruction_size, r1),
        or_(r31, r3, r3),

        # Check if trigger is set
        lis(r6, GAMES[game_version]["HUD_TRIGGER_ADDRESS"] >> 16),  # Load upper 16 bits of address
        ori(r6, r6, GAMES[game_version]["HUD_TRIGGER_ADDRESS"] & 0xFFFF),  # Load lower 16 bits of address
        lbz(r5, 0, r6),

        cmpwi(r5, 1),
        bne('early_return'),

        # If trigger is set then reset it to 0
        li(r5, 0),
        stb(r5, 0, r6),

        # Prep function arguments
        lis(r5, struct.unpack('<I', struct.pack('<f', HUD_MESSAGE_DURATION))[0] >> 16),  # Float duration to show message
        li(r6, 0x0),
        li(r7, 0x1),
        li(r9, 0x9),
        stw(r5, 0x10, r1),
        stb(r7, 0x14, r1),
        stb(r6, 0x15, r1),
        stb(r6, 0x16, r1),
        stb(r7, 0x17, r1),
        stw(r9, 0x18, r1),
        addi(r3, r1, 0x1C),
        lis(r4, GAMES[game_version]["HUD_MESSAGE_ADDRESS"] >> 16),  # Load upper 16 bits of message address
        ori(r4, r4, GAMES[game_version]["HUD_MESSAGE_ADDRESS"] & 0xFFFF),  # Load lower 16 bits of message address
        bl(symbols["wstring_l__4rstlFPCw"]),
        addi(r4, r1, 0x10),

        # Call function
        bl(symbols["DisplayHudMemo__9CSamusHudFRC7wstringRC12SHudMemoInfo"]),

        lmw(GeneralRegister(block_size - num_preserved_registers), patch_stack_length - instruction_size - num_preserved_registers * instruction_size, r1).with_label('early_return'),
        lwz(r0, patch_stack_length, r1),
        mtspr(LR, r0),
        addi(r1, r1, patch_stack_length - instruction_size),
        blr()
    ]

    # Fill remaining instructions with nops
    while len(instructions) < num_required_instructions:
        instructions.append(nop())

    return list(
        assembler.assemble_instructions(
            symbols["UpdateHintState__13CStateManagerFf"], instructions,
            symbols=symbols
        )
    )
