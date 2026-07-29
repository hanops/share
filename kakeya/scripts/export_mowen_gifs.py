#!/usr/bin/env python3
"""Export self-contained Kakeya animations sized for MoWen notes."""

from __future__ import annotations

import math
import random
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFont


W, H = 720, 960
GIF_OUTPUT_W, GIF_OUTPUT_H = 1200, 1600
TIMELINE_OUTPUT_W = 1440
RENDER_SCALE = 3
FPS = 10
FRAMES = 36
THREE_MAIN_FRAMES = 64
THREE_MAIN_FPS = 8
OUT = Path(__file__).resolve().parents[1] / "output" / "mowen"

BG = "#1A1714"
PANEL = "#211E1A"
PANEL_2 = "#28231E"
INK = "#F5EDE3"
MUTED = "#B8A998"
DIM = "#786C60"
LINE = "#4A4037"
CORAL = "#FF6B4A"
CORAL_2 = "#FF9A7A"
JADE = "#5EC4A0"
JADE_2 = "#8EDFC4"
ROSE = "#E85D75"
GREEN = "#6BCB8B"

FONT_CJK = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_CJK_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"
FONT_MONO = "/System/Library/Fonts/SFNSMono.ttf"


def font(size: int, mono: bool = False, light: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_MONO if mono else (FONT_CJK_LIGHT if light else FONT_CJK)
    return ImageFont.truetype(path, size)


F10 = font(18, mono=True)
F12 = font(22, light=True)
F14 = font(26)
F18 = font(34)
F24 = font(46)
F32 = font(60)
F_TIMELINE_YEAR = font(34, mono=True)
F_TIMELINE_TAG = font(16, light=True)


class ScaledDraw:
    """Draw in 720×960 logical coordinates on a supersampled canvas."""

    def __init__(self, image: Image.Image):
        self.draw = ImageDraw.Draw(image, "RGBA")

    @staticmethod
    def _xy(value):
        if isinstance(value, (tuple, list)):
            return type(value)(ScaledDraw._xy(item) for item in value)
        return value * RENDER_SCALE

    @staticmethod
    def _font(value: ImageFont.FreeTypeFont) -> ImageFont.FreeTypeFont:
        return value.font_variant(size=round(value.size * RENDER_SCALE))

    def ellipse(self, xy, **kwargs) -> None:
        if "width" in kwargs:
            kwargs["width"] *= RENDER_SCALE
        self.draw.ellipse(self._xy(xy), **kwargs)

    def line(self, xy, **kwargs) -> None:
        if "width" in kwargs:
            kwargs["width"] *= RENDER_SCALE
        self.draw.line(self._xy(xy), **kwargs)

    def pieslice(self, xy, start, end, **kwargs) -> None:
        if "width" in kwargs:
            kwargs["width"] *= RENDER_SCALE
        self.draw.pieslice(self._xy(xy), start, end, **kwargs)

    def polygon(self, xy, **kwargs) -> None:
        if "width" in kwargs:
            kwargs["width"] *= RENDER_SCALE
        self.draw.polygon(self._xy(xy), **kwargs)

    def rounded_rectangle(self, xy, radius=0, **kwargs) -> None:
        if "width" in kwargs:
            kwargs["width"] *= RENDER_SCALE
        self.draw.rounded_rectangle(
            self._xy(xy),
            radius=radius * RENDER_SCALE,
            **kwargs,
        )

    def text(self, xy, text, font, **kwargs) -> None:
        if "stroke_width" in kwargs:
            kwargs["stroke_width"] *= RENDER_SCALE
        self.draw.text(self._xy(xy), text, font=self._font(font), **kwargs)


def rgba(hex_color: str, alpha: int) -> tuple[int, int, int, int]:
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def ease(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def mix(a: tuple[float, float], b: tuple[float, float], t: float) -> tuple[float, float]:
    return a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t


def base_frame(scene: str, title: str, subtitle: str, progress: float) -> tuple[Image.Image, ScaledDraw]:
    im = Image.new("RGB", (W * RENDER_SCALE, H * RENDER_SCALE), BG)
    d = ScaledDraw(im)

    # Fixed ambient texture keeps GIF compression efficient.
    rng = random.Random(1917)
    for _ in range(54):
        x, y = rng.randrange(W), rng.randrange(H)
        r = rng.choice((1, 1, 2))
        d.ellipse((x - r, y - r, x + r, y + r), fill=rgba(JADE_2, rng.randrange(10, 26)))

    badge_right = min(675, 53 + F10.getbbox(scene)[2] + 19)
    d.rounded_rectangle((34, 30, badge_right, 68), radius=19, fill=rgba(JADE, 22), outline=rgba(JADE, 88), width=2)
    d.text((53, 40), scene, font=F10, fill=JADE_2)
    d.text((38, 92), title, font=F32, fill=INK)
    d.text((40, 161), subtitle, font=F12, fill=MUTED)
    d.rounded_rectangle((32, 210, 688, 770), radius=30, fill=PANEL, outline=rgba("#C8B49B", 30), width=2)

    d.line((40, 900, 680, 900), fill=rgba("#C8B49B", 36), width=2)
    d.line((40, 900, 40 + 640 * progress, 900), fill=CORAL, width=4)
    d.ellipse((35 + 640 * progress, 895, 45 + 640 * progress, 905), fill=CORAL_2)
    d.text((40, 918), "KAKEYA CONJECTURE · LOOP", font=F10, fill=DIM)
    return im, d


def footer(d: ImageDraw.ImageDraw, headline: str, detail: str) -> None:
    d.text((42, 800), headline, font=F18, fill=INK)
    d.text((42, 849), detail, font=F12, fill=MUTED)


def needle(d: ImageDraw.ImageDraw, p1: tuple[float, float], p2: tuple[float, float]) -> None:
    d.line((*p1, *p2), fill=rgba(CORAL, 52), width=24)
    d.line((*p1, *p2), fill=CORAL, width=7)
    for x, y in (p1, p2):
        d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=CORAL_2)


def save_gif(
    name: str,
    make_frame,
    frame_count: int = FRAMES,
    colors: int = 256,
    fps: int = FPS,
) -> None:
    images = [
        make_frame(i, frame_count).resize((GIF_OUTPUT_W, GIF_OUTPUT_H), Image.Resampling.LANCZOS)
        for i in range(frame_count)
    ]
    palette = images[0].convert("P", palette=Image.Palette.ADAPTIVE, colors=colors)
    quantized = [palette]
    quantized.extend(im.quantize(palette=palette, dither=Image.Dither.NONE) for im in images[1:])
    path = OUT / name
    durations = [
        round((idx + 1) * 1000 / fps / 10) * 10 - round(idx * 1000 / fps / 10) * 10
        for idx in range(frame_count)
    ]
    quantized[0].save(
        path,
        save_all=True,
        append_images=quantized[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=2,
    )


def wrap_text(text: str, text_font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines = []
    current = ""
    for char in text:
        candidate = current + char
        if current and text_font.getlength(candidate) > max_width:
            lines.append(current)
            current = char
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def save_timeline() -> None:
    timeline_h = 2200
    im = Image.new("RGB", (W * RENDER_SCALE, timeline_h * RENDER_SCALE), BG)
    d = ScaledDraw(im)

    rng = random.Random(1917)
    for _ in range(120):
        x, y = rng.randrange(W), rng.randrange(timeline_h)
        r = rng.choice((1, 1, 2))
        d.ellipse((x - r, y - r, x + r, y + r), fill=rgba(JADE_2, rng.randrange(8, 22)))

    scene = "SCENE 04 · 1917 — 2026"
    badge_right = 53 + F10.getbbox(scene)[2] + 19
    d.rounded_rectangle((34, 34, badge_right, 72), radius=19, fill=rgba(JADE, 22), outline=rgba(JADE, 88), width=2)
    d.text((53, 44), scene, font=F10, fill=JADE_2)
    d.text((38, 105), "一根针的百年之旅", font=F32, fill=INK)
    intro = "从转针问题、零测集和 Perron 树，到三维证明与仍然开放的高维世界。"
    for idx, line in enumerate(wrap_text(intro, F12, 620)):
        d.text((40, 182 + idx * 32), line, font=F12, fill=MUTED)

    events = [
        ("1917", "问题诞生", "挂谷宗一提问", "单位针旋转 180°，最小需要多大区域？他猜想答案是圆盘。", JADE),
        ("1919", "反直觉", "Besicovitch 的零测集", "面积可以为 0，却仍能包含每个方向的一根单位线段。", JADE),
        ("1928", "构造", "Perron 树", "切割、平移、重叠并反复迭代，占据面积可任意接近 0。", JADE),
        ("1971", "二维已证", "Davies 证明平面情形", "平面 Besicovitch 集的 Hausdorff 维数必为 2。", GREEN),
        ("1995", "高维推进", "Wolff 与调和分析", "挂谷问题与 Fourier 限制性猜想等核心问题建立深刻联系。", JADE),
        ("2017", "下界提升", "Katz–Zahl：三维至少 5/2", "三维 Hausdorff 维数下界推进到 5/2。", JADE),
        ("2025", "重大突破", "王虹–Zahl 证明三维情形", "三维 Kakeya 集的 Minkowski 与 Hausdorff 维数都等于 3。", CORAL),
        ("2026", "菲尔兹奖", "王虹获颁菲尔兹奖", "颁奖说明特别提到她在三维 Kakeya 问题上的重大进展。", CORAL),
        ("n ≥ 4", "仍待突破", "高维情形依然开放", "四维及更高维的挂谷猜想，仍在等待新的方法。", ROSE),
    ]

    line_x = 72
    start_y = 315
    step_y = 195
    d.line((line_x, start_y + 16, line_x, start_y + step_y * (len(events) - 1) + 20), fill=rgba(JADE_2, 65), width=3)

    for idx, (year, tag, title, body, color) in enumerate(events):
        y = start_y + idx * step_y
        d.rounded_rectangle((100, y - 12, 680, y + 170), radius=22, fill=rgba(PANEL, 235), outline=rgba(color, 52), width=2)
        d.ellipse((line_x - 8, y + 8, line_x + 8, y + 24), fill=BG, outline=color, width=4)

        tag_right = 120 + F_TIMELINE_TAG.getbbox(tag)[2] + 20
        d.rounded_rectangle((120, y + 10, tag_right, y + 44), radius=16, fill=rgba(color, 20), outline=rgba(color, 90), width=2)
        d.text((130, y + 17), tag, font=F_TIMELINE_TAG, fill=color)
        d.text((120, y + 55), year, font=F_TIMELINE_YEAR, fill=color)
        d.text((270, y + 59), title, font=F18, fill=INK)

        for line_no, line in enumerate(wrap_text(body, F12, 520)[:2]):
            d.text((120, y + 105 + line_no * 29), line, font=F12, fill=MUTED)

    footer_y = start_y + step_y * len(events) + 4
    d.line((40, footer_y, 680, footer_y), fill=rgba("#C8B49B", 38), width=2)
    d.text((40, footer_y + 22), "KAKEYA CONJECTURE · TIMELINE", font=F10, fill=DIM)
    d.text((40, footer_y + 58), "1917 → 2026 → OPEN", font=F14, fill=JADE_2)

    output = im.resize((TIMELINE_OUTPUT_W, timeline_h * 2), Image.Resampling.LANCZOS)
    output.save(OUT / "04-kakeya-timeline.png", optimize=True)


def draw_disk_scene(i: int, total: int, compact: bool = False) -> Image.Image:
    p = i / total
    im, d = base_frame("SCENE 01 · 1917", "转针问题" if not compact else "圆盘容器", "一根单位针，旋转 180°", p)
    cx, cy = 360, 490
    r = 185 if not compact else 175
    theta = p * math.tau
    sweep = min(theta % math.tau, math.pi)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 180, 180 + math.degrees(sweep), fill=rgba(CORAL, 48))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=JADE_2, width=4)
    dx, dy = math.cos(theta) * r, math.sin(theta) * r
    needle(d, (cx - dx, cy - dy), (cx + dx, cy + dy))
    d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=JADE)
    if compact:
        footer(d, "A = π/4 ≈ 0.7854", "针绕中心转动，扫过整个圆盘")
    else:
        area = min(sweep / 4, math.pi / 4)
        d.rounded_rectangle((472, 238, 650, 315), radius=16, fill=rgba(BG, 190), outline=rgba(CORAL, 70), width=2)
        d.text((490, 252), "扫过面积", font=F10, fill=MUTED)
        d.text((490, 277), f"{area:.4f}", font=F14, fill=CORAL_2)
        footer(d, "直觉从圆盘开始", "但最小面积远小于 π/4")
    return im


def clip_polygon(poly, nx: float, ny: float, c: float):
    out = []
    for idx, a in enumerate(poly):
        b = poly[(idx + 1) % len(poly)]
        da, db = nx * a[0] + ny * a[1] - c, nx * b[0] + ny * b[1] - c
        if da <= 0:
            out.append(a)
        if (da <= 0) != (db <= 0):
            q = da / (da - db)
            out.append((a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q))
    return out


def triangle_center(theta: float) -> tuple[float, float]:
    ux, uy = math.cos(theta), math.sin(theta)
    poly = [(-2, -1), (2, -1), (2, 2), (-2, 2)]
    poly = clip_polygon(poly, 0, -1, -0.5 * abs(uy))
    poly = clip_polygon(poly, math.sqrt(3), 1, 1 - 0.5 * abs(math.sqrt(3) * ux + uy))
    poly = clip_polygon(poly, -math.sqrt(3), 1, 1 - 0.5 * abs(-math.sqrt(3) * ux + uy))
    if not poly:
        # At exact tangent angles the feasible polygon can collapse to a point
        # and disappear through floating-point clipping. Recover that point
        best = None
        for yi in range(201):
            cy = yi / 200
            for xi in range(-150, 151):
                cx = xi / 200
                endpoints = (
                    (cx - ux * 0.5, cy - uy * 0.5),
                    (cx + ux * 0.5, cy + uy * 0.5),
                )
                if all(y >= -1e-6 and math.sqrt(3) * abs(x) + y <= 1 + 1e-6 for x, y in endpoints):
                    score = cy + abs(cx) * 0.02
                    if best is None or score < best[0]:
                        best = (score, cx, cy)
            if best is not None:
                return best[1], best[2]
        return 0.0, 0.5
    return (
        sum(x for x, _ in poly) / len(poly),
        sum(y for _, y in poly) / len(poly),
    )


def draw_triangle_scene(i: int, total: int) -> Image.Image:
    p = i / total
    im, d = base_frame("SCENE 01 · CONTAINER 02", "等边三角形", "转动的同时，针也在平移", p)
    scale, cx, base = 390, 360, 690
    top = (cx, base - scale)
    left = (cx - scale / math.sqrt(3), base)
    right = (cx + scale / math.sqrt(3), base)
    d.polygon((top, left, right), fill=rgba(JADE, 15), outline=JADE_2, width=4)
    th = p * math.pi
    center = triangle_center(th)
    px, py = cx + center[0] * scale, base - center[1] * scale
    dx, dy = math.cos(th) * scale * 0.5, -math.sin(th) * scale * 0.5
    d.line((cx, base - 8, px, py), fill=rgba(JADE_2, 55), width=3)
    needle(d, (px - dx, py - dy), (px + dx, py + dy))
    footer(d, "A = 1/√3 ≈ 0.5774", "贴边转动，比圆盘节省约 26%")
    return im


def draw_deltoid_scene(i: int, total: int) -> Image.Image:
    p = i / total
    im, d = base_frame("SCENE 01 · CONTAINER 03", "三尖内摆线", "针的运动包络出三尖边界", p)
    cx, cy, a = 360, 490, 85
    points = []
    for k in range(241):
        q = k / 240 * math.tau
        points.append((cx + a * (2 * math.cos(q) + math.cos(2 * q)), cy + a * (2 * math.sin(q) - math.sin(2 * q))))
    d.polygon(points, fill=rgba(JADE, 14))
    d.line(points + [points[0]], fill=JADE_2, width=4, joint="curve")
    th = p * math.pi
    mx, my = cx + a * 0.72 * math.cos(2 * th), cy - a * 0.72 * math.sin(2 * th)
    length = 172
    dx, dy = math.cos(th) * length, math.sin(th) * length
    needle(d, (mx - dx, my + dy), (mx + dx, my - dy))
    footer(d, "A = π/8 ≈ 0.3927", "只剩圆盘面积的一半")
    return im


BASE_TRI = ((0.0, 1.0), (-0.72, 0.0), (0.72, 0.0))


def perron_step(tris, m=3):
    out = []
    for a, b, c in tris:
        dx, dy = c[0] - b[0], c[1] - b[1]
        for j in range(m):
            ap = (a[0] - dx * j / m, a[1] - dy * j / m)
            cp = (b[0] + dx / m, b[1] + dy / m)
            out.append((ap, b, cp))
    return out


def perron_levels(max_n=4):
    levels = [[BASE_TRI]]
    for _ in range(max_n):
        levels.append(perron_step(levels[-1]))
    return levels


LEVELS = perron_levels()


def draw_perron(d: ImageDraw.ImageDraw, tris, opacity: int = 130, scale: float = 200, ox: float = 360, oy: float = 675) -> None:
    for idx, tri in enumerate(tris):
        pts = [(ox + x * scale, oy - y * scale) for x, y in tri]
        color = CORAL if idx % 4 == 0 else JADE
        d.polygon(pts, fill=rgba(color, opacity // 2), outline=rgba(JADE_2, opacity), width=2)


def draw_perron_main(i: int, total: int) -> Image.Image:
    p = i / total
    im, d = base_frame("SCENE 02 · 1928", "Perron 树", "切割 → 平移 → 重叠 → 再迭代", p)
    stage = min(4, int(p * 5))
    draw_perron(d, LEVELS[stage], opacity=120)
    d.rounded_rectangle((470, 250, 638, 342), radius=18, fill=rgba(BG, 196), outline=rgba(JADE, 72), width=2)
    d.text((492, 267), f"n = {stage}", font=F14, fill=JADE_2)
    d.text((492, 306), f"S / S0 ≈ {0.625 ** stage:.3f}", font=F10, fill=MUTED)
    footer(d, "面积不断缩小", "无限迭代后趋近于 0")
    return im


def draw_perron_iteration(i: int, total: int) -> Image.Image:
    p = i / total
    im, d = base_frame("SCENE 02 · SUB 01", "迭代构造", "每一步都把三角形压得更密", p)
    stage = min(4, int(p * 5))
    draw_perron(d, LEVELS[stage], opacity=145, scale=205)
    for n in range(5):
        x = 150 + n * 105
        d.ellipse((x - 15, 248, x + 15, 278), fill=JADE if n <= stage else PANEL_2, outline=JADE_2 if n == stage else LINE, width=2)
        d.text((x - 8, 286), str(n), font=F10, fill=INK if n <= stage else DIM)
        if n < 4:
            d.line((x + 18, 263, x + 87, 263), fill=rgba(JADE, 85 if n < stage else 28), width=3)
    footer(d, f"当前深度 n = {stage}", f"三角形数量：{len(LEVELS[stage])}")
    return im


def draw_decay(i: int, total: int) -> Image.Image:
    p = i / (total - 1)
    im, d = base_frame("SCENE 02 · SUB 02", "面积衰减", "理论曲线与栅格实测同步下降", p)
    x0, y0, x1, y1 = 105, 660, 635, 285
    d.line((x0, y0, x1, y0), fill=LINE, width=3)
    d.line((x0, y0, x0, y1), fill=LINE, width=3)
    for g in range(5):
        y = y0 - (y0 - y1) * g / 4
        d.line((x0, y, x1, y), fill=rgba("#C8B49B", 22), width=2)
        d.text((52, y - 10), f"{g * .2:.1f}", font=F10, fill=DIM)
    theory = [0.82 * (0.58**n) for n in range(7)]
    measured = [0.82, 0.51, 0.34, 0.22, 0.15, 0.10, 0.07]

    def xy(n, value):
        return x0 + (x1 - x0) * n / 6, y0 - (y0 - y1) * value / 0.85

    d.line([xy(n, v) for n, v in enumerate(theory)], fill=rgba(CORAL, 150), width=4)
    visible = max(1, min(7, int(p * 8)))
    pts = [xy(n, v) for n, v in enumerate(measured[:visible])]
    if len(pts) > 1:
        d.line(pts, fill=JADE_2, width=6)
    for x, y in pts:
        d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=JADE)
    d.text((560, 678), "迭代 n", font=F10, fill=DIM)
    footer(d, "S(n) → 0", "方向仍被保留，面积却可任意小")
    return im


def draw_cut_slide(i: int, total: int) -> Image.Image:
    p = i / total
    im, d = base_frame("SCENE 02 · SUB 03", "切割与平移", "单步机理：四块三角形逐渐重叠", p)
    phase = p * 3
    split = ease(min(1, phase))
    slide = ease(max(0, min(1, phase - 1)))
    glow = ease(max(0, min(1, phase - 2)))
    a, b, c = (360, 315), (180, 670), (540, 670)
    dx, dy = c[0] - b[0], c[1] - b[1]
    for j in range(4):
        pi = (b[0] + dx * j / 4, b[1] + dy * j / 4)
        natural = [a, pi, (b[0] + dx * (j + 1) / 4, b[1])]
        shifted = [(a[0] - dx * j / 4, a[1]), b, (b[0] + dx / 4, b[1])]
        cur = [mix(x, y, slide) for x, y in zip(natural, shifted)]
        d.polygon(cur, fill=rgba(JADE, 36 + int(glow * 25)), outline=rgba(JADE_2, 145 + int(glow * 80)), width=3)
    if split > 0 and slide < 0.6:
        for j in range(1, 4):
            px = b[0] + dx * j / 4
            d.line((*a, px, b[1]), fill=rgba(CORAL, int(180 * split * (1 - slide))), width=3)
    label = "① 切割底边" if phase < 1 else ("② 平移重叠" if phase < 2 else "③ 面积缩小")
    d.rounded_rectangle((230, 704, 490, 752), radius=20, fill=rgba(BG, 210))
    d.text((268, 716), label, font=F12, fill=CORAL_2 if phase < 2 else JADE_2)
    footer(d, "重叠越多，占地越小", "这就是 Perron 树的核心动作")
    return im


def sphere_project(theta: float, phi: float, rot: float, radius: float = 195):
    x = math.sin(phi) * math.cos(theta)
    y = math.cos(phi)
    z = math.sin(phi) * math.sin(theta)
    xr = x * math.cos(rot) + z * math.sin(rot)
    zr = -x * math.sin(rot) + z * math.cos(rot)
    return 360 + xr * radius, 495 - y * radius, zr


def fibonacci_dirs(n: int):
    ga = math.pi * (3 - math.sqrt(5))
    result = []
    for idx in range(n):
        y = 1 - 2 * idx / max(1, n - 1)
        phi = math.acos(max(-1, min(1, y)))
        result.append((ga * idx, phi))
    return result


DIRS = fibonacci_dirs(180)


def draw_sphere(
    d: ImageDraw.ImageDraw,
    progress: float,
    dense: bool = False,
    reveal_progress: Optional[float] = None,
) -> int:
    rot = progress * math.tau
    d.ellipse((165, 300, 555, 690), fill=rgba(JADE, 10), outline=rgba(JADE_2, 100), width=3)
    reveal = progress if reveal_progress is None else reveal_progress
    maximum = 180 if dense else 90
    count = max(8, int(maximum * ease(min(1, reveal))))
    if reveal >= 1:
        count = maximum
    projected = []
    for theta, phi in DIRS[:count]:
        x, y, z = sphere_project(theta, phi, rot)
        projected.append((z, x, y))
    for z, x, y in sorted(projected):
        alpha = 55 if z < 0 else 150
        d.line((360, 495, x, y), fill=rgba(CORAL if y < 495 else JADE, alpha), width=2 if dense else 3)
        d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=rgba(JADE_2, alpha + 45))
    return count


def draw_three_main(i: int, total: int) -> Image.Image:
    p = i / (total - 1)
    im, d = base_frame("SCENE 03 · 2025", "三维挂谷", "每个方向，都装着一根单位针", p)
    # Spend most of the extended loop revealing directions, then keep the
    # completed sphere on screen while it continues rotating.
    reveal = min(1, p / 0.82)
    count = draw_sphere(d, p, dense=True, reveal_progress=reveal)
    d.rounded_rectangle((487, 240, 644, 319), radius=16, fill=rgba(BG, 200), outline=rgba(CORAL, 70), width=2)
    d.text((508, 252), "方向数", font=F10, fill=MUTED)
    d.text((508, 280), f"{count:03d}", font=F14, fill=CORAL_2)
    footer(d, "dim_H(K in R3) = 3", "Wang–Zahl · 2025")
    return im


def draw_fibonacci(i: int, total: int) -> Image.Image:
    p = i / total
    im, d = base_frame("SCENE 03 · SUB 01", "方向填充", "Fibonacci 球面均匀采样", p)
    count = draw_sphere(d, p, dense=False)
    d.rounded_rectangle((245, 700, 475, 745), radius=18, fill=rgba(BG, 210))
    d.text((279, 710), f"N = {count:03d} directions", font=F10, fill=JADE_2)
    footer(d, "方向越来越密", "极限对应“每一个方向”")
    return im


def draw_dimension_status(i: int, total: int) -> Image.Image:
    p = i / total
    im, d = base_frame("SCENE 03 · SUB 02", "各维数状态", "已解决、重大突破与开放问题", p)
    active = min(2, int(p * 3))
    rows = [
        ("n = 2", "1971 · 已证明", GREEN, "平面情形"),
        ("n = 3", "2025 · Wang–Zahl", CORAL, "三维完全证明"),
        ("n ≥ 4", "OPEN · 未解决", ROSE, "仍等待突破"),
    ]
    for idx, (n, status, color, note) in enumerate(rows):
        y = 285 + idx * 145
        pulse = (math.sin(p * math.tau * 3) + 1) / 2 if idx == active else 0
        fill = rgba(color, 30 + int(pulse * 20)) if idx == active else rgba(PANEL_2, 220)
        outline = rgba(color, 190 if idx == active else 55)
        d.rounded_rectangle((92, y, 628, y + 112), radius=22, fill=fill, outline=outline, width=3)
        d.text((122, y + 21), n, font=F24, fill=color)
        d.text((300, y + 22), status, font=F14, fill=INK if idx == active else MUTED)
        d.text((302, y + 65), note, font=F12, fill=MUTED)
        if idx < active:
            d.ellipse((575, y + 42, 595, y + 62), fill=GREEN)
        elif idx == active:
            r = 6 + pulse * 7
            d.ellipse((585 - r, y + 52 - r, 585 + r, y + 52 + r), fill=color)
    footer(d, "三维已证，高维未解", "挂谷猜想的故事还没有结束")
    return im


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = [
        ("01-turning-needle-main.gif", lambda i, n: draw_disk_scene(i, n, compact=False)),
        ("01a-disk-container.gif", lambda i, n: draw_disk_scene(i, n, compact=True)),
        ("01b-triangle-container.gif", draw_triangle_scene),
        ("01c-deltoid-container.gif", draw_deltoid_scene),
        ("02-perron-tree-main.gif", draw_perron_main),
        ("02a-perron-iteration.gif", draw_perron_iteration),
        ("02b-area-decay.gif", draw_decay),
        ("02c-cut-slide-overlap.gif", draw_cut_slide),
        ("03-kakeya-3d-main.gif", draw_three_main, THREE_MAIN_FRAMES),
        ("03a-fibonacci-directions.gif", draw_fibonacci),
        ("03b-dimension-status.gif", draw_dimension_status),
    ]
    for job in jobs:
        name, maker, *frame_count = job
        print(f"rendering {name}", flush=True)
        colors = 128 if name == "03-kakeya-3d-main.gif" else 256
        fps = THREE_MAIN_FPS if name == "03-kakeya-3d-main.gif" else FPS
        save_gif(name, maker, frame_count[0] if frame_count else FRAMES, colors=colors, fps=fps)
    print("rendering 04-kakeya-timeline.png", flush=True)
    save_timeline()
    print(f"done: {len(jobs)} GIFs and 1 timeline in {OUT}", flush=True)


if __name__ == "__main__":
    main()
