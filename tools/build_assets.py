"""Genera assets/banner.svg y assets/pokedex.svg (sprite incrustado en base64).

Uso: python3 tools/build_assets.py <sprite.gif>
Sprite: PokeAPI/sprites, generation-v/black-white/animated/137.gif
"""
import base64
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

MONO = "ui-monospace, SFMono-Regular, 'JetBrains Mono', Consolas, Menlo, monospace"
SANS = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

BG, PANEL, LINE = "#0d1117", "#161b22", "#30363d"
RED, RED_DK, YELLOW, BLUE, TEXT, MUTED = "#e3350d", "#a8270a", "#ffcb05", "#3d7dca", "#e6edf3", "#8b949e"


def pokeball(x0, y0, px, n=18):
    """Pokéball pixel art en una grilla n x n."""
    c = (n - 1) / 2
    r = n / 2 - 0.2
    cells = []
    for gy in range(n):
        for gx in range(n):
            dx, dy = gx - c, gy - c
            d = math.hypot(dx, dy)
            if d > r + 1:
                continue
            if d > r:
                cells.append(f'<rect x="{x0 + gx * px}" y="{y0 + gy * px}" width="{px}" height="{px}" fill="#3d444d"/>')
                continue
            if d > r - 1.1 or abs(dy) < 1:
                color = "#0b0b0b"
            elif d < 2.6:
                color = "#0b0b0b" if d > 1.6 else "#f5f5f5"
            elif dy < 0:
                color = RED if not (dx < -2 and dy < -3 and dx > -6 and dy > -6.5) else "#ff8a70"
            else:
                color = "#f5f5f5" if dy < r - 3 else "#cfd4da"
            cells.append(f'<rect x="{x0 + gx * px}" y="{y0 + gy * px}" width="{px}" height="{px}" fill="{color}"/>')
    return "\n    ".join(cells)


def banner():
    w, h = 1280, 300
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Agustín Lamendola — Backend, Networking, Linux, Cybersecurity">
  <defs>
    <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse">
      <rect width="2" height="2" fill="{LINE}"/>
    </pattern>
    <linearGradient id="fade" x1="0" x2="1">
      <stop offset="0" stop-color="{BG}" stop-opacity="1"/>
      <stop offset=".55" stop-color="{BG}" stop-opacity=".2"/>
      <stop offset="1" stop-color="{BG}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="card"><rect width="{w}" height="{h}" rx="14"/></clipPath>
    <style>
      .blink {{ animation: blink 2.4s steps(1) infinite; }}
      .blink.b {{ animation-delay: .8s; }}
      .blink.c {{ animation-delay: 1.6s; }}
      .cursor {{ animation: blink 1.1s steps(1) infinite; }}
      .bob {{ animation: bob 3s ease-in-out infinite; transform-box: fill-box; }}
      @keyframes blink {{ 0%,100% {{ opacity: 1 }} 50% {{ opacity: .25 }} }}
      @keyframes bob {{ 0%,100% {{ transform: translateY(0) }} 50% {{ transform: translateY(-6px) }} }}
      @media (prefers-reduced-motion: reduce) {{ .blink, .cursor, .bob {{ animation: none; }} }}
    </style>
  </defs>
  <g clip-path="url(#card)">
    <rect width="{w}" height="{h}" fill="{BG}"/>
    <rect width="{w}" height="{h}" fill="url(#dots)"/>
    <rect width="{w}" height="{h}" fill="url(#fade)"/>
    <rect width="{w}" height="10" fill="{RED}"/>
    <rect y="10" width="{w}" height="3" fill="{RED_DK}"/>
  </g>
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14" fill="none" stroke="{LINE}"/>

  <!-- luces de Pokédex -->
  <circle cx="72" cy="66" r="20" fill="#cfe3ff"/>
  <circle cx="72" cy="66" r="15" fill="{BLUE}"/>
  <circle cx="66" cy="60" r="5" fill="#9ec5ff"/>
  <circle class="blink" cx="112" cy="54" r="6" fill="{RED}"/>
  <circle class="blink b" cx="132" cy="54" r="6" fill="{YELLOW}"/>
  <circle class="blink c" cx="152" cy="54" r="6" fill="#4caf50"/>

  <text x="72" y="140" fill="{MUTED}" font-family="{MONO}" font-size="17" letter-spacing="3">TRAINER CARD · ID No. 163334540</text>
  <text x="70" y="200" fill="{TEXT}" font-family="{SANS}" font-size="62" font-weight="800" letter-spacing="-1">Agustín Lamendola</text>
  <text x="72" y="246" fill="{MUTED}" font-family="{MONO}" font-size="20">
    <tspan fill="{RED}">&gt;</tspan> Backend <tspan fill="{LINE}">·</tspan> Networking <tspan fill="{LINE}">·</tspan> Linux <tspan fill="{LINE}">·</tspan> Cybersecurity<tspan class="cursor" fill="{YELLOW}"> ▌</tspan>
  </text>

  <g class="bob">
    {pokeball(990, 50, 10, 20)}
  </g>
  <ellipse cx="1090" cy="262" rx="70" ry="8" fill="#000" opacity=".45"/>
</svg>
'''


def pokedex(gif_path):
    gif = base64.b64encode(pathlib.Path(gif_path).read_bytes()).decode()
    w, h = 340, 412
    sw, sh = 57 * 4, 53 * 4
    sx, sy = (w - sw) / 2, 74 + (230 - sh) / 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Pokédex entry #137 Porygon">
  <defs>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1" fill="#000" opacity=".22"/>
    </pattern>
    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M20 0H0V20" fill="none" stroke="#1f3a2c" stroke-width="1"/>
    </pattern>
    <style>.led {{ animation: blink 2.4s steps(1) infinite; }} @keyframes blink {{ 50% {{ opacity: .25 }} }}
      @media (prefers-reduced-motion: reduce) {{ .led {{ animation: none; }} }}</style>
  </defs>
  <rect width="{w}" height="{h}" rx="18" fill="#c42b0a"/>
  <rect x="4" y="4" width="{w - 8}" height="{h - 8}" rx="15" fill="none" stroke="{RED_DK}" stroke-width="3"/>
  <circle cx="38" cy="36" r="13" fill="#cfe3ff"/><circle cx="38" cy="36" r="9" fill="{BLUE}"/>
  <circle class="led" cx="66" cy="30" r="5" fill="{YELLOW}"/>
  <circle cx="84" cy="30" r="5" fill="#4caf50"/>
  <text x="{w - 24}" y="36" text-anchor="end" fill="#fff" font-family="{MONO}" font-size="13" letter-spacing="2">POKéDEX</text>

  <rect x="20" y="62" width="{w - 40}" height="254" rx="10" fill="#dfe3e8"/>
  <rect x="30" y="72" width="{w - 60}" height="234" rx="4" fill="#0f2419"/>
  <rect x="30" y="72" width="{w - 60}" height="234" rx="4" fill="url(#grid)"/>
  <image x="{sx}" y="{sy}" width="{sw}" height="{sh}" style="image-rendering:pixelated" href="data:image/gif;base64,{gif}" xlink:href="data:image/gif;base64,{gif}"/>
  <rect x="30" y="72" width="{w - 60}" height="234" rx="4" fill="url(#scan)"/>
  <text x="42" y="94" fill="#7ee2a8" font-family="{MONO}" font-size="12">#137</text>

  <text x="24" y="346" fill="#fff" font-family="{MONO}" font-size="17" font-weight="700">PORYGON</text>
  <text x="{w - 24}" y="346" text-anchor="end" fill="#fff" font-family="{MONO}" font-size="12">TYPE / NORMAL</text>
  <text x="24" y="372" fill="#fff" font-family="{MONO}" font-size="12">The first Pokémon made</text>
  <text x="24" y="388" fill="#fff" font-family="{MONO}" font-size="12">entirely of programming code.</text>
</svg>
'''


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "banner.svg").write_text(banner(), encoding="utf-8")
    (ASSETS / "pokedex.svg").write_text(pokedex(sys.argv[1]), encoding="utf-8")
    print("ok")
