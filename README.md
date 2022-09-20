# AdwSteamGtk

A simple GTK wrapper that installs and updates the [Adwaita for Steam](https://github.com/tkashkin/Adwaita-for-Steam) skin.

<p align="center"><img src="img/screen.png?raw=true" /></p>

## Installation

Available on Flathub

<a href="https://flathub.org/apps/details/io.github.Foldex.AdwSteamGtk">
    <img width="200" alt="Download on Flathub" src="https://flathub.org/assets/badges/flathub-badge-i-en.svg"/>
</a>

## Skin Install

1. Install via app
2. Restart Steam if running
3. Go to Settings -> Interface
4. Select `Adwaita` from the dropdown
5. Restart Steam

## Skin Updates

On Startup new releases will automatically be downloaded and display a notification:

<p align="center"><img src="img/update.png?raw=true" /></p>

Simply reinstall the skin afterwards to update.

## Building

It is recommended to use [Gnome Builder](https://wiki.gnome.org/Apps/Builder) or `flatpak-builder` to build the project.

```
flatpak install org.gnome.Platform//42 org.gnome.Sdk//42
flatpak-builder --install --force-clean --user build-dir io.github.Foldex.AdwSteamGtk.json
```

See the below requirements otherwise.

### Requirements

- Blueprint Compiler
- GNU Patch
- GTK4
- Libadwaita
- Meson
- Ninja
- PyGObject
- Python 3
- Python python-packaging

