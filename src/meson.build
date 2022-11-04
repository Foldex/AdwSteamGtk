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
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'adwaita-steam-gtk.in',
  output: 'adwaita-steam-gtk',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

adwaita_steam_gtk_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'dl.py',
  'install.py',
  'paths.py',
  'update.py',
]

install_data(adwaita_steam_gtk_sources, install_dir: moduledir)
