project('f2py_example', 'c',
  meson_version: '>=0.64.0',
  default_options : ['warning_level=2', 'optimization=3', 'c_args=-march=native'],
)

add_languages('fortran')

py_mod = import('python')
py = py_mod.find_installation(pure: false)
py_dep = py.dependency()

incdir_numpy = run_command(py,
  ['-c', 'import numpy; print(numpy.get_include())'],
  check : true
).stdout().strip()

incdir_f2py = run_command(py,
    ['-c', 'import numpy.f2py; print(numpy.f2py.get_include())'],
    check : true
).stdout().strip()

fibby_source = custom_target('fibmodule.c',
  input : ['fib.f90'],
  output : ['fibmodule.c', 'fib-f2pywrappers.f'],
  command : [py, '-m', 'numpy.f2py', '@INPUT@', '-m', 'fib', '--lower']
)

inc_np = include_directories(incdir_numpy, incdir_f2py)

py.extension_module('fib',
  ['fib.f90', fibby_source],
  incdir_f2py / 'fortranobject.c',
  include_directories: inc_np,
  dependencies : py_dep,
  install : true,
  subdir: 'f2py_example'
)
