# port.c 代码解说

源文件：`portable/IAR/STR91x/port.c`

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

## 片段 2: 预处理配置

```c
/*-----------------------------------------------------------
* Implementation of functions defined in portable.h for the ST STR91x ARM9
* port.
*----------------------------------------------------------*/
/* Library includes. */
#include "91x_lib.h"

/* Standard includes. */
#include <stdlib.h>
#include <assert.h>

/* Scheduler includes. */
#include "FreeRTOS.h"
#include "task.h"

#ifndef configUSE_WATCHDOG_TICK
    #error configUSE_WATCHDOG_TICK must be set to either 1 or 0 in FreeRTOSConfig.h to use either the Watchdog or timer 2 to generate the tick interrupt respectively.
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 预处理配置 portINITIAL_SPSR

```c
/* Constants required to setup the initial stack. */
#ifndef _RUN_TASK_IN_ARM_MODE_
    #define portINITIAL_SPSR       ( ( StackType_t ) 0x3f )      /* System mode, THUMB mode, interrupts enabled. */
#else
    #define portINITIAL_SPSR       ( ( StackType_t ) 0x1f )      /* System mode, ARM mode, interrupts enabled. */
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 4: 宏 portINSTRUCTION_SIZE

```c
#define portINSTRUCTION_SIZE       ( ( StackType_t ) 4 )

/* Constants required to handle critical sections. */
#define portNO_CRITICAL_NESTING    ( ( uint32_t ) 0 )

#ifndef abs
    #define abs( x )    ( ( x ) > 0 ? ( x ) : -( x ) )
#endif
```

**解说：** 这一段定义宏 `portINSTRUCTION_SIZE`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 5: 宏 TOGGLE_LED

```c
/**
 * Toggle a led using the following algorithm:
 * if ( GPIO_ReadBit(GPIO9, GPIO_Pin_2) )
 * {
 *   GPIO_WriteBit( GPIO9, GPIO_Pin_2, Bit_RESET );
 * }
 * else
 * {
 *   GPIO_WriteBit( GPIO9, GPIO_Pin_2, Bit_RESET );
 * }
 *
 */
#define TOGGLE_LED( port, pin )                                           \
    if( ( ( ( ( port )->DR[ ( pin ) << 2 ] ) ) & ( pin ) ) != Bit_RESET ) \
    {                                                                     \
        ( port )->DR[ ( pin ) << 2 ] = 0x00;                              \
    }                                                                     \
    else                                                                  \
    {                                                                     \
        ( port )->DR[ ( pin ) << 2 ] = ( pin );                           \
    }
```

**解说：** 这一段定义宏 `TOGGLE_LED`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 6: 代码片段 6

```c
/*-----------------------------------------------------------*/
/* Setup the watchdog to generate the tick interrupts. */
static void prvSetupTimerInterrupt( void );
/* ulCriticalNesting will get set to zero when the first task starts.  It
 * cannot be initialised to 0 as this will cause interrupts to be enabled
 * during the kernel initialisation process. */
uint32_t ulCriticalNesting = ( uint32_t ) 9999;
/* Tick interrupt routines for cooperative and preemptive operation
 * respectively.  The preemptive version is not defined as __irq as it is called
 * from an asm wrapper function. */
void WDG_IRQHandler( void );
/* VIC interrupt default handler. */
static void prvDefaultHandler( void );
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 7: 预处理配置

```c
#if configUSE_WATCHDOG_TICK == 0
    /* Used to update the OCR timer register */
    static u16 s_nPulseLength;
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 8: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 9: 函数 pxPortInitialiseStack

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
    pxTopOfStack--;

    /* Interrupt flags cannot always be stored on the stack and will
     * instead be stored in a variable, which is then saved as part of the
     * tasks context. */
    *pxTopOfStack = portNO_CRITICAL_NESTING;

    return pxTopOfStack;
}
```

**解说：** 这一段实现函数 `pxPortInitialiseStack`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 10: 函数 xPortStartScheduler

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

## 片段 11: 函数 vPortEndScheduler

```c
/*-----------------------------------------------------------*/
void vPortEndScheduler( void )
{
    /* It is unlikely that the ARM port will require this function as there
     * is nothing to return to.  */
}
```

**解说：** 这一段实现函数 `vPortEndScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 12: 预处理配置 prvFindFactors

```c
/*-----------------------------------------------------------*/
/* This function is called from an asm wrapper, so does not require the __irq
 * keyword. */
#if configUSE_WATCHDOG_TICK == 1

    static void prvFindFactors( u32 n,
                                u16 * a,
                                u32 * b )
    {
        /* This function is copied from the ST STR7 library and is
         * copyright STMicroelectronics.  Reproduced with permission. */

        u32 b0;
        u16 a0;
        int32_t err, err_min = n;

        *a = a0 = ( ( n - 1 ) / 65536ul ) + 1;
        *b = b0 = n / *a;

        for( ; *a <= 256; ( *a )++ )
        {
            *b = n / *a;
            err = ( int32_t ) *a * ( int32_t ) *b - ( int32_t ) n;

            if( abs( err ) > ( *a / 2 ) )
            {
                ( *b )++;
                err = ( int32_t ) *a * ( int32_t ) *b - ( int32_t ) n;
            }

            if( abs( err ) < abs( err_min ) )
            {
                err_min = err;
                a0 = *a;
                b0 = *b;

                if( err == 0 )
                {
                    break;
                }
            }
        }

        *a = a0;
        *b = b0;
    }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 13: 函数 prvSetupTimerInterrupt

```c
    /*-----------------------------------------------------------*/
    static void prvSetupTimerInterrupt( void )
    {
        WDG_InitTypeDef xWdg;
        uint16_t a;
        uint32_t n = configCPU_PERIPH_HZ / configTICK_RATE_HZ, b;

        /* Configure the watchdog as a free running timer that generates a
         * periodic interrupt. */

        SCU_APBPeriphClockConfig( __WDG, ENABLE );
        WDG_DeInit();
        WDG_StructInit( &xWdg );
        prvFindFactors( n, &a, &b );
        xWdg.WDG_Prescaler = a - 1;
        xWdg.WDG_Preload = b - 1;
        WDG_Init( &xWdg );
        WDG_ITConfig( ENABLE );

        /* Configure the VIC for the WDG interrupt. */
        VIC_Config( WDG_ITLine, VIC_IRQ, 10 );
        VIC_ITCmd( WDG_ITLine, ENABLE );

        /* Install the default handlers for both VIC's. */
        VIC0->DVAR = ( uint32_t ) prvDefaultHandler;
        VIC1->DVAR = ( uint32_t ) prvDefaultHandler;

        WDG_Cmd( ENABLE );
    }
```

**解说：** 这一段实现函数 `prvSetupTimerInterrupt`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 14: 函数 WDG_IRQHandler

```c
    /*-----------------------------------------------------------*/
    void WDG_IRQHandler( void )
    {
        {
            /* Increment the tick counter. */
            if( xTaskIncrementTick() != pdFALSE )
            {
                /* Select a new task to execute. */
                vTaskSwitchContext();
            }

            /* Clear the interrupt in the watchdog. */
            WDG->SR &= ~0x0001;
        }
    }
```

**解说：** 这一段实现函数 `WDG_IRQHandler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 15: 预处理配置 prvFindFactors

```c
#else /* if configUSE_WATCHDOG_TICK == 1 */

    static void prvFindFactors( u32 n,
                                u8 * a,
                                u16 * b )
    {
        /* This function is copied from the ST STR7 library and is
         * copyright STMicroelectronics.  Reproduced with permission. */

        u16 b0;
        u8 a0;
        int32_t err, err_min = n;


        *a = a0 = ( ( n - 1 ) / 256 ) + 1;
        *b = b0 = n / *a;

        for( ; *a <= 256; ( *a )++ )
        {
            *b = n / *a;
            err = ( int32_t ) *a * ( int32_t ) *b - ( int32_t ) n;

            if( abs( err ) > ( *a / 2 ) )
            {
                ( *b )++;
                err = ( int32_t ) *a * ( int32_t ) *b - ( int32_t ) n;
            }

            if( abs( err ) < abs( err_min ) )
            {
                err_min = err;
                a0 = *a;
                b0 = *b;

                if( err == 0 )
                {
                    break;
                }
            }
        }

        *a = a0;
        *b = b0;
    }
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 16: 函数 prvSetupTimerInterrupt

```c
    /*-----------------------------------------------------------*/
    static void prvSetupTimerInterrupt( void )
    {
        uint8_t a;
        uint16_t b;
        uint32_t n = configCPU_PERIPH_HZ / configTICK_RATE_HZ;

        TIM_InitTypeDef timer;

        SCU_APBPeriphClockConfig( __TIM23, ENABLE );
        TIM_DeInit( TIM2 );
        TIM_StructInit( &timer );
        prvFindFactors( n, &a, &b );

        timer.TIM_Mode = TIM_OCM_CHANNEL_1;
        timer.TIM_OC1_Modes = TIM_TIMING;
        timer.TIM_Clock_Source = TIM_CLK_APB;
        timer.TIM_Clock_Edge = TIM_CLK_EDGE_RISING;
        timer.TIM_Prescaler = a - 1;
        timer.TIM_Pulse_Level_1 = TIM_HIGH;
        timer.TIM_Pulse_Length_1 = s_nPulseLength = b - 1;

        TIM_Init( TIM2, &timer );
        TIM_ITConfig( TIM2, TIM_IT_OC1, ENABLE );
        /* Configure the VIC for the WDG interrupt. */
        VIC_Config( TIM2_ITLine, VIC_IRQ, 10 );
        VIC_ITCmd( TIM2_ITLine, ENABLE );

        /* Install the default handlers for both VIC's. */
        VIC0->DVAR = ( uint32_t ) prvDefaultHandler;
        VIC1->DVAR = ( uint32_t ) prvDefaultHandler;

        TIM_CounterCmd( TIM2, TIM_CLEAR );
        TIM_CounterCmd( TIM2, TIM_START );
    }
```

**解说：** 这一段实现函数 `prvSetupTimerInterrupt`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 17: 函数 TIM2_IRQHandler

```c
    /*-----------------------------------------------------------*/
    void TIM2_IRQHandler( void )
    {
        /* Reset the timer counter to avoid overflow. */
        TIM2->OC1R += s_nPulseLength;

        /* Increment the tick counter. */
        if( xTaskIncrementTick() != pdFALSE )
        {
            /* Select a new task to run. */
            vTaskSwitchContext();
        }

        /* Clear the interrupt in the watchdog. */
        TIM2->SR &= ~TIM_FLAG_OC1;
    }
```

**解说：** 这一段实现函数 `TIM2_IRQHandler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 18: 预处理配置

```c
#endif /* USE_WATCHDOG_TICK */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 19: 函数 vPortEnterCritical

```c
/*-----------------------------------------------------------*/
__arm __interwork void vPortEnterCritical( void )
{
    /* Disable interrupts first! */
    portDISABLE_INTERRUPTS();

    /* Now that interrupts are disabled, ulCriticalNesting can be accessed
     * directly.  Increment ulCriticalNesting to keep a count of how many times
     * portENTER_CRITICAL() has been called. */
    ulCriticalNesting++;
}
```

**解说：** 这一段实现函数 `vPortEnterCritical`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 20: 函数 vPortExitCritical

```c
/*-----------------------------------------------------------*/
__arm __interwork void vPortExitCritical( void )
{
    if( ulCriticalNesting > portNO_CRITICAL_NESTING )
    {
        /* Decrement the nesting count as we are leaving a critical section. */
        ulCriticalNesting--;

        /* If the nesting level has reached zero then interrupts should be
         * re-enabled. */
        if( ulCriticalNesting == portNO_CRITICAL_NESTING )
        {
            portENABLE_INTERRUPTS();
        }
    }
}
```

**解说：** 这一段实现函数 `vPortExitCritical`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 21: 函数 prvDefaultHandler

```c
/*-----------------------------------------------------------*/
static void prvDefaultHandler( void )
{
}
```

**解说：** 这一段实现函数 `prvDefaultHandler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。
