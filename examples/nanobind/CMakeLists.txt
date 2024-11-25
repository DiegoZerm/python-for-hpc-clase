cmake_minimum_required(VERSION 3.18)
project(${SKBUILD_PROJECT_NAME})

if (NOT SKBUILD)
  message(WARNING "\
  This CMake file is meant to be executed using 'scikit-build-core'.
  Install this package with: pip install .")
endif()

find_package(OpenMP)

# find python
set(DEV_MODULE Development.Module)
find_package(Python 3.8 COMPONENTS Interpreter ${DEV_MODULE} REQUIRED)

# find nanobind
execute_process(
  COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
  OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT)
find_package(nanobind CONFIG REQUIRED)

# configure extension module
nanobind_add_module(_pybex src/pybex.cpp)
target_link_libraries(_pybex PRIVATE OpenMP::OpenMP_CXX)

install(TARGETS _pybex LIBRARY DESTINATION ${SKBUILD_PROJECT_NAME})
