#!/usr/bin/python3

import os
import sys


class CppProject:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.path: str = os.path.join(os.getcwd(), self.name)

        if os.path.exists(self.path):
            print("The project already exists")
            sys.exit(1)

    def generate(self) -> None:
        self._gen_root_directory()
        self._gen_src_directory()

        self._init_git_repository()

    def _gen_root_directory(self) -> None:
        # .clang-format
        self._write_file("", ".clang-format", CLANG_FORMAT_TEMPLATE)

        # .gitignore
        self._write_file("", ".gitignore", GIT_IGNORE_TEMPLATE)

        # CMakeLists.txt
        cmake_lists = ROOT_CMAKE_LISTS_TEMPLATE.format(self.name)
        self._write_file("", "CMakeLists.txt", cmake_lists)

    def _gen_src_directory(self) -> None:
        # main.cpp
        self._write_file("src/", "main.cpp", MAIN_CPP_TEMPLATE)

        # CMakeLists.txt
        self._write_file("src/", "CMakeLists.txt", CMAKE_LISTS_TEMPLATE)

    def _init_git_repository(self) -> None:
        cmd = f"git init {self.path}"
        print(os.popen(cmd).read(), end='')

    def _create_directory(self, relative_path: str) -> None:
        dir = os.path.join(self.path, relative_path)
        if not os.path.exists(dir):
            os.mkdir(dir)

    def _write_file(self, relative_path: str, file_name: str, file_content: str) -> None:
        self._create_directory(relative_path)

        file_path = os.path.join(self.path, relative_path, file_name)
        with open(file_path, "w") as file:
            file.write(file_content)


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <name>")
        sys.exit(1)

    cpp_project = CppProject(sys.argv[1])
    cpp_project.generate()

    sys.exit(0)


CLANG_FORMAT_TEMPLATE = """---
BasedOnStyle: LLVM
IndentWidth: 4
---
Language: Cpp
AccessModifierOffset: -4
ColumnLimit: 0
PointerAlignment: Left
"""

GIT_IGNORE_TEMPLATE = """# VS Code
/.vscode
/build

# MSVC
/.vs
/out
/CMakeSettings.json

# CLion
/.idea
/cmake-build-debug
/cmake-build-debug-coverage
/cmake-build-release

# Mac OS
.DS_Store
"""

ROOT_CMAKE_LISTS_TEMPLATE = """cmake_minimum_required(VERSION 3.5)

project({})

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

########### Conan Package Manager ###########################################################
#############################################################################################

list(APPEND CMAKE_MODULE_PATH ${{CMAKE_BINARY_DIR}})
list(APPEND CMAKE_PREFIX_PATH ${{CMAKE_BINARY_DIR}})

if(NOT EXISTS "${{CMAKE_BINARY_DIR}}/conan.cmake")
    message(STATUS "Downloading conan.cmake from https://github.com/conan-io/cmake-conan")
    file(DOWNLOAD "https://raw.githubusercontent.com/conan-io/cmake-conan/release/0.17/conan.cmake"
         "${{CMAKE_BINARY_DIR}}/conan.cmake"
         EXPECTED_HASH SHA256=3bef79da16c2e031dc429e1dac87a08b9226418b300ce004cc125a82687baeef
         TLS_VERIFY ON)
endif()

include(${{CMAKE_BINARY_DIR}}/conan.cmake)

# Add requires here
conan_cmake_configure(
    REQUIRES

    GENERATORS
        cmake_find_package
    IMPORTS
        "bin, *.dll -> ./src"
        "lib, *.dylib* -> ./src")

conan_cmake_autodetect(settings)
conan_cmake_install(
    PATH_OR_REFERENCE .
    BUILD missing
    REMOTE conancenter
    SETTINGS ${{settings}})

# Add `find_package` here

#############################################################################################
########### Conan Package Manager End #######################################################

add_subdirectory(src)
"""

MAIN_CPP_TEMPLATE = """#include <iostream>

int main() {
    std::cout << "Hello World!\\n";
}
"""

CMAKE_LISTS_TEMPLATE = """add_executable(${CMAKE_PROJECT_NAME} main.cpp)
"""

if __name__ == "__main__":
    main()
