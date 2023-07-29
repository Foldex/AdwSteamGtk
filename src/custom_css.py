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
	--bg: #242424;
	--fg: #FFFFFF;

	--headerbar_bg: #303030;
	--popover_bg: #383838;
	--view_bg: #1E1E1E;

	--accent: #78AEED;
	--accent_bg: #3584E4;
	--accent_disabled: #78AEED80;
	--accent_hover_bg: #78AEED12;
	--accent_active_bg: #78AEED29;
	--focusring: #78AEED80;

	--destructive: #FF7B63;
	--destructive_bg: #C01C28;
	--destructive_disabled: #FF7B6380;
	--destructive_hover_bg: #FF7B6312;
	--destructive_active_bg: #FF7B6329;

	--success: #8FF0A4;
	--success_bg: #26A269;
	--success_fg: var(--fg);

	--warning: #F8E45C;
	--warning_bg: #CD9309;
	--warning_fg: var(--fg);

	--error: #FF7B63;
	--error_bg: #C01C28;
	--error_fg: var(--fg);
}
-- DELETE BOTH LINES TO ENABLE */

/* --- EXAMPLE: Hide Whats New --- */
/* -- DELETE BOTH LINES TO ENABLE
#SteamDesktop .library_Container_3xRRJ div[class*="libraryhome_UpdatesContainer_"]
{
	display: none !important;
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
