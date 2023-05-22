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

from gettext import gettext as _

import json
import urllib.request

API_URL="https://api.github.com/repos/tkashkin/Adwaita-for-Steam/releases/latest"

def get_release_info():
    try:
        data = urllib.request.urlopen(API_URL).read()
        out = json.loads(data)
    except urllib.error.HTTPError as e:
        return (False, _("API: HTTP Error Code ") + str(e.code))
    except ValueError:
        return (False, _("API: Error Parsing JSON"))
    except:
        return (False, _("API: Error retrieving release info"))

    if all(key in out for key in ("name", "zipball_url")):
        return (out, None)

    return (False, _("API: JSON is missing required keys"))

def download_release(url, path):
    try:
        urllib.request.urlretrieve(url, path)
    except urllib.error.HTTPError as e:
        return (False, _("Release: HTTP Error Code ") + str(e.code))
    except ConnectionResetError:
        return (False, _("Release: Connection Reset"))
    except PermissionError:
        return (False, _("Release: Permission Error"))
    except TimeoutError:
        return (False, _("Release: Connection Timeout"))
    except:
        return (False, _("Release: Error Retrieving Zip"))

    return (True, None)

