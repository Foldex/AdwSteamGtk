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

def parse_css(file):
    with open (file, 'r' ) as f:
        content = f.read()

    pattern = r'--([\w-]+)\s*:\s*(.*?)(?:\s*!important)?;'
    matches = re.findall(pattern, content)

    vars = {}

    for match in matches:
        key = match[0]
        value = match[1]

        vars[key] = value

    return vars

def generate_style(theme_name):
    theme_dir = paths.THEMES_DIR
    theme_path = f"{theme_dir}/{theme_name}/{theme_name}.css"

    if install.zip_not_extracted():
        (ret, msg) = update.post_download()
        if not ret:
            return (ret, msg)

    if not os.path.exists(theme_path):
        return (False, _("Style: Could not find theme {theme_name}").format(theme_name=theme_name))

    theme_vars = parse_css(theme_path)

    # Generated Styles
    style_vars = {
        "accent_color": theme_vars.get("adw-accent-rgb"),
        "accent_bg_color": theme_vars.get("adw-accent-bg-rgb"),
        "accent_fg_color": theme_vars.get("adw-accent-fg-rgb"),

        "destructive": theme_vars.get("adw-destructive-rgb"),
        "destructive_fg_color": theme_vars.get("adw-destructive-fg-rgb"),
        "destructive_bg_color": theme_vars.get("adw-destructive-bg-rgb"),

        "success_color": theme_vars.get("adw-success-rgb"),
        "success_bg_color": theme_vars.get("adw-success-bg-rgb"),
        "success_fg_color": theme_vars.get("adw-success-fg-rgb"),

        "warning_color": theme_vars.get("adw-warning-rgb"),
        "warning_bg_color": theme_vars.get("adw-warning-bg-rgb"),
        "warning_fg_color": (theme_vars.get("adw-warning-fg-rgb"), theme_vars.get("adw-warning-fg-a")),

        "error_color": theme_vars.get("adw-error-rgb"),
        "error_bg_color": theme_vars.get("adw-error-bg-rgb"),
        "error_fg_color": theme_vars.get("adw-error-fg-rgb"),

        "headerbar_bg_color": theme_vars.get("adw-headerbar-bg-rgb"),
        "headerbar_fg_color": theme_vars.get("adw-headerbar-fg-rgb"),
        "headerbar_backdrop_color": theme_vars.get("adw-headerbar-backdrop-rgb"),
        "headerbar_shade_color": theme_vars.get("adw-headerbar-shade-rgb"),

        "window_bg_color": theme_vars.get("adw-window-bg-rgb"),
        "window_fg_color": theme_vars.get("adw-window-fg-rgb"),

        "view_bg_color": theme_vars.get("adw-view-bg-rgb"),
        "view_fg_color": theme_vars.get("adw-view-fg-rgb"),

        "popover_bg_color": theme_vars.get("adw-popover-bg-rgb"),
        "popover_fg_color": theme_vars.get("adw-popover-fg-rgb"),

        "dialog_bg_color": theme_vars.get("adw-popover-bg-rgb"),
        "dialog_fg_color": theme_vars.get("adw-popover-fg-rgb"),

        "card_fg_color": theme_vars.get("adw-card-fg-rgb"),
        "card_bg_color": (theme_vars.get("adw-card-bg-rgb"), theme_vars.get("adw-card-bg-a")),
    }

    style_vars = lookup_css(style_vars, theme_vars)
    style = format_css(style_vars)

    if all(x is None for x in style_vars.values()):
        return (False, _("Style: Theme {theme_name} seems to be invalid").format(theme_name=theme_name))

    # Hardcoded Styles
    style += "tooltip.background { background-color: rgba(0, 0, 0, 0.8); color: @card_fg_color; }\n"
    style += "list.boxed-list > row:not(:last-child) { border-bottom: 1px solid rgba(0, 0, 0, 0.36); }\n"


    return (True, style)

def lookup_css(style_vars, theme_vars):
    # non-recursive, meh
    for adw_color, theme_color in style_vars.items():

        if not theme_color:
            continue

        if isinstance(theme_color, tuple):
            continue

        var_result = None

        var_pattern = r'var\(\s*--([\w-]+)\s*\)'
        var_result = re.search(var_pattern, theme_color)

        if var_result:
            resolved = theme_vars.get(var_result.group(1))
        else:
            resolved = None

        if resolved:
            style_vars[adw_color] = resolved

    return style_vars

def format_css(style_vars):

    css = ""

    for adw_color, theme_color in style_vars.items():
        if theme_color:

            # tuples are rgba
            if isinstance(theme_color, tuple) and theme_color[0] and theme_color[1]:
                final_color = f"rgba({theme_color[0]}, {theme_color[1]})"
            # rgb
            else:
                final_color = f"rgb({theme_color})"

            css += f"@define-color {adw_color} {final_color};\n"

    return css
