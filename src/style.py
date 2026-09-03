# style.py
#
# Copyright 2022 Foldex
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os.path
import re
from pathlib import Path

from . import install
from . import paths
from . import update

def get_color_themes():
    themes = []
    fallback = ["Adwaita"]

    if install.zip_not_extracted():
        (ret, msg) = update.post_download()
        if not ret:
            return (ret, msg)

    theme_dir = Path(paths.THEMES_DIR)
    theme_ext = "css"
    themes = [ x.stem.title() for x in theme_dir.glob(f"*/*.{theme_ext}")]

    if not themes:
        return (fallback, _("Get Themes: Failed to get themes"))

    return (themes, None)

def merge_css_files(file_paths):
    combined = []

    for path in file_paths:
        if os.path.exists(path):
            combined.append(f"/* {path} */")
            with open(path, 'r', encoding='utf-8') as f:
                combined.append(convert_light_dark(f.read()))
    return '\n'.join(combined)

def convert_light_dark(css):

    def find_calls(text):
        calls = []
        i = 0
        while True:
            idx = text.find("light-dark(", i)
            if idx == -1:
                break
            depth, j = 0, idx + len("light-dark")
            while j < len(text):
                if text[j] == "(":
                    depth += 1
                elif text[j] == ")":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            if j >= len(text):
                break

            inner = text[idx + len("light-dark(") : j]

            depth, comma_idx = 0, -1
            for k, ch in enumerate(inner):
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                elif ch == "," and depth == 0:
                    comma_idx = k
                    break

            if comma_idx == -1:
                i = idx + len("light-dark(")
                continue

            light_val = inner[:comma_idx].strip()
            dark_val = inner[comma_idx + 1 :].strip()
            calls.append((idx, j + 1, light_val, dark_val))
            i = j + 1
        return calls

    def get_context(text, pos):
        depth, p = 0, pos - 1
        while p >= 0:
            if text[p] == "}":
                depth += 1
            elif text[p] == "{":
                if depth == 0:
                    before = text[:p]
                    last_close = before.rfind("}")
                    selector = (
                        before.strip() if last_close == -1
                        else before[last_close + 1 :].strip()
                    )
                    between = text[p + 1 : pos]
                    prop = None
                    for m in re.finditer(r"([\w-]+)\s*:", between):
                        prop = m.group(1)
                    return selector, prop
                depth -= 1
            p -= 1
        return None, None

    calls = find_calls(css)
    dark_rules: dict[str, dict[str, str]] = {}

    for start, end, light_val, dark_val in reversed(calls):
        selector, prop = get_context(css, start)
        if selector and prop:
            dark_rules.setdefault(selector, {})[prop] = dark_val
        css = css[:start] + light_val + css[end:]

    if dark_rules:
        css += "\n\n@media (prefers-color-scheme: dark) {\n"
        for selector, props in dark_rules.items():
            css += f"  {selector} {{\n"
            for prop, value in props.items():
                css += f"    {prop}: {value};\n"
            css += "  }\n"
        css += "}\n"

    return css

def generate_style(theme_name):
    theme_dir = paths.THEMES_DIR
    theme_path = f"{theme_dir}/{theme_name}/{theme_name}.css"

    if install.zip_not_extracted():
        (ret, msg) = update.post_download()
        if not ret:
            return (ret, msg)

    if not os.path.exists(theme_path):
        return (False, _("Style: Could not find theme {theme_name}").format(theme_name=theme_name))

    style = merge_css_files([paths.CSS_DEFAULT_FILE, paths.CSS_PALETTE_FILE, theme_path])

    # fixes for differences in naming
    style = style.replace("--adw-", "--")
    style = style.replace("fg:", "fg-color:")
    style = style.replace("bg:", "bg-color:")
    style = style.replace("accent-bg-dark", "accent-bg-color")
    style = style.replace("destructive-bg-dark", "destructive-bg-color")
    style = style.replace(" !important", "")

    style += "\n.color-swatch { background-color: #e62d42;   border-radius: 4px; }"

    return (True, style)
