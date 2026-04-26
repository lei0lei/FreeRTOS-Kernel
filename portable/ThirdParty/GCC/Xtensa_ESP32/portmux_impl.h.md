# portmux_impl.h 代码解说

源文件：`portable/ThirdParty/GCC/Xtensa_ESP32/portmux_impl.h`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 文件头和许可证

```c
/*
 * SPDX-FileCopyrightText: 2017-2021 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Apache-2.0
 */
```

**解说：** 这一段是文件头，说明项目归属、许可证和免责条款；它告诉使用者这个文件按 MIT 许可证发布。

## 片段 2: 预处理配置 CORE_ID_XOR_SWAP

```c
/* This header exists for performance reasons, in order to inline the
 * implementation of vPortCPUAcquireMutexIntsDisabled and
 * vPortCPUReleaseMutexIntsDisabled into the
 * vTaskEnterCritical/vTaskExitCritical functions in task.c as well as the
 * vPortCPUAcquireMutex/vPortCPUReleaseMutex implementations.
 *
 * Normally this kind of performance hack is over the top, but
 * vTaskEnterCritical/vTaskExitCritical is called a great
 * deal by FreeRTOS internals.
 *
 * It should be #included by freertos port.c or tasks.c, in esp-idf.
 *
 * The way it works is that it essentially uses portmux_impl.inc.h as a
 * generator template of sorts. When no external memory is used, this
 * template is only used to generate the vPortCPUAcquireMutexIntsDisabledInternal
 * and vPortCPUReleaseMutexIntsDisabledInternal functions, which use S32C1 to
 * do an atomic compare & swap. When external memory is used the functions
 * vPortCPUAcquireMutexIntsDisabledExtram and vPortCPUReleaseMutexIntsDisabledExtram
 * are also generated, which use uxPortCompareSetExtram to fake the S32C1 instruction.
 * The wrapper functions vPortCPUAcquireMutexIntsDisabled and
 * vPortCPUReleaseMutexIntsDisabled will then use the appropriate function to do the
 * actual lock/unlock.
 */
#include "soc/cpu.h"
#include "portable.h"

/* XOR one core ID with this value to get the other core ID */
#if ( ESP_IDF_VERSION < ESP_IDF_VERSION_VAL( 4, 2, 0 ) )
    #define CORE_ID_XOR_SWAP           ( CORE_ID_PRO ^ CORE_ID_APP )
#else
    #define CORE_ID_REGVAL_XOR_SWAP    ( CORE_ID_REGVAL_PRO ^ CORE_ID_REGVAL_APP )
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 宏 PORTMUX_AQUIRE_MUX_FN_NAME

```c
/*Define the mux routines for use with muxes in internal RAM */
#define PORTMUX_AQUIRE_MUX_FN_NAME     vPortCPUAcquireMutexIntsDisabledInternal
#define PORTMUX_RELEASE_MUX_FN_NAME    vPortCPUReleaseMutexIntsDisabledInternal
#define PORTMUX_COMPARE_SET_FN_NAME    uxPortCompareSet
#include "portmux_impl.inc.h"
#undef PORTMUX_AQUIRE_MUX_FN_NAME
#undef PORTMUX_RELEASE_MUX_FN_NAME
#undef PORTMUX_COMPARE_SET_FN_NAME


#if defined( CONFIG_SPIRAM_SUPPORT )

    #define PORTMUX_AQUIRE_MUX_FN_NAME     vPortCPUAcquireMutexIntsDisabledExtram
    #define PORTMUX_RELEASE_MUX_FN_NAME    vPortCPUReleaseMutexIntsDisabledExtram
    #define PORTMUX_COMPARE_SET_FN_NAME    uxPortCompareSetExtram
    #include "portmux_impl.inc.h"
    #undef PORTMUX_AQUIRE_MUX_FN_NAME
    #undef PORTMUX_RELEASE_MUX_FN_NAME
    #undef PORTMUX_COMPARE_SET_FN_NAME

#endif
```

**解说：** 这一段定义宏 `PORTMUX_AQUIRE_MUX_FN_NAME`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 4: 预处理配置 PORTMUX_AQUIRE_MUX_FN_ARGS

```c
#ifdef CONFIG_FREERTOS_PORTMUX_DEBUG
    #define PORTMUX_AQUIRE_MUX_FN_ARGS     portMUX_TYPE * mux, int timeout_cycles, const char * fnName, int line
    #define PORTMUX_RELEASE_MUX_FN_ARGS    portMUX_TYPE * mux, const char * fnName, int line
    #define PORTMUX_AQUIRE_MUX_FN_CALL_ARGS( x )     x, timeout_cycles, fnName, line
    #define PORTMUX_RELEASE_MUX_FN_CALL_ARGS( x )    x, fnName, line
#else
    #define PORTMUX_AQUIRE_MUX_FN_ARGS     portMUX_TYPE * mux, int timeout_cycles
    #define PORTMUX_RELEASE_MUX_FN_ARGS    portMUX_TYPE * mux
    #define PORTMUX_AQUIRE_MUX_FN_CALL_ARGS( x )     x, timeout_cycles
    #define PORTMUX_RELEASE_MUX_FN_CALL_ARGS( x )    x
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 5: 函数实现

```c
static inline bool __attribute__( ( always_inline ) ) vPortCPUAcquireMutexIntsDisabled( PORTMUX_AQUIRE_MUX_FN_ARGS )
{
    #if defined( CONFIG_SPIRAM_SUPPORT )
        if( esp_ptr_external_ram( mux ) )
        {
            return vPortCPUAcquireMutexIntsDisabledExtram( PORTMUX_AQUIRE_MUX_FN_CALL_ARGS( mux ) );
        }
    #endif
    return vPortCPUAcquireMutexIntsDisabledInternal( PORTMUX_AQUIRE_MUX_FN_CALL_ARGS( mux ) );
}
```

**解说：** 这一段实现一个函数，把一组相关步骤封装成独立的执行单元。

## 片段 6: 函数 vPortCPUReleaseMutexIntsDisabled

```c
static inline void vPortCPUReleaseMutexIntsDisabled( PORTMUX_RELEASE_MUX_FN_ARGS )
{
    #if defined( CONFIG_SPIRAM_SUPPORT )
        if( esp_ptr_external_ram( mux ) )
        {
            vPortCPUReleaseMutexIntsDisabledExtram( PORTMUX_RELEASE_MUX_FN_CALL_ARGS( mux ) );
            return;
        }
    #endif
    vPortCPUReleaseMutexIntsDisabledInternal( PORTMUX_RELEASE_MUX_FN_CALL_ARGS( mux ) );
}
```

**解说：** 这一段实现函数 `vPortCPUReleaseMutexIntsDisabled`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。
