# Localization

## Adding a New Language Example

Assume `xx` is your [Language Code](https://www.gnu.org/software/gettext/manual/html_node/Usual-Language-Codes.html):

e.g. `fr` for French, `de` for German.

- [Fork](https://docs.github.com/en/get-started/quickstart/contributing-to-projects#forking-a-repository) and [Clone](https://docs.github.com/en/get-started/quickstart/contributing-to-projects#cloning-a-fork) this repo
- Ensure you have [gettext](#gettext) installed
- Run `./update_pot.sh` and copy `AdwSteamGtk.pot` to `xx.po`
- [Edit](#editing-po-files) `xx.po`
- Add `xx` to [LINGUAS](/po/LINGUAS) on a new line. Keep this list sorted alphabetically
- [Test](#testing) your changes (Optional, but appreciated)
- Add yourself to the [Translators credits](/src/info.py.in) section
- [Commit](https://docs.github.com/en/get-started/quickstart/contributing-to-projects#making-and-pushing-changes) your changes
- [Open a Pull Request](https://docs.github.com/en/get-started/quickstart/contributing-to-projects#making-a-pull-request)

## Gettext

`update_pot.sh` requires the xgettext utility from the gettext package.

| Distro | Package Name                                                        | Install Command              |
|--------|---------------------------------------------------------------------|------------------------------|
| Arch   | [gettext](https://archlinux.org/packages/core/x86_64/gettext/)      | sudo pacman -S gettext       |
| Debian | [gettext](https://packages.debian.org/stable/gettext)               | sudo apt-get install gettext |
| Fedora | [gettext](https://packages.fedoraproject.org/pkgs/gettext/gettext/) | sudo dnf install gettext     |
| Ubuntu | [gettext](https://packages.ubuntu.com/lunar/gettext)                | sudo apt-get install gettext |

## Editing PO Files

You'll likely want to use a PO File Editor:

- [Gtranslator](https://flathub.org/apps/org.gnome.Gtranslator)
- [Lokalize](https://flathub.org/apps/org.kde.lokalize)
- [Poedit](https://flathub.org/apps/net.poedit.Poedit)

## Testing

Follow the flatpak-builder [Instructions](https://github.com/Foldex/AdwSteamGtk#building) for building the project.

Run those commands from the top level directory of the project.

You should now be able to run the app via:

`flatpak run io.github.Foldex.AdwSteamGtk`

To test out your localization changes you will need to force the locale.

### Generating Locale

If you already have the locale for the language you are translating installed, you may skip this step.

In order to run the program with a new locale, you must first generate it on your system.

See: [Generating Locale](https://wiki.archlinux.org/title/Locale#Generating_locales)

### Flatpak Locale

For freshly generated locales, flatpak will also need to fetch the new locale information.

Switch to the new locale and run:

`flatpak update`

### Running with Locale

For example, to run the Ukrainian locale:

`LANG=uk_UA.UTF-8 flatpak run io.github.Foldex.AdwSteamGtk`

#### Locale not Supported Error

If you get this error:

`Locale not supported by C library. Using the fallback 'C' locale.`

Ensure that:
- The locale has been [Generated](#generating-locale) on your system
- You have typed the locale name correctly when passing `LANG=`
- Flatpak has downloaded the [Runtime Locale](#flatpak-locale)
- The Language Code is present in the [LINGUAS](/po/LINGUAS) file
