# CMakeLists.txt 代码解说

源文件：`portable/ThirdParty/GCC/RP2040/CMakeLists.txt`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 脚本片段

```cmake
cmake_minimum_required(VERSION 3.13)
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 2: 脚本片段

```cmake
if (NOT TARGET _FreeRTOS_kernel_inclusion_marker)
    add_library(_FreeRTOS_kernel_inclusion_marker INTERFACE)
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 3: 脚本片段

```cmake
    # Pull in PICO SDK (must be before project)
    include(pico_sdk_import.cmake)
    if (PICO_SDK_VERSION_STRING VERSION_LESS "1.2.0")
        message(FATAL_ERROR "Require at least Raspberry Pi Pico SDK version 1.2.0")
    endif()
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 4: 脚本片段

```cmake
    if (NOT FREERTOS_KERNEL_PATH)
        get_filename_component(FREERTOS_KERNEL_PATH ${CMAKE_CURRENT_LIST_DIR}/../../../.. REALPATH)
    endif ()
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 5: 脚本片段

```cmake
    message(DEBUG "FREERTOS_KERNEL_PATH is ${FREERTOS_KERNEL_PATH}")
    project(FreeRTOS-Kernel C CXX)
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 6: 脚本片段

```cmake
    set(CMAKE_C_STANDARD 11)
    set(CMAKE_CXX_STANDARD 17)
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 7: 脚本片段

```cmake
    pico_is_top_level_project(FREERTOS_KERNEL_TOP_LEVEL_PROJECT)
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 8: 脚本片段

```cmake
    # if the SDK has already been initialized, then just add our libraries now - this allows
    # this FreeRTOS port to just be added as a sub-directory or include within another project, rather than
    # having to include it at the top level before pico_sdk_init()
    if (TARGET _pico_sdk_inclusion_marker)
        if (PICO_SDK_VERSION_STRING VERSION_LESS "1.3.2")
            message(FATAL_ERROR "Require at least Raspberry Pi Pico SDK version 1.3.2 to include FreeRTOS after pico_sdk_init()")
        endif()
        include(${CMAKE_CURRENT_LIST_DIR}/library.cmake)
    else()
        # The real work gets done in library.cmake which is called at the end of pico_sdk_init
        list(APPEND PICO_SDK_POST_LIST_FILES ${CMAKE_CURRENT_LIST_DIR}/library.cmake)
        if (PICO_SDK_VERSION_STRING VERSION_LESS "1.3.2")
            # We need to inject the following header file into ALL SDK files (which we do via the config header)
            list(APPEND PICO_CONFIG_HEADER_FILES ${CMAKE_CURRENT_LIST_DIR}/include/freertos_sdk_config.h)
        endif()
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 9: 脚本片段

```cmake
        if (FREERTOS_KERNEL_TOP_LEVEL_PROJECT)
            message("FreeRTOS: initialize SDK since we're the top-level")
            # Initialize the SDK
            pico_sdk_init()
        else()
            set(FREERTOS_KERNEL_PATH ${FREERTOS_KERNEL_PATH} PARENT_SCOPE)
            set(PICO_CONFIG_HEADER_FILES ${PICO_CONFIG_HEADER_FILES} PARENT_SCOPE)
            set(PICO_SDK_POST_LIST_FILES ${PICO_SDK_POST_LIST_FILES} PARENT_SCOPE)
            set(PICO_SDK_VERSION_MAJOR ${PICO_SDK_VERSION_MAJOR} PARENT_SCOPE)
            set(PICO_SDK_VERSION_MINOR ${PICO_SDK_VERSION_MINOR} PARENT_SCOPE)
            set(PICO_SDK_VERSION_REVISION ${PICO_SDK_VERSION_REVISION} PARENT_SCOPE)
        endif()
    endif()
endif()
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。
