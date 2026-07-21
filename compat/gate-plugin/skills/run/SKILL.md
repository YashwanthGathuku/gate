---
name: run
description: Deprecated Gate alias for running a coding task through TheUstad. Use only when the user invokes $gate:run.
---

# Gate Compatibility Run

Resolve this installed package's absolute root from this SKILL.md, resolve an
absolute Python 3.10+ executable, and invoke:

```text
<absolute-python> <plugin-root>/scripts/gate_plugin.py run --repo <repo> --task-text <task>
```

Pass the user's remaining command options unchanged. Relay the adapter warning,
exit code, verdict, audit log, and audit root exactly.
