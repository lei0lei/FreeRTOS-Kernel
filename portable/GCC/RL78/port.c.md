# port.c 代码解说

源文件：`portable/GCC/RL78/port.c`

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

## 片段 2: 预处理配置 portINITIAL_CRITICAL_NESTING

```c
/* Scheduler includes. */
#include "FreeRTOS.h"
#include "task.h"

/* The critical nesting value is initialised to a non zero value to ensure
 * interrupts don't accidentally become enabled before the scheduler is started. */
#define portINITIAL_CRITICAL_NESTING    ( ( uint16_t ) 10 )

/* Initial PSW value allocated to a newly created task.
 *   11000110
 *   ||||||||-------------- Fill byte
 *   |||||||--------------- Carry Flag cleared
 *   |||||----------------- In-service priority Flags set to low level
 *   ||||------------------ Register bank Select 0 Flag cleared
 *   |||------------------- Auxiliary Carry Flag cleared
 *   ||-------------------- Register bank Select 1 Flag cleared
 *   |--------------------- Zero Flag set
 *   ---------------------- Global Interrupt Flag set (enabled)
 */
#define portPSW                         ( 0xc6UL )

/* Each task maintains a count of the critical section nesting depth.  Each time
 * a critical section is entered the count is incremented.  Each time a critical
 * section is exited the count is decremented - with interrupts only being
 * re-enabled if the count is zero.
 *
 * usCriticalNesting will get set to zero when the scheduler starts, but must
 * not be initialised to zero as that could cause problems during the startup
 * sequence. */
volatile uint16_t usCriticalNesting = portINITIAL_CRITICAL_NESTING;
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 代码片段 3

```c
/*-----------------------------------------------------------*/
/*
 * Sets up the periodic ISR used for the RTOS tick.
 */
__attribute__( ( weak ) ) void vApplicationSetupTimerInterrupt( void );
/*
 * Starts the scheduler by loading the context of the first task to run.
 * (defined in portasm.S).
 */
extern void vPortStartFirstTask( void );
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 函数 pxPortInitialiseStack

```c
/*-----------------------------------------------------------*/
/*
 * Initialise the stack of a task to look exactly as if a call to
 * portSAVE_CONTEXT had been called.
 *
 * See the header file portable.h.
 */
StackType_t * pxPortInitialiseStack( StackType_t * pxTopOfStack,
                                     TaskFunction_t pxCode,
                                     void * pvParameters )
{
    uint32_t * pulLocal;

    /* Stack type and pointers to the stack type are both 2 bytes. */

    /* Parameters are passed in on the stack, and written using a 32bit value
     * hence a space is left for the second two bytes. */
    pxTopOfStack--;

    /* Write in the parameter value. */
    pulLocal = ( uint32_t * ) pxTopOfStack;
    *pulLocal = ( StackType_t ) pvParameters;
    pxTopOfStack--;

    /* The return address, leaving space for the first two bytes of the
     * 32-bit value. */
    pxTopOfStack--;
    pulLocal = ( uint32_t * ) pxTopOfStack;
    *pulLocal = ( uint32_t ) 0;
    pxTopOfStack--;

    /* The start address / PSW value is also written in as a 32bit value,
     * so leave a space for the second two bytes. */
    pxTopOfStack--;

    /* Task function start address combined with the PSW. */
    pulLocal = ( uint32_t * ) pxTopOfStack;
    *pulLocal = ( ( ( uint32_t ) pxCode ) | ( portPSW << 24UL ) );
    pxTopOfStack--;

    /* An initial value for the AX register. */
    *pxTopOfStack = ( StackType_t ) 0x1111;
    pxTopOfStack--;

    /* An initial value for the HL register. */
    *pxTopOfStack = ( StackType_t ) 0x2222;
    pxTopOfStack--;

    /* CS and ES registers. */
    *pxTopOfStack = ( StackType_t ) 0x0F00;
    pxTopOfStack--;

    /* The remaining general purpose registers bank 0 (DE and BC) and the other
     * two register banks...register bank 3 is dedicated for use by interrupts so
     * is not saved as part of the task context. */
    pxTopOfStack -= 10;

    /* Finally the critical section nesting count is set to zero when the task
     * first starts. */
    *pxTopOfStack = ( StackType_t ) portNO_CRITICAL_SECTION_NESTING;

    /* Return a pointer to the top of the stack that has been generated so it
     * can be stored in the task control block for the task. */
    return pxTopOfStack;
}
```

**解说：** 这一段实现函数 `pxPortInitialiseStack`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 5: 函数 xPortStartScheduler

```c
/*-----------------------------------------------------------*/
BaseType_t xPortStartScheduler( void )
{
    /* Setup the hardware to generate the tick.  Interrupts are disabled when
     * this function is called. */
    vApplicationSetupTimerInterrupt();

    /* Restore the context of the first task that is going to run. */
    vPortStartFirstTask();

    /* Execution should not reach here as the tasks are now running! */
    return pdTRUE;
}
```

**解说：** 这一段实现函数 `xPortStartScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 6: 函数 vPortEndScheduler

```c
/*-----------------------------------------------------------*/
void vPortEndScheduler( void )
{
    /* It is unlikely that the RL78 port will get stopped. */
}
```

**解说：** 这一段实现函数 `vPortEndScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 7: 函数 vApplicationSetupTimerInterrupt

```c
/*-----------------------------------------------------------*/
__attribute__( ( weak ) ) void vApplicationSetupTimerInterrupt( void )
{
    const uint16_t usClockHz = 15000UL; /* Internal clock. */
    const uint16_t usCompareMatch = ( usClockHz / configTICK_RATE_HZ ) + 1UL;

    /* Use the internal 15K clock. */
    OSMC = ( unsigned char ) 0x16;

    #ifdef RTCEN
    {
        /* Supply the interval timer clock. */
        RTCEN = ( unsigned char ) 1U;

        /* Disable INTIT interrupt. */
        ITMK = ( unsigned char ) 1;

        /* Disable ITMC operation. */
        ITMC = ( unsigned char ) 0x0000;

        /* Clear INIT interrupt. */
        ITIF = ( unsigned char ) 0;

        /* Set interval and enable interrupt operation. */
        ITMC = usCompareMatch | 0x8000U;

        /* Enable INTIT interrupt. */
        ITMK = ( unsigned char ) 0;
    }
    #endif /* ifdef RTCEN */

    #ifdef TMKAEN
    {
        /* Supply the interval timer clock. */
        TMKAEN = ( unsigned char ) 1U;

        /* Disable INTIT interrupt. */
        TMKAMK = ( unsigned char ) 1;

        /* Disable ITMC operation. */
        ITMC = ( unsigned char ) 0x0000;

        /* Clear INIT interrupt. */
        TMKAIF = ( unsigned char ) 0;

        /* Set interval and enable interrupt operation. */
        ITMC = usCompareMatch | 0x8000U;

        /* Enable INTIT interrupt. */
        TMKAMK = ( unsigned char ) 0;
    }
    #endif /* ifdef TMKAEN */
}
```

**解说：** 这一段实现函数 `vApplicationSetupTimerInterrupt`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 8: 说明性注释

```c
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。
