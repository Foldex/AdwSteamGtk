# Localization

## Adding a New Language Example

Assume `xx` is your [Language Code](https://www.gnu.org/software/gettext/manual/html_node/Usual-Language-Codes.html):

e.g. `fr` for French, `de` for German.

- Run `./update_pot.sh` and copy `AdwSteamGtk.pot` to `xx.po`.
- Make your changes and add `xx` to `LINGUAS` on a new line. Keep this list sorted.
- Add yourself to the [Translators credits](/src/info.py.in)
