# prefs.py
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

import gi

from gi.repository import Adw, Gtk

@Gtk.Template(resource_path='/io/github/Foldex/AdwSteamGtk/ui/prefs.ui')
class AdwaitaSteamGtkPrefs(Adw.PreferencesWindow):
    __gtype_name__ = 'AdwaitaSteamGtkPrefs'

    preview_theme_switch = Gtk.Template.Child()
    update_check_switch = Gtk.Template.Child()

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent
        self.settings = parent.settings
        self.app = self.parent.get_application()
        self.win = self.app.get_active_window()
        self.set_transient_for(self.win)
        self.portal = None

        self.load_config()

    def load_config(self):
        preview_theme = self.settings.get_boolean("prefs-ui-preview-theme")
        self.preview_theme_switch.set_active(preview_theme)
        self.preview_theme_switch.connect("state-set", self.on_preview_theme_switch_toggle)

        update_check = self.settings.get_boolean("prefs-autostart-update-check")
        self.update_check_switch.set_active(update_check)
        self.update_check_switch.connect("state-set", self.on_update_check_switch_toggle)

    def on_preview_theme_switch_toggle(self, *args):
        state = not self.preview_theme_switch.props.state
        self.settings.set_boolean("prefs-ui-preview-theme", state)
        self.parent.load_app_style(self.parent.color_theme_options, None)

    def on_update_check_switch_toggle(self, *args):
        gi.require_version('Xdp', '1.0')
        from gi.repository import Xdp

        if self.portal == None:
            self.portal = Xdp.Portal()

        state = not self.update_check_switch.props.state
        self.settings.set_boolean("prefs-autostart-update-check", state)

        if state:
            flag = Xdp.BackgroundFlags.AUTOSTART
        else:
            flag = Xdp.BackgroundFlags.NONE

        self.portal.request_background(
            None,
            "Update Check",
            ["adwaita-steam-gtk",  "--check"],
            flag,
            None,
            None,
            None
        )
