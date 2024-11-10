# dl.py
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

from gi.repository import Gio
from enum import Enum

from . import info
from . import install
from . import update
from . import zip

class result(Enum):
    CONTINUE = 0
    EXIT = 1
    NOTIFY_AND_EXIT = 2
    PRINT_AND_EXIT = 3
    FAIL = 4

def update_install(cli_args, beta_support=False):
    (code, msg) = update.check(False, beta_support)
    force_install = cli_args.get("install", False)
    option_string = cli_args.get("options")

    if code == update.ExitCode.FAIL:
        code = result.PRINT_AND_EXIT
        t = msg
    elif code == update.ExitCode.SUCCESS or force_install:
        options = get_options(option_string)
        (code, msg) = install.run(options, beta_support)
        t = msg
    elif code == update.ExitCode.CURRENT:
        code = result.PRINT_AND_EXIT
        t = _("Up to Date.")
    else:
        code = result.EXIT
        t = None
    return (code, t)

def get_options(option_string):
        settings = Gio.Settings.new(info.APP_ID)
        options = {
            "custom_css": settings.get_boolean('prefs-install-custom-css'),

            "color_theme": settings.get_string('color-theme-options'),
            "rounded_corners": not settings.get_boolean('no-rounded-corners-switch'),

            "win_controls": settings.get_string('window-controls-options'),
            "win_controls_layout": settings.get_string('window-controls-layout-options'),

            "library_sidebar": settings.get_string('library-sidebar-options'),
            "library_whats_new": not settings.get_boolean('hide-whats-new-switch'),

            "login_qr": settings.get_string('login-qr-options'),
        }

        if option_string is None:
            return options

        valid_options = {
            "custom_css": (True, False),

            "rounded_corners": (True, False),

            "win_controls": ("Adwaita", "MacOS", "Windows"),
            "win_controls_layout": ("Auto", "Adwaita", "Elementary", "MacOS", "Windows"),

            "library_sidebar": ("Show", "Hover Only"),
            "library_whats_new": (True, False),

            "login_qr": ("Show", "Hover Only", "Hide"),
        }

        if ":" not in option_string:
            return options

        user_options = option_string_dict(option_string)

        # override defaults/last selected options
        for key,val in user_options.items():
            cur_val = val.title().replace("_", " ")

            # map boolean values
            if cur_val in ("True", "Yes", "On", "T", "Y"):
                cur_val = True
            elif cur_val in ("False", "No", "Off", "F", "N"):
                cur_val = False

            if cur_val in valid_options.get(key, ()):
                options[key] = cur_val
            elif key != "color_theme":
                print(_("{key}: {cur_val} invalid value").format(key=key, cur_val=cur_val))


        themes_list, msg = zip.get_color_themes()

        if themes_list == ["Adwaita"]:
            print(_("Could not get theme list. Falling back to last selected theme."))
            return options

        if user_options.get("color_theme", "").title() in themes_list:
            options["color_theme"] = user_options["color_theme"]
        elif user_options.get("color_theme") is not None:
            print(_("Could not find theme {colortheme} in theme list. Falling back to last selected theme.").format(colortheme=user_options['color_theme']))

        return options

def option_string_dict(option_string):
    if option_string[-1] == ";":
        option_string = option_string[:-1]

    return dict(x.split(":") for x in option_string.split(";"))

def update_notify():
    (code, msg) = update.check(check_only := True, False)

    if code == update.ExitCode.SUCCESS:
        code = result.NOTIFY_AND_EXIT
        t = _("New Release Available: ") + msg
    elif code == update.ExitCode.FAIL:
        code = result.NOTIFY_AND_EXIT
        t = _("Update Check Failed: ") + msg
    elif code == update.ExitCode.CURRENT:
        code = result.PRINT_AND_EXIT
        t = _("Up to Date.")
    else:
        code = result.EXIT
        t = None

    return (code, t)
