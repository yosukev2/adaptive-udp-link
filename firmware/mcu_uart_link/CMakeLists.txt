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

project(mcu_uart_link C CXX ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

option(MCU_UART_LINK_ENABLE_PICOTOOL "Enable picotool-backed extra outputs such as UF2" ON)
if(NOT MCU_UART_LINK_ENABLE_PICOTOOL)
    set(PICO_NO_PICOTOOL 1)
endif()

pico_sdk_init()

add_executable(mcu_uart_link
    main.c
    mcu_uart_protocol.c
)

target_link_libraries(mcu_uart_link
    pico_stdlib
    hardware_uart
)

# Packet link uses uart0 on GPIO0/GPIO1.
# Telemetry CSV is emitted over USB CDC so it never collides with the packet link.
pico_enable_stdio_usb(mcu_uart_link 1)
pico_enable_stdio_uart(mcu_uart_link 0)

pico_add_extra_outputs(mcu_uart_link)
