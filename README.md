# c64-sid-core

An independently tracked reference snapshot of Python C64/SID core
components: 6502 CPU handling, C64 memory banking, CIA and VIC-II helpers,
SID chip logic, playback coordination, tracing, and SID-PRO export support.

## Status

This repository intentionally preserves the supplied component snapshot as
source material. It is **not yet a supported, installable package or release
artifact**. The source is kept in `reference/sid/` unchanged apart from
excluding transient local files.

The initial import audit identified these blockers to standalone execution:

- `reference/sid/vic_dma.py` has an `IndentationError` at line 21.
- Several modules expect a parent `logger` package that is absent from this
  snapshot.
- The snapshot has no packaging metadata, test suite, or runtime fixtures.

No release is published until those points are resolved and covered by tests.

## Layout

| Path | Purpose |
| --- | --- |
| `reference/sid/` | Original imported core-component snapshot |
| `STATUS.md` | Scope and next remediation work |

## Intended direction

The project can later become a standalone `c64sid_core` package once imports,
logging, syntax, public API boundaries, tests, and packaging are established.
Until then, use the maintained [c64-sid-py](https://github.com/djayuffe/c64-sid-py)
project for runnable SID inspection, rendering, capture, analysis, and export.

## License

No distribution license has been selected. Treat this source as
all-rights-reserved unless the repository owner grants other permission.
