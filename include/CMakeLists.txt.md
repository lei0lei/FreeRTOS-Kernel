# CMakeLists.txt 代码解说

源文件：`include/CMakeLists.txt`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 脚本片段

```cmake
# FreeRTOS internal cmake file. Do not use it in user top-level project
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 2: 脚本片段

```cmake
add_library(freertos_kernel_include INTERFACE)
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 3: 脚本片段

```cmake
target_include_directories(freertos_kernel_include
    INTERFACE
        .
        # Note: DEPRECATED but still supported, may be removed in a future release.
        $<$<NOT:$<TARGET_EXISTS:freertos_config>>:${FREERTOS_CONFIG_FILE_DIRECTORY}>
)
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 4: 脚本片段

```cmake
target_link_libraries(freertos_kernel_include
    INTERFACE
        $<$<TARGET_EXISTS:freertos_config>:freertos_config>
)
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。
