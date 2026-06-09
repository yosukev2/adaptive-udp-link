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

project(w07_rtos_jitter C CXX ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

option(W07_ENABLE_PICOTOOL "Enable picotool-backed extra outputs such as UF2" ON)
if(NOT W07_ENABLE_PICOTOOL)
    set(PICO_NO_PICOTOOL 1)
endif()

pico_sdk_init()

if(NOT DEFINED FREERTOS_KERNEL_PATH)
    if(DEFINED ENV{FREERTOS_KERNEL_PATH})
        set(FREERTOS_KERNEL_PATH "$ENV{FREERTOS_KERNEL_PATH}")
    else()
        message(FATAL_ERROR "FREERTOS_KERNEL_PATH is not set. Export it or pass -DFREERTOS_KERNEL_PATH=/path/to/FreeRTOS-Kernel.")
    endif()
endif()

set(FREERTOS_PORT_DIR "${FREERTOS_KERNEL_PATH}/portable/ThirdParty/GCC/RP2040")
if(NOT EXISTS "${FREERTOS_PORT_DIR}/CMakeLists.txt")
    message(FATAL_ERROR "FreeRTOS RP2040 port not found at ${FREERTOS_PORT_DIR}.")
endif()

set(FREERTOS_CONFIG_FILE_DIRECTORY "${CMAKE_CURRENT_LIST_DIR}")
add_subdirectory("${FREERTOS_PORT_DIR}" FREERTOS_KERNEL)

add_executable(w07_baremetal_jitter
    baremetal_main.c
)

target_link_libraries(w07_baremetal_jitter
    pico_stdlib
    pico_time
)

pico_enable_stdio_usb(w07_baremetal_jitter 1)
pico_enable_stdio_uart(w07_baremetal_jitter 0)

pico_add_extra_outputs(w07_baremetal_jitter)

add_executable(w07_freertos_jitter
    freertos_main.c
)

target_include_directories(w07_freertos_jitter PRIVATE
    ${CMAKE_CURRENT_LIST_DIR}
)

target_link_libraries(w07_freertos_jitter
    FreeRTOS-Kernel-Heap4
    pico_stdlib
    pico_time
)

pico_enable_stdio_usb(w07_freertos_jitter 1)
pico_enable_stdio_uart(w07_freertos_jitter 0)

pico_add_extra_outputs(w07_freertos_jitter)
