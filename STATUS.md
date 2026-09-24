# Import status

## Included

- The complete supplied `sid/` source tree, tracked under `reference/sid/`.
- Historical tracing, SID-PRO, CPU, VIC-II, CIA, memory, and playback modules.

## Reference snapshot limitations

- Standalone execution without remediation.
- Hardware-accurate or cycle-exact C64 emulation.
- Compatibility with arbitrary PSID/RSID files.

## Promotion decisions

- `sid_exporter.py` is superseded by the maintained SID-PRO export modules.
- `vic_dma_original.py` is superseded by the maintained VIC-DMA model.
- `sid_names.py`, `trace_recorder.py`, and `sid_dump.py` remain archival
  diagnostics until they have a distinct, tested public API.

## Remediation required before promoting the reference code

1. Repair the `vic_dma.py` syntax error.
2. Supply or replace the missing parent logger contract.
3. Define a non-generic package name and public API.
4. Add parser, CPU, memory, SID, and playback regression tests.
5. Add packaging metadata and verify a clean isolated installation.

The maintained `src/c64sid_core` package is independently validated. This
status document applies only to the preserved imported reference source.
