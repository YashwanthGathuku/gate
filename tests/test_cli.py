import io
import importlib

import theustad


def test_console_output_escapes_characters_unsupported_by_stream_encoding():
    raw = io.BytesIO()
    stream = io.TextIOWrapper(
        raw,
        encoding="cp1252",
        errors="strict",
        newline="",
    )

    theustad._console_output("before \x9d after", stream=stream)
    stream.flush()

    assert raw.getvalue().decode("cp1252") == "before \\x9d after\n"


def test_canonical_theustad_modules_are_importable():
    cli = importlib.import_module("theustad")
    freezer = importlib.import_module("theustadlib.freezer")

    assert cli.Verdict.VERIFIED.value == "VERIFIED"
    assert "tests/**" in freezer.DEFAULT_PATTERNS
