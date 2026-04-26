# port.c 代码解说

源文件：`portable/IAR/AtmelSAM7S64/port.c`

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

## 片段 2: 预处理配置 prvSetupTimerInterrupt

```c
/*-----------------------------------------------------------
* Implementation of functions defined in portable.h for the Atmel ARM7 port.
*----------------------------------------------------------*/
/* Standard includes. */
#include <stdlib.h>

/* Scheduler includes. */
#include "FreeRTOS.h"
#include "task.h"

/* Constants required to setup the initial stack. */
#define portINITIAL_SPSR           ( ( StackType_t ) 0x1f )      /* System mode, ARM mode, interrupts enabled. */
#define portTHUMB_MODE_BIT         ( ( StackType_t ) 0x20 )
#define portINSTRUCTION_SIZE       ( ( StackType_t ) 4 )

/* Constants required to setup the PIT. */
#define portPIT_CLOCK_DIVISOR      ( ( uint32_t ) 16 )
#define portPIT_COUNTER_VALUE      ( ( ( configCPU_CLOCK_HZ / portPIT_CLOCK_DIVISOR ) / 1000UL ) * portTICK_PERIOD_MS )

/* Constants required to handle critical sections. */
#define portNO_CRITICAL_NESTING    ( ( uint32_t ) 0 )


#define portINT_LEVEL_SENSITIVE    0
#define portPIT_ENABLE             ( ( uint16_t ) 0x1 << 24 )
#define portPIT_INT_ENABLE         ( ( uint16_t ) 0x1 << 25 )
/*-----------------------------------------------------------*/

/* Setup the PIT to generate the tick interrupts. */
static void prvSetupTimerInterrupt( void );
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 代码片段 3

```c
/* ulCriticalNesting will get set to zero when the first task starts.  It
 * cannot be initialised to 0 as this will cause interrupts to be enabled
 * during the kernel initialisation process. */
uint32_t ulCriticalNesting = ( uint32_t ) 9999;
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 函数 pxPortInitialiseStack

```c
/*-----------------------------------------------------------*/
/*
 * Initialise the stack of a task to look exactly as if a call to
 * portSAVE_CONTEXT had been called.
 *
 * See header file for description.
 */
StackType_t * pxPortInitialiseStack( StackType_t * pxTopOfStack,
                                     TaskFunction_t pxCode,
                                     void * pvParameters )
{
    StackType_t * pxOriginalTOS;

    pxOriginalTOS = pxTopOfStack;

    /* To ensure asserts in tasks.c don't fail, although in this case the assert
     * is not really required. */
    pxTopOfStack--;

    /* Setup the initial stack of the task.  The stack is set exactly as
     * expected by the portRESTORE_CONTEXT() macro. */

    /* First on the stack is the return address - which in this case is the
     * start of the task.  The offset is added to make the return address appear
     * as it would within an IRQ ISR. */
    *pxTopOfStack = ( StackType_t ) pxCode + portINSTRUCTION_SIZE;
    pxTopOfStack--;

    *pxTopOfStack = ( StackType_t ) 0xaaaaaaaa;    /* R14 */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) pxOriginalTOS; /* Stack used when task starts goes in R13. */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x12121212;    /* R12 */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x11111111;    /* R11 */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x10101010;    /* R10 */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x09090909;    /* R9 */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x08080808;    /* R8 */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x07070707;    /* R7 */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x06060606;    /* R6 */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x05050505;    /* R5 */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x04040404;    /* R4 */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x03030303;    /* R3 */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x02020202;    /* R2 */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x01010101;    /* R1 */
    pxTopOfStack--;

    /* When the task starts is will expect to find the function parameter in
     * R0. */
    *pxTopOfStack = ( StackType_t ) pvParameters; /* R0 */
    pxTopOfStack--;

    /* The status register is set for system mode, with interrupts enabled. */
    *pxTopOfStack = ( StackType_t ) portINITIAL_SPSR;

    if( ( ( uint32_t ) pxCode & 0x01UL ) != 0x00UL )
    {
        /* We want the task to start in thumb mode. */
        *pxTopOfStack |= portTHUMB_MODE_BIT;
    }

    pxTopOfStack--;

    /* Interrupt flags cannot always be stored on the stack and will
     * instead be stored in a variable, which is then saved as part of the
     * tasks context. */
    *pxTopOfStack = portNO_CRITICAL_NESTING;

    return pxTopOfStack;
}
```

**解说：** 这一段实现函数 `pxPortInitialiseStack`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 5: 函数 xPortStartScheduler

```c
/*-----------------------------------------------------------*/
BaseType_t xPortStartScheduler( void )
{
    extern void vPortStartFirstTask( void );

    /* Start the timer that generates the tick ISR.  Interrupts are disabled
     * here already. */
    prvSetupTimerInterrupt();

    /* Start the first task. */
    vPortStartFirstTask();

    /* Should not get here! */
    return 0;
}
```

**解说：** 这一段实现函数 `xPortStartScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 6: 函数 vPortEndScheduler

```c
/*-----------------------------------------------------------*/
void vPortEndScheduler( void )
{
    /* It is unlikely that the ARM port will require this function as there
     * is nothing to return to.  */
}
```

**解说：** 这一段实现函数 `vPortEndScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 7: 预处理配置 vPortNonPreemptiveTick

```c
/*-----------------------------------------------------------*/
#if configUSE_PREEMPTION == 0

/* The cooperative scheduler requires a normal IRQ service routine to
 * simply increment the system tick. */
    static __arm __irq void vPortNonPreemptiveTick( void );
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 8: 函数 vPortNonPreemptiveTick

```c
    static __arm __irq void vPortNonPreemptiveTick( void )
    {
        uint32_t ulDummy;

        /* Increment the tick count - which may wake some tasks but as the
         * preemptive scheduler is not being used any woken task is not given
         * processor time no matter what its priority. */
        xTaskIncrementTick();

        /* Clear the PIT interrupt. */
        ulDummy = AT91C_BASE_PITC->PITC_PIVR;

        /* End the interrupt in the AIC. */
        AT91C_BASE_AIC->AIC_EOICR = ulDummy;
    }
```

**解说：** 这一段实现函数 `vPortNonPreemptiveTick`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 9: 预处理配置

```c
#else /* if configUSE_PREEMPTION == 0 */

/* Currently the IAR port requires the preemptive tick function to be
 * defined in an asm file. */

#endif /* if configUSE_PREEMPTION == 0 */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 10: 函数 prvSetupTimerInterrupt

```c
/*-----------------------------------------------------------*/
static void prvSetupTimerInterrupt( void )
{
    AT91PS_PITC pxPIT = AT91C_BASE_PITC;

    /* Setup the AIC for PIT interrupts.  The interrupt routine chosen depends
     * on whether the preemptive or cooperative scheduler is being used. */
    #if configUSE_PREEMPTION == 0
        AT91F_AIC_ConfigureIt( AT91C_BASE_AIC, AT91C_ID_SYS, AT91C_AIC_PRIOR_HIGHEST, portINT_LEVEL_SENSITIVE, ( void ( * )( void ) )vPortNonPreemptiveTick );
    #else
        extern void( vPortPreemptiveTick )( void );
        AT91F_AIC_ConfigureIt( AT91C_BASE_AIC, AT91C_ID_SYS, AT91C_AIC_PRIOR_HIGHEST, portINT_LEVEL_SENSITIVE, ( void ( * )( void ) )vPortPreemptiveTick );
    #endif

    /* Configure the PIT period. */
    pxPIT->PITC_PIMR = portPIT_ENABLE | portPIT_INT_ENABLE | portPIT_COUNTER_VALUE;

    /* Enable the interrupt.  Global interrupts are disabled at this point so
     * this is safe. */
    AT91F_AIC_EnableIt( AT91C_BASE_AIC, AT91C_ID_SYS );
}
```

**解说：** 这一段实现函数 `prvSetupTimerInterrupt`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 11: 函数 vPortEnterCritical

```c
/*-----------------------------------------------------------*/
void vPortEnterCritical( void )
{
    /* Disable interrupts first! */
    __disable_interrupt();

    /* Now that interrupts are disabled, ulCriticalNesting can be accessed
     * directly.  Increment ulCriticalNesting to keep a count of how many times
     * portENTER_CRITICAL() has been called. */
    ulCriticalNesting++;
}
```

**解说：** 这一段实现函数 `vPortEnterCritical`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 12: 函数 vPortExitCritical

```c
/*-----------------------------------------------------------*/
void vPortExitCritical( void )
{
    if( ulCriticalNesting > portNO_CRITICAL_NESTING )
    {
        /* Decrement the nesting count as we are leaving a critical section. */
        ulCriticalNesting--;

        /* If the nesting level has reached zero then interrupts should be
         * re-enabled. */
        if( ulCriticalNesting == portNO_CRITICAL_NESTING )
        {
            __enable_interrupt();
        }
    }
}
```

**解说：** 这一段实现函数 `vPortExitCritical`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 13: 说明性注释

```c
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。
