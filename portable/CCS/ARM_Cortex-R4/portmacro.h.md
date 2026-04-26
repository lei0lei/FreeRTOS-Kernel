# portmacro.h 代码解说

源文件：`portable/CCS/ARM_Cortex-R4/portmacro.h`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 文件头和许可证

```c
/*
 * FreeRTOS Kernel <DEVELOPMENT BRANCH>
 * Copyright (C) 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * SPDX-License-Identifier: MIT
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
 *
 */
```

**解说：** 这一段是文件头，说明项目归属、许可证和免责条款；它告诉使用者这个文件按 MIT 许可证发布。

## 片段 2: 预处理配置 __PORTMACRO_H__

```c
#ifndef __PORTMACRO_H__
#define __PORTMACRO_H__

/*-----------------------------------------------------------
 * Port specific definitions.
 *
 * The settings in this file configure FreeRTOS correctly for the
 * given hardware and compiler.
 *
 * These settings should not be altered.
 *-----------------------------------------------------------
 */

/* Type definitions. */
#define portCHAR        char
#define portFLOAT       float
#define portDOUBLE      double
#define portLONG        long
#define portSHORT       short
#define portSTACK_TYPE  uint32_t
#define portBASE_TYPE   long

typedef portSTACK_TYPE StackType_t;
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 3: 类型定义 BaseType_t

```c
typedef long BaseType_t;
```

**解说：** 这一段定义类型 `BaseType_t`，把相关字段或取值组织成一个明确的数据结构，方便内核代码传递和维护状态。

## 片段 4: 类型定义 UBaseType_t

```c
typedef unsigned long UBaseType_t;
```

**解说：** 这一段定义类型 `UBaseType_t`，把相关字段或取值组织成一个明确的数据结构，方便内核代码传递和维护状态。

## 片段 5: 预处理配置 TickType_t

```c
#if (configTICK_TYPE_WIDTH_IN_BITS == TICK_TYPE_WIDTH_16_BITS)
    typedef uint16_t TickType_t;
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 6: 宏 portMAX_DELAY

```c
    #define portMAX_DELAY (TickType_t) 0xFFFF
#elif ( configTICK_TYPE_WIDTH_IN_BITS == TICK_TYPE_WIDTH_32_BITS )
    typedef uint32_t TickType_t;
```

**解说：** 这一段定义宏 `portMAX_DELAY`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 7: 宏 portMAX_DELAY

```c
    #define portMAX_DELAY (TickType_t) 0xFFFFFFFFF

    /* 32-bit tick type on a 32-bit architecture, so reads of the tick count do
    not need to be guarded with a critical section. */
    #define portTICK_TYPE_IS_ATOMIC 1
#else
    #error configTICK_TYPE_WIDTH_IN_BITS set to unsupported tick type width.
#endif
```

**解说：** 这一段定义宏 `portMAX_DELAY`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 8: 宏 vPortEnterCritical

```c
/* Architecture specifics. */
#define portSTACK_GROWTH    (-1)
#define portTICK_PERIOD_MS    ((TickType_t) 1000 / configTICK_RATE_HZ)
#define portBYTE_ALIGNMENT  8

/* Critical section handling. */
extern void vPortEnterCritical(void);
```

**解说：** 这一段定义宏 `vPortEnterCritical`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 9: 代码片段 9

```c
extern void vPortExitCritical(void);
```

**解说：** 这一段是 `portmacro.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 10: 宏 vPortYield

```c
#define portENTER_CRITICAL()        vPortEnterCritical()
#define portEXIT_CRITICAL()         vPortExitCritical()
#define portDISABLE_INTERRUPTS()    asm( " CPSID I" )
#define portENABLE_INTERRUPTS()     asm( " CPSIE I" )

/* Scheduler utilities. */
#pragma SWI_ALIAS( vPortYield, 0 )
extern void vPortYield( void );
```

**解说：** 这一段定义宏 `vPortYield`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 11: 宏 portYIELD

```c
#define portYIELD()                 vPortYield()
#define portSYS_SSIR1_REG           ( * ( ( volatile uint32_t * ) 0xFFFFFFB0 ) )
#define portSYS_SSIR1_SSKEY         ( 0x7500UL )
#define portYIELD_WITHIN_API()      { portSYS_SSIR1_REG = portSYS_SSIR1_SSKEY;  asm( " DSB " ); asm( " ISB " ); }
```

**解说：** 这一段定义宏 `portYIELD`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 12: 宏 portYIELD_FROM_ISR

```c
#define portYIELD_FROM_ISR( x )     do { if( x != pdFALSE ) { portSYS_SSIR1_REG = portSYS_SSIR1_SSKEY;  ( void ) portSYS_SSIR1_REG; } } while( 0 )

#ifndef configUSE_PORT_OPTIMISED_TASK_SELECTION
    #define configUSE_PORT_OPTIMISED_TASK_SELECTION 1
#endif
```

**解说：** 这一段定义宏 `portYIELD_FROM_ISR`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 13: 预处理配置

```c
/* Architecture specific optimisations. */
#if configUSE_PORT_OPTIMISED_TASK_SELECTION == 1

    /* Check the configuration. */
    #if( configMAX_PRIORITIES > 32 )
        #error configUSE_PORT_OPTIMISED_TASK_SELECTION can only be set to 1 when configMAX_PRIORITIES is less than or equal to 32.  It is very rare that a system requires more than 10 to 15 difference priorities as tasks that share a priority will time slice.
    #endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 14: 宏 portRECORD_READY_PRIORITY

```c
    /* Store/clear the ready priorities in a bit map. */
    #define portRECORD_READY_PRIORITY( uxPriority, uxReadyPriorities ) ( uxReadyPriorities ) |= ( 1UL << ( uxPriority ) )
    #define portRESET_READY_PRIORITY( uxPriority, uxReadyPriorities ) ( uxReadyPriorities ) &= ~( 1UL << ( uxPriority ) )

    /*-----------------------------------------------------------*/

    #define portGET_HIGHEST_PRIORITY( uxTopPriority, uxReadyPriorities ) uxTopPriority = ( 31 - __clz( ( uxReadyPriorities ) ) )

#endif /* configUSE_PORT_OPTIMISED_TASK_SELECTION */
```

**解说：** 这一段定义宏 `portRECORD_READY_PRIORITY`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 15: 宏 vFunction

```c
/* Task function macros as described on the FreeRTOS.org WEB site. */
#define portTASK_FUNCTION(vFunction, pvParameters)       void vFunction(void *pvParameters)
#define portTASK_FUNCTION_PROTO(vFunction, pvParameters) void vFunction(void *pvParameters)

#endif /* __PORTMACRO_H__ */
```

**解说：** 这一段定义宏 `vFunction`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。
