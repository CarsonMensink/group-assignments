"""Part 1B plots, drawn as SVG with the standard library only.

Reads benchmark_results.csv (written by benchmark.py) and writes:
  runtime_loglog.svg   median runtime vs n, log-log axes
  speedup.svg          brute-force time / divide-and-conquer time vs n
  normalized.svg       runtime divided by the predicted growth term

Plotting is separate from timing: run benchmark.py first.
"""

import csv
import html
import math
from pathlib import Path

script_folder = Path(__file__).resolve().parent

WIDTH, HEIGHT = 760, 440
MARGIN = {"left": 84, "right": 170, "top": 56, "bottom": 60}
SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e4e3df"
AXIS = "#9a9893"
BRUTE_COLOR = "#2a78d6"   # categorical slot 1
DC_COLOR = "#eb6834"      # categorical slot 2


def load_results():
    with open(script_folder / "benchmark_results.csv", newline="") as f:
        rows = list(csv.DictReader(f))
    data = {}
    for row in rows:
        data.setdefault(row["algorithm"], []).append({
            "n": int(row["n"]),
            "median_s": float(row["median_s"]),
            "ns_per_n2": float(row["ns_per_n2"]),
            "ns_per_nlog2n": float(row["ns_per_nlog2n"]),
        })
    for points in data.values():
        points.sort(key=lambda p: p["n"])
    return data


def format_power(value, base):
    exponent = round(math.log(value, base))
    if base == 2:
        return f"{2 ** exponent:,}" if exponent <= 13 else f"2^{exponent}"
    if -2 <= exponent <= 3:
        return f"{value:g}"
    return f"1e{exponent}"


def log_ticks(low, high, base):
    start = math.floor(math.log(low, base))
    stop = math.ceil(math.log(high, base))
    return [base ** e for e in range(start, stop + 1)]


def line_chart(path, title, subtitle, x_label, y_label, series,
               y_base=10, x_step=2, reference=None):
    """series: list of (label, color, [(x, y), ...]); both axes logarithmic."""

    esc = html.escape
    title, subtitle = esc(title), esc(subtitle)
    x_label, y_label = esc(x_label), esc(y_label)
    series = [(esc(label), color, pts) for label, color, pts in series]

    xs = [x for _, _, pts in series for x, _ in pts]
    ys = [y for _, _, pts in series for _, y in pts]
    if reference is not None:
        ys.append(reference[0])
    x_ticks = log_ticks(min(xs), max(xs), 2)
    y_ticks = log_ticks(min(ys), max(ys), y_base)
    x_lo, x_hi = math.log2(x_ticks[0]), math.log2(x_ticks[-1])
    y_lo, y_hi = math.log(y_ticks[0], y_base), math.log(y_ticks[-1], y_base)

    plot_w = WIDTH - MARGIN["left"] - MARGIN["right"]
    plot_h = HEIGHT - MARGIN["top"] - MARGIN["bottom"]

    def px(x):
        return MARGIN["left"] + (math.log2(x) - x_lo) / (x_hi - x_lo) * plot_w

    def py(y):
        return MARGIN["top"] + (1 - (math.log(y, y_base) - y_lo) / (y_hi - y_lo)) * plot_h

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" font-family="Helvetica, Arial, sans-serif">',
        f'<rect width="100%" height="100%" fill="{SURFACE}"/>',
        f'<text x="{MARGIN["left"]}" y="24" font-size="16" font-weight="600" '
        f'fill="{TEXT_PRIMARY}">{title}</text>',
        f'<text x="{MARGIN["left"]}" y="42" font-size="12" fill="{TEXT_SECONDARY}">'
        f'{subtitle}</text>',
    ]

    bottom = MARGIN["top"] + plot_h
    right = MARGIN["left"] + plot_w
    for tick in y_ticks:
        y = py(tick)
        out.append(f'<line x1="{MARGIN["left"]}" x2="{right}" y1="{y:.1f}" '
                   f'y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
        out.append(f'<text x="{MARGIN["left"] - 8}" y="{y + 4:.1f}" font-size="11" '
                   f'text-anchor="end" fill="{TEXT_SECONDARY}">'
                   f'{format_power(tick, y_base)}</text>')
    for tick in x_ticks[::x_step]:
        x = px(tick)
        out.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{MARGIN["top"]}" '
                   f'y2="{bottom}" stroke="{GRID}" stroke-width="1"/>')
        out.append(f'<text x="{x:.1f}" y="{bottom + 18}" font-size="11" '
                   f'text-anchor="middle" fill="{TEXT_SECONDARY}">'
                   f'{format_power(tick, 2)}</text>')
    out.append(f'<line x1="{MARGIN["left"]}" x2="{right}" y1="{bottom}" y2="{bottom}" '
               f'stroke="{AXIS}" stroke-width="1"/>')
    out.append(f'<text x="{MARGIN["left"] + plot_w / 2}" y="{HEIGHT - 16}" '
               f'font-size="12" text-anchor="middle" fill="{TEXT_SECONDARY}">'
               f'{x_label}</text>')
    out.append(f'<text transform="translate(20 {MARGIN["top"] + plot_h / 2}) rotate(-90)" '
               f'font-size="12" text-anchor="middle" fill="{TEXT_SECONDARY}">'
               f'{y_label}</text>')

    if reference is not None:
        value, label = reference
        y = py(value)
        out.append(f'<line x1="{MARGIN["left"]}" x2="{right}" y1="{y:.1f}" y2="{y:.1f}" '
                   f'stroke="{TEXT_SECONDARY}" stroke-width="1" stroke-dasharray="4 4"/>')
        out.append(f'<text x="{MARGIN["left"] + 6}" y="{y - 6:.1f}" font-size="11" '
                   f'fill="{TEXT_SECONDARY}">{label}</text>')

    # Lines and markers, then direct labels at each line's last point.
    for label, color, pts in series:
        coords = " ".join(f"{px(x):.1f},{py(y):.1f}" for x, y in pts)
        out.append(f'<polyline points="{coords}" fill="none" stroke="{color}" '
                   f'stroke-width="2" stroke-linejoin="round"/>')
        for x, y in pts:
            out.append(f'<circle cx="{px(x):.1f}" cy="{py(y):.1f}" r="4" fill="{color}" '
                       f'stroke="{SURFACE}" stroke-width="2"><title>{label}: n = {x:,}, '
                       f'{y:.3g}</title></circle>')
        last_x, last_y = pts[-1]
        out.append(f'<text x="{px(last_x) + 10:.1f}" y="{py(last_y) + 4:.1f}" '
                   f'font-size="12" fill="{TEXT_PRIMARY}">{label}</text>')

    # Legend (top right, outside the plot).
    if len(series) > 1:
        for i, (label, color, _) in enumerate(series):
            y = MARGIN["top"] + 8 + i * 20
            out.append(f'<rect x="{right + 16}" y="{y - 8}" width="12" height="12" '
                       f'rx="2" fill="{color}"/>')
            out.append(f'<text x="{right + 34}" y="{y + 2}" font-size="12" '
                       f'fill="{TEXT_PRIMARY}">{label}</text>')

    out.append("</svg>")
    Path(path).write_text("\n".join(out) + "\n")


def main():
    data = load_results()
    brute = data["brute_force"]
    dc = data["divide_conquer"]

    line_chart(
        script_folder / "runtime_loglog.svg",
        "Inversion counting: median runtime vs n",
        "Random permutations, median of 7 repetitions; on log-log axes slope 2 is n^2",
        "n (array length, log scale)",
        "median seconds per call (log scale)",
        [("Brute force", BRUTE_COLOR, [(p["n"], p["median_s"]) for p in brute]),
         ("Divide & conquer", DC_COLOR, [(p["n"], p["median_s"]) for p in dc])],
    )

    dc_by_n = {p["n"]: p["median_s"] for p in dc}
    speedup = [(p["n"], p["median_s"] / dc_by_n[p["n"]]) for p in brute
               if p["n"] in dc_by_n]
    line_chart(
        script_folder / "speedup.svg",
        "Speedup of divide and conquer over brute force",
        "Brute-force median / divide-and-conquer median; above 1 means D&C is faster",
        "n (array length, log scale)",
        "speedup (log scale)",
        [("Speedup", BRUTE_COLOR, speedup)],
        reference=(1.0, "break-even (1x)"),
        x_step=1,
    )

    line_chart(
        script_folder / "normalized.svg",
        "Runtime divided by the predicted growth term",
        "A flat line means the measured growth matches the asymptotic prediction",
        "n (array length, log scale)",
        "nanoseconds per unit of predicted work (log)",
        [("Brute force: t / n^2", BRUTE_COLOR,
          [(p["n"], p["ns_per_n2"]) for p in brute]),
         ("D&C: t / (n log2 n)", DC_COLOR,
          [(p["n"], p["ns_per_nlog2n"]) for p in dc])],
    )
    print("Wrote runtime_loglog.svg, speedup.svg, normalized.svg")


if __name__ == "__main__":
    main()
