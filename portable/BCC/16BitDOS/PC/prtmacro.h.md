# prtmacro.h 代码解说

源文件：`portable/BCC/16BitDOS/PC/prtmacro.h`

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

## 片段 2: 预处理配置 PORTMACRO_H

```c
#ifndef PORTMACRO_H
#define PORTMACRO_H

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
#define portFLOAT       long
#define portDOUBLE      long
#define portLONG        long
#define portSHORT       int
#define portSTACK_TYPE  uint16_t
#define portBASE_TYPE   portSHORT

typedef portSTACK_TYPE StackType_t;
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 3: 类型定义 BaseType_t

```c
typedef short BaseType_t;
```

**解说：** 这一段定义类型 `BaseType_t`，把相关字段或取值组织成一个明确的数据结构，方便内核代码传递和维护状态。

## 片段 4: 类型定义 UBaseType_t

```c
typedef unsigned short UBaseType_t;
```

**解说：** 这一段定义类型 `UBaseType_t`，把相关字段或取值组织成一个明确的数据结构，方便内核代码传递和维护状态。

## 片段 5: 预处理配置 TickType_t

```c
#if( configTICK_TYPE_WIDTH_IN_BITS == TICK_TYPE_WIDTH_16_BITS )
    typedef uint16_t TickType_t;
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 6: 宏 portMAX_DELAY

```c
    #define portMAX_DELAY ( TickType_t ) 0xffff
#elif ( configTICK_TYPE_WIDTH_IN_BITS == TICK_TYPE_WIDTH_32_BITS )
    typedef uint32_t TickType_t;
```

**解说：** 这一段定义宏 `portMAX_DELAY`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 7: 宏 portMAX_DELAY

```c
    #define portMAX_DELAY ( TickType_t ) 0xffffffffUL
#else
    #error configTICK_TYPE_WIDTH_IN_BITS set to unsupported tick type width.
#endif
```

**解说：** 这一段定义宏 `portMAX_DELAY`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 8: 宏 portENTER_CRITICAL

```c
/*-----------------------------------------------------------*/
/* Critical section management. */
#define portENTER_CRITICAL()            __asm{ pushf }  \
                                        __asm{ cli   }  \

#define portEXIT_CRITICAL()             __asm{ popf }
```

**解说：** 这一段定义宏 `portENTER_CRITICAL`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 9: 宏 portDISABLE_INTERRUPTS

```c
#define portDISABLE_INTERRUPTS()        __asm{ cli }
```

**解说：** 这一段定义宏 `portDISABLE_INTERRUPTS`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 10: 宏 portENABLE_INTERRUPTS

```c
#define portENABLE_INTERRUPTS()         __asm{ sti }
```

**解说：** 这一段定义宏 `portENABLE_INTERRUPTS`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 11: 宏 portNOP

```c
/*-----------------------------------------------------------*/
/* Hardware specifics. */
#define portNOP()               __asm{ nop }
```

**解说：** 这一段定义宏 `portNOP`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 12: 宏 portSTACK_GROWTH

```c
#define portSTACK_GROWTH        ( -1 )
#define portSWITCH_INT_NUMBER   0x80
#define portYIELD()             __asm{ int portSWITCH_INT_NUMBER }
```

**解说：** 这一段定义宏 `portSTACK_GROWTH`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 13: 宏 vTaskFunction

```c
#define portDOS_TICK_RATE       ( 18.20648 )
#define portTICK_PERIOD_MS      ( ( TickType_t ) 1000 / configTICK_RATE_HZ )
#define portTICKS_PER_DOS_TICK  ( ( uint16_t ) ( ( ( portDOUBLE ) configTICK_RATE_HZ / portDOS_TICK_RATE ) + 0.5 ) )
#define portINITIAL_SW          ( ( portSTACK_TYPE ) 0x0202 )   /* Start the tasks with interrupts enabled. */
#define portBYTE_ALIGNMENT      ( 2 )
/*-----------------------------------------------------------*/

/* Compiler specifics. */
#define portINPUT_BYTE( xAddr )             inp( xAddr )
#define portOUTPUT_BYTE( xAddr, ucValue )   outp( xAddr, ucValue )

/*-----------------------------------------------------------*/

/* Task function macros as described on the FreeRTOS.org WEB site. */
#define portTASK_FUNCTION_PROTO( vTaskFunction, pvParameters ) void vTaskFunction( void *pvParameters )
#define portTASK_FUNCTION( vTaskFunction, pvParameters ) void vTaskFunction( void *pvParameters )

#endif /* PORTMACRO_H */
```

**解说：** 这一段定义宏 `vTaskFunction`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。
