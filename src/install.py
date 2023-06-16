# install.py
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

import os
import shlex
import subprocess

from . import paths
from . import update

def gen_cmd_line(options, beta_support):
    installer = "python install.py "

    if options.get("uninstall"):
        return f"{installer} -u"

    match options["install_fonts"]:
        case True:
            install_fonts = "-fi "
        case _:
            install_fonts = ""

    match options["custom_css"]:
        case True:
            custom_css = f"-we {paths.CUSTOM_CSS_FILE} "
        case _:
            custom_css = ""


    match options["color_theme"].lower():
        case "adwaita":
            color_theme = ""
        case _:
            color_theme = f"-c {options['color_theme'].lower()} "

    match options["web_theme"].lower():
        case "base":
            web_theme = "-w base "
        case "full":
            web_theme = "-w full "
        case _:
            web_theme = ""

    match options["rounded_corners"]:
        case False:
            rounded_corners = "-we general/no_rounded_corners "
        case _:
            rounded_corners = ""

    match options["win_controls"].lower():
        case "left":
            win_controls = f"-we windowcontrols/left "
        case "left-all":
            win_controls = f"-we windowcontrols/left-all "
        case "right-all":
            win_controls = f"-we windowcontrols/right-all "
        case "none":
            win_controls = f"-we windowcontrols/none "
        case _:
            win_controls = ""

    match options["win_controls_style"].lower():
        case "dots":
            win_controls_style = "-we windowcontrols/dots "
        case _:
            win_controls_style = ""


    match options["library_sidebar"].lower():
        case "hover only":
            library_sidebar = "-we library/sidebar_hover "
        case _:
            library_sidebar = ""

    match options["library_whats_new"]:
        case False:
            library_whats_new = "-we library/hide_whats_new "
        case _:
            library_whats_new = ""


    match options["login_qr"].lower():
        case "hide":
            login_qr = "-we login/hide_qr "
        case "hover only":
            login_qr = "-we login/hover_qr "
        case _:
            login_qr = ""


    match options["top_bar_bp_button"]:
        case False:
            top_bar_bp_button = "-we topbar/hide_bp "
        case _:
            top_bar_bp_button = ""

    match options["top_bar_nav_url"]:
        case False:
            top_bar_nav_url = "-we topbar/hide_url "
        case _:
            top_bar_nav_url = ""

    match options["top_bar_nav_arrows"]:
        case True:
            top_bar_nav_arrows = "-we topbar/show_arrows "
        case _:
            top_bar_nav_arrows = ""


    match options["bottom_bar"]:
        case False:
            bottom_bar = "-we bottombar/hide_bar "
        case _:
            bottom_bar = ""

    cmd = (
        f"{installer}"
        f"{install_fonts}"

        f"{color_theme}"
        f"{web_theme}"
        f"{rounded_corners}"

        f"{win_controls}"
        f"{win_controls_style}"

        f"{library_sidebar}"
        f"{library_whats_new}"

        f"{login_qr}"

        f"{top_bar_bp_button}"
        f"{top_bar_nav_url}"
        f"{top_bar_nav_arrows}"

        f"{bottom_bar}"

        f"{custom_css}"
    )

    return cmd


def install(cmd):
    try:
        ret = subprocess.run(shlex.split(cmd), cwd=paths.EXTRACTED_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
        out = ret.stdout.decode()
        print(out)
        if not out.find("Installing skin"):
            return (False, _("Install: Found no Valid Install Targets"))
    except subprocess.CalledProcessError as e:
        print(e.output.decode())
        return (False, _("Install: Installer Process Failed"))

    return (True, None)

def steam_dir_missing():
    return not os.path.exists(paths.STEAM_DIR) and not os.path.exists(paths.STEAM_FLATPAK_DIR)

def release_missing():
    return not os.path.exists(paths.LAST_RELEASE_FILE) and not os.path.exists(paths.EXTRACTED_DIR)

def zip_not_extracted():
    return os.path.exists(paths.LAST_RELEASE_FILE) and not os.path.exists(paths.EXTRACTED_DIR)

def run(options, beta_support=False):
    if steam_dir_missing():
        return(False, _("Install: Failed to Find Valid '~/.steam/steam' Symlink"))

    if release_missing():
        (ret, msg) = update.check(False, beta_support)
        if not ret:
            return (ret, msg)

    if zip_not_extracted():
        (ret, msg) = update.post_download()
        if not ret:
            return (ret, msg)

    cmd = gen_cmd_line(options, beta_support)
    (ret, msg) = install(cmd)

    return (ret, msg)
