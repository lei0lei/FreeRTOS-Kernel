# portmacro.h 代码解说

源文件：`portable/Paradigm/Tern_EE/small/portmacro.h`

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

## 片段 2: 预处理配置 vTaskFunction

```c
#ifndef PORTMACRO_H
#define PORTMACRO_H

/* *INDENT-OFF* */
#ifdef __cplusplus
    extern "C" {
#endif
/* *INDENT-ON* */

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
#define portDOUBLE      long
#define portLONG        long
#define portSHORT       int
#define portSTACK_TYPE  uint16_t
#define portBASE_TYPE   short

typedef portSTACK_TYPE StackType_t;
typedef short BaseType_t;
typedef unsigned short UBaseType_t;


typedef void ( __interrupt __far *pxISR )();

#if( configTICK_TYPE_WIDTH_IN_BITS == TICK_TYPE_WIDTH_16_BITS )
    typedef uint16_t TickType_t;
    #define portMAX_DELAY ( TickType_t ) 0xffff
#elif ( configTICK_TYPE_WIDTH_IN_BITS  == TICK_TYPE_WIDTH_32_BITS )
    typedef uint32_t             TickType_t;
    #define portMAX_DELAY    ( TickType_t ) 0xffffffffUL
#else
    #error configTICK_TYPE_WIDTH_IN_BITS set to unsupported tick type width.
#endif
/*-----------------------------------------------------------*/

/* Critical section handling. */
#define portENTER_CRITICAL()            __asm{ pushf }  \
                                        __asm{ cli   }  \

#define portEXIT_CRITICAL()             __asm{ popf }

#define portDISABLE_INTERRUPTS()        __asm{ cli }

#define portENABLE_INTERRUPTS()         __asm{ sti }
/*-----------------------------------------------------------*/

/* Hardware specifics. */
#define portNOP()                       __asm{ nop }
#define portSTACK_GROWTH                ( -1 )
#define portSWITCH_INT_NUMBER           0x80
#define portYIELD()                     __asm{ int portSWITCH_INT_NUMBER }
#define portTICK_PERIOD_MS              ( ( TickType_t ) 1000 / configTICK_RATE_HZ )
#define portBYTE_ALIGNMENT              2
#define portINITIAL_SW                  ( ( portSTACK_TYPE ) 0x0202 )   /* Start the tasks with interrupts enabled. */
/*-----------------------------------------------------------*/

/* Compiler specifics. */
#define portINPUT_BYTE( xAddr )             inp( xAddr )
#define portOUTPUT_BYTE( xAddr, ucValue )   outp( xAddr, ucValue )
#define portINPUT_WORD( xAddr )             inpw( xAddr )
#define portOUTPUT_WORD( xAddr, usValue )   outpw( xAddr, usValue )
/*-----------------------------------------------------------*/

/* Task function macros as described on the FreeRTOS.org WEB site. */
#define portTASK_FUNCTION_PROTO( vTaskFunction, vParameters ) void vTaskFunction( void *pvParameters )
#define portTASK_FUNCTION( vTaskFunction, vParameters ) void vTaskFunction( void *pvParameters )

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
#endif /* PORTMACRO_H */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。
