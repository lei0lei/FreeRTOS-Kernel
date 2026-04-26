# rp2040_config.h 代码解说

源文件：`portable/ThirdParty/GCC/RP2040/include/rp2040_config.h`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 文件头和许可证

```c
/*
 * FreeRTOS Kernel <DEVELOPMENT BRANCH>
 * Copyright (C) 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * Copyright (c) 2021 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: MIT AND BSD-3-Clause
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 * the Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *
 * https://www.FreeRTOS.org
 * https://github.com/FreeRTOS
 */
```

**解说：** 这一段是文件头，说明项目归属、许可证和免责条款；它告诉使用者这个文件按 MIT 许可证发布。

## 片段 2: 预处理配置 RP2040_CONFIG_H

```c
#ifndef RP2040_CONFIG_H
#define RP2040_CONFIG_H

/* *INDENT-OFF* */
#ifdef __cplusplus
    extern "C" {
#endif
/* *INDENT-ON* */

/* configUSE_DYNAMIC_EXCEPTION_HANDLERS == 1 means set the exception handlers dynamically on cores
 * that need them in case the user has set up distinct vector table offsets per core
 */
#ifndef configUSE_DYNAMIC_EXCEPTION_HANDLERS
    #if defined( PICO_NO_RAM_VECTOR_TABLE ) && ( PICO_NO_RAM_VECTOR_TABLE == 1 )
        #define configUSE_DYNAMIC_EXCEPTION_HANDLERS    0
    #else
        #define configUSE_DYNAMIC_EXCEPTION_HANDLERS    1
    #endif
#endif

/* configSUPPORT_PICO_SYNC_INTEROP == 1 means that SDK pico_sync
 * sem/mutex/queue etc. will work correctly when called from FreeRTOS tasks
 */
#ifndef configSUPPORT_PICO_SYNC_INTEROP
    #if LIB_PICO_SYNC
        #define configSUPPORT_PICO_SYNC_INTEROP    1
    #endif
#endif

/* configSUPPORT_PICO_SYNC_INTEROP == 1 means that SDK pico_time
 * sleep_ms/sleep_us/sleep_until will work correctly when called from FreeRTOS
 * tasks, and will actually block at the FreeRTOS level
 */
#ifndef configSUPPORT_PICO_TIME_INTEROP
    #if LIB_PICO_TIME
        #define configSUPPORT_PICO_TIME_INTEROP    1
    #endif
#endif

#if ( configNUMBER_OF_CORES > 1 )

/* configTICK_CORE indicates which core should handle the SysTick
 * interrupts */
    #ifndef configTICK_CORE
        #define configTICK_CORE    0
    #endif
#endif

/* This SMP port requires two spin locks, which are claimed from the SDK.
 * the spin lock numbers to be used are defined statically and defaulted here
 * to the values nominally set aside for RTOS by the SDK */
#ifndef configSMP_SPINLOCK_0
    #define configSMP_SPINLOCK_0    PICO_SPINLOCK_ID_OS1
#endif

#ifndef configSMP_SPINLOCK_1
    #define configSMP_SPINLOCK_1    PICO_SPINLOCK_ID_OS2
#endif

/* *INDENT-OFF* */
#ifdef __cplusplus
    }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 3: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 4: 预处理配置

```c
/* *INDENT-ON* */
#endif /* ifndef RP2040_CONFIG_H */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。
