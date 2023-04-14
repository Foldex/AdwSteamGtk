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

def gen_cmd_line(options):
    installer = "python install.py "

    if options["color_theme"].lower() == "adwaita":
        color_theme = ""
    else:
        color_theme = f"-c {options['color_theme'].lower()} "

    if options["win_controls"] == "Left":
        patch = "-p windowcontrols/left "
    elif options["win_controls"] == "Left-All":
        patch = "-p windowcontrols/left-all "
    elif options["win_controls"] == "Right-All":
        patch = "-p windowcontrols/right-all "
    elif options["win_controls"] == "None":
        patch = "-p windowcontrols/hide-close "
    else:
        patch = ""

    if options["web_theme"] == "Full":
        web_theme = "-w full "
    elif options["web_theme"] == "None":
        web_theme = "-w none "
    else:
        web_theme = "-w base "

    if options["qr_login"] == "Hover Only":
        qr_login = "-we login/hover_qr "
    elif options["qr_login"] == "Hide":
        qr_login = "-we login/hide_qr "
    else:
        qr_login = ""

    if options["library_sidebar"] == "Hover Only":
        library_sidebar = "-we library/sidebar_hover "
    else:
        library_sidebar = ""

    if options["whats_new"]:
        whats_new = "-we library/hide_whats_new "
    else:
        whats_new = ""

    cmd = (
        f"{installer}"
        f"{color_theme}"
        f"{patch}"
        f"{web_theme}"
        f"{qr_login}"
        f"{library_sidebar}"
        f"{whats_new}"
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

def zip_not_extracted():
    return os.path.exists(paths.LAST_RELEASE_FILE) and not os.path.exists(paths.EXTRACTED_DIR)

def run(options):

    if steam_dir_missing():
        return(False, "Install: Failed to Find Valid '~/.steam/steam' Symlink")

    if zip_not_extracted():
        (ret, msg) = update.post_download()
        if not ret:
            return (ret, msg)

    cmd = gen_cmd_line(options)
    (ret, msg) = install(cmd)

    return (ret, msg)
