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
from gettext import gettext as _

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

def update_install(cli_args):
    (code, msg) = update.check()
    force_install = cli_args.get("install", False)
    option_string = cli_args.get("options")

    if code == update.ExitCode.FAIL:
        code = result.PRINT_AND_EXIT
        t = msg
    elif code == update.ExitCode.SUCCESS or force_install:
        options = get_options(option_string)
        (code, msg) = install.run(options)
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
            "color_theme": settings.get_string('color-theme-options'),
            "win_controls": settings.get_string('window-controls-options'),
            "web_theme": settings.get_string('web-theme-options'),
            "qr_login": settings.get_string('qr-login-options'),
            "library_sidebar": settings.get_string('library-sidebar-options'),
            "whats_new": settings.get_boolean('whats-new-switch')
        }

        if option_string is None:
            return options

        valid_options = {
            "win_controls": ("Default", "Right-All", "Left", "Left-All", "None"),
            "web_theme": ("None", "Base", "Full"),
            "qr_login": ("Show", "Hover Only", "Hide"),
            "library_sidebar": ("Show", "Hover Only"),
            "whats_new": (True, False)
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

            # invert whats new
            if key == "whats_new":
                cur_val = not cur_val

            if cur_val in valid_options.get(key, ()):
                options[key] = cur_val
            elif key != "colortheme":
                print(_("{key}: {cur_val} invalid value").format(key=key, cur_val=cur_val))


        themes_list, msg = zip.get_color_themes()

        if themes_list == ["Adwaita"]:
            print(_("Could not get theme list. Falling back to last selected theme."))
            return options

        if user_options.get("colortheme", "").title() in themes_list:
            options["color_theme"] = user_options["colortheme"]
        elif user_options.get("colortheme") is not None:
            print(_("Could not find theme {colortheme} in theme list. Falling back to last selected theme.").format(colortheme=user_options['colortheme']))

        return options

def option_string_dict(option_string):
    if option_string[-1] == ";":
        option_string = option_string[:-1]

    return dict(x.split(":") for x in option_string.split(";"))

def update_notify():
    (code, msg) = update.check(check_only := True)

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
