from setuptools import setup, find_packages
from glob import iglob
import argparse
import os
import shutil
import sys
import tempfile

SUPPORTED_PLATFORMS = ['linux', 'linux2']
COMMAND_ARG_INDEX = 1

COMMAND_BDIST = 'bdist_wheel'

ERROR_CODE_UNSUPPORTED_PLATFORM = -1
ERROR_CODE_UNSUPPORTED_COMMAND = -2

COMPOSE_DIRECTORY = 'dist_composed'
SOURCE_FILE_PATTERNS = ['**/*.py', '**/*.pyi']
BINARY_FILE_PATTERNS = ['*.so']
STUB_FILE_PATTERNS = ['*.pyi']


def print_error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def find_all(where, what, absolute=False):
    filenames = list()
    for pattern in what:
        pattern = os.path.join(where, pattern)
        for filename in iglob(pattern, recursive=True):
            if absolute:
                absolute_filename = os.path.abspath(filename)
                filenames.append(absolute_filename)
            else:
                relative_filename = os.path.relpath(filename, where)
                filenames.append(relative_filename)

    return filenames


def copy_all(source_directory, filenames, destination_directory):
    for source_filename in filenames:
        if os.path.isabs(source_filename):
            shutil.copy(source_filename, destination_directory)
        else:
            relative_directory, pure_filename = os.path.split(source_filename)
            target_directory = os.path.join(destination_directory, relative_directory)
            if not os.path.exists(target_directory):
                os.makedirs(target_directory)

            source_filename = os.path.join(source_directory, source_filename)
            shutil.copy(source_filename, target_directory)


def compose_package(compose_dir, source_dir, binary_dir):
    source_files = find_all(source_dir, SOURCE_FILE_PATTERNS)
    binary_files = find_all(binary_dir, BINARY_FILE_PATTERNS)

    copy_all(source_dir, source_files, compose_dir)
    copy_all(binary_dir, binary_files, compose_dir)


if __name__ == '__main__':
    if sys.platform not in SUPPORTED_PLATFORMS:
        print_error('Unsupported platform {sys.name}!')
        exit(ERROR_CODE_UNSUPPORTED_PLATFORM)

    command = sys.argv[COMMAND_ARG_INDEX]
    if command == COMMAND_BDIST:
        """
        Arguments required when building binary distribution:
        * version
        * source directory (to source python files)
        * binary directory (to source _so files).
        """
        parser = argparse.ArgumentParser(description='bdist')
        parser.add_argument('--version',
                            required=True,
                            help='Version of the produced package.')
        parser.add_argument('--source-dir',
                            required=True,
                            help='Source directory to load python and cpp files from.')
        parser.add_argument('--binary-dir',
                            required=True,
                            help='Binary directory to load compiled files from.')

        args, unknown_args = parser.parse_known_args()
        with tempfile.TemporaryDirectory(dir='.') as compose_dir:
            compose_package(compose_dir, args.source_dir, args.binary_dir)

            packages = find_packages(where=compose_dir)
            packages_data = {'': find_all(compose_dir, BINARY_FILE_PATTERNS, absolute=True)};

            for package in packages:
                package_dir = package.replace('.', os.path.sep)
                package_dir = os.path.join(compose_dir, package_dir)
                files = find_all(where=package_dir, what=STUB_FILE_PATTERNS, absolute=True)

                if package not in packages_data:
                    packages_data[package] = files
                else:
                    packages_data[package] += files

            sys.argv = sys.argv[:1] + unknown_args
            setup(
                name='pysyscall_intercept',
                version=args.version,
                author='Lukasz Laszko',
                author_email='',
                url='https://github.com/lukaszlaszko/pysyscall_intercept',
                description='Python binding for syscall_intercept',
                long_description='Python interceptor for Linux syscall',
                packages=packages,
                package_dir={'': compose_dir},
                include_package_data=True,
                package_data=packages_data,
                #ext_modules=ext_modules,
                install_requires=[],
                #cmdclass={'build_ext': BuildExt},
                zip_safe=False,
                platforms=['Linux'],
                python_requires='>=3.6.0'
            )
    else:
        print_error('Usupported command - {0}'.format(sys.argv[COMMAND_ARG_INDEX]))
        exit(ERROR_CODE_UNSUPPORTED_COMMAND)
