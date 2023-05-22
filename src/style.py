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

import configparser
import os.path
from gettext import gettext as _

from . import install
from . import paths
from . import update

def generate_style(theme_name):
    theme_path = f"{paths.THEMES_DIR}/{theme_name}/{theme_name}.theme"

    if install.zip_not_extracted():
        (ret, msg) = update.post_download()
        if not ret:
            return (ret, msg)

    if not os.path.exists(theme_path):
        return (False, _("Style: Could not find theme {theme_name}").format(theme_name=theme_name))

    config = configparser.ConfigParser()
    config.read(theme_path)
    css = ""

    css += format_css("accent_color", config["accent"]["accent"])
    css += format_css("accent_bg_color", config["accent"]["accent_bg"])
    css += format_css("accent_fg_color", config["accent"]["accent_fg"])

    css += format_css("destructive", config["destructive"]["destructive"])
    css += format_css("destructive_fg_color", config["destructive"]["destructive_fg"])
    css += format_css("destructive_bg_color", config["destructive"]["destructive_bg"])

    css += format_css("success_color", config["success"]["success"])
    css += format_css("success_bg_color", config["success"]["success_bg"])
    css += format_css("success_fg_color", config["success"]["success_fg"])

    css += format_css("warning_color", config["warning"]["warning"])
    css += format_css("warning_bg_color", config["warning"]["warning_bg"])
    css += format_css("warning_fg_color", config["warning"]["warning_fg"])

    css += format_css("error_color", config["error"]["error"])
    css += format_css("error_bg_color", config["error"]["error_bg"])
    css += format_css("error_fg_color", config["error"]["error_fg"])

    css += format_css("headerbar_bg_color", config["headerbar"]["headerbar_bg"])
    css += format_css("headerbar_fg_color", config["headerbar"]["headerbar_fg"])
    css += format_css("headerbar_backdrop_color", config["headerbar"]["headerbar_backdrop"])
    css += format_css("headerbar_shade_color", config["headerbar"]["headerbar_shade"])

    css += format_css("window_bg_color", config["window"]["window_bg"])
    css += format_css("window_fg_color", config["window"]["window_fg"])

    css += format_css("view_bg_color", config["view"]["view_bg"])
    css += format_css("view_fg_color", config["view"]["view_fg"])

    css += format_css("popover_bg_color", config["popover"]["popover_bg"])
    css += format_css("popover_fg_color", config["popover"]["popover_fg"])

    css += format_css("card_fg_color", config["general"]["fg"])
    css += format_css("card_bg_color", "rgba(255, 255, 255, 0.08)")

    return (True, css)

def format_css(name, color):
    return f"@define-color {name} {color};\n"
