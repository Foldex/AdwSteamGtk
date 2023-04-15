pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'adwaita_steam_gtk')
gnome = import('gnome')

blueprints = custom_target('blueprints',
  input: files(
    'window.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gnome.compile_resources('adwaita-steam-gtk',
  'adwaita_steam_gtk.gresource.xml',
  dependencies: blueprints,
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())

conf.set('APP_ID', 'io.github.Foldex.AdwSteamGtk')
conf.set('APP_NAME', 'AdwSteamGtk')
conf.set('VERSION', meson.project_version())

conf.set('BUG_TRACKER_URL', 'https://github.com/Foldex/AdwSteamGtk/issues')
conf.set('PROJECT_URL', 'https://github.com/Foldex/AdwSteamGtk')

conf.set('COPYRIGHT', '© 2022 Foldex')
conf.set('LICENSE', 'GTK_LICENSE_GPL_3_0')

conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'adwaita-steam-gtk.in',
  output: 'adwaita-steam-gtk',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

configure_file(
  input: 'info.py.in',
  output: '@BASENAME@',
  configuration: conf,
  install: true,
  install_dir: moduledir
)

adwaita_steam_gtk_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'cli.py',
  'dl.py',
  'install.py',
  'paths.py',
  'style.py',
  'update.py',
  'zip.py',
]

install_data(adwaita_steam_gtk_sources, install_dir: moduledir)
