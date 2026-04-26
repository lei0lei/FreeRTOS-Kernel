# port.c 代码解说

源文件：`portable/GCC/NiosII/port.c`

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

## 片段 2: 预处理配置 _alt_ic_isr_register

```c
/*-----------------------------------------------------------
* Implementation of functions defined in portable.h for the NIOS2 port.
*----------------------------------------------------------*/
/* Standard Includes. */
#include <string.h>
#include <errno.h>

/* Altera includes. */
#include "sys/alt_irq.h"
#include "sys/alt_exceptions.h"
#include "altera_avalon_timer_regs.h"
#include "priv/alt_irq_table.h"

/* Scheduler includes. */
#include "FreeRTOS.h"
#include "task.h"

/* Interrupts are enabled. */
#define portINITIAL_ESTATUS    ( StackType_t ) 0x01

int _alt_ic_isr_register( alt_u32 ic_id,
                          alt_u32 irq,
                          alt_isr_func isr,
                          void * isr_context,
                          void * flags );
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 代码片段 3

```c
/*-----------------------------------------------------------*/
/*
 * Setup the timer to generate the tick interrupts.
 */
static void prvSetupTimerInterrupt( void );
/*
 * Call back for the alarm function.
 */
void vPortSysTickHandler( void * context );
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 函数 prvReadGp

```c
/*-----------------------------------------------------------*/
static void prvReadGp( uint32_t * ulValue )
{
    asm ( "stw gp, (%0)" ::"r" ( ulValue ) );
}
```

**解说：** 这一段实现函数 `prvReadGp`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 5: 函数 pxPortInitialiseStack

```c
/*-----------------------------------------------------------*/
/*
 * See header file for description.
 */
StackType_t * pxPortInitialiseStack( StackType_t * pxTopOfStack,
                                     TaskFunction_t pxCode,
                                     void * pvParameters )
{
    StackType_t * pxFramePointer = pxTopOfStack - 1;
    StackType_t xGlobalPointer;

    prvReadGp( &xGlobalPointer );

    /* End of stack marker. */
    *pxTopOfStack = 0xdeadbeef;
    pxTopOfStack--;

    *pxTopOfStack = ( StackType_t ) pxFramePointer;
    pxTopOfStack--;

    *pxTopOfStack = xGlobalPointer;

    /* Space for R23 to R16. */
    pxTopOfStack -= 9;

    *pxTopOfStack = ( StackType_t ) pxCode;
    pxTopOfStack--;

    *pxTopOfStack = portINITIAL_ESTATUS;

    /* Space for R15 to R5. */
    pxTopOfStack -= 12;

    *pxTopOfStack = ( StackType_t ) pvParameters;

    /* Space for R3 to R1, muldiv and RA. */
    pxTopOfStack -= 5;

    return pxTopOfStack;
}
```

**解说：** 这一段实现函数 `pxPortInitialiseStack`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 6: 函数 xPortStartScheduler

```c
/*-----------------------------------------------------------*/
/*
 * See header file for description.
 */
BaseType_t xPortStartScheduler( void )
{
    /* Start the timer that generates the tick ISR.  Interrupts are disabled
     * here already. */
    prvSetupTimerInterrupt();

    /* Start the first task. */
    asm volatile ( " movia r2, restore_sp_from_pxCurrentTCB        \n"
                   " jmp r2                                          " );

    /* Should not get here! */
    return 0;
}
```

**解说：** 这一段实现函数 `xPortStartScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 7: 函数 vPortEndScheduler

```c
/*-----------------------------------------------------------*/
void vPortEndScheduler( void )
{
    /* It is unlikely that the NIOS2 port will require this function as there
     * is nothing to return to.  */
}
```

**解说：** 这一段实现函数 `vPortEndScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 8: 函数 prvSetupTimerInterrupt

```c
/*-----------------------------------------------------------*/
/*
 * Setup the systick timer to generate the tick interrupts at the required
 * frequency.
 */
void prvSetupTimerInterrupt( void )
{
    /* Try to register the interrupt handler. */
    if( -EINVAL == _alt_ic_isr_register( SYS_CLK_IRQ_INTERRUPT_CONTROLLER_ID, SYS_CLK_IRQ, vPortSysTickHandler, 0x0, 0x0 ) )
    {
        /* Failed to install the Interrupt Handler. */
        asm ( "break" );
    }
    else
    {
        /* Configure SysTick to interrupt at the requested rate. */
        IOWR_ALTERA_AVALON_TIMER_CONTROL( SYS_CLK_BASE, ALTERA_AVALON_TIMER_CONTROL_STOP_MSK );
        IOWR_ALTERA_AVALON_TIMER_PERIODL( SYS_CLK_BASE, ( configCPU_CLOCK_HZ / configTICK_RATE_HZ ) & 0xFFFF );
        IOWR_ALTERA_AVALON_TIMER_PERIODH( SYS_CLK_BASE, ( configCPU_CLOCK_HZ / configTICK_RATE_HZ ) >> 16 );
        IOWR_ALTERA_AVALON_TIMER_CONTROL( SYS_CLK_BASE, ALTERA_AVALON_TIMER_CONTROL_CONT_MSK | ALTERA_AVALON_TIMER_CONTROL_START_MSK | ALTERA_AVALON_TIMER_CONTROL_ITO_MSK );
    }

    /* Clear any already pending interrupts generated by the Timer. */
    IOWR_ALTERA_AVALON_TIMER_STATUS( SYS_CLK_BASE, ~ALTERA_AVALON_TIMER_STATUS_TO_MSK );
}
```

**解说：** 这一段实现函数 `prvSetupTimerInterrupt`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 9: 函数 vPortSysTickHandler

```c
/*-----------------------------------------------------------*/
void vPortSysTickHandler( void * context )
{
    /* Increment the kernel tick. */
    if( xTaskIncrementTick() != pdFALSE )
    {
        vTaskSwitchContext();
    }

    /* Clear the interrupt. */
    IOWR_ALTERA_AVALON_TIMER_STATUS( SYS_CLK_BASE, ~ALTERA_AVALON_TIMER_STATUS_TO_MSK );
}
```

**解说：** 这一段实现函数 `vPortSysTickHandler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 10: 函数 _alt_ic_isr_register

```c
/*-----------------------------------------------------------*/
/** This function is a re-implementation of the Altera provided function.
 * The function is re-implemented to prevent it from enabling an interrupt
 * when it is registered. Interrupts should only be enabled after the FreeRTOS.org
 * kernel has its scheduler started so that contexts are saved and switched
 * correctly.
 */
int _alt_ic_isr_register( alt_u32 ic_id,
                          alt_u32 irq,
                          alt_isr_func isr,
                          void * isr_context,
                          void * flags )
{
    int rc = -EINVAL;
    alt_irq_context status;
    int id = irq; /* IRQ interpreted as the interrupt ID. */

    if( id < ALT_NIRQ )
    {
        /*
         * interrupts are disabled while the handler tables are updated to ensure
         * that an interrupt doesn't occur while the tables are in an inconsistent
         * state.
         */

        status = alt_irq_disable_all();

        alt_irq[ id ].handler = isr;
        alt_irq[ id ].context = isr_context;

        rc = ( isr ) ? alt_ic_irq_enable( ic_id, id ) : alt_ic_irq_disable( ic_id, id );

        /* alt_irq_enable_all(status); This line is removed to prevent the interrupt from being immediately enabled. */
    }

    return rc;
}
```

**解说：** 这一段实现函数 `_alt_ic_isr_register`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 11: 说明性注释

```c
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。
