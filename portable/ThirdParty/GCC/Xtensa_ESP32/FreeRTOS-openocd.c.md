# FreeRTOS-openocd.c 代码解说

源文件：`portable/ThirdParty/GCC/Xtensa_ESP32/FreeRTOS-openocd.c`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 预处理配置 USED

```c
/*
 * Since at least FreeRTOS V7.5.3 uxTopUsedPriority is no longer
 * present in the kernel, so it has to be supplied by other means for
 * OpenOCD's threads awareness.
 *
 * Add this file to your project, and, if you're using --gc-sections,
 * ``--undefined=uxTopUsedPriority'' (or
 * ``-Wl,--undefined=uxTopUsedPriority'' when using gcc for final
 * linking) to your LDFLAGS; same with all the other symbols you need.
 */
#include "FreeRTOS.h"
#include "esp_attr.h"
#include "sdkconfig.h"

#ifdef __GNUC__
    #define USED    __attribute__( ( used ) )
#else
    #define USED
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 2: 说明性注释

```c
/*
 * This file is no longer needed as AFTER FreeRTOS V10.14.1 OpenOCD is fixed in the kernel.
 * #ifdef CONFIG_ESP32_DEBUG_OCDAWARE
 *   const int USED DRAM_ATTR uxTopUsedPriority = configMAX_PRIORITIES - 1;
 * #endif
 */
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：This file is no longer needed as AFTER FreeRTOS V10.14.1 OpenOCD is fixed in the kernel. ifdef CONFIG_ESP32_DEBUG_OCDAWARE const int USED DRAM_ATTR uxTopUsedPriority = configMAX_PRIORITIES - 1; endif。
