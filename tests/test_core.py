from __future__ import annotations

import math
import unittest

from c64sid_core import C64System, SidChip, __version__, parse_sid_header
from c64sid_core.resid_lut import load_combined_waveform_table


def minimal_sid() -> bytes:
    raw = bytearray(0x77)
    raw[0:4] = b"PSID"
    raw[4:6] = (1).to_bytes(2, "big")
    raw[6:8] = (0x76).to_bytes(2, "big")
    raw[8:10] = (0x1000).to_bytes(2, "big")
    raw[10:12] = (0x1000).to_bytes(2, "big")
    raw[14:16] = (1).to_bytes(2, "big")
    raw[16:18] = (1).to_bytes(2, "big")
    raw[0x76] = 0x60  # RTS
    return bytes(raw)


class CoreTests(unittest.TestCase):
    def test_public_api_and_system_construct(self) -> None:
        self.assertEqual(__version__, "0.1.0")
        system = C64System()
        self.assertEqual(len(system.memory.ram), 65_536)

    def test_parser_and_sid_render_path(self) -> None:
        header, payload = parse_sid_header(minimal_sid())
        self.assertEqual((header.magic, header.loadAddress, payload), ("PSID", 0x1000, b"\x60"))

        sid = SidChip(985_248)
        sid.write(0x18, 0x0F)
        sid.write(0x04, 0x21)
        sid.update(100)
        self.assertTrue(math.isfinite(sid.render_sample()))

    def test_bundled_combined_waveform_resources_load(self) -> None:
        self.assertEqual(len(load_combined_waveform_table("6581", 0x30)), 4096)
        self.assertEqual(len(load_combined_waveform_table("8580", 0x70)), 4096)


if __name__ == "__main__":
    unittest.main()
