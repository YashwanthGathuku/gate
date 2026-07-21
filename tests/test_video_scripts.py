import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VIDEO = ROOT / "docs" / "video"


def read_script(name):
    return (VIDEO / name).read_text(encoding="utf-8")


def test_narrated_demo_has_required_claims_and_captions():
    transcript = read_script("theustad-build-week-demo-transcript.txt")
    captions = read_script("theustad-build-week-demo.en.srt")

    required_claims = (
        "claim, not proof",
        "pinned open-source project",
        "one Codex plugin",
        "outside the target repository",
        "resumes that exact child",
        "does not mean all software is universally correct",
        "deterministic adversarial rehearsal",
        "reports TAMPERED",
        "copied audit record makes validation BROKEN",
        "externally anchored root",
        "Codex with GPT-5.6",
    )
    for claim in required_claims:
        assert claim in transcript
        assert claim in captions


def test_narrated_demo_probe_and_checksum_match_artifact():
    artifact = VIDEO / "theustad-build-week-demo.mp4"
    evidence = ROOT / "docs" / "evidence" / "theustad-1.0" / "video"
    probe = json.loads((evidence / "video_probe.json").read_text(encoding="utf-8"))
    streams = {stream["codec_type"]: stream for stream in probe["streams"]}

    assert float(probe["format"]["duration"]) < 180
    assert streams["video"]["codec_name"] == "h264"
    assert (streams["video"]["width"], streams["video"]["height"]) == (1920, 1080)
    assert streams["audio"]["codec_name"] == "aac"
    assert streams["audio"]["channels"] >= 1

    expected = (evidence / "video_sha256.txt").read_text(encoding="utf-8").split()[0]
    actual = hashlib.sha256(artifact.read_bytes()).hexdigest().upper()
    assert re.fullmatch(r"[0-9A-F]{64}", expected)
    assert actual == expected
