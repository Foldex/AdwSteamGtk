# paths.py
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

STEAM_DIR=os.path.expanduser("~/.steam/steam")
STEAM_FLATPAK_DIR=os.path.expanduser("~/.var/app/com.valvesoftware.Steam/.steam/steam")

XDG_CACHE_DIR=os.path.expanduser(os.environ.get("XDG_CACHE_HOME", "~/.cache"))
CACHE_DIR=os.path.join(XDG_CACHE_DIR, "AdwSteamInstaller")
TMP_DIR=os.path.join(CACHE_DIR, "tmp")
EXTRACTED_DIR=os.path.join(CACHE_DIR, "extracted")
THEMES_DIR=os.path.join(EXTRACTED_DIR, "extras/colorthemes")

LAST_CHECK_FILE=os.path.join(CACHE_DIR, "last_check")
LAST_VERSION_FILE=os.path.join(CACHE_DIR, "last_ver")
LAST_RELEASE_FILE=os.path.join(CACHE_DIR, "latest.zip")
