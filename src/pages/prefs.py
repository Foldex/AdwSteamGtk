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
import os

gi.require_version('Xdp', '1.0')
gi.require_version('XdpGtk4', '1.0')
from gi.repository import Adw, Gtk, Xdp, XdpGtk4

from . import paths
from . import update

@Gtk.Template(resource_path='/io/github/Foldex/AdwSteamGtk/ui/prefs.ui')
class AdwaitaSteamGtkPrefs(Adw.PreferencesWindow):
    __gtype_name__ = 'AdwaitaSteamGtkPrefs'

    custom_css_switch = Gtk.Template.Child()
    install_fonts_switch = Gtk.Template.Child()
    preview_theme_switch = Gtk.Template.Child()
    update_check_switch = Gtk.Template.Child()
    beta_support_switch = Gtk.Template.Child()

    open_custom_css_button = Gtk.Template.Child()

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent
        self.settings = parent.settings
        self.app = self.parent.get_application()
        self.win = self.app.get_active_window()
        self.set_transient_for(self.win)
        self.portal = None

        self.setup_widgets()

    def setup_switch(self, switch, config, callback):
        switch.set_active(self.settings.get_boolean(config))
        switch.connect("state-set", callback)

    def setup_widgets(self):
        self.setup_switch(self.preview_theme_switch, "prefs-ui-preview-theme", self.on_preview_theme_switch_toggle)
        self.setup_switch(self.update_check_switch, "prefs-autostart-update-check", self.on_update_check_switch_toggle)
        self.setup_switch(self.install_fonts_switch, "prefs-install-fonts", self.on_install_fonts_switch_toggle)
        self.setup_switch(self.custom_css_switch, "prefs-install-custom-css", self.on_custom_css_switch_toggle)
        self.setup_switch(self.beta_support_switch, "prefs-beta-support", self.on_beta_support_switch_toggle)
        self.open_custom_css_button.connect("clicked", self.on_open_custom_css_button_clicked)

    def on_preview_theme_switch_toggle(self, *args):
        state = not self.preview_theme_switch.props.state
        self.settings.set_boolean("prefs-ui-preview-theme", state)
        self.parent.load_app_style(self.parent.color_theme_options, None)

    def on_beta_support_switch_toggle(self, *args):
        state = not self.beta_support_switch.props.state
        self.settings.set_boolean("prefs-beta-support", state)

        dialog = Adw.MessageDialog(transient_for=self.parent,
                                   heading=_("Shutting Down"),
                                   body=_("Relaunch AdwSteamGtk to apply this change."))

        dialog.add_response("confirm", _("Okay"))
        dialog.set_default_response("confirm")

        dialog.connect("response", self.on_beta_support_response)
        dialog.present()

    def on_beta_support_response(self, dialog, response):
        update.clean_dir(paths.EXTRACTED_DIR)
        os.remove(paths.LAST_CHECK_FILE)
        os.remove(paths.LAST_RELEASE_FILE)
        os.remove(paths.LAST_VERSION_FILE)
        self.app.quit()

    def on_update_check_switch_toggle(self, *args):
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

    def on_install_fonts_switch_toggle(self, *args):
        state = not self.install_fonts_switch.props.state
        self.settings.set_boolean("prefs-install-fonts", state)

    def on_custom_css_switch_toggle(self, *args):
        state = not self.custom_css_switch.props.state
        self.settings.set_boolean("prefs-install-custom-css", state)

    def on_open_custom_css_button_clicked(self, *args):
        if self.portal == None:
            self.portal = Xdp.Portal()

        parent = XdpGtk4.parent_new_gtk(self)
        self.portal.open_uri(parent, paths.CUSTOM_CSS_URI, Xdp.OpenUriFlags.WRITABLE, None, None);

