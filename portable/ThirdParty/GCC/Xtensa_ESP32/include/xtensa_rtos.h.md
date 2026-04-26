# xtensa_rtos.h 代码解说

源文件：`portable/ThirdParty/GCC/Xtensa_ESP32/include/xtensa_rtos.h`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 文件头和许可证

```c
/*
 * SPDX-FileCopyrightText: 2015-2019 Cadence Design Systems, Inc.
 *
 * SPDX-License-Identifier: MIT
 *
 * SPDX-FileContributor: 2016-2022 Espressif Systems (Shanghai) CO LTD
 */
```

**解说：** 这一段是文件头，说明项目归属、许可证和免责条款；它告诉使用者这个文件按 MIT 许可证发布。

## 片段 2: 预处理配置 XTENSA_RTOS_H

```c
/*
 * Copyright (c) 2015-2019 Cadence Design Systems, Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
/*******************************************************************************
*
*       RTOS-SPECIFIC INFORMATION FOR XTENSA RTOS ASSEMBLER SOURCES
*                           (FreeRTOS Port)
*
*  This header is the primary glue between generic Xtensa RTOS support
*  sources and a specific RTOS port for Xtensa.  It contains definitions
*  and macros for use primarily by Xtensa assembly coded source files.
*
*  Macros in this header map callouts from generic Xtensa files to specific
*  RTOS functions. It may also be included in C source files.
*
*  Xtensa RTOS ports support all RTOS-compatible configurations of the Xtensa
*  architecture, using the Xtensa hardware abstraction layer (HAL) to deal
*  with configuration specifics.
*
*  Should be included by all Xtensa generic and RTOS port-specific sources.
*
*******************************************************************************/
#ifndef XTENSA_RTOS_H
#define XTENSA_RTOS_H

#ifdef __ASSEMBLER__
    #include    <xtensa/coreasm.h>
#else
    #include    <xtensa/config/core.h>
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 预处理配置 XT_SIMULATOR

```c
#include    <xtensa/corebits.h>
#include    <xtensa/config/system.h>
#include    "sdkconfig.h"

/*
 * Include any RTOS specific definitions that are needed by this header.
 */
#include    "FreeRTOSConfig.h"

/*
 * Convert FreeRTOSConfig definitions to XTENSA definitions.
 * However these can still be overridden from the command line.
 */

#ifndef XT_SIMULATOR
    #if configXT_SIMULATOR
        #define XT_SIMULATOR    1       /* Simulator mode */
    #endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 4: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 5: 预处理配置 XT_BOARD

```c
#ifndef XT_BOARD
    #if configXT_BOARD
        #define XT_BOARD    1           /* Board mode */
    #endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 6: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 7: 预处理配置 XT_TIMER_INDEX

```c
#ifndef XT_TIMER_INDEX
    #if defined configXT_TIMER_INDEX
        #define XT_TIMER_INDEX    configXT_TIMER_INDEX     /* Index of hardware timer to be used */
    #endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 8: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 9: 预处理配置 XT_INTEXC_HOOKS

```c
#ifndef XT_INTEXC_HOOKS
    #if configXT_INTEXC_HOOKS
        #define XT_INTEXC_HOOKS    1    /* Enables exception hooks */
    #endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 10: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 11: 预处理配置

```c
#if !defined( XT_SIMULATOR ) && !defined( XT_BOARD )
    #error Either XT_SIMULATOR or XT_BOARD must be defined.
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 12: 宏 XT_RTOS_NAME

```c
/*
 * Name of RTOS (for messages).
 */
#define XT_RTOS_NAME    FreeRTOS

/*
 * Check some Xtensa configuration requirements and report error if not met.
 * Error messages can be customize to the RTOS port.
 */

#if !XCHAL_HAVE_XEA2
    #error "FreeRTOS/Xtensa requires XEA2 (exception architecture 2)."
#endif
```

**解说：** 这一段定义宏 `XT_RTOS_NAME`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 13: 宏 XT_RTOS_INT_ENTER

```c
/*******************************************************************************
*
*  RTOS CALLOUT MACROS MAPPED TO RTOS PORT-SPECIFIC FUNCTIONS.
*
*  Define callout macros used in generic Xtensa code to interact with the RTOS.
*  The macros are simply the function names for use in calls from assembler code.
*  Some of these functions may call back to generic functions in xtensa_context.h .
*
*******************************************************************************/
/*
 * Inform RTOS of entry into an interrupt handler that will affect it.
 * Allows RTOS to manage switch to any system stack and count nesting level.
 * Called after minimal context has been saved, with interrupts disabled.
 * RTOS port can call0 _xt_context_save to save the rest of the context.
 * May only be called from assembly code by the 'call0' instruction.
 */
/* void XT_RTOS_INT_ENTER(void) */
#define XT_RTOS_INT_ENTER    _frxt_int_enter

/*
 * Inform RTOS of completion of an interrupt handler, and give control to
 * RTOS to perform thread/task scheduling, switch back from any system stack
 * and restore the context, and return to the exit dispatcher saved in the
 * stack frame at XT_STK_EXIT. RTOS port can call0 _xt_context_restore
 * to save the context saved in XT_RTOS_INT_ENTER via _xt_context_save,
 * leaving only a minimal part of the context to be restored by the exit
 * dispatcher. This function does not return to the place it was called from.
 * May only be called from assembly code by the 'call0' instruction.
 */
/* void XT_RTOS_INT_EXIT(void) */
#define XT_RTOS_INT_EXIT    _frxt_int_exit

/*
 * Inform RTOS of the occurrence of a tick timer interrupt.
 * If RTOS has no tick timer, leave XT_RTOS_TIMER_INT undefined.
 * May be coded in or called from C or assembly, per ABI conventions.
 * RTOS may optionally define XT_TICK_PER_SEC in its own way (eg. macro).
 */
/* void XT_RTOS_TIMER_INT(void) */
#ifdef CONFIG_FREERTOS_SYSTICK_USES_CCOUNT
    #define XT_RTOS_TIMER_INT    _frxt_timer_int
#endif
```

**解说：** 这一段定义宏 `XT_RTOS_INT_ENTER`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 14: 宏 XT_RTOS_CP_STATE

```c
#define XT_TICK_PER_SEC          configTICK_RATE_HZ

/*
 * Return in a15 the base address of the co-processor state save area for the
 * thread that triggered a co-processor exception, or 0 if no thread was running.
 * The state save area is structured as defined in xtensa_context.h and has size
 * XT_CP_SIZE. Co-processor instructions should only be used in thread code, never
 * in interrupt handlers or the RTOS kernel. May only be called from assembly code
 * and by the 'call0' instruction. A result of 0 indicates an unrecoverable error.
 * The implementation may use only a2-4, a15 (all other regs must be preserved).
 */
/* void* XT_RTOS_CP_STATE(void) */
#define XT_RTOS_CP_STATE    _frxt_task_coproc_state


/*******************************************************************************
*
*  HOOKS TO DYNAMICALLY INSTALL INTERRUPT AND EXCEPTION HANDLERS PER LEVEL.
*
*  This Xtensa RTOS port provides hooks for dynamically installing exception
*  and interrupt handlers to facilitate automated testing where each test
*  case can install its own handler for user exceptions and each interrupt
*  priority (level). This consists of an array of function pointers indexed
*  by interrupt priority, with index 0 being the user exception handler hook.
*  Each entry in the array is initially 0, and may be replaced by a function
*  pointer of type XT_INTEXC_HOOK. A handler may be uninstalled by installing 0.
*
*  The handler for low and medium priority obeys ABI conventions so may be coded
*  in C. For the exception handler, the cause is the contents of the EXCCAUSE
*  reg, and the result is -1 if handled, else the cause (still needs handling).
*  For interrupt handlers, the cause is a mask of pending enabled interrupts at
*  that level, and the result is the same mask with the bits for the handled
*  interrupts cleared (those not cleared still need handling). This allows a test
*  case to either pre-handle or override the default handling for the exception
*  or interrupt level (see xtensa_vectors.S).
*
*  High priority handlers (including NMI) must be coded in assembly, are always
*  called by 'call0' regardless of ABI, must preserve all registers except a0,
*  and must not use or modify the interrupted stack. The hook argument 'cause'
*  is not passed and the result is ignored, so as not to burden the caller with
*  saving and restoring a2 (it assumes only one interrupt per level - see the
*  discussion in high priority interrupts in xtensa_vectors.S). The handler
*  therefore should be coded to prototype 'void h(void)' even though it plugs
*  into an array of handlers of prototype 'unsigned h(unsigned)'.
*
*  To enable interrupt/exception hooks, compile the RTOS with '-DXT_INTEXC_HOOKS'.
*
*******************************************************************************/

#define XT_INTEXC_HOOK_NUM    ( 1 + XCHAL_NUM_INTLEVELS + XCHAL_HAVE_NMI )

#ifndef __ASSEMBLER__
    typedef unsigned (* XT_INTEXC_HOOK)( unsigned cause );
```

**解说：** 这一段定义宏 `XT_RTOS_CP_STATE`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 15: 代码片段 15

```c
    extern volatile XT_INTEXC_HOOK _xt_intexc_hooks[ XT_INTEXC_HOOK_NUM ];
```

**解说：** 这一段是 `xtensa_rtos.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 16: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 17: 预处理配置

```c
/*******************************************************************************
*
*  CONVENIENCE INCLUSIONS.
*
*  Ensures RTOS specific files need only include this one Xtensa-generic header.
*  These headers are included last so they can use the RTOS definitions above.
*
*******************************************************************************/
#include    "xtensa_context.h"

#ifdef XT_RTOS_TIMER_INT
    #include    "xtensa_timer.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 18: 宏 XTENSA_PORT_VERSION

```c
/*******************************************************************************
*
*  Xtensa Port Version.
*
*******************************************************************************/
#define XTENSA_PORT_VERSION           1.4 .2
#define XTENSA_PORT_VERSION_STRING    "1.4.2"

#endif /* XTENSA_RTOS_H */
```

**解说：** 这一段定义宏 `XTENSA_PORT_VERSION`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。
