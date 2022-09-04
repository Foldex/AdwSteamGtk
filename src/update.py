# update.py
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
import time
from packaging import version
from enum import Enum

from . import dl
from . import paths

UPDATE_INTERVAL=3600 # 1 hour

class ExitCode(Enum):
    SUCCESS = 0
    FAIL = 1
    CURRENT = 2

def read_check_file(path):
    if not os.path.exists(path):
        return 0

    with open(path, "r") as f:
        line = f.readline()

    if line == "":
        line = 0

    return line

def write_file(string, path):
    with open(path, 'w') as f:
        f.write(string)

def need_update():
    new_stamp = int(time.time())
    old_stamp = int(read_check_file(paths.LAST_CHECK_FILE))

    if old_stamp == 0:
        write_file(str(new_stamp), paths.LAST_CHECK_FILE)
        return True

    if new_stamp - old_stamp > UPDATE_INTERVAL:
        write_file(str(new_stamp), paths.LAST_CHECK_FILE)
        return True
    else:
        return False

def release_is_newer(server_version, cached_version):
    return version.parse(server_version) > version.parse(cached_version)

def check():
    if not os.path.exists(paths.CACHE_DIR):
        os.makedirs(paths.CACHE_DIR)

    if not need_update() and not os.path.exists(paths.LAST_RELEASE_FILE):
        return (ExitCode.CURRENT, None)

    (dict, api_msg) = dl.get_release_info()

    if dict:
        last_ver=read_check_file(paths.LAST_VERSION_FILE)

        if os.path.exists(paths.LAST_RELEASE_FILE) and not release_is_newer(dict["name"], str(last_ver)):
            return (ExitCode.CURRENT, None)
        (ret, dl_msg) = dl.download_release(dict["zipball_url"], paths.LAST_RELEASE_FILE)

        if ret:
            write_file(dict["name"], paths.LAST_VERSION_FILE)
            return (ExitCode.SUCCESS, dict["name"])
        else:
            return (ExitCode.FAIL, dl_msg)
    else:
        return (ExitCode.FAIL, api_msg)

