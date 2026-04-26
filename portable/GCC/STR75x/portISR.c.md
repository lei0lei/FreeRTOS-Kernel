# portISR.c 代码解说

源文件：`portable/GCC/STR75x/portISR.c`

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

## 片段 2: 预处理配置 portNO_CRITICAL_NESTING

```c
/*-----------------------------------------------------------
* Components that can be compiled to either ARM or THUMB mode are
* contained in port.c  The ISR routines, which can only be compiled
* to ARM mode, are contained in this file.
*----------------------------------------------------------*/
/*
 */
/* Scheduler includes. */
#include "FreeRTOS.h"
#include "task.h"

/* Constants required to handle critical sections. */
#define portNO_CRITICAL_NESTING    ( ( uint32_t ) 0 )

volatile uint32_t ulCriticalNesting = 9999UL;
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 代码片段 3

```c
/*-----------------------------------------------------------*/
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
    asm volatile (                                                        \
        "LDR        R0, =pxCurrentTCB                               \n\t" \
        "LDR        R0, [R0]                                        \n\t" \
        "LDR        LR, [R0]                                        \n\t" \
                                                                          \
        /* The critical nesting depth is the first item on the stack. */  \
        /* Load it into the ulCriticalNesting variable. */                \
        "LDR        R0, =ulCriticalNesting                          \n\t" \
        "LDMFD  LR!, {R1}                                           \n\t" \
        "STR        R1, [R0]                                        \n\t" \
                                                                          \
        /* Get the SPSR from the stack. */                                \
        "LDMFD  LR!, {R0}                                           \n\t" \
        "MSR        SPSR, R0                                        \n\t" \
                                                                          \
        /* Restore all system mode registers for the task. */             \
        "LDMFD  LR, {R0-R14}^                                       \n\t" \
        "NOP                                                        \n\t" \
                                                                          \
        /* Restore the return address. */                                 \
        "LDR        LR, [LR, #+60]                                  \n\t" \
                                                                          \
        /* And return - correcting the offset in the LR to obtain the */  \
        /* correct address. */                                            \
        "SUBS PC, LR, #4                                            \n\t" \
        );
}
```

**解说：** 这一段实现函数 `vPortISRStartFirstTask`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 5: 函数 vPortTickISR

```c
/*-----------------------------------------------------------*/
void vPortTickISR( void )
{
    /* Increment the RTOS tick count, then look for the highest priority
     * task that is ready to run. */
    if( xTaskIncrementTick() != pdFALSE )
    {
        vTaskSwitchContext();
    }

    /* Ready for the next interrupt. */
    TB_ClearITPendingBit( TB_IT_Update );
}
```

**解说：** 这一段实现函数 `vPortTickISR`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 6: 预处理配置 vPortDisableInterruptsFromThumb

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

## 片段 7: 代码片段 7

```c
    void vPortEnableInterruptsFromThumb( void ) __attribute__( ( naked ) );
```

**解说：** 这一段是 `portISR.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 8: 函数 vPortDisableInterruptsFromThumb

```c
    void vPortDisableInterruptsFromThumb( void )
    {
        asm volatile (
            "STMDB  SP!, {R0}       \n\t" /* Push R0.                                 */
            "MRS    R0, CPSR        \n\t" /* Get CPSR.                                */
            "ORR    R0, R0, #0xC0   \n\t" /* Disable IRQ, FIQ.                        */
            "MSR    CPSR, R0        \n\t" /* Write back modified value.               */
            "LDMIA  SP!, {R0}       \n\t" /* Pop R0.                                  */
            "BX     R14" );               /* Return back to thumb.                    */
    }
```

**解说：** 这一段实现函数 `vPortDisableInterruptsFromThumb`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 9: 函数 vPortEnableInterruptsFromThumb

```c
    void vPortEnableInterruptsFromThumb( void )
    {
        asm volatile (
            "STMDB  SP!, {R0}       \n\t" /* Push R0.                                 */
            "MRS    R0, CPSR        \n\t" /* Get CPSR.                                */
            "BIC    R0, R0, #0xC0   \n\t" /* Enable IRQ, FIQ.                         */
            "MSR    CPSR, R0        \n\t" /* Write back modified value.               */
            "LDMIA  SP!, {R0}       \n\t" /* Pop R0.                                  */
            "BX     R14" );               /* Return back to thumb.                    */
    }
```

**解说：** 这一段实现函数 `vPortEnableInterruptsFromThumb`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 10: 预处理配置

```c
#endif /* THUMB_INTERWORK */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 11: 函数 vPortEnterCritical

```c
/*-----------------------------------------------------------*/
void vPortEnterCritical( void )
{
    /* Disable interrupts as per portDISABLE_INTERRUPTS();                          */
    asm volatile (
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
            /* Enable interrupts as per portEXIT_CRITICAL().                    */
            asm volatile (
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
