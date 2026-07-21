from pathlib import Path

import pytest

from theustadlib import events


SCHEMA_SAMPLES = Path(__file__).parents[1] / "docs" / "schema_samples.jsonl"


def test_parse_line_returns_json_object():
    assert events.parse_line('{"type":"turn.started"}') == {
        "type": "turn.started"
    }


def test_parse_line_tolerates_malformed_and_non_object_json():
    assert events.parse_line("not json") is None
    assert events.parse_line("") is None
    assert events.parse_line('["valid", "but", "not", "an", "event"]') is None
    assert events.parse_line('"also not an event"') is None


@pytest.mark.parametrize(
    ("event", "expected"),
    [
        (
            {
                "type": "item.completed",
                "item": {"type": "agent_message", "text": "item text"},
            },
            "item text",
        ),
        (
            {"msg": {"type": "agent_message", "message": "msg text"}},
            "msg text",
        ),
        ({"type": "agent_message", "text": "top-level text"}, "top-level text"),
        (
            {"type": "agent_message", "message": "top-level message"},
            "top-level message",
        ),
        ({"type": "agent_message", "content": "content text"}, "content text"),
        (
            {
                "type": "agent_message",
                "content": [{"text": "first"}, {"text": "second"}],
            },
            "first\nsecond",
        ),
        (
            {
                "msg": {
                    "type": "agent_message",
                    "message": {"content": [{"text": "nested block"}]},
                }
            },
            "nested block",
        ),
    ],
)
def test_extract_agent_text_supports_documented_schemas(event, expected):
    assert events.extract_agent_text(event) == expected


@pytest.mark.parametrize(
    "event",
    [
        {"type": "turn.started"},
        {"type": "item.completed", "item": {"type": "error", "message": "no"}},
        {"msg": {"type": "command_execution", "message": "no"}},
        {"type": "agent_message", "content": [{"kind": "image"}]},
    ],
)
def test_extract_agent_text_ignores_events_without_agent_text(event):
    assert events.extract_agent_text(event) is None


@pytest.mark.parametrize(
    ("event", "expected"),
    [
        ({"thread_id": "thread-top"}, "thread-top"),
        ({"session_id": "session-top"}, "session-top"),
        ({"msg": {"thread_id": "thread-msg"}}, "thread-msg"),
        ({"msg": {"session_id": "session-msg"}}, "session-msg"),
        (
            {"thread_id": "preferred", "session_id": "fallback"},
            "preferred",
        ),
        (
            {"session_id": "top", "msg": {"thread_id": "nested"}},
            "top",
        ),
    ],
)
def test_extract_thread_id_supports_thread_and_session_fields(event, expected):
    assert events.extract_thread_id(event) == expected


@pytest.mark.parametrize(
    "event",
    [{}, {"thread_id": 123}, {"session_id": ""}, {"msg": "not an object"}],
)
def test_extract_thread_id_ignores_missing_or_invalid_values(event):
    assert events.extract_thread_id(event) is None


def test_describe_surfaces_commands_files_and_generic_event_types():
    command_event = {
        "type": "item.completed",
        "item": {
            "type": "command_execution",
            "command": "python -m pytest tests -q",
        },
    }
    file_event = {
        "type": "item.completed",
        "item": {
            "type": "file_change",
            "changes": [
                {"path": "theustadlib/events.py", "kind": "update"},
                {"path": "tests/test_events.py", "kind": "create"},
            ],
        },
    }

    assert events.describe(command_event) == "command: python -m pytest tests -q"
    assert events.describe(file_event) == (
        "files: theustadlib/events.py, tests/test_events.py"
    )
    assert events.describe({"type": "turn.started"}) == "turn.started"
    assert events.describe({}) == "event"


def test_describe_compacts_multiline_commands():
    event = {
        "type": "item.started",
        "item": {"type": "command_execution", "command": "python  -m\npytest -q"},
    }

    assert events.describe(event) == "command: python -m pytest -q"


def test_recorded_schema_samples_are_supported():
    parsed = [
        events.parse_line(line) for line in SCHEMA_SAMPLES.read_text().splitlines()
    ]

    assert all(event is not None for event in parsed)
    assert [event["type"] for event in parsed] == [
        "thread.started",
        "turn.started",
        "item.completed",
        "item.completed",
        "turn.completed",
    ]
    assert [events.extract_thread_id(event) for event in parsed] == [
        "019f7562-4c64-7712-aec5-1bea8cdd37c4",
        None,
        None,
        None,
        None,
    ]
    assert [
        text
        for event in parsed
        if (text := events.extract_agent_text(event)) is not None
    ] == ["GATE_SCHEMA_PING"]
    assert all(events.describe(event) for event in parsed)
