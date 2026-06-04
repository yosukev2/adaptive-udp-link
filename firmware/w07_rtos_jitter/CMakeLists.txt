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

if(NOT EXISTS "${FREERTOS_KERNEL_PATH}/tasks.c")
    message(FATAL_ERROR "FreeRTOS-Kernel not found at ${FREERTOS_KERNEL_PATH}.")
endif()

set(FREERTOS_PORT_DIR "${FREERTOS_KERNEL_PATH}/portable/ThirdParty/GCC/RP2040")
if(EXISTS "${FREERTOS_PORT_DIR}/port.c")
    set(FREERTOS_PORT_SOURCE "${FREERTOS_PORT_DIR}/port.c")
    set(FREERTOS_PORT_INCLUDE "${FREERTOS_PORT_DIR}/include")
else()
    set(FREERTOS_PORT_DIR "${FREERTOS_KERNEL_PATH}/portable/GCC/ARM_CM0")
    set(FREERTOS_PORT_SOURCE "${FREERTOS_PORT_DIR}/port.c")
    set(FREERTOS_PORT_INCLUDE "${FREERTOS_PORT_DIR}")
endif()

if(NOT EXISTS "${FREERTOS_PORT_SOURCE}")
    message(FATAL_ERROR "FreeRTOS port source not found. Expected RP2040 or ARM_CM0 port under ${FREERTOS_KERNEL_PATH}/portable.")
endif()

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
    ${FREERTOS_KERNEL_PATH}/tasks.c
    ${FREERTOS_KERNEL_PATH}/queue.c
    ${FREERTOS_KERNEL_PATH}/list.c
    ${FREERTOS_KERNEL_PATH}/timers.c
    ${FREERTOS_KERNEL_PATH}/event_groups.c
    ${FREERTOS_KERNEL_PATH}/portable/MemMang/heap_4.c
    ${FREERTOS_PORT_SOURCE}
)

target_include_directories(w07_freertos_jitter PRIVATE
    ${CMAKE_CURRENT_LIST_DIR}
    ${FREERTOS_KERNEL_PATH}/include
    ${FREERTOS_PORT_INCLUDE}
)

target_link_libraries(w07_freertos_jitter
    pico_stdlib
    pico_time
)

pico_enable_stdio_usb(w07_freertos_jitter 1)
pico_enable_stdio_uart(w07_freertos_jitter 0)

pico_add_extra_outputs(w07_freertos_jitter)
