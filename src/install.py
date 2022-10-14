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

import glob
import os
import shlex
import shutil
import subprocess
import zipfile

from . import paths

def clean_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def extract(path, out_dir):
    try:
        with zipfile.ZipFile(path) as f:
             f.extractall(out_dir)
    except IOError:
        return (False, _("Extract: Failed to read ZIP archive"))
    except zipfile.BadZipFile:
        return (False, _("Extract: Bad ZIP File"))
    except:
        return (False, _("Extract: Failed to Extract ZIP File"))

    return (True, None)

def move_extract_dir(path, rename):
    for dir in glob.glob(path + "/tkashkin-Adwaita-for-Steam-*"):
        shutil.move(dir, rename)

def gen_cmd_line(options):

    installer = "python install.py "

    if options["win_controls"] == "Left":
        patch = "-p windowcontrols/left "
    elif options["win_controls"] == "Left-All":
        patch = "-p windowcontrols/left-all "
    elif options["win_controls"] == "Right-All":
        patch = "-p windowcontrols/right-all "
    else:
        patch = ""

    if options["web_theme"] == "Full":
        web_theme = "-w full "
    elif options["web_theme"] == "None":
        web_theme = "-w none "
    else:
        web_theme = "-w base "

    if options["whats_new"]:
        whats_new = "-we library/hide_whats_new "
    else:
        whats_new = ""

    cmd = (
        f"{installer}"
        f"{patch}"
        f"{web_theme}"
        f"{whats_new}"
    )

    return cmd


def install(cmd):
    try:
        ret = subprocess.run(shlex.split(cmd), cwd=paths.EXTRACTED_DIR, check=True, capture_output=True)
        if not ret.stdout.decode().find("Installing skin"):
            return (False, _("Install: Found no Valid Install Targets"))
    except subprocess.CalledProcessError:
        return (False, _("Install: Installer Process Failed"))

    return (True, None)

def steam_dir_missing():
    return not os.path.exists(paths.STEAM_DIR) and not os.path.exists(paths.STEAM_FLATPAK_DIR)

def run(options):

    if steam_dir_missing():
        return(False, "Install: Failed to Find Valid '~/.steam/steam' Symlink")

    clean_dir(paths.TMP_DIR)
    clean_dir(paths.EXTRACTED_DIR)

    (ret, msg) = extract(paths.LAST_RELEASE_FILE, paths.TMP_DIR)

    if not ret:
        clean_dir(paths.TMP_DIR)
        clean_dir(paths.EXTRACTED_DIR)
        return (ret, msg)

    move_extract_dir(paths.TMP_DIR, paths.EXTRACTED_DIR)
    clean_dir(paths.TMP_DIR)

    cmd = gen_cmd_line(options)
    (ret, msg) = install(cmd)

    clean_dir(paths.EXTRACTED_DIR)

    return (ret, msg)
