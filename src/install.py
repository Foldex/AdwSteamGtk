# install.py
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
import shlex
import subprocess
import gi

from gi.repository import Gio, GLib

from . import custom_css
from . import paths
from . import update

def gen_cmd_line(options, beta_support):
    installer = "python install.py "

    if options.get("uninstall"):
        return f"{installer} -u"

    match options["custom_css"]:
        case True:
            custom_css = "--custom-css "
        case _:
            custom_css = ""


    match options["color_theme"].lower():
        case "adwaita":
            color_theme = ""
        case _:
            color_theme = f"-c {options['color_theme'].lower()} "

    match options["rounded_corners"]:
        case False:
            rounded_corners = "-e general/no_rounded_corners "
        case _:
            rounded_corners = ""

    match options["win_controls"].lower():
        case "auto":
            win_controls = "--windowcontrols-theme auto "
        case "adwaita":
            win_controls = "--windowcontrols-theme adwaita "
        case "windows":
            win_controls = "--windowcontrols-theme windows "
        case "macos":
            win_controls = "--windowcontrols-theme macos "
        case _:
            win_controls = ""

    match options["win_controls_layout"].lower():
        case "auto":
            button_layout = get_button_layout()
            if button_layout:
                win_controls_layout = f"--windowcontrols-layout {button_layout} "
            else:
                win_controls_layout = ""
        case "adwaita":
            win_controls_layout = "--windowcontrols-layout adwaita "
        case "elementary":
            win_controls_layout = "--windowcontrols-layout elementary "
        case "windows":
            win_controls_layout = "--windowcontrols-layout windows "
        case "macos":
            win_controls_layout = "--windowcontrols-layout macos "
        case "none":
            win_controls_layout = "--windowcontrols-layout ':' "
        case _:
            win_controls_layout = ""


    match options["library_sidebar"].lower():
        case "hover only":
            library_sidebar = "-e library/sidebar_hover "
        case _:
            library_sidebar = ""

    match options["library_whats_new"]:
        case False:
            library_whats_new = "-e library/hide_whats_new "
        case _:
            library_whats_new = ""


    match options["login_qr"].lower():
        case "hide":
            login_qr = "-e login/hide_qr "
        case "hover only":
            login_qr = "-e login/hover_qr "
        case _:
            login_qr = ""

    cmd = (
        f"{installer}"

        f"{color_theme}"
        f"{rounded_corners}"

        f"{win_controls}"
        f"{win_controls_layout}"

        f"{library_sidebar}"
        f"{library_whats_new}"

        f"{login_qr}"

        f"{custom_css}"
    )

    return cmd


def install(cmd):
    try:
        ret = subprocess.run(shlex.split(cmd), cwd=paths.EXTRACTED_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
        out = ret.stdout.decode()
        print(out)
        if not out.find("Installing skin"):
            return (False, _("Install: Found no Valid Install Targets"))
    except subprocess.CalledProcessError as e:
        print(e.output.decode())
        return (False, _("Install: Installer Process Failed"))

    return (True, None)

def steam_dir_missing():
    return not os.path.exists(paths.STEAM_DIR) and not os.path.exists(paths.STEAM_FLATPAK_DIR)

def release_missing():
    return not os.path.exists(paths.LAST_RELEASE_FILE) and not os.path.exists(paths.EXTRACTED_DIR)

def zip_not_extracted():
    return os.path.exists(paths.LAST_RELEASE_FILE) and not os.path.exists(paths.EXTRACTED_DIR)

def get_button_layout():
    portal = Gio.DBusProxy.new_for_bus_sync(
        Gio.BusType.SESSION,
        Gio.DBusProxyFlags.NONE,
        None,
        "org.freedesktop.portal.Desktop",
        "/org/freedesktop/portal/desktop",
        "org.freedesktop.portal.desktop",
        None
    )

    args = GLib.Variant('(ss)', ('org.gnome.desktop.wm.preferences', 'button-layout'))

    try:
        button_layout = portal.call_sync('org.freedesktop.portal.Settings.ReadOne', args, Gio.DBusCallFlags.NONE, -1, None)
    except GLib.GError:
        print(_("Could not grab window control settings from desktop portal, falling back to default"))
        button_layout = None

    if button_layout:
        return button_layout[0]
    else:
        return None

def run(options, beta_support=False):
    if steam_dir_missing():
        return(False, _("Install: Failed to Find Valid '~/.steam/steam' Symlink"))

    if release_missing():
        (ret, msg) = update.check(False, beta_support)
        if not ret:
            return (ret, msg)

    if zip_not_extracted():
        (ret, msg) = update.post_download()
        if not ret:
            return (ret, msg)

    if options.get("custom_css"):
        custom_css.install()

    cmd = gen_cmd_line(options, beta_support)
    (ret, msg) = install(cmd)

    return (ret, msg)
