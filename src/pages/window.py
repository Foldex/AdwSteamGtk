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

from . import custom_css
from . import info
from . import install
from . import style
from . import update
from . import zip

@Gtk.Template(resource_path='/io/github/Foldex/AdwSteamGtk/ui/window.ui')
class AdwaitaSteamGtkWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'AdwaitaSteamGtkWindow'

    settings = Gio.Settings.new(info.APP_ID)
    install_button = Gtk.Template.Child()
    toast_overlay = Gtk.Template.Child()

    theme_group = Gtk.Template.Child()
    color_theme_options = Gtk.Template.Child()
    no_rounded_corners = Gtk.Template.Child()
    no_rounded_corners_switch = Gtk.Template.Child()

    window_controls_group = Gtk.Template.Child()
    window_controls_options = Gtk.Template.Child()
    window_controls_layout_options = Gtk.Template.Child()

    library_group = Gtk.Template.Child()
    library_sidebar_options = Gtk.Template.Child()
    hide_whats_new_switch = Gtk.Template.Child()

    login_group = Gtk.Template.Child()
    login_qr_options = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Disable Beta Support
        self.settings.set_boolean("prefs-beta-support", False)
        self.beta_support = self.settings.get_boolean("prefs-beta-support")

        self.opt_array = {
            "color_theme": ["Adwaita"],

            "win_controls": ["Adwaita", "MacOS", "Windows"],
            "win_controls_layout": ["Auto", "Adwaita", "Elementary", "MacOS", "Windows", "None"],

            "library_sidebar": ["Show", "Hover Only"],

            "login_qr": ["Show", "Hover Only", "Hide"]
        }

        self.make_action("install", self.install_theme)
        self.make_action("retry_dl", self.retry_check)
        self.check_latest_release()
        self.check_custom_css()
        self.load_color_themes()
        self.load_config()
        self.style_provider = None
        self.load_app_style()
        self.color_theme_options.connect("notify::selected", self.load_app_style)

    def make_action(self, action, func):
        install_action = Gio.SimpleAction(name=action)
        install_action.connect("activate", func)
        self.add_action(install_action)

    def pop_toast(self, toast):
        self.toast_overlay.add_toast(toast)

    def load_app_style(self, *args):
        if self.style_provider is None:
            self.style_provider = Gtk.CssProvider()
            Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER + 1)

        preview_theme = self.settings.get_boolean("prefs-ui-preview-theme")

        if not preview_theme:
            self.style_provider.load_from_data("", -1)
            return

        selected_theme = self.get_selected_pref(self.color_theme_options, self.opt_array["color_theme"]).lower()
        ret, msg = style.generate_style(selected_theme)

        if not ret:
            t = Adw.Toast(title=msg, priority="high")
            self.pop_toast(t)

        self.style_provider.load_from_data(msg, -1)

    def load_color_themes(self):
        (themes, msg) = style.get_color_themes()

        if msg:
            t = Adw.Toast(title=msg, priority="high")
            self.pop_toast(t)

        self.opt_array["color_theme"] = themes
        self.color_theme_options.set_model(Gtk.StringList.new(themes))

    def load_config(self):
        self.select_from_config('color-theme-options', self.color_theme_options, self.opt_array["color_theme"])
        self.select_from_config('no-rounded-corners-switch', self.no_rounded_corners_switch)

        self.select_from_config('window-controls-options', self.window_controls_options, self.opt_array["win_controls"])
        self.select_from_config('window-controls-layout-options', self.window_controls_layout_options, self.opt_array["win_controls_layout"])

        self.select_from_config('library-sidebar-options', self.library_sidebar_options, self.opt_array["library_sidebar"])
        self.select_from_config('hide-whats-new-switch', self.hide_whats_new_switch)

        self.select_from_config('login-qr-options', self.login_qr_options, self.opt_array["login_qr"])

    def save_config(self):
        self.config_from_select('color-theme-options', self.color_theme_options, self.opt_array["color_theme"])
        self.config_from_select('no-rounded-corners-switch', self.no_rounded_corners_switch)

        self.config_from_select('window-controls-options', self.window_controls_options, self.opt_array["win_controls"])
        self.config_from_select('window-controls-layout-options', self.window_controls_layout_options, self.opt_array["win_controls_layout"])

        self.config_from_select('library-sidebar-options', self.library_sidebar_options, self.opt_array["library_sidebar"])
        self.config_from_select('hide-whats-new-switch', self.hide_whats_new_switch)

        self.config_from_select('login-qr-options', self.login_qr_options, self.opt_array["login_qr"])


    def get_selected_pref(self, widget, array=None):
        match type := widget.get_name():
            case "AdwComboRow":
                if not array:
                    print("get_selected_pref: AdwComboRows need array passed")
                    selected = None
                else:
                    selected = array[widget.get_selected()]
            case "GtkSwitch":
                selected = widget.get_active()
            case _:
                print(f"get_selected_pref: unsupported type {type}")
                selected = None
        return selected

    def config_to_pos(self, config, array):
        string = self.settings.get_string(config)
        for pos,s in enumerate(array):
            if string == s:
                return pos
        return 0

    def select_from_config(self, config, widget, array=None):
        match type := widget.get_name():
            case "AdwComboRow":
                if not array:
                    print("select_from_config: AdwComboRows need array passed")
                else:
                    widget.set_selected(self.config_to_pos(config, array))
            case "GtkSwitch":
                widget.set_active(self.settings.get_boolean(config))
            case _:
                print(f"set_from_config: unsupported type {type}")

    def config_from_select(self, config, widget, array=None):
        match type := widget.get_name():
            case "AdwComboRow":
                if not array:
                    print("config_from_select: AdwComboRows need array passed")
                else:
                    self.settings.set_string(config, array[widget.get_selected()])
            case "GtkSwitch":
                self.settings.set_boolean(config, widget.get_active())
            case _:
                print(f"config_from_select: unsupported type {type}")

    def check_latest_release(self):
        (code, msg) = update.check(False, self.beta_support)
        t = None

        if code == update.ExitCode.SUCCESS:
            t = Adw.Toast(title=_("New Release Downloaded: ") + msg, timeout=2)
        elif code == update.ExitCode.FAIL:
            t = Adw.Toast(title=msg, button_label=_("Retry"), action_name="win.retry_dl", timeout=30)
        # elif code == update.ExitCode.CURRENT:
        #     t = Adw.Toast(title=_("Up to Date"))

        if t:
            self.pop_toast(t)

    def retry_check(self, *args):
        self.check_latest_release()

    def check_custom_css(self):
        custom_css.check()

    def install_theme(self, *args):
        options = {
            # switches that hide/disable get inverted
            "custom_css": self.settings.get_boolean('prefs-install-custom-css'),

            "color_theme": self.get_selected_pref(self.color_theme_options, self.opt_array["color_theme"]),
            "rounded_corners": not self.get_selected_pref(self.no_rounded_corners_switch),

            "win_controls": self.get_selected_pref(self.window_controls_options, self.opt_array["win_controls"]),
            "win_controls_layout": self.get_selected_pref(self.window_controls_layout_options, self.opt_array["win_controls_layout"]),

            "library_sidebar": self.get_selected_pref(self.library_sidebar_options, self.opt_array["library_sidebar"]),
            "library_whats_new": not self.get_selected_pref(self.hide_whats_new_switch),

            "login_qr": self.get_selected_pref(self.login_qr_options, self.opt_array["login_qr"]),
        }

        (ret, msg) = install.run(options, self.beta_support)

        if ret:
            t = Adw.Toast(title=_("Theme Installed"), priority="high", timeout=2)
            self.save_config()
        else:
            t = Adw.Toast(title=msg, priority="high")

        self.pop_toast(t)
