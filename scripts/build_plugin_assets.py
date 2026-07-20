#!/usr/bin/env python3
"""Generate deterministic Gate plugin PNG assets with the standard library."""

from __future__ import annotations

import struct
import zlib
from pathlib import Path


Color = tuple[int, int, int, int]
BACKGROUND: Color = (16, 23, 29, 255)
BORDER: Color = (51, 70, 79, 255)
GATE_GREEN: Color = (20, 184, 110, 255)
WHITE: Color = (245, 248, 250, 255)


def _chunk(kind: bytes, payload: bytes) -> bytes:
    checksum = zlib.crc32(kind)
    checksum = zlib.crc32(payload, checksum)
    return (
        struct.pack(">I", len(payload))
        + kind
        + payload
        + struct.pack(">I", checksum & 0xFFFFFFFF)
    )


class Canvas:
    def __init__(self, size: int, color: Color):
        self.size = size
        self.pixels = bytearray(color * (size * size))

    def pixel(self, x: int, y: int, color: Color) -> None:
        if 0 <= x < self.size and 0 <= y < self.size:
            offset = (y * self.size + x) * 4
            self.pixels[offset : offset + 4] = bytes(color)

    def rectangle(self, x0: int, y0: int, x1: int, y1: int, color: Color) -> None:
        for y in range(max(0, y0), min(self.size, y1)):
            for x in range(max(0, x0), min(self.size, x1)):
                self.pixel(x, y, color)

    def line(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        width: int,
        color: Color,
    ) -> None:
        x0, y0 = start
        x1, y1 = end
        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1
        dy = -abs(y1 - y0)
        sy = 1 if y0 < y1 else -1
        error = dx + dy
        radius = max(1, width // 2)
        while True:
            self.rectangle(x0 - radius, y0 - radius, x0 + radius, y0 + radius, color)
            if x0 == x1 and y0 == y1:
                break
            doubled = 2 * error
            if doubled >= dy:
                error += dy
                x0 += sx
            if doubled <= dx:
                error += dx
                y0 += sy

    def png(self) -> bytes:
        stride = self.size * 4
        raw = b"".join(
            b"\x00" + bytes(self.pixels[y * stride : (y + 1) * stride])
            for y in range(self.size)
        )
        header = struct.pack(">IIBBBBB", self.size, self.size, 8, 6, 0, 0, 0)
        return (
            b"\x89PNG\r\n\x1a\n"
            + _chunk(b"IHDR", header)
            + _chunk(b"IDAT", zlib.compress(raw, level=9))
            + _chunk(b"IEND", b"")
        )


def _render(size: int) -> bytes:
    canvas = Canvas(size, BACKGROUND)
    margin = round(size * 0.08)
    border = max(1, round(size * 0.012))
    canvas.rectangle(margin, margin, size - margin, margin + border, BORDER)
    canvas.rectangle(margin, size - margin - border, size - margin, size - margin, BORDER)
    canvas.rectangle(margin, margin, margin + border, size - margin, BORDER)
    canvas.rectangle(size - margin - border, margin, size - margin, size - margin, BORDER)

    left = round(size * 0.22)
    right = round(size * 0.78)
    top = round(size * 0.2)
    bottom = round(size * 0.82)
    gate_width = max(4, round(size * 0.075))
    canvas.rectangle(left, top, left + gate_width, bottom, GATE_GREEN)
    canvas.rectangle(right - gate_width, top, right, bottom, GATE_GREEN)
    canvas.rectangle(left, top, right, top + gate_width, GATE_GREEN)

    check_width = max(4, round(size * 0.055))
    canvas.line(
        (round(size * 0.36), round(size * 0.57)),
        (round(size * 0.48), round(size * 0.69)),
        check_width,
        WHITE,
    )
    canvas.line(
        (round(size * 0.48), round(size * 0.69)),
        (round(size * 0.68), round(size * 0.43)),
        check_width,
        WHITE,
    )
    return canvas.png()


def build_assets(output_dir: Path) -> None:
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "icon.png").write_bytes(_render(128))
    (destination / "logo.png").write_bytes(_render(512))


def main() -> int:
    build_assets(Path(__file__).resolve().parents[1] / "assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
