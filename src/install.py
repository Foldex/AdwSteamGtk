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
from gettext import gettext as _

from . import paths
from . import update

def gen_cmd_line(options):
    installer = "python install.py "

    if options.get("uninstall"):
        return f"{installer} -u"

    match options["color_theme"].lower():
        case "adwaita":
            color_theme = ""
        case _:
            color_theme = f"-c {options['color_theme'].lower()} "

    match options["win_controls"].lower():
        case "left":
            win_controls = "-we windowcontrols/left "
        case "left-all":
            win_controls = "-we windowcontrols/left-all "
        case "right-all":
            win_controls = "-we windowcontrols/right-all "
        case "none":
            win_controls = "-we windowcontrols/none "
        case _:
            win_controls = ""

    match options["web_theme"].lower():
        case "base":
            web_theme = "-w base "
        case "full":
            web_theme = "-w full "
        case _:
            web_theme = ""

    match options["qr_login"].lower():
        case "hide":
            qr_login = "-we login/hide_qr "
        case "hover only":
            qr_login = "-we login/hover_qr "
        case _:
            qr_login = ""

    match options["library_sidebar"].lower():
        case "hover only":
            library_sidebar = "-we library/sidebar_hover "
        case _:
            library_sidebar = ""

    match options["whats_new"]:
        case True:
            whats_new = "-we library/hide_whats_new "
        case _:
            whats_new = ""

    match options["install_fonts"]:
        case True:
            install_fonts = "-fi "
        case _:
            install_fonts = ""

    cmd = (
        f"{installer}"
        f"{color_theme}"
        f"{win_controls}"
        f"{web_theme}"
        f"{qr_login}"
        f"{library_sidebar}"
        f"{whats_new}"
        f"{install_fonts}"
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

def skin_installed():
    return os.path.exists(paths.STEAM_SKIN_DIR) or os.path.exists(paths.STEAM_FLATPAK_SKIN_DIR)

def steam_dir_missing():
    return not os.path.exists(paths.STEAM_DIR) and not os.path.exists(paths.STEAM_FLATPAK_DIR)

def release_missing():
    return not os.path.exists(paths.LAST_RELEASE_FILE) and not os.path.exists(paths.EXTRACTED_DIR)

def zip_not_extracted():
    return os.path.exists(paths.LAST_RELEASE_FILE) and not os.path.exists(paths.EXTRACTED_DIR)

def run(options):
    if steam_dir_missing():
        return(False, "Install: Failed to Find Valid '~/.steam/steam' Symlink")

    if release_missing():
        (ret, msg) = update.check()
        if not ret:
            return (ret, msg)

    if zip_not_extracted():
        (ret, msg) = update.post_download()
        if not ret:
            return (ret, msg)

    cmd = gen_cmd_line(options)
    (ret, msg) = install(cmd)

    return (ret, msg)
