import io
import importlib

import theustad
from theustad import _protected_patterns, build_parser
from theustadlib.freezer import DEFAULT_PATTERNS


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


def test_protect_add_appends_to_defaults_without_removing_them():
    assert _protected_patterns(None, [["package.json"], ["vitest.config.js"]]) == (
        *DEFAULT_PATTERNS,
        "package.json",
        "vitest.config.js",
    )


def test_protect_override_remains_exact_and_can_accept_additions():
    assert _protected_patterns([["spec/**"]], [["package.json"]]) == (
        "spec/**",
        "package.json",
    )


def test_parser_accepts_repeatable_protect_add():
    args = build_parser().parse_args(
        [
            "--repo",
            ".",
            "--protect-add",
            "package.json",
            "--protect-add",
            "vite.config.js",
        ]
    )
    assert args.protect_add == [["package.json"], ["vite.config.js"]]
