# pybind11
set(PYBIND11_INCLUDE_DIRS ${CMAKE_CURRENT_SOURCE_DIR}/pybind11/include PARENT_SCOPE)

# syscall_intercept
ExternalProject_Add(syscall_intercept
        SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/syscall_intercept
        CMAKE_ARGS
        -DCMAKE_BUILD_TYPE=Release
        -DCMAKE_C_COMPILER=${CMAKE_C_COMPILER}
        -DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}
        -DCMAKE_MAKE_PROGRAM=${CMAKE_MAKE_PROGRAM}
        -DCMAKE_GENERATOR=${CMAKE_GENERATOR}
        -DCMAKE_CXX_FLAGS=${CMAKE_CXX_FLAGS}
        -DCMAKE_EXE_LINKER_FLAGS=${CMAKE_EXE_LINKER_FLAGS}
        BUILD_COMMAND ${CMAKE_COMMAND} --build .
        INSTALL_COMMAND ""
        BUILD_BYPRODUCTS
        "${CMAKE_CURRENT_BINARY_DIR}/syscall_intercept-prefix/src/syscall_intercept-build/libsyscall_intercept.a")

ExternalProject_Get_Property(syscall_intercept SOURCE_DIR)
set(SYSCALL_INTERCEPT_INCLUDE_DIRS ${SOURCE_DIR}/include PARENT_SCOPE)

ExternalProject_Get_Property(syscall_intercept BINARY_DIR)
set(SYSCALL_INTERCEPT_LIBRARIES "${BINARY_DIR}/libsyscall_intercept.a" PARENT_SCOPE)