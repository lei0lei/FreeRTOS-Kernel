# portmacro.h 代码解说

源文件：`portable/IAR/MSP430/portmacro.h`

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
#define portCHAR          char
#define portFLOAT         float
#define portDOUBLE        double
#define portLONG          long
#define portSHORT         int
#define portSTACK_TYPE    uint16_t
#define portBASE_TYPE     short

typedef portSTACK_TYPE   StackType_t;
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 3: 类型定义 BaseType_t

```c
typedef short            BaseType_t;
```

**解说：** 这一段定义类型 `BaseType_t`，把相关字段或取值组织成一个明确的数据结构，方便内核代码传递和维护状态。

## 片段 4: 类型定义 UBaseType_t

```c
typedef unsigned short   UBaseType_t;
```

**解说：** 这一段定义类型 `UBaseType_t`，把相关字段或取值组织成一个明确的数据结构，方便内核代码传递和维护状态。

## 片段 5: 预处理配置 TickType_t

```c
#if ( configTICK_TYPE_WIDTH_IN_BITS == TICK_TYPE_WIDTH_16_BITS )
    typedef uint16_t     TickType_t;
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 6: 宏 portMAX_DELAY

```c
    #define portMAX_DELAY    ( TickType_t ) 0xffff
#elif ( configTICK_TYPE_WIDTH_IN_BITS == TICK_TYPE_WIDTH_32_BITS )
    typedef uint32_t     TickType_t;
```

**解说：** 这一段定义宏 `portMAX_DELAY`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 7: 宏 portMAX_DELAY

```c
    #define portMAX_DELAY    ( TickType_t ) ( 0xFFFFFFFFUL )
#else
    #error configTICK_TYPE_WIDTH_IN_BITS set to unsupported tick type width.
#endif
```

**解说：** 这一段定义宏 `portMAX_DELAY`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 8: 宏 portDISABLE_INTERRUPTS

```c
/*-----------------------------------------------------------*/
/* Interrupt control macros. */
#define portDISABLE_INTERRUPTS()    _DINT(); _NOP()
#define portENABLE_INTERRUPTS()     _EINT(); _NOP()
/*-----------------------------------------------------------*/

/* Critical section control macros. */
#define portNO_CRITICAL_SECTION_NESTING    ( ( uint16_t ) 0 )

#define portENTER_CRITICAL()                                                     \
    {                                                                            \
        extern volatile uint16_t usCriticalNesting;                              \
                                                                                 \
        portDISABLE_INTERRUPTS();                                                \
                                                                                 \
        /* Now interrupts are disabled usCriticalNesting can be accessed */      \
        /* directly.  Increment ulCriticalNesting to keep a count of how many */ \
        /* times portENTER_CRITICAL() has been called. */                        \
        usCriticalNesting++;                                                     \
    }
```

**解说：** 这一段定义宏 `portDISABLE_INTERRUPTS`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 9: 宏 portEXIT_CRITICAL

```c
#define portEXIT_CRITICAL()                                                         \
    {                                                                               \
        extern volatile uint16_t usCriticalNesting;                                 \
                                                                                    \
        if( usCriticalNesting > portNO_CRITICAL_SECTION_NESTING )                   \
        {                                                                           \
            /* Decrement the nesting count as we are leaving a critical section. */ \
            usCriticalNesting--;                                                    \
                                                                                    \
            /* If the nesting level has reached zero then interrupts should be */   \
            /* re-enabled. */                                                       \
            if( usCriticalNesting == portNO_CRITICAL_SECTION_NESTING )              \
            {                                                                       \
                portENABLE_INTERRUPTS();                                            \
            }                                                                       \
        }                                                                           \
    }
```

**解说：** 这一段定义宏 `portEXIT_CRITICAL`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 10: 代码片段 10

```c
/*-----------------------------------------------------------*/
/* Task utilities. */
/*
 * Manual context switch called by portYIELD or taskYIELD.
 */
extern void vPortYield( void );
```

**解说：** 这一段是 `portmacro.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 11: 宏 vFunction

```c
#define portYIELD()    vPortYield()
/*-----------------------------------------------------------*/

/* Hardware specifics. */
#define portBYTE_ALIGNMENT       2
#define portSTACK_GROWTH         ( -1 )
#define portTICK_PERIOD_MS       ( ( TickType_t ) 1000 / configTICK_RATE_HZ )
#define portNOP()
#define portPOINTER_SIZE_TYPE    uint16_t
/*-----------------------------------------------------------*/

/* Task function macros as described on the FreeRTOS.org WEB site. */
#define portTASK_FUNCTION_PROTO( vFunction, pvParameters )    void vFunction( void * pvParameters )
#define portTASK_FUNCTION( vFunction, pvParameters )          void vFunction( void * pvParameters )

#if configINTERRUPT_EXAMPLE_METHOD == 2

    extern void vTaskSwitchContext( void );
```

**解说：** 这一段定义宏 `vFunction`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 12: 宏 portYIELD_FROM_ISR

```c
    #define portYIELD_FROM_ISR( x )    do { if( x ) vTaskSwitchContext( ); } while( 0 )

#endif
```

**解说：** 这一段定义宏 `portYIELD_FROM_ISR`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 13: 预处理配置

```c
#endif /* PORTMACRO_H */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。
