cmake_minimum_required(VERSION 3.13)

set(PICO_BOARD pico CACHE STRING "Pico SDK board target")

if(NOT DEFINED PICO_SDK_PATH)
    if(DEFINED ENV{PICO_SDK_PATH})
        set(PICO_SDK_PATH "$ENV{PICO_SDK_PATH}")
    else()
        message(FATAL_ERROR "PICO_SDK_PATH is not set. Export it or pass -DPICO_SDK_PATH=/path/to/pico-sdk.")
    endif()
endif()

include(${PICO_SDK_PATH}/external/pico_sdk_import.cmake)

project(w06_pico_jitter C CXX ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

option(W06_ENABLE_PICOTOOL "Enable picotool-backed extra outputs such as UF2" ON)
if(NOT W06_ENABLE_PICOTOOL)
    set(PICO_NO_PICOTOOL 1)
endif()

pico_sdk_init()

add_executable(w06_pico_jitter
    main.c
)

target_link_libraries(w06_pico_jitter
    pico_stdlib
    pico_time
)

pico_enable_stdio_usb(w06_pico_jitter 1)
pico_enable_stdio_uart(w06_pico_jitter 0)

pico_add_extra_outputs(w06_pico_jitter)
