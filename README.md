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

## Skin Updates

On Startup new releases will automatically be downloaded and display a notification:

<p align="center"><img src="img/update.png?raw=true" /></p>

Simply reinstall the skin afterwards to update.

## Command Line Usage

`flatpak run io.github.Foldex.AdwSteamGtk`

| Arg             | Short  | Description                                              |
| --------------  | ------ | -------------------------------------------------------- |
| --check         | -c     | Checks for updates and displays a notification           |
| --install       | -i     | Checks for updates and installs them, always installs    |
| --options       | -o     | Overrides Install Options, see below                     |
| --update        | -u     | Checks for updates and installs them                     |

### Install Options

By default installs with `-i/-u` will use your last selected settings within the app.

You may override this by using `-o` option.

Please note that these options are one time overrides, they will not save themselves.

Options should be passed as a single string like so:

`flatpak run io.github.Foldex.AdwSteamGtk -i -o 'option_name:option_value;option_name:option_value'`

| Key                | Description                                                 | Accepted Values                                          |
| ------------------ | ----------------------------------------------------------- | -------------------------------------------------------- |
| bottom_bar         | Show the Bottom Bar                                         | true, false, yes, no, on, off, t, f, y, n                |
| color_theme        | Colortheme for skin                                         | Any valid theme name                                     |
| install_fonts      | Install Cantarell Fonts                                     | true, false, yes, no, on, off, t, f, y, n                |
| library_sidebar    | Display Options for Library Sidebar                         | show, hover_only                                         |
| library_whats_new  | Show the Library What's New Section                         | true, false, yes, no, on, off, t, f, y, n                |
| login_qr           | Display Options for the QR Code Login                       | show, hover_only, hide                                   |
| rounded_corners    | Show Rounded Corners on Elements                            | true, false, yes, no, on, off, t, f, y, n                |
| top_bar_bp_button  | Show the Big Picture Button on the Top Bar                  | true, false, yes, no, on, off, t, f, y, n                |
| top_bar_nav_arrows | Show the Back/Forward Nav Buttons on the Top Bar            | true, false, yes, no, on, off, t, f, y, n                |
| top_bar_nav_url    | Show the Browser URL on Top Bar                             | true, false, yes, no, on, off, t, f, y, n                |
| top_bar_original   | Use Steam's Original Top Bar (instead of the Adwaita style) | true, false, yes, no, on, off, t, f, y, n                |
| web_theme          | Type of Web Theme to Install                                | full, base                                               |
| win_controls       | Window Controls Presets (Maximize, Minimize, etc)           | default, right-all, left, left-all, none                 |
| win_controls_style | Window Controls Visual Style (Mac OS Dots)                  | default, dots                                            |

## Troubleshooting

See [Troubleshooting](https://github.com/Foldex/AdwSteamGtk/wiki/Troubleshooting)

## Contribute Translations

See [here](/po)

## Building

It is recommended to use [Gnome Builder](https://wiki.gnome.org/Apps/Builder) or `flatpak-builder` to build the project.

```
flatpak install org.gnome.Platform//44 org.gnome.Sdk//44
flatpak-builder --install --force-clean --user build-dir io.github.Foldex.AdwSteamGtk.json
```

See the below requirements otherwise.

### Requirements

- Blueprint Compiler >= `0.8.0`
- GNU Patch (Runtime Dependency)
- GTK4
- Libadwaita
- Libportal
- Meson
- Ninja
- PyGObject
- Python >= `3.10`
- Python python-packaging

