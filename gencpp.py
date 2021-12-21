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
        # self._gen_test_directory()
        # self._gen_build_directory()

        self._init_git_repository()

    def _gen_root_directory(self) -> None:
        # .clang-format
        clang_format = """---
BasedOnStyle: LLVM
IndentWidth: 4
---
Language: Cpp
AccessModifierOffset: -4
ColumnLimit: 0
PointerAlignment: Left
"""
        self._write_file("", ".clang-format", clang_format)

        # .gitignore
        git_ignore = """# VS Code
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
        self._write_file("", ".gitignore", git_ignore)

        # CMakeLists.txt
        cmake_lists = f"""cmake_minimum_required(VERSION 3.1.2)

project({self.name})

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

########### Conan Package Manager ###########################################################
#############################################################################################

list(APPEND CMAKE_MODULE_PATH ${{CMAKE_BINARY_DIR}})
list(APPEND CMAKE_PREFIX_PATH ${{CMAKE_BINARY_DIR}})

# Add `find_package` here

#############################################################################################
########### Conan Package Manager End #######################################################

add_subdirectory(src)
"""
        self._write_file("", "CMakeLists.txt", cmake_lists)

        # conanfile.txt
        conan_file = """[requires]

[generators]
cmake_find_package
"""
        self._write_file("", "conanfile.txt", conan_file)

        # README.md
#         readme = f"""# {self.name}
# """
#         self._write_file("", "README.md", readme)

    def _gen_src_directory(self) -> None:
        # main.cpp
        main = """#include <iostream>

int main() {
    std::cout << "Hello World!\\n";
}
"""
        self._write_file("src/", "main.cpp", main)

        # CMakeLists.txt
        cmake_lists = """add_executable(${CMAKE_PROJECT_NAME} main.cpp)
"""
        self._write_file("src/", "CMakeLists.txt", cmake_lists)

    def _gen_test_directory(self) -> None:
        # CMakeLists.txt
        self._write_file("test/", "CMakeLists.txt", "")

    def _gen_build_directory(self) -> None:
        self._create_directory("./build/")

        install_folder = os.path.join(self.path, "build")
        cmd = f"conan install -if {install_folder} {self.path}"
        print(os.popen(cmd).read(), end='')

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


if __name__ == "__main__":
    main()
