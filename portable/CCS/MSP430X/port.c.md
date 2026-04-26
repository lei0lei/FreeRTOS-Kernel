# port.c 代码解说

源文件：`portable/CCS/MSP430X/port.c`

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

## 片段 2: 预处理配置 portACLK_FREQUENCY_HZ

```c
/* Hardware includes. */
#include "msp430.h"

/* Scheduler includes. */
#include "FreeRTOS.h"
#include "task.h"

/*-----------------------------------------------------------
 * Implementation of functions defined in portable.h for the MSP430X port.
 *----------------------------------------------------------*/

/* Constants required for hardware setup.  The tick ISR runs off the ACLK,
not the MCLK. */
#define portACLK_FREQUENCY_HZ           ( ( TickType_t ) 32768 )
#define portINITIAL_CRITICAL_NESTING    ( ( uint16_t ) 10 )
#define portFLAGS_INT_ENABLED           ( ( StackType_t ) 0x08 )

/* We require the address of the pxCurrentTCB variable, but don't want to know
any details of its type. */
typedef void TCB_t;
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 代码片段 3

```c
extern volatile TCB_t * volatile pxCurrentTCB;
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 代码片段 4

```c
/* Each task maintains a count of the critical section nesting depth.  Each
time a critical section is entered the count is incremented.  Each time a
critical section is exited the count is decremented - with interrupts only
being re-enabled if the count is zero.

usCriticalNesting will get set to zero when the scheduler starts, but must
not be initialised to zero as this will cause problems during the startup
sequence. */
volatile uint16_t usCriticalNesting = portINITIAL_CRITICAL_NESTING;
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 5: 代码片段 5

```c
/*-----------------------------------------------------------*/
/*
 * Sets up the periodic ISR used for the RTOS tick.  This uses timer 0, but
 * could have alternatively used the watchdog timer or timer 1.
 */
void vPortSetupTimerInterrupt( void );
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 6: 函数实现

```c
/*-----------------------------------------------------------*/
/*
 * Initialise the stack of a task to look exactly as if a call to
 * portSAVE_CONTEXT had been called.
 *
 * See the header file portable.h.
 */
StackType_t *pxPortInitialiseStack( StackType_t *pxTopOfStack, TaskFunction_t pxCode, void *pvParameters )
{
uint16_t *pusTopOfStack;
uint32_t *pulTopOfStack, ulTemp;

    /*
        Place a few bytes of known values on the bottom of the stack.
        This is just useful for debugging and can be included if required.

        *pxTopOfStack = ( StackType_t ) 0x1111;
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) 0x2222;
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) 0x3333;
        pxTopOfStack--;
    */

    /* Data types are need either 16 bits or 32 bits depending on the data
    and code model used. */
    if( sizeof( pxCode ) == sizeof( uint16_t ) )
    {
        pusTopOfStack = ( uint16_t * ) pxTopOfStack;
        ulTemp = ( uint32_t ) pxCode;
        *pusTopOfStack = ( uint16_t ) ulTemp;
    }
    else
    {
        /* Make room for a 20 bit value stored as a 32 bit value. */
        pusTopOfStack = ( uint16_t * ) pxTopOfStack;
        pusTopOfStack--;
        pulTopOfStack = ( uint32_t * ) pusTopOfStack;
        *pulTopOfStack = ( uint32_t ) pxCode;
    }

    pusTopOfStack--;
    *pusTopOfStack = portFLAGS_INT_ENABLED;
    pusTopOfStack -= ( sizeof( StackType_t ) / 2 );

    /* From here on the size of stacked items depends on the memory model. */
    pxTopOfStack = ( StackType_t * ) pusTopOfStack;

    /* Next the general purpose registers. */
    #ifdef PRELOAD_REGISTER_VALUES
        *pxTopOfStack = ( StackType_t ) 0xffff;
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) 0xeeee;
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) 0xdddd;
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) pvParameters;
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) 0xbbbb;
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) 0xaaaa;
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) 0x9999;
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) 0x8888;
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) 0x5555;
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) 0x6666;
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) 0x5555;
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) 0x4444;
        pxTopOfStack--;
    #else
        pxTopOfStack -= 3;
        *pxTopOfStack = ( StackType_t ) pvParameters;
        pxTopOfStack -= 9;
    #endif

    /* A variable is used to keep track of the critical section nesting.
    This variable has to be stored as part of the task context and is
    initially set to zero. */
    *pxTopOfStack = ( StackType_t ) portNO_CRITICAL_SECTION_NESTING;

    /* Return a pointer to the top of the stack we have generated so this can
    be stored in the task control block for the task. */
    return pxTopOfStack;
}
```

**解说：** 这一段实现一个函数，把一组相关步骤封装成独立的执行单元。

## 片段 7: 函数 vPortEndScheduler

```c
/*-----------------------------------------------------------*/
void vPortEndScheduler( void )
{
    /* It is unlikely that the MSP430 port will get stopped.  If required simply
    disable the tick interrupt here. */
}
```

**解说：** 这一段实现函数 `vPortEndScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 8: 函数 vPortSetupTimerInterrupt

```c
/*-----------------------------------------------------------*/
/*
 * Hardware initialisation to generate the RTOS tick.
 */
void vPortSetupTimerInterrupt( void )
{
    vApplicationSetupTimerInterrupt();
}
```

**解说：** 这一段实现函数 `vPortSetupTimerInterrupt`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 9: 预处理配置 vTickISREntry

```c
/*-----------------------------------------------------------*/
#pragma vector=configTICK_VECTOR
interrupt void vTickISREntry( void )
{
extern void vPortTickISR( void );

    __bic_SR_register_on_exit( SCG1 + SCG0 + OSCOFF + CPUOFF );
    #if configUSE_PREEMPTION == 1
        extern void vPortPreemptiveTickISR( void );
        vPortPreemptiveTickISR();
    #else
        extern void vPortCooperativeTickISR( void );
        vPortCooperativeTickISR();
    #endif
}
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。
