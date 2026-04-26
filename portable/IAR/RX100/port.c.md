# port.c 代码解说

源文件：`portable/IAR/RX100/port.c`

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

## 片段 2: 预处理配置 portINITIAL_PSW

```c
/*-----------------------------------------------------------
* Implementation of functions defined in portable.h for the SH2A port.
*----------------------------------------------------------*/
/* Standard C includes. */
#include "limits.h"

/* Scheduler includes. */
#include "FreeRTOS.h"
#include "task.h"

/* Library includes. */
#include "string.h"

/* Hardware specifics. */
#include "machine.h"

/*-----------------------------------------------------------*/

/* Tasks should start with interrupts enabled and in Supervisor mode, therefore
 * PSW is set with U and I set, and PM and IPL clear. */
#define portINITIAL_PSW    ( ( StackType_t ) 0x00030000 )

/* The peripheral clock is divided by this value before being supplying the
 * CMT. */
#if ( configUSE_TICKLESS_IDLE == 0 )
    /* If tickless idle is not used then the divisor can be fixed. */
    #define portCLOCK_DIVISOR    8UL
#elif ( configPERIPHERAL_CLOCK_HZ >= 12000000 )
    #define portCLOCK_DIVISOR    512UL
#elif ( configPERIPHERAL_CLOCK_HZ >= 6000000 )
    #define portCLOCK_DIVISOR    128UL
#elif ( configPERIPHERAL_CLOCK_HZ >= 1000000 )
    #define portCLOCK_DIVISOR    32UL
#else
    #define portCLOCK_DIVISOR    8UL
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 宏 prvStartFirstTask

```c
/* Keys required to lock and unlock access to certain system registers
 * respectively. */
#define portUNLOCK_KEY    0xA50B
#define portLOCK_KEY      0xA500

/*-----------------------------------------------------------*/

/*
 * Function to start the first task executing - written in asm code as direct
 * access to registers is required.
 */
extern void prvStartFirstTask( void );
```

**解说：** 这一段定义宏 `prvStartFirstTask`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 4: 代码片段 4

```c
/*
 * The tick ISR handler.  The peripheral used is configured by the application
 * via a hook/callback function.
 */
__interrupt static void prvTickISR( void );
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 5: 代码片段 5

```c
/*
 * Sets up the periodic ISR used for the RTOS tick using the CMT.
 * The application writer can define configSETUP_TICK_INTERRUPT() (in
 * FreeRTOSConfig.h) such that their own tick interrupt configuration is used
 * in place of prvSetupTimerInterrupt().
 */
static void prvSetupTimerInterrupt( void );
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 6: 预处理配置 configSETUP_TICK_INTERRUPT

```c
#ifndef configSETUP_TICK_INTERRUPT

/* The user has not provided their own tick interrupt configuration so use
 * the definition in this file (which uses the interval timer). */
    #define configSETUP_TICK_INTERRUPT()    prvSetupTimerInterrupt()
#endif /* configSETUP_TICK_INTERRUPT */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 7: 预处理配置 prvSleep

```c
/*
 * Called after the sleep mode registers have been configured, prvSleep()
 * executes the pre and post sleep macros, and actually calls the wait
 * instruction.
 */
#if configUSE_TICKLESS_IDLE == 1
    static void prvSleep( TickType_t xExpectedIdleTime );
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 8: 预处理配置

```c
#endif /* configUSE_TICKLESS_IDLE */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 9: 代码片段 9

```c
/*-----------------------------------------------------------*/
extern void * pxCurrentTCB;
/*-----------------------------------------------------------*/
/* Calculate how many clock increments make up a single tick period. */
static const uint32_t ulMatchValueForOneTick = ( ( configPERIPHERAL_CLOCK_HZ / portCLOCK_DIVISOR ) / configTICK_RATE_HZ );
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 10: 预处理配置

```c
#if configUSE_TICKLESS_IDLE == 1

/* Holds the maximum number of ticks that can be suppressed - which is
 * basically how far into the future an interrupt can be generated. Set
 * during initialisation.  This is the maximum possible value that the
 * compare match register can hold divided by ulMatchValueForOneTick. */
    static const TickType_t xMaximumPossibleSuppressedTicks = USHRT_MAX / ( ( configPERIPHERAL_CLOCK_HZ / portCLOCK_DIVISOR ) / configTICK_RATE_HZ );
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 11: 代码片段 11

```c
/* Flag set from the tick interrupt to allow the sleep processing to know if
 * sleep mode was exited because of a tick interrupt, or an interrupt
 * generated by something else. */
    static volatile uint32_t ulTickFlag = pdFALSE;
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 12: 代码片段 13

```c
/* The CMT counter is stopped temporarily each time it is re-programmed.
 * The following constant offsets the CMT counter match value by the number of
 * CMT counts that would typically be missed while the counter was stopped to
 * compensate for the lost time.  The large difference between the divided CMT
 * clock and the CPU clock means it is likely ulStoppedTimerCompensation will
 * equal zero - and be optimised away. */
    static const uint32_t ulStoppedTimerCompensation = 100UL / ( configCPU_CLOCK_HZ / ( configPERIPHERAL_CLOCK_HZ / portCLOCK_DIVISOR ) );
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 13: 预处理配置

```c
#endif /* if configUSE_TICKLESS_IDLE == 1 */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 14: 函数 pxPortInitialiseStack

```c
/*-----------------------------------------------------------*/
/*
 * See header file for description.
 */
StackType_t * pxPortInitialiseStack( StackType_t * pxTopOfStack,
                                     TaskFunction_t pxCode,
                                     void * pvParameters )
{
    /* Offset to end up on 8 byte boundary. */
    pxTopOfStack--;

    /* R0 is not included as it is the stack pointer. */
    *pxTopOfStack = 0x00;
    pxTopOfStack--;
    *pxTopOfStack = 0x00;
    pxTopOfStack--;
    *pxTopOfStack = portINITIAL_PSW;
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) pxCode;

    /* When debugging it can be useful if every register is set to a known
     * value.  Otherwise code space can be saved by just setting the registers
     * that need to be set. */
    #ifdef USE_FULL_REGISTER_INITIALISATION
    {
        pxTopOfStack--;
        *pxTopOfStack = 0x12345678; /* r15. */
        pxTopOfStack--;
        *pxTopOfStack = 0xaaaabbbb;
        pxTopOfStack--;
        *pxTopOfStack = 0xdddddddd;
        pxTopOfStack--;
        *pxTopOfStack = 0xcccccccc;
        pxTopOfStack--;
        *pxTopOfStack = 0xbbbbbbbb;
        pxTopOfStack--;
        *pxTopOfStack = 0xaaaaaaaa;
        pxTopOfStack--;
        *pxTopOfStack = 0x99999999;
        pxTopOfStack--;
        *pxTopOfStack = 0x88888888;
        pxTopOfStack--;
        *pxTopOfStack = 0x77777777;
        pxTopOfStack--;
        *pxTopOfStack = 0x66666666;
        pxTopOfStack--;
        *pxTopOfStack = 0x55555555;
        pxTopOfStack--;
        *pxTopOfStack = 0x44444444;
        pxTopOfStack--;
        *pxTopOfStack = 0x33333333;
        pxTopOfStack--;
        *pxTopOfStack = 0x22222222;
        pxTopOfStack--;
    }
    #else /* ifdef USE_FULL_REGISTER_INITIALISATION */
    {
        /* Leave space for the registers that will get popped from the stack
         * when the task first starts executing. */
        pxTopOfStack -= 15;
    }
    #endif /* ifdef USE_FULL_REGISTER_INITIALISATION */

    *pxTopOfStack = ( StackType_t ) pvParameters; /* R1 */
    pxTopOfStack--;
    *pxTopOfStack = 0x12345678;                   /* Accumulator. */
    pxTopOfStack--;
    *pxTopOfStack = 0x87654321;                   /* Accumulator. */

    return pxTopOfStack;
}
```

**解说：** 这一段实现函数 `pxPortInitialiseStack`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 15: 函数 xPortStartScheduler

```c
/*-----------------------------------------------------------*/
BaseType_t xPortStartScheduler( void )
{
    /* Use pxCurrentTCB just so it does not get optimised away. */
    if( pxCurrentTCB != NULL )
    {
        /* Call an application function to set up the timer that will generate
         * the tick interrupt.  This way the application can decide which
         * peripheral to use.  If tickless mode is used then the default
         * implementation defined in this file (which uses CMT0) should not be
         * overridden. */
        configSETUP_TICK_INTERRUPT();

        /* Enable the software interrupt. */
        _IEN( _ICU_SWINT ) = 1;

        /* Ensure the software interrupt is clear. */
        _IR( _ICU_SWINT ) = 0;

        /* Ensure the software interrupt is set to the kernel priority. */
        _IPR( _ICU_SWINT ) = configKERNEL_INTERRUPT_PRIORITY;

        /* Start the first task. */
        prvStartFirstTask();
    }

    /* Execution should not reach here as the tasks are now running!
     * prvSetupTimerInterrupt() is called here to prevent the compiler outputting
     * a warning about a statically declared function not being referenced in the
     * case that the application writer has provided their own tick interrupt
     * configuration routine (and defined configSETUP_TICK_INTERRUPT() such that
     * their own routine will be called in place of prvSetupTimerInterrupt()). */
    prvSetupTimerInterrupt();

    /* Should not get here. */
    return pdFAIL;
}
```

**解说：** 这一段实现函数 `xPortStartScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 16: 预处理配置 prvTickISR

```c
/*-----------------------------------------------------------*/
#pragma vector = configTICK_VECTOR
__interrupt static void prvTickISR( void )
{
    /* Re-enable interrupts. */
    __enable_interrupt();

    /* Increment the tick, and perform any processing the new tick value
     * necessitates. */
    __set_interrupt_level( configMAX_SYSCALL_INTERRUPT_PRIORITY );
    {
        if( xTaskIncrementTick() != pdFALSE )
        {
            taskYIELD();
        }
    }
    __set_interrupt_level( configKERNEL_INTERRUPT_PRIORITY );

    #if configUSE_TICKLESS_IDLE == 1
    {
        /* The CPU woke because of a tick. */
        ulTickFlag = pdTRUE;

        /* If this is the first tick since exiting tickless mode then the CMT
         * compare match value needs resetting. */
        CMT0.CMCOR = ( uint16_t ) ulMatchValueForOneTick;
    }
    #endif
}
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 17: 函数 vPortEndScheduler

```c
/*-----------------------------------------------------------*/
void vPortEndScheduler( void )
{
    /* Not implemented in ports where there is nothing to return to.
     * Artificially force an assert. */
    configASSERT( pxCurrentTCB == NULL );
}
```

**解说：** 这一段实现函数 `vPortEndScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 18: 函数 prvSetupTimerInterrupt

```c
/*-----------------------------------------------------------*/
static void prvSetupTimerInterrupt( void )
{
    /* Unlock. */
    SYSTEM.PRCR.WORD = portUNLOCK_KEY;

    /* Enable CMT0. */
    MSTP( CMT0 ) = 0;

    /* Lock again. */
    SYSTEM.PRCR.WORD = portLOCK_KEY;

    /* Interrupt on compare match. */
    CMT0.CMCR.BIT.CMIE = 1;

    /* Set the compare match value. */
    CMT0.CMCOR = ( uint16_t ) ulMatchValueForOneTick;

    /* Divide the PCLK. */
    #if portCLOCK_DIVISOR == 512
    {
        CMT0.CMCR.BIT.CKS = 3;
    }
    #elif portCLOCK_DIVISOR == 128
    {
        CMT0.CMCR.BIT.CKS = 2;
    }
    #elif portCLOCK_DIVISOR == 32
    {
        CMT0.CMCR.BIT.CKS = 1;
    }
    #elif portCLOCK_DIVISOR == 8
    {
        CMT0.CMCR.BIT.CKS = 0;
    }
    #else /* if portCLOCK_DIVISOR == 512 */
    {
        #error Invalid portCLOCK_DIVISOR setting
    }
    #endif /* if portCLOCK_DIVISOR == 512 */


    /* Enable the interrupt... */
    _IEN( _CMT0_CMI0 ) = 1;

    /* ...and set its priority to the application defined kernel priority. */
    _IPR( _CMT0_CMI0 ) = configKERNEL_INTERRUPT_PRIORITY;

    /* Start the timer. */
    CMT.CMSTR0.BIT.STR0 = 1;
}
```

**解说：** 这一段实现函数 `prvSetupTimerInterrupt`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 19: 预处理配置 prvSleep

```c
/*-----------------------------------------------------------*/
#if configUSE_TICKLESS_IDLE == 1

    static void prvSleep( TickType_t xExpectedIdleTime )
    {
        /* Allow the application to define some pre-sleep processing. */
        configPRE_SLEEP_PROCESSING( xExpectedIdleTime );

        /* xExpectedIdleTime being set to 0 by configPRE_SLEEP_PROCESSING()
         * means the application defined code has already executed the WAIT
         * instruction. */
        if( xExpectedIdleTime > 0 )
        {
            __wait_for_interrupt();
        }

        /* Allow the application to define some post sleep processing. */
        configPOST_SLEEP_PROCESSING( xExpectedIdleTime );
    }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 20: 预处理配置

```c
#endif /* configUSE_TICKLESS_IDLE */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 21: 预处理配置 vPortSuppressTicksAndSleep

```c
/*-----------------------------------------------------------*/
#if configUSE_TICKLESS_IDLE == 1

    void vPortSuppressTicksAndSleep( TickType_t xExpectedIdleTime )
    {
        uint32_t ulMatchValue, ulCompleteTickPeriods, ulCurrentCount;
        eSleepModeStatus eSleepAction;

        /* THIS FUNCTION IS CALLED WITH THE SCHEDULER SUSPENDED. */

        /* Make sure the CMT reload value does not overflow the counter. */
        if( xExpectedIdleTime > xMaximumPossibleSuppressedTicks )
        {
            xExpectedIdleTime = xMaximumPossibleSuppressedTicks;
        }

        /* Calculate the reload value required to wait xExpectedIdleTime tick
         * periods. */
        ulMatchValue = ulMatchValueForOneTick * xExpectedIdleTime;

        if( ulMatchValue > ulStoppedTimerCompensation )
        {
            /* Compensate for the fact that the CMT is going to be stopped
             * momentarily. */
            ulMatchValue -= ulStoppedTimerCompensation;
        }

        /* Stop the CMT momentarily.  The time the CMT is stopped for is
         * accounted for as best it can be, but using the tickless mode will
         * inevitably result in some tiny drift of the time maintained by the
         * kernel with respect to calendar time. */
        CMT.CMSTR0.BIT.STR0 = 0;

        while( CMT.CMSTR0.BIT.STR0 == 1 )
        {
            /* Nothing to do here. */
        }

        /* Critical section using the global interrupt bit as the i bit is
         * automatically reset by the WAIT instruction. */
        __disable_interrupt();

        /* The tick flag is set to false before sleeping.  If it is true when
         * sleep mode is exited then sleep mode was probably exited because the
         * tick was suppressed for the entire xExpectedIdleTime period. */
        ulTickFlag = pdFALSE;

        /* If a context switch is pending then abandon the low power entry as
         * the context switch might have been pended by an external interrupt that
         * requires processing. */
        eSleepAction = eTaskConfirmSleepModeStatus();

        if( eSleepAction == eAbortSleep )
        {
            /* Restart tick. */
            CMT.CMSTR0.BIT.STR0 = 1;
            __enable_interrupt();
        }
        else if( eSleepAction == eNoTasksWaitingTimeout )
        {
            /* Protection off. */
            SYSTEM.PRCR.WORD = portUNLOCK_KEY;

            /* Ready for software standby with all clocks stopped. */
            SYSTEM.SBYCR.BIT.SSBY = 1;

            /* Protection on. */
            SYSTEM.PRCR.WORD = portLOCK_KEY;

            /* Sleep until something happens.  Calling prvSleep() will
             * automatically reset the i bit in the PSW. */
            prvSleep( xExpectedIdleTime );

            /* Restart the CMT. */
            CMT.CMSTR0.BIT.STR0 = 1;
        }
        else
        {
            /* Protection off. */
            SYSTEM.PRCR.WORD = portUNLOCK_KEY;

            /* Ready for deep sleep mode. */
            SYSTEM.MSTPCRC.BIT.DSLPE = 1;
            SYSTEM.MSTPCRA.BIT.MSTPA28 = 1;
            SYSTEM.SBYCR.BIT.SSBY = 0;

            /* Protection on. */
            SYSTEM.PRCR.WORD = portLOCK_KEY;

            /* Adjust the match value to take into account that the current
             * time slice is already partially complete. */
            ulMatchValue -= ( uint32_t ) CMT0.CMCNT;
            CMT0.CMCOR = ( uint16_t ) ulMatchValue;

            /* Restart the CMT to count up to the new match value. */
            CMT0.CMCNT = 0;
            CMT.CMSTR0.BIT.STR0 = 1;

            /* Sleep until something happens.  Calling prvSleep() will
             * automatically reset the i bit in the PSW. */
            prvSleep( xExpectedIdleTime );

            /* Stop CMT.  Again, the time the SysTick is stopped for is
             * accounted for as best it can be, but using the tickless mode will
             * inevitably result in some tiny drift of the time maintained by the
             * kernel with respect to calendar time. */
            CMT.CMSTR0.BIT.STR0 = 0;

            while( CMT.CMSTR0.BIT.STR0 == 1 )
            {
                /* Nothing to do here. */
            }

            ulCurrentCount = ( uint32_t ) CMT0.CMCNT;

            if( ulTickFlag != pdFALSE )
            {
                /* The tick interrupt has already executed, although because
                 * this function is called with the scheduler suspended the actual
                 * tick processing will not occur until after this function has
                 * exited.  Reset the match value with whatever remains of this
                 * tick period. */
                ulMatchValue = ulMatchValueForOneTick - ulCurrentCount;
                CMT0.CMCOR = ( uint16_t ) ulMatchValue;

                /* The tick interrupt handler will already have pended the tick
                 * processing in the kernel.  As the pending tick will be
                 * processed as soon as this function exits, the tick value
                 * maintained by the tick is stepped forward by one less than the
                 * time spent sleeping.  The actual stepping of the tick appears
                 * later in this function. */
                ulCompleteTickPeriods = xExpectedIdleTime - 1UL;
            }
            else
            {
                /* Something other than the tick interrupt ended the sleep.
                 * How many complete tick periods passed while the processor was
                 * sleeping? */
                ulCompleteTickPeriods = ulCurrentCount / ulMatchValueForOneTick;

                /* The match value is set to whatever fraction of a single tick
                 * period remains. */
                ulMatchValue = ulCurrentCount - ( ulCompleteTickPeriods * ulMatchValueForOneTick );
                CMT0.CMCOR = ( uint16_t ) ulMatchValue;
            }

            /* Restart the CMT so it runs up to the match value.  The match value
             * will get set to the value required to generate exactly one tick period
             * the next time the CMT interrupt executes. */
            CMT0.CMCNT = 0;
            CMT.CMSTR0.BIT.STR0 = 1;

            /* Wind the tick forward by the number of tick periods that the CPU
             * remained in a low power state. */
            vTaskStepTick( ulCompleteTickPeriods );
        }
    }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 22: 预处理配置

```c
#endif /* configUSE_TICKLESS_IDLE */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。
