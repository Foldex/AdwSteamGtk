# main.py
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
import sys

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from . import info
from .window import AdwaitaSteamGtkWindow


class Adwaita_steam_gtkApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id=info.APP_ID,
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.create_action('quit', self.on_quit_action, ['<primary>q'])
        self.create_action('about', self.on_about_action)

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = AdwaitaSteamGtkWindow(application=self)
        win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name=info.APP_NAME,
                                application_icon=info.APP_ID,
                                website=info.PROJECT_URL,
                                issue_url=info.BUG_TRACKER_URL,
                                version=info.VERSION,
                                developers=info.DEVELOPERS,
                                license_type=info.LICENSE,
                                copyright=info.COPYRIGHT)
        about.add_credit_section('Upstream', info.UPSTREAM)
        about.present()

    def on_quit_action(self, widget, _):
        self.quit()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = Adwaita_steam_gtkApplication()
    return app.run(sys.argv)
