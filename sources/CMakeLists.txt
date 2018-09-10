include_directories(${PYTHON_INCLUDE_DIRS})
include_directories(${PYBIND11_INCLUDE_DIRS})
include_directories(${SYSCALL_INTERCEPT_INCLUDE_DIRS})

set(CMAKE_SHARED_MODULE_PREFIX)

set(modules_SRC "")
file(GLOB_RECURSE modules_SRC "*.cpp")

foreach(module_file ${modules_SRC})
    get_filename_component (name_without_extension ${module_file} NAME_WE)
    add_library(${name_without_extension} MODULE
            ${modules_SRC})

    target_link_libraries(${name_without_extension}
            ${PYTHON_LIBRARIES}
            ${SYSCALL_INTERCEPT_LIBRARIES}
            ${CMAKE_THREAD_LIBS_INIT}
            ${RT_LIBRARY})

    add_dependencies(${name_without_extension}
            syscall_intercept)

    list(APPEND modules ${name_without_extension})
endforeach()

# build wheel package
add_custom_target(pack-wheel
        COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/setup.py bdist_wheel --version ${RELEASE_VERSION} --source-dir=${CMAKE_SOURCE_DIR}/src/package --binary-dir ${CMAKE_BINARY_DIR}/src/package)

add_dependencies(pack-wheel
        ${modules})

add_custom_target(upload-wheel
        COMMAND ${PYTHON_EXECUTABLE} -m twine --repository-url $ENV{PYPI_URL} -u $ENV{PYPI_USERNAME} -p $ENV{PYPI_PASSWORD} ${CMAKE_CURRENT_BINARY_DIR}/dist/*)