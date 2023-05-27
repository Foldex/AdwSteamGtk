# zip.py
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

import zipfile
from gettext import gettext as _
from pathlib import Path

from . import paths

COLOR_THEMES_PREFIX="/colorthemes"
COLOR_THEMES_EXT=".theme"

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

# TODO No longer need to parse ZIP for this
def get_color_themes():
    themes = []
    fallback = ["Adwaita"]

    try:
        with zipfile.ZipFile(paths.LAST_RELEASE_FILE) as f:
             nl = f.namelist()
             themes = [s for s in nl if s[-6:] == COLOR_THEMES_EXT]
             themes = [s for s in themes if COLOR_THEMES_PREFIX in s]
             themes = [str(Path(s).stem.title()) for s in themes]
    except IOError:
        return (fallback, _("Get Themes: Failed to read ZIP archive"))
    except zipfile.BadZipFile:
        return (fallback, _("Get Themes: Bad ZIP File"))
    except:
        return (fallback, _("Get Themes: Failed to get themes"))

    return (themes, None)
