# port.c 代码解说

源文件：`portable/IAR/AVR32_UC3/port.c`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 文件头和许可证

```c
/*
 * FreeRTOS Kernel <DEVELOPMENT BRANCH>
 * Copyright (C) 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * SPDX-License-Identifier: MIT AND BSD-3-Clause
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

## 片段 2: 预处理配置

```c
/*This file has been prepared for Doxygen automatic documentation generation.*/
/*! \file *********************************************************************
 *
 * \brief FreeRTOS port source for AVR32 UC3.
 *
 * - Compiler:           IAR EWAVR32
 * - Supported devices:  All AVR32 devices can be used.
 * - AppNote:
 *
 * \author               Atmel Corporation (Now Microchip):
 *                                        https://www.microchip.com \n
 *                       Support and FAQ: https://www.microchip.com/support/
 *
 *****************************************************************************/
/*
 * Copyright (c) 2007, Atmel Corporation All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * 3. The name of ATMEL may not be used to endorse or promote products derived
 * from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY ATMEL ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE EXPRESSLY AND
 * SPECIFICALLY DISCLAIMED. IN NO EVENT SHALL ATMEL BE LIABLE FOR ANY DIRECT,
 * INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 * THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
/* Scheduler includes. */
#include "FreeRTOS.h"
#include "task.h"

/* AVR32 UC3 includes. */
#include <avr32/io.h>
#include <intrinsics.h>
#include "gpio.h"

#if configDBG
    #include "usart.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 预处理配置

```c
#if ( configTICK_USE_TC == 1 )
    #include "tc.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 4: 宏 portINITIAL_SR

```c
/* Constants required to setup the task context. */
#define portINITIAL_SR             ( ( StackType_t ) 0x00400000 ) /* AVR32 : [M2:M0]=001 I1M=0 I0M=0, GM=0 */
#define portINSTRUCTION_SIZE       ( ( StackType_t ) 0 )

/* Each task maintains its own critical nesting variable. */
#define portNO_CRITICAL_NESTING    ( ( uint32_t ) 0 )
volatile uint32_t ulCriticalNesting = 9999UL;
```

**解说：** 这一段定义宏 `portINITIAL_SR`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 5: 预处理配置 prvScheduleNextTick

```c
#if ( configTICK_USE_TC == 0 )
    static void prvScheduleNextTick( void );
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 6: 预处理配置 prvClearTcInt

```c
#else
    static void prvClearTcInt( void );
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 7: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 8: 代码片段 8

```c
/* Setup the timer to generate the tick interrupts. */
static void prvSetupTimerInterrupt( void );
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 9: 函数 __low_level_init

```c
/*-----------------------------------------------------------*/
/*
 * Low-level initialization routine called during startup, before the main
 * function.
 */
int __low_level_init( void )
{
    #if configHEAP_INIT
    #pragma segment = "HEAP"
        BaseType_t * pxMem;
    #endif

    /* Enable exceptions. */
    ENABLE_ALL_EXCEPTIONS();

    /* Initialize interrupt handling. */
    INTC_init_interrupts();

    #if configHEAP_INIT
    {
        /* Initialize the heap used by malloc. */
        for( pxMem = __segment_begin( "HEAP" ); pxMem < ( BaseType_t * ) __segment_end( "HEAP" ); )
        {
            *pxMem++ = 0xA5A5A5A5;
        }
    }
    #endif

    /* Code section present if and only if the debug trace is activated. */
    #if configDBG
    {
        static const gpio_map_t DBG_USART_GPIO_MAP =
        {
            { configDBG_USART_RX_PIN, configDBG_USART_RX_FUNCTION },
            { configDBG_USART_TX_PIN, configDBG_USART_TX_FUNCTION }
        };

        static const usart_options_t DBG_USART_OPTIONS =
        {
            .baudrate    = configDBG_USART_BAUDRATE,
            .charlength  = 8,
            .paritytype  = USART_NO_PARITY,
            .stopbits    = USART_1_STOPBIT,
            .channelmode = USART_NORMAL_CHMODE
        };

        /* Initialize the USART used for the debug trace with the configured parameters. */
        extern volatile avr32_usart_t * volatile stdio_usart_base;
        stdio_usart_base = configDBG_USART;
        gpio_enable_module( DBG_USART_GPIO_MAP,
                            sizeof( DBG_USART_GPIO_MAP ) / sizeof( DBG_USART_GPIO_MAP[ 0 ] ) );
        usart_init_rs232( configDBG_USART, &DBG_USART_OPTIONS, configCPU_CLOCK_HZ );
    }
    #endif /* if configDBG */

    /* Request initialization of data segments. */
    return 1;
}
```

**解说：** 这一段实现函数 `__low_level_init`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 10: 函数 pvPortRealloc

```c
/*-----------------------------------------------------------*/
/* Added as there is no such function in FreeRTOS. */
void * pvPortRealloc( void * pv,
                      size_t xWantedSize )
{
    void * pvReturn;

    vTaskSuspendAll();
    {
        pvReturn = realloc( pv, xWantedSize );
    }
    xTaskResumeAll();

    return pvReturn;
}
```

**解说：** 这一段实现函数 `pvPortRealloc`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 11: 预处理配置 vTick

```c
/*-----------------------------------------------------------*/
/* The cooperative scheduler requires a normal IRQ service routine to
 * simply increment the system tick. */
/* The preemptive scheduler is defined as "naked" as the full context is saved
 * on entry as part of the context switch. */
#pragma shadow_registers = full /* Naked. */
static void vTick( void )
{
    /* Save the context of the interrupted task. */
    portSAVE_CONTEXT_OS_INT();

    #if ( configTICK_USE_TC == 1 )
        /* Clear the interrupt flag. */
        prvClearTcInt();
    #else

        /* Schedule the COUNT&COMPARE match interrupt in (configCPU_CLOCK_HZ/configTICK_RATE_HZ)
         * clock cycles from now. */
        prvScheduleNextTick();
    #endif

    /* Because FreeRTOS is not supposed to run with nested interrupts, put all OS
     * calls in a critical section . */
    portENTER_CRITICAL();
    xTaskIncrementTick();
    portEXIT_CRITICAL();

    /* Restore the context of the "elected task". */
    portRESTORE_CONTEXT_OS_INT();
}
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 12: 预处理配置 SCALLYield

```c
/*-----------------------------------------------------------*/
#pragma shadow_registers = full /* Naked. */
void SCALLYield( void )
{
    /* Save the context of the interrupted task. */
    portSAVE_CONTEXT_SCALL();
    vTaskSwitchContext();
    portRESTORE_CONTEXT_SCALL();
}
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 13: 预处理配置 vPortEnterCritical

```c
/*-----------------------------------------------------------*/
/* The code generated by the GCC compiler uses the stack in different ways at
 * different optimisation levels.  The interrupt flags can therefore not always
 * be saved to the stack.  Instead the critical section nesting level is stored
 * in a variable, which is then saved as part of the stack context. */
#pragma optimize = no_inline
void vPortEnterCritical( void )
{
    /* Disable interrupts */
    portDISABLE_INTERRUPTS();

    /* Now that interrupts are disabled, ulCriticalNesting can be accessed
     * directly.  Increment ulCriticalNesting to keep a count of how many times
     * portENTER_CRITICAL() has been called. */
    ulCriticalNesting++;
}
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 14: 预处理配置 vPortExitCritical

```c
/*-----------------------------------------------------------*/
#pragma optimize = no_inline
void vPortExitCritical( void )
{
    if( ulCriticalNesting > portNO_CRITICAL_NESTING )
    {
        ulCriticalNesting--;

        if( ulCriticalNesting == portNO_CRITICAL_NESTING )
        {
            /* Enable all interrupt/exception. */
            portENABLE_INTERRUPTS();
        }
    }
}
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 15: 函数 pxPortInitialiseStack

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
    /* Setup the initial stack of the task.  The stack is set exactly as
     * expected by the portRESTORE_CONTEXT() macro. */

    /* When the task starts, it will expect to find the function parameter in R12. */
    pxTopOfStack--;
    *pxTopOfStack-- = ( StackType_t ) 0x08080808;                    /* R8 */
    *pxTopOfStack-- = ( StackType_t ) 0x09090909;                    /* R9 */
    *pxTopOfStack-- = ( StackType_t ) 0x0A0A0A0A;                    /* R10 */
    *pxTopOfStack-- = ( StackType_t ) 0x0B0B0B0B;                    /* R11 */
    *pxTopOfStack-- = ( StackType_t ) pvParameters;                  /* R12 */
    *pxTopOfStack-- = ( StackType_t ) 0xDEADBEEF;                    /* R14/LR */
    *pxTopOfStack-- = ( StackType_t ) pxCode + portINSTRUCTION_SIZE; /* R15/PC */
    *pxTopOfStack-- = ( StackType_t ) portINITIAL_SR;                /* SR */
    *pxTopOfStack-- = ( StackType_t ) 0xFF0000FF;                    /* R0 */
    *pxTopOfStack-- = ( StackType_t ) 0x01010101;                    /* R1 */
    *pxTopOfStack-- = ( StackType_t ) 0x02020202;                    /* R2 */
    *pxTopOfStack-- = ( StackType_t ) 0x03030303;                    /* R3 */
    *pxTopOfStack-- = ( StackType_t ) 0x04040404;                    /* R4 */
    *pxTopOfStack-- = ( StackType_t ) 0x05050505;                    /* R5 */
    *pxTopOfStack-- = ( StackType_t ) 0x06060606;                    /* R6 */
    *pxTopOfStack-- = ( StackType_t ) 0x07070707;                    /* R7 */
    *pxTopOfStack = ( StackType_t ) portNO_CRITICAL_NESTING;         /* ulCriticalNesting */

    return pxTopOfStack;
}
```

**解说：** 这一段实现函数 `pxPortInitialiseStack`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 16: 函数 xPortStartScheduler

```c
/*-----------------------------------------------------------*/
BaseType_t xPortStartScheduler( void )
{
    /* Start the timer that generates the tick ISR.  Interrupts are disabled
     * here already. */
    prvSetupTimerInterrupt();

    /* Start the first task. */
    portRESTORE_CONTEXT();

    /* Should not get here! */
    return 0;
}
```

**解说：** 这一段实现函数 `xPortStartScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 17: 函数 vPortEndScheduler

```c
/*-----------------------------------------------------------*/
void vPortEndScheduler( void )
{
    /* It is unlikely that the AVR32 port will require this function as there
     * is nothing to return to.  */
}
```

**解说：** 这一段实现函数 `vPortEndScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 18: 预处理配置 prvScheduleFirstTick

```c
/*-----------------------------------------------------------*/
/* Schedule the COUNT&COMPARE match interrupt in (configCPU_CLOCK_HZ/configTICK_RATE_HZ)
 * clock cycles from now. */
#if ( configTICK_USE_TC == 0 )
    static void prvScheduleFirstTick( void )
    {
        uint32_t lCycles;

        lCycles = Get_system_register( AVR32_COUNT );
        lCycles += ( configCPU_CLOCK_HZ / configTICK_RATE_HZ );

        /* If lCycles ends up to be 0, make it 1 so that the COMPARE and exception */
        /* generation feature does not get disabled. */
        if( 0 == lCycles )
        {
            lCycles++;
        }

        Set_system_register( AVR32_COMPARE, lCycles );
    }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 19: 预处理配置 prvScheduleNextTick

```c
    #pragma optimize = no_inline
    static void prvScheduleNextTick( void )
    {
        uint32_t lCycles, lCount;

        lCycles = Get_system_register( AVR32_COMPARE );
        lCycles += ( configCPU_CLOCK_HZ / configTICK_RATE_HZ );

        /* If lCycles ends up to be 0, make it 1 so that the COMPARE and exception */
        /* generation feature does not get disabled. */
        if( 0 == lCycles )
        {
            lCycles++;
        }

        lCount = Get_system_register( AVR32_COUNT );

        if( lCycles < lCount )
        { /* We missed a tick, recover for the next. */
            lCycles += ( configCPU_CLOCK_HZ / configTICK_RATE_HZ );
        }

        Set_system_register( AVR32_COMPARE, lCycles );
    }
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 20: 预处理配置 prvClearTcInt

```c
#else /* if ( configTICK_USE_TC == 0 ) */
    #pragma optimize = no_inline
    static void prvClearTcInt( void )
    {
        AVR32_TC.channel[ configTICK_TC_CHANNEL ].sr;
    }
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 21: 预处理配置

```c
#endif /* if ( configTICK_USE_TC == 0 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 22: 函数 prvSetupTimerInterrupt

```c
/*-----------------------------------------------------------*/
/* Setup the timer to generate the tick interrupts. */
static void prvSetupTimerInterrupt( void )
{
    #if ( configTICK_USE_TC == 1 )
        volatile avr32_tc_t * tc = &AVR32_TC;

        /* Options for waveform generation. */
        tc_waveform_opt_t waveform_opt =
        {
            .channel = configTICK_TC_CHANNEL,              /* Channel selection. */

            .bswtrg  = TC_EVT_EFFECT_NOOP,                 /* Software trigger effect on TIOB. */
            .beevt   = TC_EVT_EFFECT_NOOP,                 /* External event effect on TIOB. */
            .bcpc    = TC_EVT_EFFECT_NOOP,                 /* RC compare effect on TIOB. */
            .bcpb    = TC_EVT_EFFECT_NOOP,                 /* RB compare effect on TIOB. */

            .aswtrg  = TC_EVT_EFFECT_NOOP,                 /* Software trigger effect on TIOA. */
            .aeevt   = TC_EVT_EFFECT_NOOP,                 /* External event effect on TIOA. */
            .acpc    = TC_EVT_EFFECT_NOOP,                 /* RC compare effect on TIOA: toggle. */
            .acpa    = TC_EVT_EFFECT_NOOP,                 /* RA compare effect on TIOA: toggle (other possibilities are none, set and clear). */

            .wavsel  = TC_WAVEFORM_SEL_UP_MODE_RC_TRIGGER, /* Waveform selection: Up mode without automatic trigger on RC compare. */
            .enetrg  = FALSE,                              /* External event trigger enable. */
            .eevt    = 0,                                  /* External event selection. */
            .eevtedg = TC_SEL_NO_EDGE,                     /* External event edge selection. */
            .cpcdis  = FALSE,                              /* Counter disable when RC compare. */
            .cpcstop = FALSE,                              /* Counter clock stopped with RC compare. */

            .burst   = FALSE,                              /* Burst signal selection. */
            .clki    = FALSE,                              /* Clock inversion. */
            .tcclks  = TC_CLOCK_SOURCE_TC2                 /* Internal source clock 2. */
        };

        tc_interrupt_t tc_interrupt =
        {
            .etrgs = 0,
            .ldrbs = 0,
            .ldras = 0,
            .cpcs  = 1,
            .cpbs  = 0,
            .cpas  = 0,
            .lovrs = 0,
            .covfs = 0,
        };
    #endif /* if ( configTICK_USE_TC == 1 ) */

    /* Disable all interrupt/exception. */
    portDISABLE_INTERRUPTS();

    /* Register the compare interrupt handler to the interrupt controller and
     * enable the compare interrupt. */

    #if ( configTICK_USE_TC == 1 )
    {
        INTC_register_interrupt( ( __int_handler ) & vTick, configTICK_TC_IRQ, INT0 );

        /* Initialize the timer/counter. */
        tc_init_waveform( tc, &waveform_opt );

        /* Set the compare triggers.
         * Remember TC counter is 16-bits, so counting second is not possible!
         * That's why we configure it to count ms. */
        tc_write_rc( tc, configTICK_TC_CHANNEL, ( configPBA_CLOCK_HZ / 4 ) / configTICK_RATE_HZ );

        tc_configure_interrupts( tc, configTICK_TC_CHANNEL, &tc_interrupt );

        /* Start the timer/counter. */
        tc_start( tc, configTICK_TC_CHANNEL );
    }
    #else /* if ( configTICK_USE_TC == 1 ) */
    {
        INTC_register_interrupt( ( __int_handler ) & vTick, AVR32_CORE_COMPARE_IRQ, INT0 );
        prvScheduleFirstTick();
    }
    #endif /* if ( configTICK_USE_TC == 1 ) */
}
```

**解说：** 这一段实现函数 `prvSetupTimerInterrupt`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。
