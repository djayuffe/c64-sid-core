from __future__ import annotations

import math
import tempfile
import unittest
import zlib
from pathlib import Path

from c64sid_core import C64System, SidChip, __version__, parse_sid_header
from c64sid_core.analysis.bpm_detector import BPMDetector
from c64sid_core.analysis.pattern_finder import PatternFinder
from c64sid_core.playback.seeking import SeekEngine
from c64sid_core.resid_lut import load_combined_waveform_table
from c64sid_core.sidpro_binary import CHUNK_EOF, MAGIC, export_to_binary, load_from_binary
from c64sid_core.sidpro_forensic import SIDProForensicExport
from c64sid_core.sid_types import C64Config


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

    def test_system_interrupts_and_calls(self) -> None:
        system = C64System()
        system.memory.cia1.irqLine = True
        system._poll_irqs()
        system.memory.cia2.irqLine = True
        system._poll_irqs()
        self.assertEqual([event.type for event in system._pending_irqs], ["IRQ", "NMI"])

        call_system = C64System()
        call_system.cpu.pc = 0x2000
        call_system.memory.ram[0x1000] = 0x60  # RTS
        elapsed = call_system.call(0x1000, max_cycles=32)
        self.assertLess(elapsed, 32)
        self.assertEqual(call_system.cpu.pc, 0x2000)

    def test_parser_rejects_invalid_data_offset(self) -> None:
        raw = bytearray(minimal_sid())
        raw[6:8] = (0xFFFF).to_bytes(2, "big")
        with self.assertRaises(ValueError):
            parse_sid_header(bytes(raw))

    def test_sidpro_binary_round_trip_and_validation(self) -> None:
        export = SIDProForensicExport()
        export.set_metadata_config(
            title="Test", author="", released="", clock_hz=985_248,
            standard="PAL", sid_count=1, sid_models=["6581"], sid_bases=[0xD400],
            sample_rate=44_100, frame_rate=50, song=1,
        )
        export.set_bus_stream(cycles_f64=b"\x00" * 8, events_u8=bytes([0, 1, 2]))
        export.set_ram_snapshots(ram_initial=b"\x00" * 65_536, ram_final=b"\x01" * 65_536)
        export.telemetry["frames"].append({"cycle": 0, "chips": []})
        with tempfile.TemporaryDirectory() as directory:
            capture = Path(directory) / "capture.sidprob"
            export_to_binary(export.export_to_dict(compress=False), str(capture))
            loaded = load_from_binary(str(capture))
            self.assertEqual(loaded["_bus_events_decoded"], [(0.0, 0, 1, 2)])

            malformed = Path(directory) / "malformed.sidprob"
            malformed.write_bytes(
                MAGIC
                + bytes([CHUNK_EOF, 0])
                + (1).to_bytes(4, "little")
                + zlib.crc32(b"x").to_bytes(4, "little")
                + b"x"
            )
            with self.assertRaises(ValueError):
                load_from_binary(str(malformed))

    def test_analysis_and_seeking_helpers(self) -> None:
        export = SIDProForensicExport()
        export.metadata["config"] = {"clock_hz": 1_000}
        frames = []
        for onset in range(10):
            cycle = onset * 500
            frames.extend([
                {"frame": cycle, "cycle": cycle, "chips": [{"voices": [{"derived": {"gate": True}}]}]},
                {"frame": cycle + 100, "cycle": cycle + 100, "chips": [{"voices": [{"derived": {"gate": False}}]}]},
            ])
        export.telemetry["frames"] = frames
        self.assertEqual(BPMDetector.detect(export)["bpm"], 120.0)
        self.assertEqual(PatternFinder.find_loops(export), PatternFinder.find_loops(export))
        self.assertEqual(SeekEngine.find_nearest_frame(export, 250), 1)

    def test_voice_mix_is_not_doubled(self) -> None:
        sid = SidChip(985_248, C64Config())
        sid.env[1] = 255
        sid.regs[0x0B] = 0x20
        sid.regs[0x08] = 0xFF
        sid.regs[0x18] = 0x0F
        sid.phase[1] = 0xFFFFFF
        self.assertAlmostEqual(sid.render_sample(), 1.0 / 3.0, places=4)


if __name__ == "__main__":
    unittest.main()
