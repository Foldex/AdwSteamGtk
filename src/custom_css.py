# custom_css.py
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
import shutil

from . import paths

TEMPLATE = """/* ------------------ */
/* --- Custom CSS --- */
/* ------------------ */

/* --- EXAMPLE: Override Theme Colors --- */
/* -- DELETE BOTH LINES TO ENABLE
:root
{
	--adw-accent-bg-rgb: 53, 132, 228;
	--adw-accent-fg-rgb: 255, 255, 255;
	--adw-accent-rgb: 120, 174, 237;
}
-- DELETE BOTH LINES TO ENABLE */
"""

def check():
    if not os.path.exists(paths.CONFIG_DIR):
        os.makedirs(paths.CONFIG_DIR)

    if not os.path.exists(paths.CUSTOM_CSS_FILE):
        create()

def create():
    with open(paths.CUSTOM_CSS_FILE, "w") as f:
        f.write(TEMPLATE)

def install():
    shutil.copy(paths.CUSTOM_CSS_FILE, paths.CUSTOM_CSS_FILE_DEST)
