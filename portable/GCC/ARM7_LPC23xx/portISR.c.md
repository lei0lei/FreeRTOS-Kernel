# portISR.c 代码解说

源文件：`portable/GCC/ARM7_LPC23xx/portISR.c`

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

## 片段 2: 预处理配置 portTIMER_MATCH_ISR_BIT

```c
/*-----------------------------------------------------------
* Components that can be compiled to either ARM or THUMB mode are
* contained in port.c  The ISR routines, which can only be compiled
* to ARM mode, are contained in this file.
*----------------------------------------------------------*/
/* Scheduler includes. */
#include "FreeRTOS.h"
#include "task.h"

/* Constants required to handle interrupts. */
#define portTIMER_MATCH_ISR_BIT    ( ( uint8_t ) 0x01 )
#define portCLEAR_VIC_INTERRUPT    ( ( uint32_t ) 0 )

/* Constants required to handle critical sections. */
#define portNO_CRITICAL_NESTING    ( ( uint32_t ) 0 )
volatile uint32_t ulCriticalNesting = 9999UL;
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 代码片段 3

```c
/*-----------------------------------------------------------*/
/* ISR to handle manual context switches (from a call to taskYIELD()). */
void vPortYieldProcessor( void ) __attribute__( ( interrupt( "SWI" ), naked ) );
/*
 * The scheduler can only be started from ARM mode, hence the inclusion of this
 * function here.
 */
void vPortISRStartFirstTask( void );
```

**解说：** 这一段是 `portISR.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 函数 vPortISRStartFirstTask

```c
/*-----------------------------------------------------------*/
void vPortISRStartFirstTask( void )
{
    /* Simply start the scheduler.  This is included here as it can only be
     * called from ARM mode. */
    portRESTORE_CONTEXT();
}
```

**解说：** 这一段实现函数 `vPortISRStartFirstTask`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 5: 函数 vPortYieldProcessor

```c
/*-----------------------------------------------------------*/
/*
 * Called by portYIELD() or taskYIELD() to manually force a context switch.
 *
 * When a context switch is performed from the task level the saved task
 * context is made to look as if it occurred from within the tick ISR.  This
 * way the same restore context function can be used when restoring the context
 * saved from the ISR or that saved from a call to vPortYieldProcessor.
 */
void vPortYieldProcessor( void )
{
    /* Within an IRQ ISR the link register has an offset from the true return
     * address, but an SWI ISR does not.  Add the offset manually so the same
     * ISR return code can be used in both cases. */
    __asm volatile ( "ADD       LR, LR, #4" );

    /* Perform the context switch.  First save the context of the current task. */
    portSAVE_CONTEXT();

    /* Find the highest priority task that is ready to run. */
    __asm volatile ( "bl         vTaskSwitchContext" );

    /* Restore the context of the new task. */
    portRESTORE_CONTEXT();
}
```

**解说：** 这一段实现函数 `vPortYieldProcessor`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 6: 预处理配置 vNonPreemptiveTick

```c
/*-----------------------------------------------------------*/
/*
 * The ISR used for the scheduler tick depends on whether the cooperative or
 * the preemptive scheduler is being used.
 */
#if configUSE_PREEMPTION == 0

/* The cooperative scheduler requires a normal IRQ service routine to
 * simply increment the system tick. */
    void vNonPreemptiveTick( void ) __attribute__( ( interrupt( "IRQ" ) ) );
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 7: 函数 vNonPreemptiveTick

```c
    void vNonPreemptiveTick( void )
    {
        xTaskIncrementTick();
        T0IR = 2;
        VICVectAddr = portCLEAR_VIC_INTERRUPT;
    }
```

**解说：** 这一段实现函数 `vNonPreemptiveTick`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 8: 预处理配置 vPreemptiveTick

```c
#else /* if configUSE_PREEMPTION == 0 */

/* The preemptive scheduler is defined as "naked" as the full context is
 * saved on entry as part of the context switch. */
    void vPreemptiveTick( void ) __attribute__( ( naked ) );
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 9: 函数 vPreemptiveTick

```c
    void vPreemptiveTick( void )
    {
        /* Save the context of the interrupted task. */
        portSAVE_CONTEXT();

        /* Increment the RTOS tick count, then look for the highest priority
         * task that is ready to run. */
        __asm volatile
        (
            "   bl xTaskIncrementTick   \t\n" \
            "   cmp r0, #0              \t\n" \
            "   beq SkipContextSwitch   \t\n" \
            "   bl vTaskSwitchContext   \t\n" \
            "SkipContextSwitch:         \t\n"
        );

        /* Ready for the next interrupt. */
        T0IR = 2;
        VICVectAddr = portCLEAR_VIC_INTERRUPT;

        /* Restore the context of the new task. */
        portRESTORE_CONTEXT();
    }
```

**解说：** 这一段实现函数 `vPreemptiveTick`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 10: 预处理配置

```c
#endif /* if configUSE_PREEMPTION == 0 */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 11: 预处理配置 vPortDisableInterruptsFromThumb

```c
/*-----------------------------------------------------------*/
/*
 * The interrupt management utilities can only be called from ARM mode.  When
 * THUMB_INTERWORK is defined the utilities are defined as functions here to
 * ensure a switch to ARM mode.  When THUMB_INTERWORK is not defined then
 * the utilities are defined as macros in portmacro.h - as per other ports.
 */
#ifdef THUMB_INTERWORK

    void vPortDisableInterruptsFromThumb( void ) __attribute__( ( naked ) );
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 12: 代码片段 12

```c
    void vPortEnableInterruptsFromThumb( void ) __attribute__( ( naked ) );
```

**解说：** 这一段是 `portISR.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 13: 函数 vPortDisableInterruptsFromThumb

```c
    void vPortDisableInterruptsFromThumb( void )
    {
        __asm volatile (
            "STMDB  SP!, {R0}       \n\t" /* Push R0.                                 */
            "MRS    R0, CPSR        \n\t" /* Get CPSR.                                */
            "ORR    R0, R0, #0xC0   \n\t" /* Disable IRQ, FIQ.                        */
            "MSR    CPSR, R0        \n\t" /* Write back modified value.               */
            "LDMIA  SP!, {R0}       \n\t" /* Pop R0.                                  */
            "BX     R14" );               /* Return back to thumb.                    */
    }
```

**解说：** 这一段实现函数 `vPortDisableInterruptsFromThumb`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 14: 函数 vPortEnableInterruptsFromThumb

```c
    void vPortEnableInterruptsFromThumb( void )
    {
        __asm volatile (
            "STMDB  SP!, {R0}       \n\t" /* Push R0.                                 */
            "MRS    R0, CPSR        \n\t" /* Get CPSR.                                */
            "BIC    R0, R0, #0xC0   \n\t" /* Enable IRQ, FIQ.                         */
            "MSR    CPSR, R0        \n\t" /* Write back modified value.               */
            "LDMIA  SP!, {R0}       \n\t" /* Pop R0.                                  */
            "BX     R14" );               /* Return back to thumb.                    */
    }
```

**解说：** 这一段实现函数 `vPortEnableInterruptsFromThumb`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 15: 预处理配置

```c
#endif /* THUMB_INTERWORK */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 16: 函数 vPortEnterCritical

```c
/* The code generated by the GCC compiler uses the stack in different ways at
 * different optimisation levels.  The interrupt flags can therefore not always
 * be saved to the stack.  Instead the critical section nesting level is stored
 * in a variable, which is then saved as part of the stack context. */
void vPortEnterCritical( void )
{
    /* Disable interrupts as per portDISABLE_INTERRUPTS();                          */
    __asm volatile (
        "STMDB  SP!, {R0}           \n\t" /* Push R0.                             */
        "MRS    R0, CPSR            \n\t" /* Get CPSR.                            */
        "ORR    R0, R0, #0xC0       \n\t" /* Disable IRQ, FIQ.                    */
        "MSR    CPSR, R0            \n\t" /* Write back modified value.           */
        "LDMIA  SP!, {R0}" );             /* Pop R0.                              */

    /* Now that interrupts are disabled, ulCriticalNesting can be accessed
     * directly.  Increment ulCriticalNesting to keep a count of how many times
     * portENTER_CRITICAL() has been called. */
    ulCriticalNesting++;
}
```

**解说：** 这一段实现函数 `vPortEnterCritical`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 17: 函数 vPortExitCritical

```c
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
            /* Enable interrupts as per portEXIT_CRITICAL().                    */
            __asm volatile (
                "STMDB  SP!, {R0}       \n\t" /* Push R0.                     */
                "MRS    R0, CPSR        \n\t" /* Get CPSR.                    */
                "BIC    R0, R0, #0xC0   \n\t" /* Enable IRQ, FIQ.             */
                "MSR    CPSR, R0        \n\t" /* Write back modified value.   */
                "LDMIA  SP!, {R0}" );         /* Pop R0.                      */
        }
    }
}
```

**解说：** 这一段实现函数 `vPortExitCritical`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。
