add_test(NAME run-tests
        COMMAND ${PYTHON_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR} --junitxml=run-tests.xml)

set_property(TEST run-tests
        PROPERTY
        ENVIRONMENT "PYTHONPATH=$ENV{PYTHONPATH}:${CMAKE_CURRENT_SOURCE_DIR}:${CMAKE_SOURCE_DIR}/sources:${CMAKE_BINARY_DIR}/sources")
set_property(TEST run-tests
        APPEND PROPERTY
        ENVIRONMENT "BINARY_DIR=${CMAKE_BINARY_DIR}")
