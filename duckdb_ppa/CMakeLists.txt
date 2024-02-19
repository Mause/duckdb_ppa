cmake_minimum_required(VERSION 3.20)
include(ExternalProject)
ExternalProject_Add(duckdb SOURCE_DIR ${CMAKE_SOURCE_DIR}/duckdb INSTALL_COMMAND echo "Skipping install step.")
