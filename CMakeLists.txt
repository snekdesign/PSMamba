cmake_minimum_required(VERSION 3.21)
cmake_policy(SET CMP0092 NEW)

project(PSMamba LANGUAGES CSharp CXX)

add_library(PSMamba SHARED psmamba.cc)
set_target_properties(PSMamba PROPERTIES
                      COMMON_LANGUAGE_RUNTIME ""
                      CXX_STANDARD 17
                      VS_DOTNET_REFERENCES System)
target_compile_options(PSMamba PRIVATE "/W4")
target_link_libraries(PSMamba libmamba)
install(TARGETS PSMamba)
