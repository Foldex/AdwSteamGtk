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
from gettext import gettext as _

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

    color_theme_options = Gtk.Template.Child()
    web_theme_options = Gtk.Template.Child()
    no_rounded_corners_switch = Gtk.Template.Child()

    window_controls_options = Gtk.Template.Child()
    window_controls_style_options = Gtk.Template.Child()

    library_sidebar_options = Gtk.Template.Child()
    hide_whats_new_switch = Gtk.Template.Child()

    login_qr_options = Gtk.Template.Child()

    hide_bp_button_switch = Gtk.Template.Child()
    hide_nav_url_switch = Gtk.Template.Child()
    show_nav_arrows_switch = Gtk.Template.Child()

    hide_bottom_bar_switch = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.make_action("install", self.install_theme)
        self.make_action("retry_dl", self.retry_check)
        self.check_latest_release()
        self.check_custom_css()
        self.load_color_themes()
        self.load_config()
        self.style_provider = None
        self.color_theme_options.connect("notify", self.load_app_style)

    def make_action(self, action, func):
        install_action = Gio.SimpleAction(name=action)
        install_action.connect("activate", func)
        self.add_action(install_action)

    def pop_toast(self, toast):
        self.toast_overlay.add_toast(toast)

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
        self.select_from_config('color-theme-options', self.color_theme_options)
        self.select_from_config('web-theme-options', self.web_theme_options)
        self.select_from_config('no-rounded-corners-switch', self.no_rounded_corners_switch)

        self.select_from_config('window-controls-options', self.window_controls_options)
        self.select_from_config('window-controls-style-options', self.window_controls_style_options)

        self.select_from_config('library-sidebar-options', self.library_sidebar_options)
        self.select_from_config('hide-whats-new-switch', self.hide_whats_new_switch)

        self.select_from_config('login-qr-options', self.login_qr_options)

        self.select_from_config('hide-bp-button-switch', self.hide_bp_button_switch)
        self.select_from_config('hide-nav-url-switch', self.hide_nav_url_switch)
        self.select_from_config('show-nav-arrows-switch', self.show_nav_arrows_switch)

        self.select_from_config('hide-bottom-bar-switch', self.hide_bottom_bar_switch)


    def save_config(self):
        self.config_from_select('color-theme-options', self.color_theme_options)
        self.config_from_select('web-theme-options', self.web_theme_options)
        self.config_from_select('no-rounded-corners-switch', self.no_rounded_corners_switch)

        self.config_from_select('window-controls-options', self.window_controls_options)
        self.config_from_select('window-controls-style-options', self.window_controls_style_options)

        self.config_from_select('library-sidebar-options', self.library_sidebar_options)
        self.config_from_select('hide-whats-new-switch', self.hide_whats_new_switch)

        self.config_from_select('login-qr-options', self.login_qr_options)

        self.config_from_select('hide-bp-button-switch', self.hide_bp_button_switch)
        self.config_from_select('hide-nav-url-switch', self.hide_nav_url_switch)
        self.config_from_select('show-nav-arrows-switch', self.show_nav_arrows_switch)

        self.config_from_select('hide-bottom-bar-switch', self.hide_bottom_bar_switch)

    def get_selected_pref(self, widget):
        match type := widget.get_name():
            case "AdwComboRow":
                selected = widget.get_selected_item().get_string()
            case "GtkSwitch":
                selected = widget.get_active()
            case _:
                print(f"get_selected_pref: unsupported type {type}")
                selected = None
        return selected

    def config_to_pos(self, config, comborow):
        string = self.settings.get_string(config)
        for pos,s in enumerate(comborow.get_model()):
            if string == s.get_string():
                return pos
        return 0

    def select_from_config(self, config, widget):
        match type := widget.get_name():
            case "AdwComboRow":
                widget.set_selected(self.config_to_pos(config, widget))
            case "GtkSwitch":
                widget.set_active(self.settings.get_boolean(config))
            case _:
                print(f"set_from_config: unsupported type {type}")

    def config_from_select(self, config, widget):
        match type := widget.get_name():
            case "AdwComboRow":
                self.settings.set_string(config, widget.get_selected_item().get_string())
            case "GtkSwitch":
                self.settings.set_boolean(config, widget.get_active())
            case _:
                print(f"config_from_select: unsupported type {type}")

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

    def retry_check(self, *args):
        self.check_latest_release()

    def check_custom_css(self):
        custom_css.check()

    def install_theme(self, *args):
        options = {
            # switches that hide/disable get inverted
            "install_fonts": self.settings.get_boolean('prefs-install-fonts'),
            "custom_css": self.settings.get_boolean('prefs-install-custom-css'),

            "color_theme": self.get_selected_pref(self.color_theme_options),
            "web_theme": self.get_selected_pref(self.web_theme_options),
            "rounded_corners": not self.get_selected_pref(self.no_rounded_corners_switch),

            "win_controls": self.get_selected_pref(self.window_controls_options),
            "win_controls_style": self.get_selected_pref(self.window_controls_style_options),

            "library_sidebar": self.get_selected_pref(self.library_sidebar_options),
            "library_whats_new": not self.get_selected_pref(self.hide_whats_new_switch),

            "login_qr": self.get_selected_pref(self.login_qr_options),

            "top_bar_bp_button": not self.get_selected_pref(self.hide_bp_button_switch),
            "top_bar_nav_url": not self.get_selected_pref(self.hide_nav_url_switch),
            "top_bar_nav_arrows": self.get_selected_pref(self.show_nav_arrows_switch),

            "bottom_bar": not self.get_selected_pref(self.hide_bottom_bar_switch),
        }

        (ret, msg) = install.run(options)

        if ret:
            t = Adw.Toast(title=_("Theme Installed"), priority="high", timeout=2)
            self.save_config()
        else:
            t = Adw.Toast(title=msg, priority="high")

        self.pop_toast(t)
