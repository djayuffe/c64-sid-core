# c64-sid-core

Reusable Python C64/SID emulation-core components: 6502 CPU handling, memory
banking, CIA and VIC-II helpers, SID chip logic, timing, playback, capture,
and analysis primitives. It is a focused library project; use
[c64-sid-py](https://github.com/djayuffe/c64-sid-py) for end-user inspection,
rendering, and export commands.

## Install

```bash
python3 -m pip install .
```

The package has no runtime dependencies beyond the Python standard library.

## Supported API

```python
from pathlib import Path

from c64sid_core import C64System, SidChip, parse_sid_header

header, program = parse_sid_header(Path("music.sid").read_bytes())
system = C64System()
sid = SidChip(header.clockFreq)
```

The package exposes `C64System`, `Cpu6502`, `MachineTiming`, `SidChip`, and
`parse_sid_header`. Lower-level CIA, VIC-II, memory, playback, SID-PRO, and
analysis modules remain available under `c64sid_core` for advanced users.

## Validation

```bash
python3 -m unittest discover -v
ruff check src tests
```

## Layout

| Path | Purpose |
| --- | --- |
| `src/c64sid_core/` | Maintained standalone package |
| `tests/` | Core import, parser, SID, and waveform-resource checks |
| `reference/sid/` | Original imported snapshot retained for provenance |
| `STATUS.md` | Reference snapshot remediation record |

## Intended direction

The maintained package is intentionally separated from the original snapshot.
The reference tree still documents the incoming source and its historical
limitations; it is not imported, packaged, or claimed as supported runtime
code.

## License

No distribution license has been selected. Treat this source as
all-rights-reserved unless the repository owner grants other permission.
