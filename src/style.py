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

    pattern = r'--(\w+)\s*:\s*(.*);'
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

    css_vars = parse_css(theme_path)
    css = ""

    css += format_css("accent_color", css_vars["accent"])
    css += format_css("accent_bg_color", css_vars["accent_bg"])
    css += format_css("accent_fg_color", css_vars["accent_fg"])

    css += format_css("destructive", css_vars["destructive"])
    css += format_css("destructive_fg_color", css_vars["destructive_fg"])
    css += format_css("destructive_bg_color", css_vars["destructive_bg"])

    css += format_css("success_color", css_vars["success"])
    css += format_css("success_bg_color", css_vars["success_bg"])
    css += format_css("success_fg_color", css_vars["success_fg"])

    css += format_css("warning_color", css_vars["warning"])
    css += format_css("warning_bg_color", css_vars["warning_bg"])
    css += format_css("warning_fg_color", css_vars["warning_fg"])

    css += format_css("error_color", css_vars["error"])
    css += format_css("error_bg_color", css_vars["error_bg"])
    css += format_css("error_fg_color", css_vars["error_fg"])

    css += format_css("headerbar_bg_color", css_vars["headerbar_bg"])
    css += format_css("headerbar_fg_color", css_vars["headerbar_fg"])
    css += format_css("headerbar_backdrop_color", css_vars["headerbar_backdrop"])
    css += format_css("headerbar_shade_color", css_vars["headerbar_shade"])

    css += format_css("window_bg_color", css_vars["window_bg"])
    css += format_css("window_fg_color", css_vars["window_fg"])

    css += format_css("view_bg_color", css_vars["view_bg"])
    css += format_css("view_fg_color", css_vars["view_fg"])

    css += format_css("popover_bg_color", css_vars["popover_bg"])
    css += format_css("popover_fg_color", css_vars["popover_fg"])

    css += format_css("dialog_bg_color", css_vars["popover_bg"])
    css += format_css("dialog_fg_color", css_vars["popover_fg"])

    css += format_css("card_fg_color", css_vars["fg"])
    css += format_css("card_bg_color", "rgba(255, 255, 255, 0.08)")

    css += "tooltip.background { background-color: rgba(0, 0, 0, 0.8); color: @card_fg_color; }\n"
    css += "list.boxed-list > row:not(:last-child) { border-bottom: 1px solid rgba(0, 0, 0, 0.36); }\n"

    return (True, css)

def format_css(name, color):
    return f"@define-color {name} {color};\n"
