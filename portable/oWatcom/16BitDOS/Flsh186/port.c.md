# port.c 代码解说

源文件：`portable/oWatcom/16BitDOS/Flsh186/port.c`

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

## 片段 2: 预处理配置 prvSetTickFrequency

```c
/*
Changes from V1.00:

    + Call to taskYIELD() from within tick ISR has been replaced by the more
      efficient portSWITCH_CONTEXT().
    + ISR function definitions renamed to include the prv prefix.

Changes from V1.2.0:

    + portRESET_PIC() is now called last thing before the end of the preemptive
      tick routine.

Changes from V2.6.1

    + Replaced the sUsingPreemption variable with the configUSE_PREEMPTION
      macro to be consistent with the later ports.
*/
/*-----------------------------------------------------------
 * Implementation of functions defined in portable.h for the Flashlite 186
 * port.
 *----------------------------------------------------------*/
#include <stdlib.h>
#include <i86.h>
#include <dos.h>
#include <setjmp.h>

#include "FreeRTOS.h"
#include "task.h"
#include "portasm.h"

/*lint -e950 Non ANSI reserved words okay in this file only. */

#define portTIMER_EOI_TYPE      ( 8 )
#define portRESET_PIC()         portOUTPUT_WORD( ( uint16_t ) 0xff22, portTIMER_EOI_TYPE )
#define portTIMER_INT_NUMBER    0x12

#define portTIMER_1_CONTROL_REGISTER    ( ( uint16_t ) 0xff5e )
#define portTIMER_0_CONTROL_REGISTER    ( ( uint16_t ) 0xff56 )
#define portTIMER_INTERRUPT_ENABLE      ( ( uint16_t ) 0x2000 )

/* Setup the hardware to generate the required tick frequency. */
static void prvSetTickFrequency( uint32_t ulTickRateHz );
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 代码片段 3

```c
/* Set the hardware back to the state as per before the scheduler started. */
static void prvExitFunction( void );
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 预处理配置

```c
#if configUSE_PREEMPTION == 1
    /* Tick service routine used by the scheduler when preemptive scheduling is
    being used. */
    static void __interrupt __far prvPreemptiveTick( void );
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 5: 预处理配置

```c
#else
    /* Tick service routine used by the scheduler when cooperative scheduling is
    being used. */
    static void __interrupt __far prvNonPreemptiveTick( void );
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 6: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 7: 代码片段 7

```c
/* Trap routine used by taskYIELD() to manually cause a context switch. */
static void __interrupt __far prvYieldProcessor( void );
/*lint -e956 File scopes necessary here. */
/* Set true when the vectors are set so the scheduler will service the tick. */
static int16_t sSchedulerRunning = pdFALSE;
/* Points to the original routine installed on the vector we use for manual context switches.  This is then used to restore the original routine during prvExitFunction(). */
static void ( __interrupt __far *pxOldSwitchISR )();
/* Used to restore the original DOS context when the scheduler is ended. */
static jmp_buf xJumpBuf;
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 8: 函数 xPortStartScheduler

```c
/*lint +e956 */
/*-----------------------------------------------------------*/
BaseType_t xPortStartScheduler( void )
{
    /* This is called with interrupts already disabled. */

    /* Remember what was on the interrupts we are going to use
    so we can put them back later if required. */
    pxOldSwitchISR = _dos_getvect( portSWITCH_INT_NUMBER );

    /* Put our manual switch (yield) function on a known
    vector. */
    _dos_setvect( portSWITCH_INT_NUMBER, prvYieldProcessor );

    #if configUSE_PREEMPTION == 1
    {
        /* Put our tick switch function on the timer interrupt. */
        _dos_setvect( portTIMER_INT_NUMBER, prvPreemptiveTick );
    }
    #else
    {
        /* We want the timer interrupt to just increment the tick count. */
        _dos_setvect( portTIMER_INT_NUMBER, prvNonPreemptiveTick );
    }
    #endif

    prvSetTickFrequency( configTICK_RATE_HZ );

    /* Clean up function if we want to return to DOS. */
    if( setjmp( xJumpBuf ) != 0 )
    {
        prvExitFunction();
        sSchedulerRunning = pdFALSE;
    }
    else
    {
        sSchedulerRunning = pdTRUE;

        /* Kick off the scheduler by setting up the context of the first task. */
        portFIRST_CONTEXT();
    }

    return sSchedulerRunning;
}
```

**解说：** 这一段实现函数 `xPortStartScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 9: 预处理配置

```c
/*-----------------------------------------------------------*/
/* The tick ISR used depend on whether or not the preemptive or cooperative
kernel is being used. */
#if configUSE_PREEMPTION == 1
    static void __interrupt __far prvPreemptiveTick( void )
    {
        /* Get the scheduler to update the task states following the tick. */
        if( xTaskIncrementTick() != pdFALSE )
        {
            /* Switch in the context of the next task to be run. */
            portSWITCH_CONTEXT();
        }

        /* Reset the PIC ready for the next time. */
        portRESET_PIC();
    }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 10: 预处理配置

```c
#else
    static void __interrupt __far prvNonPreemptiveTick( void )
    {
        /* Same as preemptive tick, but the cooperative scheduler is being used
        so we don't have to switch in the context of the next task. */
        xTaskIncrementTick();
        portRESET_PIC();
    }
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 11: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 12: 函数实现

```c
/*-----------------------------------------------------------*/
static void __interrupt __far prvYieldProcessor( void )
{
    /* Switch in the context of the next task to be run. */
    portSWITCH_CONTEXT();
}
```

**解说：** 这一段实现一个函数，把一组相关步骤封装成独立的执行单元。

## 片段 13: 函数 vPortEndScheduler

```c
/*-----------------------------------------------------------*/
void vPortEndScheduler( void )
{
    /* Jump back to the processor state prior to starting the
    scheduler.  This means we are not going to be using a
    task stack frame so the task can be deleted. */
    longjmp( xJumpBuf, 1 );
}
```

**解说：** 这一段实现函数 `vPortEndScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 14: 函数 prvExitFunction

```c
/*-----------------------------------------------------------*/
static void prvExitFunction( void )
{
const uint16_t usTimerDisable = 0x0000;
uint16_t usTimer0Control;

    /* Interrupts should be disabled here anyway - but no
    harm in making sure. */
    portDISABLE_INTERRUPTS();
    if( sSchedulerRunning == pdTRUE )
    {
        /* Put back the switch interrupt routines that was in place
        before the scheduler started. */
        _dos_setvect( portSWITCH_INT_NUMBER, pxOldSwitchISR );
    }

    /* Disable the timer used for the tick to ensure the scheduler is
    not called before restoring interrupts.  There was previously nothing
    on this timer so there is no old ISR to restore. */
    portOUTPUT_WORD( portTIMER_1_CONTROL_REGISTER, usTimerDisable );

    /* Restart the DOS tick. */
    usTimer0Control = portINPUT_WORD( portTIMER_0_CONTROL_REGISTER );
    usTimer0Control |= portTIMER_INTERRUPT_ENABLE;
    portOUTPUT_WORD( portTIMER_0_CONTROL_REGISTER, usTimer0Control );


    portENABLE_INTERRUPTS();
}
```

**解说：** 这一段实现函数 `prvExitFunction`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 15: 函数 prvSetTickFrequency

```c
/*-----------------------------------------------------------*/
static void prvSetTickFrequency( uint32_t ulTickRateHz )
{
const uint16_t usMaxCountRegister = 0xff5a;
const uint16_t usTimerPriorityRegister = 0xff32;
const uint16_t usTimerEnable = 0xC000;
const uint16_t usRetrigger = 0x0001;
const uint16_t usTimerHighPriority = 0x0000;
uint16_t usTimer0Control;

/* ( CPU frequency / 4 ) / clock 2 max count [inpw( 0xff62 ) = 7] */

const uint32_t ulClockFrequency = 0x7f31a0;

uint32_t ulTimerCount = ulClockFrequency / ulTickRateHz;

    portOUTPUT_WORD( portTIMER_1_CONTROL_REGISTER, usTimerEnable | portTIMER_INTERRUPT_ENABLE | usRetrigger );
    portOUTPUT_WORD( usMaxCountRegister, ( uint16_t ) ulTimerCount );
    portOUTPUT_WORD( usTimerPriorityRegister, usTimerHighPriority );

    /* Stop the DOS tick - don't do this if you want to maintain a TOD clock. */
    usTimer0Control = portINPUT_WORD( portTIMER_0_CONTROL_REGISTER );
    usTimer0Control &= ~portTIMER_INTERRUPT_ENABLE;
    portOUTPUT_WORD( portTIMER_0_CONTROL_REGISTER, usTimer0Control );
}
```

**解说：** 这一段实现函数 `prvSetTickFrequency`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 16: 说明性注释

```c
/*lint +e950 */
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：lint +e950。
