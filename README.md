# AdwSteamGtk

A simple GTK wrapper that installs and updates the [Adwaita for Steam](https://github.com/tkashkin/Adwaita-for-Steam) skin.

<p align="center"><img src="img/screen.png?raw=true" /></p>

## Installation

Available on Flathub

<a href="https://flathub.org/apps/details/io.github.Foldex.AdwSteamGtk">
    <img width="200" alt="Download on Flathub" src="https://flathub.org/assets/badges/flathub-badge-i-en.svg"/>
</a>

<br/>

Arch AUR Build (Unofficial)

<a href="https://aur.archlinux.org/packages/adwsteamgtk">
    <img width="200" alt="Unofficial AUR build" src="https://img.shields.io/aur/version/adwsteamgtk?style=for-the-badge">
</a>

## Skin Install

1. Install via app
2. Restart Steam if running
3. Go to `Settings -> Interface`
4. Select `Adwaita` from the dropdown
5. Restart Steam

## Skin Updates

On Startup new releases will automatically be downloaded and display a notification:

<p align="center"><img src="img/update.png?raw=true" /></p>

Simply reinstall the skin afterwards to update.

You may also launch with the `-c` flag to force an update check and show a notification instead of showing the window.

`flatpak run io.github.Foldex.AdwSteamGtk -c`

## Troubleshooting

See [Troubleshooting](https://github.com/Foldex/AdwSteamGtk/wiki/Troubleshooting)

## Building

It is recommended to use [Gnome Builder](https://wiki.gnome.org/Apps/Builder) or `flatpak-builder` to build the project.

```
flatpak install org.gnome.Platform//43 org.gnome.Sdk//43
flatpak-builder --install --force-clean --user build-dir io.github.Foldex.AdwSteamGtk.json
```

See the below requirements otherwise.

### Requirements

- Blueprint Compiler
- GNU Patch (Runtime Dependency)
- GTK4
- Libadwaita
- Meson
- Ninja
- PyGObject
- Python 3
- Python python-packaging

