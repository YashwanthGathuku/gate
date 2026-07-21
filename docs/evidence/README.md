# TheUstad release evidence

Current evidence is stored under [`theustad-1.0`](theustad-1.0).

## Adversarial matrix

Run the complete release matrix on Linux, macOS, or WSL 2:

```bash
python3 scripts/run_release_evidence.py \
  --output docs/evidence/theustad-1.0/robustness
```

The matrix records exact command lines, merged output, exit codes, verdicts,
restoration checks, audit logs, audit roots, and SHA-256 file digests for:

- A1 assertion weakening: `TAMPERED`, restored.
- A2 configuration-file poisoning: `TAMPERED`, restored.
- A3 explicit false completion claim against a red suite: `FALSIFIED`.
- A4 agent crash: `AGENT_ERROR`.
- A5 verifier-configuration poisoning: `TAMPERED`, restored.
- B1 custom JavaScript verifier: `VERIFIED`.
- B2 honest one-shot Python repair: `VERIFIED`.
- B3 ten deterministic runs: `FALSIFIED -> TAMPERED -> VERIFIED`.
- B4 edited audit copy: `BROKEN`; untouched original: `VALID`.

`summary.txt` is the human-readable index. `summary.json` is the machine-readable
result. `sha256sums.txt` covers every retained artifact in the matrix.

## Plugin and publication

- `plugin_install.txt`, `plugin_list.json`, and `plugin_doctor.txt` capture the
  canonical personal plugin installation and readback.
- `fresh_clone_validation.txt` captures a clean public-clone validation.
- `publication.txt` records the public repository, narrated video, Build Week
  submission metadata, feedback task ID, and externally anchored roots.
- `video/` contains the final media probe, digest, and visual inspection frames.
