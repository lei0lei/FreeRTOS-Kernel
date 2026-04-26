# port.c 代码解说

源文件：`portable/GCC/ARM_AARCH64_SRE/port.c`

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
/* Standard includes. */
#include <stdlib.h>

/* Scheduler includes. */
#include "FreeRTOS.h"
#include "task.h"

#ifndef configUNIQUE_INTERRUPT_PRIORITIES
    #error "configUNIQUE_INTERRUPT_PRIORITIES must be defined.  See www.FreeRTOS.org/Using-FreeRTOS-on-Cortex-A-Embedded-Processors.html"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 预处理配置

```c
#ifndef configSETUP_TICK_INTERRUPT
    #error "configSETUP_TICK_INTERRUPT() must be defined.  See www.FreeRTOS.org/Using-FreeRTOS-on-Cortex-A-Embedded-Processors.html"
#endif /* configSETUP_TICK_INTERRUPT */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 4: 预处理配置

```c
#ifndef configMAX_API_CALL_INTERRUPT_PRIORITY
    #error "configMAX_API_CALL_INTERRUPT_PRIORITY must be defined.  See www.FreeRTOS.org/Using-FreeRTOS-on-Cortex-A-Embedded-Processors.html"
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 5: 预处理配置

```c
#if configMAX_API_CALL_INTERRUPT_PRIORITY == 0
    #error "configMAX_API_CALL_INTERRUPT_PRIORITY must not be set to 0"
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 6: 预处理配置

```c
#if configMAX_API_CALL_INTERRUPT_PRIORITY > configUNIQUE_INTERRUPT_PRIORITIES
    #error "configMAX_API_CALL_INTERRUPT_PRIORITY must be less than or equal to configUNIQUE_INTERRUPT_PRIORITIES as the lower the numeric priority value the higher the logical interrupt priority"
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 7: 预处理配置

```c
#if configUSE_PORT_OPTIMISED_TASK_SELECTION == 1
    /* Check the configuration. */
    #if ( configMAX_PRIORITIES > 32 )
        #error "configUSE_PORT_OPTIMISED_TASK_SELECTION can only be set to 1 when configMAX_PRIORITIES is less than or equal to 32.  It is very rare that a system requires more than 10 to 15 difference priorities as tasks that share a priority will time slice."
    #endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 8: 预处理配置

```c
#endif /* configUSE_PORT_OPTIMISED_TASK_SELECTION */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 9: 预处理配置

```c
/* In case security extensions are implemented. */
#if configMAX_API_CALL_INTERRUPT_PRIORITY <= ( configUNIQUE_INTERRUPT_PRIORITIES / 2 )
    #error "configMAX_API_CALL_INTERRUPT_PRIORITY must be greater than ( configUNIQUE_INTERRUPT_PRIORITIES / 2 )"
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 10: 预处理配置 configCLEAR_TICK_INTERRUPT

```c
/* Some vendor specific files default configCLEAR_TICK_INTERRUPT() in
 * portmacro.h. */
#ifndef configCLEAR_TICK_INTERRUPT
    #define configCLEAR_TICK_INTERRUPT()
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 11: 宏 portNO_CRITICAL_NESTING

```c
/* A critical section is exited when the critical section nesting count reaches
 * this value. */
#define portNO_CRITICAL_NESTING          ( ( size_t ) 0 )

/* In all GICs 255 can be written to the priority mask register to unmask all
 * (but the lowest) interrupt priority. */
#define portUNMASK_VALUE                 ( 0xFFUL )

/* Tasks are not created with a floating point context, but can be given a
 * floating point context after they have been created.  A variable is stored as
 * part of the tasks context that holds portNO_FLOATING_POINT_CONTEXT if the task
 * does not have an FPU context, or any other value if the task does have an FPU
 * context. */
#define portNO_FLOATING_POINT_CONTEXT    ( ( StackType_t ) 0 )

/* Constants required to setup the initial task context. */
#define portSP_ELx                       ( ( StackType_t ) 0x01 )
#define portSP_EL0                       ( ( StackType_t ) 0x00 )

#if defined( GUEST )
    #define portEL1                      ( ( StackType_t ) 0x04 )
    #define portINITIAL_PSTATE           ( portEL1 | portSP_EL0 )
#else
    #define portEL3                      ( ( StackType_t ) 0x0c )
    /* At the time of writing, the BSP only supports EL3. */
    #define portINITIAL_PSTATE           ( portEL3 | portSP_EL0 )
#endif
```

**解说：** 这一段定义宏 `portNO_CRITICAL_NESTING`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 12: 宏 portAPSR_MODE_BITS_MASK

```c
/* Masks all bits in the APSR other than the mode bits. */
#define portAPSR_MODE_BITS_MASK    ( 0x0C )

/* The I bit in the DAIF bits. */
#define portDAIF_I                 ( 0x80 )

/* Macro to unmask all interrupt priorities. */
/* s3_0_c4_c6_0 is ICC_PMR_EL1. */
#define portCLEAR_INTERRUPT_MASK()                     \
    {                                                  \
        __asm volatile ( "MSR DAIFSET, #2        \n"   \
                         "DSB SY                 \n"   \
                         "ISB SY                 \n"   \
                         "MSR s3_0_c4_c6_0, %0   \n"   \
                         "DSB SY                 \n"   \
                         "ISB SY                 \n"   \
                         "MSR DAIFCLR, #2        \n"   \
                         "DSB SY                 \n"   \
                         "ISB SY                 \n"   \
                         ::"r" ( portUNMASK_VALUE ) ); \
    }
```

**解说：** 这一段定义宏 `portAPSR_MODE_BITS_MASK`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 13: 宏 vPortRestoreTaskContext

```c
/* The space on the stack required to hold the FPU registers.
 * There are 32 128-bit plus 2 64-bit status registers.*/
#define portFPU_REGISTER_WORDS     ( (32 * 2) + 2 )

/*-----------------------------------------------------------*/

/*
 * Starts the first task executing.  This function is necessarily written in
 * assembly code so is implemented in portASM.s.
 */
extern void vPortRestoreTaskContext( void );
```

**解说：** 这一段定义宏 `vPortRestoreTaskContext`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 14: 代码片段 14

```c
/*
 * If the application provides an implementation of vApplicationIRQHandler(),
 * then it will get called directly without saving the FPU registers on
 * interrupt entry, and this weak implementation of
 * vApplicationFPUSafeIRQHandler() is just provided to remove linkage errors -
 * it should never actually get called so its implementation contains a
 * call to configASSERT() that will always fail.
 *
 * If the application provides its own implementation of
 * vApplicationFPUSafeIRQHandler() then the implementation of
 * vApplicationIRQHandler() provided in portASM.S will save the FPU registers
 * before calling it.
 *
 * Therefore, if the application writer wants FPU registers to be saved on
 * interrupt entry their IRQ handler must be called
 * vApplicationFPUSafeIRQHandler(), and if the application writer does not want
 * FPU registers to be saved on interrupt entry their IRQ handler must be
 * called vApplicationIRQHandler().
 */
void vApplicationFPUSafeIRQHandler( uint32_t ulICCIAR ) __attribute__((weak) );
```

**解说：** 这一段执行断言检查，用来在调试阶段尽早发现无效参数、非法状态或配置错误。

## 片段 15: 代码片段 15

```c
/*-----------------------------------------------------------*/
/* A variable is used to keep track of the critical section nesting.  This
 * variable has to be stored as part of the task context and must be initialised to
 * a non zero value to ensure interrupts don't inadvertently become unmasked before
 * the scheduler starts.  As it is stored as part of the task context it will
 * automatically be set to 0 when the first task is started. */
volatile uint64_t ullCriticalNesting = 9999ULL;
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 16: 代码片段 16

```c
/* Saved as part of the task context.  If ullPortTaskHasFPUContext is non-zero
 * then floating point context must be saved and restored for the task. */
uint64_t ullPortTaskHasFPUContext = pdFALSE;
/* Set to 1 to pend a context switch from an ISR. */
uint64_t ullPortYieldRequired = pdFALSE;
/* Counts the interrupt nesting depth.  A context switch is only performed if
 * if the nesting depth is 0. */
uint64_t ullPortInterruptNesting = 0;
/* Used in the ASM code. */
__attribute__( ( used ) ) const uint64_t ullMaxAPIPriorityMask = ( configMAX_API_CALL_INTERRUPT_PRIORITY << portPRIORITY_SHIFT );
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 17: 函数 pxPortInitialiseStack

```c
/*-----------------------------------------------------------*/
/*
 * See header file for description.
 */
StackType_t * pxPortInitialiseStack( StackType_t * pxTopOfStack,
                                     TaskFunction_t pxCode,
                                     void * pvParameters )
{
    /* Setup the initial stack of the task.  The stack is set exactly as
     * expected by the portRESTORE_CONTEXT() macro. */

    /* First all the general purpose registers. */
    pxTopOfStack--;
    *pxTopOfStack = 0x0101010101010101ULL;        /* R1 */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) pvParameters; /* R0 */
    pxTopOfStack--;
    *pxTopOfStack = 0x0303030303030303ULL;        /* R3 */
    pxTopOfStack--;
    *pxTopOfStack = 0x0202020202020202ULL;        /* R2 */
    pxTopOfStack--;
    *pxTopOfStack = 0x0505050505050505ULL;        /* R5 */
    pxTopOfStack--;
    *pxTopOfStack = 0x0404040404040404ULL;        /* R4 */
    pxTopOfStack--;
    *pxTopOfStack = 0x0707070707070707ULL;        /* R7 */
    pxTopOfStack--;
    *pxTopOfStack = 0x0606060606060606ULL;        /* R6 */
    pxTopOfStack--;
    *pxTopOfStack = 0x0909090909090909ULL;        /* R9 */
    pxTopOfStack--;
    *pxTopOfStack = 0x0808080808080808ULL;        /* R8 */
    pxTopOfStack--;
    *pxTopOfStack = 0x1111111111111111ULL;        /* R11 */
    pxTopOfStack--;
    *pxTopOfStack = 0x1010101010101010ULL;        /* R10 */
    pxTopOfStack--;
    *pxTopOfStack = 0x1313131313131313ULL;        /* R13 */
    pxTopOfStack--;
    *pxTopOfStack = 0x1212121212121212ULL;        /* R12 */
    pxTopOfStack--;
    *pxTopOfStack = 0x1515151515151515ULL;        /* R15 */
    pxTopOfStack--;
    *pxTopOfStack = 0x1414141414141414ULL;        /* R14 */
    pxTopOfStack--;
    *pxTopOfStack = 0x1717171717171717ULL;        /* R17 */
    pxTopOfStack--;
    *pxTopOfStack = 0x1616161616161616ULL;        /* R16 */
    pxTopOfStack--;
    *pxTopOfStack = 0x1919191919191919ULL;        /* R19 */
    pxTopOfStack--;
    *pxTopOfStack = 0x1818181818181818ULL;        /* R18 */
    pxTopOfStack--;
    *pxTopOfStack = 0x2121212121212121ULL;        /* R21 */
    pxTopOfStack--;
    *pxTopOfStack = 0x2020202020202020ULL;        /* R20 */
    pxTopOfStack--;
    *pxTopOfStack = 0x2323232323232323ULL;        /* R23 */
    pxTopOfStack--;
    *pxTopOfStack = 0x2222222222222222ULL;        /* R22 */
    pxTopOfStack--;
    *pxTopOfStack = 0x2525252525252525ULL;        /* R25 */
    pxTopOfStack--;
    *pxTopOfStack = 0x2424242424242424ULL;        /* R24 */
    pxTopOfStack--;
    *pxTopOfStack = 0x2727272727272727ULL;        /* R27 */
    pxTopOfStack--;
    *pxTopOfStack = 0x2626262626262626ULL;        /* R26 */
    pxTopOfStack--;
    *pxTopOfStack = 0x2929292929292929ULL;        /* R29 */
    pxTopOfStack--;
    *pxTopOfStack = 0x2828282828282828ULL;        /* R28 */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x00;         /* XZR - has no effect, used so there are an even number of registers. */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x00;         /* R30 - procedure call link register. */

    pxTopOfStack--;
    *pxTopOfStack = portINITIAL_PSTATE;

    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) pxCode; /* Exception return address. */

    #if ( configUSE_TASK_FPU_SUPPORT == 1 )
    {
        /* The task will start with a critical nesting count of 0 as interrupts are
        * enabled. */
        pxTopOfStack--;
        *pxTopOfStack = portNO_CRITICAL_NESTING;

        /* The task will start without a floating point context.  A task that
        * uses the floating point hardware must call vPortTaskUsesFPU() before
        * executing any floating point instructions. */
        pxTopOfStack--;
        *pxTopOfStack = portNO_FLOATING_POINT_CONTEXT;
    }
    #elif ( configUSE_TASK_FPU_SUPPORT == 2 )
    {
        /* The task will start with a floating point context.  Leave enough
        * space for the registers - and ensure they are initialised to 0. */
        pxTopOfStack -= portFPU_REGISTER_WORDS;
        memset( pxTopOfStack, 0x00, portFPU_REGISTER_WORDS * sizeof( StackType_t ) );

        /* The task will start with a critical nesting count of 0 as interrupts are
        * enabled. */
        pxTopOfStack--;
        *pxTopOfStack = portNO_CRITICAL_NESTING;

        pxTopOfStack--;
        *pxTopOfStack = pdTRUE;
        ullPortTaskHasFPUContext = pdTRUE;
    }
    #else /* if ( configUSE_TASK_FPU_SUPPORT == 1 ) */
    {
        #error "Invalid configUSE_TASK_FPU_SUPPORT setting - configUSE_TASK_FPU_SUPPORT must be set to 1, 2, or left undefined."
    }
    #endif /* if ( configUSE_TASK_FPU_SUPPORT == 1 ) */

    return pxTopOfStack;
}
```

**解说：** 这一段实现函数 `pxPortInitialiseStack`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 18: 函数 xPortStartScheduler

```c
/*-----------------------------------------------------------*/
BaseType_t xPortStartScheduler( void )
{
    uint32_t ulAPSR;

    __asm volatile ( "MRS %0, CurrentEL" : "=r" ( ulAPSR ) );

    ulAPSR &= portAPSR_MODE_BITS_MASK;

    #if defined( GUEST )
        configASSERT( ulAPSR == portEL1 );

        if( ulAPSR == portEL1 )
    #else
        configASSERT( ulAPSR == portEL3 );

        if( ulAPSR == portEL3 )
    #endif
    {
        /* Interrupts are turned off in the CPU itself to ensure a tick does
         * not execute while the scheduler is being started.  Interrupts are
         * automatically turned back on in the CPU when the first task starts
         * executing. */
        portDISABLE_INTERRUPTS();

        /* Start the timer that generates the tick ISR. */
        configSETUP_TICK_INTERRUPT();

        /* Start the first task executing. */
        vPortRestoreTaskContext();
    }

    return 0;
}
```

**解说：** 这一段实现函数 `xPortStartScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 19: 函数 vPortEndScheduler

```c
/*-----------------------------------------------------------*/
void vPortEndScheduler( void )
{
    /* Not implemented in ports where there is nothing to return to.
     * Artificially force an assert. */
    configASSERT( ullCriticalNesting == 1000ULL );
}
```

**解说：** 这一段实现函数 `vPortEndScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 20: 函数 vPortEnterCritical

```c
/*-----------------------------------------------------------*/
void vPortEnterCritical( void )
{
    /* Mask interrupts up to the max syscall interrupt priority. */
    uxPortSetInterruptMask();

    /* Now interrupts are disabled ullCriticalNesting can be accessed
     * directly.  Increment ullCriticalNesting to keep a count of how many times
     * portENTER_CRITICAL() has been called. */
    ullCriticalNesting++;

    /* This is not the interrupt safe version of the enter critical function so
     * assert() if it is being called from an interrupt context.  Only API
     * functions that end in "FromISR" can be used in an interrupt.  Only assert if
     * the critical nesting count is 1 to protect against recursive calls if the
     * assert function also uses a critical section. */
    if( ullCriticalNesting == 1ULL )
    {
        configASSERT( ullPortInterruptNesting == 0 );
    }
}
```

**解说：** 这一段实现函数 `vPortEnterCritical`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 21: 函数 vPortExitCritical

```c
/*-----------------------------------------------------------*/
void vPortExitCritical( void )
{
    if( ullCriticalNesting > portNO_CRITICAL_NESTING )
    {
        /* Decrement the nesting count as the critical section is being
         * exited. */
        ullCriticalNesting--;

        /* If the nesting level has reached zero then all interrupt
         * priorities must be re-enabled. */
        if( ullCriticalNesting == portNO_CRITICAL_NESTING )
        {
            /* Critical nesting has reached zero so all interrupt priorities
             * should be unmasked. */
            portCLEAR_INTERRUPT_MASK();
        }
    }
}
```

**解说：** 这一段实现函数 `vPortExitCritical`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 22: 函数 FreeRTOS_Tick_Handler

```c
/*-----------------------------------------------------------*/
void FreeRTOS_Tick_Handler( void )
{
    /* Must be the lowest possible priority. */
    #if !defined( QEMU )
    {
        uint64_t ullRunningInterruptPriority;
        /* s3_0_c12_c11_3 is ICC_RPR_EL1. */
        __asm volatile ( "MRS %0, s3_0_c12_c11_3" : "=r" ( ullRunningInterruptPriority ) );
        configASSERT( ullRunningInterruptPriority == ( portLOWEST_USABLE_INTERRUPT_PRIORITY << portPRIORITY_SHIFT ) );
    }
    #endif

    /* Interrupts should not be enabled before this point. */
    #if ( configASSERT_DEFINED == 1 )
    {
        uint32_t ulMaskBits;

        __asm volatile ( "MRS %0, DAIF" : "=r" ( ulMaskBits )::"memory" );
        configASSERT( ( ulMaskBits & portDAIF_I ) != 0 );
    }
    #endif /* configASSERT_DEFINED */

    /* Set interrupt mask before altering scheduler structures.   The tick
     * handler runs at the lowest priority, so interrupts cannot already be masked,
     * so there is no need to save and restore the current mask value.  It is
     * necessary to turn off interrupts in the CPU itself while the ICCPMR is being
     * updated. */
    /* s3_0_c4_c6_0 is ICC_PMR_EL1. */
    __asm volatile ( "MSR s3_0_c4_c6_0, %0      \n"
                     "DSB SY                    \n"
                     "ISB SY                    \n"
                     ::"r" ( configMAX_API_CALL_INTERRUPT_PRIORITY << portPRIORITY_SHIFT ) : "memory" );

    /* Ok to enable interrupts after the interrupt source has been cleared. */
    configCLEAR_TICK_INTERRUPT();
    portENABLE_INTERRUPTS();

    /* Increment the RTOS tick. */
    if( xTaskIncrementTick() != pdFALSE )
    {
        ullPortYieldRequired = pdTRUE;
    }

    /* Ensure all interrupt priorities are active again. */
    portCLEAR_INTERRUPT_MASK();
}
```

**解说：** 这一段实现函数 `FreeRTOS_Tick_Handler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 23: 预处理配置 vPortTaskUsesFPU

```c
/*-----------------------------------------------------------*/
#if ( configUSE_TASK_FPU_SUPPORT != 2 )

void vPortTaskUsesFPU( void )
{
    /* A task is registering the fact that it needs an FPU context.  Set the
     * FPU flag (which is saved as part of the task context). */
    ullPortTaskHasFPUContext = pdTRUE;

    /* Consider initialising the FPSR here - but probably not necessary in
     * AArch64. */
}
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 24: 预处理配置

```c
#endif /* configUSE_TASK_FPU_SUPPORT */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 25: 函数 vPortClearInterruptMask

```c
/*-----------------------------------------------------------*/
void vPortClearInterruptMask( UBaseType_t uxNewMaskValue )
{
    if( uxNewMaskValue == pdFALSE )
    {
        portCLEAR_INTERRUPT_MASK();
    }
}
```

**解说：** 这一段实现函数 `vPortClearInterruptMask`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 26: 函数 uxPortSetInterruptMask

```c
/*-----------------------------------------------------------*/
UBaseType_t uxPortSetInterruptMask( void )
{
    uint32_t ulReturn;
    uint64_t ullPMRValue;

    /* Interrupt in the CPU must be turned off while the ICCPMR is being
     * updated. */
    portDISABLE_INTERRUPTS();
    /* s3_0_c4_c6_0 is ICC_PMR_EL1. */
    __asm volatile ( "MRS %0, s3_0_c4_c6_0" : "=r" ( ullPMRValue ) );

    if( ullPMRValue == ( configMAX_API_CALL_INTERRUPT_PRIORITY << portPRIORITY_SHIFT ) )
    {
        /* Interrupts were already masked. */
        ulReturn = pdTRUE;
    }
    else
    {
        ulReturn = pdFALSE;
        /* s3_0_c4_c6_0 is ICC_PMR_EL1. */
        __asm volatile ( "MSR s3_0_c4_c6_0, %0      \n"
                         "DSB SY                    \n"
                         "ISB SY                    \n"
                         ::"r" ( configMAX_API_CALL_INTERRUPT_PRIORITY << portPRIORITY_SHIFT ) : "memory" );
    }

    portENABLE_INTERRUPTS();

    return ulReturn;
}
```

**解说：** 这一段实现函数 `uxPortSetInterruptMask`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 27: 预处理配置 vPortValidateInterruptPriority

```c
/*-----------------------------------------------------------*/
#if ( configASSERT_DEFINED == 1 )

    void vPortValidateInterruptPriority( void )
    {
        /* The following assertion will fail if a service routine (ISR) for
         * an interrupt that has been assigned a priority above
         * configMAX_SYSCALL_INTERRUPT_PRIORITY calls an ISR safe FreeRTOS API
         * function.  ISR safe FreeRTOS API functions must *only* be called
         * from interrupts that have been assigned a priority at or below
         * configMAX_SYSCALL_INTERRUPT_PRIORITY.
         *
         * Numerically low interrupt priority numbers represent logically high
         * interrupt priorities, therefore the priority of the interrupt must
         * be set to a value equal to or numerically *higher* than
         * configMAX_SYSCALL_INTERRUPT_PRIORITY.
         *
         * FreeRTOS maintains separate thread and ISR API functions to ensure
         * interrupt entry is as fast and simple as possible. */
        uint64_t ullRunningInterruptPriority;
        /* s3_0_c12_c11_3 is ICC_RPR_EL1. */
        __asm volatile ( "MRS %0, s3_0_c12_c11_3" : "=r" ( ullRunningInterruptPriority ) );

        configASSERT( ullRunningInterruptPriority >= ( configMAX_API_CALL_INTERRUPT_PRIORITY << portPRIORITY_SHIFT ) );
    }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 28: 预处理配置

```c
#endif /* configASSERT_DEFINED */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 29: 函数 vApplicationFPUSafeIRQHandler

```c
/*-----------------------------------------------------------*/
void vApplicationFPUSafeIRQHandler( uint32_t ulICCIAR )
{
    ( void ) ulICCIAR;
    configASSERT( ( volatile void * ) NULL );
}
```

**解说：** 这一段实现函数 `vApplicationFPUSafeIRQHandler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。
