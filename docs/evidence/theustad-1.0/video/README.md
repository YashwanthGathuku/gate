# TheUstad 1.0 video evidence

This directory contains independent checks for the narrated Build Week demo:

- `video_probe.json`: final `ffprobe` stream and format metadata.
- `video_sha256.txt`: SHA-256 digest of the final MP4.
- `inspection-005s.png`, `inspection-018s.png`, `inspection-038s.png`,
  `inspection-049s.png`, `inspection-056s.png`, and `inspection-067s.png`:
  fixed review frames across the final render.

The retained artifact has a 1920x1080 H.264 video stream, a non-silent AAC
audio stream, and a duration below three minutes. The deterministic
configuration-poisoning sequence is narrated as a scripted adversarial
rehearsal; the control and plugin runs are identified separately.

The current probe records a 70-second render with video and audio, and
`video_sha256.txt` anchors the exact publication candidate.
