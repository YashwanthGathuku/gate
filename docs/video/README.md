# TheUstad video archive

## Current TheUstad artifact

`theustad-build-week-demo.mp4` is the pending/current Build Week artifact once
generated and rendered. Until that file exists, this index intentionally makes
no claim that a new TheUstad video has been recorded. The planned demonstration
must label the deterministic scripted adversarial rehearsal as scripted and
distinguish it from a live real-project run.

## Historical Gate recordings

The following immutable files, URLs, digests, captions, and honesty labels are
preserved as historical Gate evidence. They are not canonical TheUstad setup
instructions.

### Narrated live real-project comparison

[`gate-real-project-live-narrated.mp4`](gate-real-project-live-narrated.mp4)
is a 175-second, 1920x1080 H.264/AAC recording of authenticated Codex runs
against clean clones of pinned `pytest-dev/iniconfig`. It is not a reconstruction
of earlier console text.

Public YouTube video: https://youtu.be/cAaMzRLyqWQ

```text
SHA-256: AEBC3A31727C3942CCE85D2ED4FCCD5887FD191D51565AF9E0B6068BC806D266
```

Matching captions remain at
[`gate-real-project-live-narrated.en.srt`](gate-real-project-live-narrated.en.srt).
[`gate-real-project-live.mp4`](gate-real-project-live.mp4) remains the original
silent source capture. Its original digest and machine-readable probe remain in
[`../evidence/real_project_video`](../evidence/real_project_video/README.md).

The historical timeline records an ordinary Codex control, historical plugin
installation, a protected child run, `FINAL VERIFIED`, and audit validation.
It was executed in WSL 2 because native Windows historical coding runs failed
closed.

### Original deterministic recording

[`gate-v2-demo.mp4`](gate-v2-demo.mp4) is the original 1 minute 55 second Build
Week recording. It is a 1920x1080 H.264/AAC file:

```text
SHA-256: 93A28FE92FC4827E36F320AFDC72ED281D15AA03492189087F5BE0B0DA391B38
```

Judge-accessible historical upload: https://youtu.be/kGGdz649zCQ

This is a deterministic-fixture submission video. It states that the fake
agent makes the rehearsal deterministic while the edits, deleted test, pytest
executions, historical verdicts, and audit chain are real. It also identifies
the separate live Codex run and its independently verified chain root.

The original public upload remains available at https://youtu.be/njgvvLapxs0.

## Historical rebuild commands

The retained scripts reproduce the historical renders only:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File docs/video/build_live_narrated_demo.ps1
powershell -ExecutionPolicy Bypass -File docs/video/build_demo.ps1
```

Generated intermediate assets remain intentionally ignored under `docs/video/build/`.
