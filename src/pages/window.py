# window.py
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

from gi.repository import Adw, Gio, Gtk, Gdk

from . import info
from . import install
from . import style
from . import update
from . import zip

@Gtk.Template(resource_path='/io/github/Foldex/AdwSteamGtk/ui/window.ui')
class AdwaitaSteamGtkWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'AdwaitaSteamGtkWindow'

    toast_overlay = Gtk.Template.Child()

    color_theme_options = Gtk.Template.Child()
    window_controls_options = Gtk.Template.Child()
    web_theme_options = Gtk.Template.Child()
    qr_login_options = Gtk.Template.Child()
    library_sidebar_options = Gtk.Template.Child()

    whats_new_switch = Gtk.Template.Child()
    install_button = Gtk.Template.Child()

    settings = Gio.Settings.new(info.APP_ID)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.make_action("install", self.install_theme)
        self.make_action("retry_dl", self.retry_check)

        if install.skin_installed():
            self.install_button.set_label("Update")

        self.check_latest_release()
        self.load_color_themes()
        self.load_config()
        self.style_provider = None
        self.color_theme_options.connect("notify", self.load_app_style)

    def load_app_style(self, comborow, _):
        if self.style_provider is None:
            self.style_provider = Gtk.CssProvider()
            Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER + 1)

        preview_theme = self.settings.get_boolean("prefs-ui-preview-theme")

        if not preview_theme:
            self.style_provider.load_from_data("", -1)
            return

        selected_theme = self.get_selected_pref(comborow).lower()
        ret, msg = style.generate_style(selected_theme)

        if not ret:
            t = Adw.Toast(title=msg, priority="high")
            self.pop_toast(t)

        self.style_provider.load_from_data(msg, -1)

    def load_color_themes(self):
        (themes, msg) = zip.get_color_themes()

        if msg:
            t = Adw.Toast(title=msg, priority="high")
            self.pop_toast(t)

        self.color_theme_options.set_model(Gtk.StringList.new(themes))

    def load_config(self):
        options = {
            "color_theme": self.config_to_pos('color-theme-options', self.color_theme_options),
            "win_controls": self.config_to_pos('window-controls-options', self.window_controls_options),
            "web_theme": self.config_to_pos('web-theme-options', self.web_theme_options),
            "qr_login": self.config_to_pos('qr-login-options', self.qr_login_options),
            "library_sidebar": self.config_to_pos('library-sidebar-options', self.library_sidebar_options),
            "whats_new": self.settings.get_boolean('whats-new-switch')
        }

        self.color_theme_options.set_selected(options["color_theme"])
        self.window_controls_options.set_selected(options["win_controls"])
        self.web_theme_options.set_selected(options["web_theme"])
        self.qr_login_options.set_selected(options["qr_login"])
        self.library_sidebar_options.set_selected(options["library_sidebar"])
        self.whats_new_switch.set_active(options["whats_new"])

    def save_config(self, options):
        self.settings.set_string("color-theme-options", options['color_theme'])
        self.settings.set_string("window-controls-options", options['win_controls'])
        self.settings.set_string("web-theme-options", options['web_theme'])
        self.settings.set_string("qr-login-options", options['qr_login'])
        self.settings.set_string("library-sidebar-options", options['library_sidebar'])
        self.settings.set_boolean("whats-new-switch", options['whats_new'])

    def config_to_pos(self, config, comborow):
        string = self.settings.get_string(config)
        for pos,s in enumerate(comborow.get_model()):
            if string == s.get_string():
                return pos
        return 0

    def make_action(self, action, func):
        install_action = Gio.SimpleAction(name=action)
        install_action.connect("activate", func)
        self.add_action(install_action)

    def pop_toast(self, toast):
        self.toast_overlay.add_toast(toast)

    def get_selected_pref(self, comborow):
        selected = comborow.get_selected_item()
        return selected.get_string()

    def check_latest_release(self):
        (code, msg) = update.check()
        t = None

        if code == update.ExitCode.SUCCESS:
            t = Adw.Toast(title=_("New Release Downloaded: ") + msg, timeout=2)
        elif code == update.ExitCode.FAIL:
            t = Adw.Toast(title=msg, button_label=_("Retry"), action_name="win.retry_dl", timeout=30)
        # elif code == update.ExitCode.CURRENT:
        #     t = Adw.Toast(title=_("Up to Date"))

        if t:
            self.pop_toast(t)

    def retry_check(self, action, _):
        self.check_latest_release()

    def install_theme(self, action, _):
        options = {
            "color_theme": self.get_selected_pref(self.color_theme_options),
            "win_controls": self.get_selected_pref(self.window_controls_options),
            "web_theme": self.get_selected_pref(self.web_theme_options),
            "qr_login": self.get_selected_pref(self.qr_login_options),
            "library_sidebar": self.get_selected_pref(self.library_sidebar_options),
            "whats_new":  self.whats_new_switch.get_active()
        }

        (ret, msg) = install.run(options)

        if ret:
            t = Adw.Toast(title="Theme Installed", priority="high", timeout=2)

            if install.skin_installed():
                self.install_button.set_label("Update")

            self.save_config(options)
        else:
            t = Adw.Toast(title=msg, priority="high")

        self.pop_toast(t)
