from __future__ import annotations

# this script creates a single header + source file combination out of the DuckDB sources
import os
import re
import sys
from contextlib import contextmanager
from os.path import normpath
from pathlib import Path
from typing import TYPE_CHECKING

import yaml

# from python_helpers import open_utf8, normalize_path

if TYPE_CHECKING:
    from io import TextIOWrapper

os.chdir("duckdb_ppa")


def normalize_path(paths: list[str]) -> list[str]:
    return [normpath(path) for path in paths]


@contextmanager
def open_utf8(filename: str, mode: str) -> TextIOWrapper:
    with Path(filename).open(mode, encoding="utf8") as f:
        yield f


def generate_header() -> dict[str, str]:
    """Generate a license header.

    Format: required.
    Upstream-Name: optional.
    Upstream-Contact: optional.
    Source: optional.
    Disclaimer: optional.
    Comment: optional.
    License: optional.
    Copyright: optional.
    """
    contents = open("LICENSE").read()
    return {
        "Upstream-Name": "DuckDB",
        "Upstream-Contact": "quack@duckdblabs.com",
        "Source": "https://github.com/duckdb/duckdb",
        "License": contents,
        "Copyright": extract_copyright(contents),
    }


def extract_copyright(contents: str) -> str | None:
    lines = contents.splitlines()
    for line in lines:
        if "Copyright" in line and not (
            "Grant of Copyright" in line or "name of copyright owner" in line
        ):
            return line


def generate_library_paragraph(license: str) -> dict[str, str]:
    """Generate a paragraph for the library.

    Files: required.
    Copyright: required.
    License: required.
    Comment: optional.
    """
    files = str(license.parent)
    contents = license.open().read()
    return {
        "Files": files,
        "Copyright": extract_copyright(contents),
        "License": contents,
    }


def setup() -> None:
    global amal_dir
    global header_file
    global source_file
    global skip_duckdb_includes
    global include_paths
    global compile_directories
    global excluded_files
    global excluded_compilation_files
    global extended_amalgamation, always_excluded, main_header_files

    amal_dir = Path("src/amalgamation")
    header_file = amal_dir / "duckdb.hpp"
    source_file = amal_dir / "duckdb.cpp"

    skip_duckdb_includes = False

    src_dir = "src"
    include_dir = Path("src/include")

    common = include_dir / "duckdb" / "common"
    types = common / "types"

    # files included in the amalgamated "duckdb.hpp" file
    main_header_files = [
        (include_dir / "duckdb.hpp"),
        (include_dir / "duckdb.h"),
        common / "adbc" / "adbc.h",
        common / "adbc" / "adbc.hpp",
        common / "arrow" / "arrow.hpp",
        common / "arrow" / "arrow_converter.hpp",
        common / "arrow" / "arrow_wrapper.hpp",
        types / "date.hpp",
        types / "blob.hpp",
        types / "decimal.hpp",
        types / "hugeint.hpp",
        types / "uhugeint.hpp",
        types / "uuid.hpp",
        types / "interval.hpp",
        types / "timestamp.hpp",
        types / "time.hpp",
        os.path.join(
            include_dir,
            "duckdb",
            "common",
            "serializer",
            "buffered_file_writer.hpp",
        ),
        os.path.join(
            include_dir,
            "duckdb",
            "common",
            "serializer",
            "memory_stream.hpp",
        ),
        os.path.join(include_dir, "duckdb", "main", "appender.hpp"),
        os.path.join(include_dir, "duckdb", "main", "client_context.hpp"),
        os.path.join(include_dir, "duckdb", "function", "function.hpp"),
        os.path.join(include_dir, "duckdb", "function", "table_function.hpp"),
        os.path.join(
            include_dir,
            "duckdb",
            "parser",
            "parsed_data",
            "create_table_function_info.hpp",
        ),
        os.path.join(
            include_dir,
            "duckdb",
            "parser",
            "parsed_data",
            "create_copy_function_info.hpp",
        ),
    ]
    extended_amalgamation = True
    if extended_amalgamation:

        def add_include_dir(dirpath):
            return [os.path.join(dirpath, x) for x in os.listdir(dirpath)]

        extended_amalgamation = True
        main_header_files += [
            os.path.join(include_dir, x)
            for x in [
                "duckdb/planner/expression/bound_constant_expression.hpp",
                "duckdb/planner/expression/bound_function_expression.hpp",
                "duckdb/catalog/catalog_entry/scalar_function_catalog_entry.hpp",
                "duckdb/parser/parsed_data/create_table_info.hpp",
                "duckdb/planner/parsed_data/bound_create_table_info.hpp",
                "duckdb/parser/constraints/not_null_constraint.hpp",
                "duckdb/storage/data_table.hpp",
                "duckdb/function/pragma_function.hpp",
                "duckdb/parser/qualified_name.hpp",
                "duckdb/parser/parser.hpp",
                "duckdb/planner/binder.hpp",
                "duckdb/storage/object_cache.hpp",
                "duckdb/planner/table_filter.hpp",
                "duckdb/storage/statistics/base_statistics.hpp",
                "duckdb/planner/filter/conjunction_filter.hpp",
                "duckdb/planner/filter/constant_filter.hpp",
                "duckdb/common/types/vector_cache.hpp",
                "duckdb/common/string_map_set.hpp",
                "duckdb/planner/filter/null_filter.hpp",
                "duckdb/common/arrow/arrow_wrapper.hpp",
                "duckdb/common/hive_partitioning.hpp",
                "duckdb/common/union_by_name.hpp",
                "duckdb/planner/operator/logical_get.hpp",
                "duckdb/common/compressed_file_system.hpp",
            ]
        ]
        main_header_files += add_include_dir(
            os.path.join(include_dir, "duckdb/parser/expression"),
        )
        main_header_files += add_include_dir(
            os.path.join(include_dir, "duckdb/parser/parsed_data"),
        )
        main_header_files += add_include_dir(
            os.path.join(include_dir, "duckdb/parser/tableref"),
        )
        main_header_files = normalize_path(main_header_files)

    sys.path.insert(0, "scripts")

    import package_build

    # include paths for where to search for include files during amalgamation
    include_paths = [include_dir, *package_build.third_party_includes()]
    # paths of where to look for files to compile and include to the final amalgamation
    compile_directories = [src_dir, *package_build.third_party_sources()]

    # files always excluded
    always_excluded = normalize_path(
        [
            "src/amalgamation/duckdb.cpp",
            "src/amalgamation/duckdb.hpp",
            "src/amalgamation/parquet-amalgamation.cpp",
            "src/amalgamation/parquet-amalgamation.hpp",
        ],
    )
    # files excluded from the amalgamation
    excluded_files = ["grammar.cpp", "grammar.hpp", "symbols.cpp"]
    # files excluded from individual file compilation during test_compile
    excluded_compilation_files = [
        *excluded_files,
        "gram.hpp",
        "kwlist.hpp",
        "duckdb-c.cpp",
    ]


def get_includes(fpath: str, text: str) -> tuple[list[str], list[str]]:
    # find all the includes referred to in the directory
    regex_include_statements = re.findall(
        '(^[\t ]*[#][\t ]*include[\t ]+["]([^"]+)["])',
        text,
        flags=re.MULTILINE,
    )
    include_statements = []
    include_files = []
    # figure out where they are located
    for x in regex_include_statements:
        included_file = x[1]
        if skip_duckdb_includes and "duckdb" in included_file:
            continue
        if (
            "extension_helper.cpp" in fpath
            and (included_file.endswith("_extension.hpp"))
            or included_file == "generated_extension_loader.hpp"
            or included_file == "generated_extension_headers.hpp"
        ):
            continue
        if "allocator.cpp" in fpath and included_file.endswith(
            "jemalloc_extension.hpp",
        ):
            continue
        if x[0] in include_statements:
            msg = f"duplicate include {x[0]} in file {fpath}"
            raise Exception(msg)
        include_statements.append(x[0])
        included_file = os.sep.join(included_file.split("/"))
        found = False
        for include_path in include_paths:
            ipath = os.path.join(include_path, included_file)
            if os.path.isfile(ipath):
                include_files.append(ipath)
                found = True
                break
        if not found:
            raise Exception(
                'Could not find include file "'
                + included_file
                + '", included from file "'
                + fpath
                + '"',
            )
    return (include_statements, include_files)


# recursively get all includes and write them
written_files = set()

# licenses
licenses = []


def need_to_write_file(current_file, ignore_excluded=False) -> bool:
    global always_excluded
    if str(amal_dir) in str(current_file):
        return False
    if current_file in always_excluded:
        return False
    if current_file.split(os.sep)[-1] in excluded_files and not ignore_excluded:
        # file is in ignored files set
        return False
    if current_file in written_files:
        # file is already written
        return False
    return True


def find_license(original_file):
    global licenses
    file = original_file
    license = ""
    while True:
        (file, end) = os.path.split(file)
        if file == "":
            break
        potential_license = os.path.join(file, "LICENSE")
        if os.path.exists(potential_license):
            license = potential_license
    if license == "":
        raise "Could not find license for %s" % original_file

    if license not in licenses:
        licenses.append(license)

    return licenses.index(license)


def write_file(current_file, ignore_excluded=False) -> None:
    global written_files
    if not need_to_write_file(current_file, ignore_excluded):
        return
    written_files.add(current_file)

    # first read this file
    with open_utf8(current_file, "r") as f:
        text = f.read()

    if current_file.startswith("third_party") and not current_file.endswith("LICENSE"):
        find_license(current_file)

    (statements, includes) = get_includes(current_file, text)
    # find the linenr of the final #include statement we parsed
    if statements:
        # now write all the dependencies of this header first
        for i in range(len(includes)):
            write_file(includes[i])


def write_dir(dir) -> None:
    files = os.listdir(dir)
    files.sort()
    for fname in files:
        if fname in excluded_files:
            continue
        # print(fname)
        fpath = os.path.join(dir, fname)
        if os.path.isdir(fpath):
            write_dir(fpath)
        elif fname.endswith((".cpp", ".c", ".cc")):
            write_file(fpath)


def generate_duckdb_hpp(header_file: str) -> None:
    (write_file("LICENSE"))

    for fpath in main_header_files:
        (write_file(fpath))


def generate_amalgamation(source_file: str, header_file: str) -> None:
    # construct duckdb.hpp from these headers
    generate_duckdb_hpp(header_file)

    # now construct duckdb.cpp

    # scan all the .cpp files
    for compile_dir in compile_directories:
        write_dir(compile_dir)

    license_idx = 0
    for license in licenses:
        (write_file(license))
        license_idx += 1


def main() -> None:
    setup()

    generate_amalgamation(source_file, header_file)

    lics = map(Path, licenses)
    paragraphs = [generate_header()] + [
        generate_library_paragraph(license=directory) for directory in lics
    ]

    with open("debian/copyright", "w") as f:
        f.write(
            "\n".join(
                yaml.dump(paragraph, default_style="|") for paragraph in paragraphs
            )
        )


if __name__ == "__main__":
    main()
