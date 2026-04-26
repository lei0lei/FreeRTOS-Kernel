# port.c 代码解说

源文件：`portable/CCS/ARM_Cortex-R4/port.c`

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
/* FreeRTOS includes. */
#include "FreeRTOS.h"
#include "task.h"

/*-----------------------------------------------------------*/

/* Count of the critical section nesting depth. */
uint32_t ulCriticalNesting = 9999;
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 宏 vPortStartFirstTask

```c
/*-----------------------------------------------------------*/
/* Registers required to configure the RTI. */
#define portRTI_GCTRL_REG       ( * ( ( volatile uint32_t * ) 0xFFFFFC00 ) )
#define portRTI_TBCTRL_REG      ( * ( ( volatile uint32_t * ) 0xFFFFFC04 ) )
#define portRTI_COMPCTRL_REG    ( * ( ( volatile uint32_t * ) 0xFFFFFC0C ) )
#define portRTI_CNT0_FRC0_REG   ( * ( ( volatile uint32_t * ) 0xFFFFFC10 ) )
#define portRTI_CNT0_UC0_REG    ( * ( ( volatile uint32_t * ) 0xFFFFFC14 ) )
#define portRTI_CNT0_CPUC0_REG  ( * ( ( volatile uint32_t * ) 0xFFFFFC18 ) )
#define portRTI_CNT0_COMP0_REG  ( * ( ( volatile uint32_t * ) 0xFFFFFC50 ) )
#define portRTI_CNT0_UDCP0_REG  ( * ( ( volatile uint32_t * ) 0xFFFFFC54 ) )
#define portRTI_SETINTENA_REG   ( * ( ( volatile uint32_t * ) 0xFFFFFC80 ) )
#define portRTI_CLEARINTENA_REG ( * ( ( volatile uint32_t * ) 0xFFFFFC84 ) )
#define portRTI_INTFLAG_REG     ( * ( ( volatile uint32_t * ) 0xFFFFFC88 ) )


/* Constants required to set up the initial stack of each task. */
#define portINITIAL_SPSR        ( ( StackType_t ) 0x1F )
#define portINITIAL_FPSCR       ( ( StackType_t ) 0x00 )
#define portINSTRUCTION_SIZE    ( ( StackType_t ) 0x04 )
#define portTHUMB_MODE_BIT      ( ( StackType_t ) 0x20 )

/* The number of words on the stack frame between the saved Top Of Stack and
R0 (in which the parameters are passed. */
#define portSPACE_BETWEEN_TOS_AND_PARAMETERS    ( 12 )

/*-----------------------------------------------------------*/

/* vPortStartFirstSTask() is defined in portASM.asm */
extern void vPortStartFirstTask( void );
```

**解说：** 这一段定义宏 `vPortStartFirstTask`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 4: 代码片段 4

```c
/*-----------------------------------------------------------*/
/* Saved as part of the task context.  Set to pdFALSE if the task does not
require an FPU context. */
uint32_t ulTaskHasFPUContext = 0;
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 5: 函数实现

```c
/*-----------------------------------------------------------*/
/*
 * See header file for description.
 */
StackType_t *pxPortInitialiseStack( StackType_t *pxTopOfStack, TaskFunction_t pxCode, void *pvParameters )
{
StackType_t *pxOriginalTOS;

    pxOriginalTOS = pxTopOfStack;

    #if __TI_VFP_SUPPORT__
    {
        /* Ensure the stack is correctly aligned on exit. */
        pxTopOfStack--;
    }
    #endif

    /* Setup the initial stack of the task.  The stack is set exactly as
    expected by the portRESTORE_CONTEXT() macro. */

    /* First on the stack is the return address - which is the start of the as
    the task has not executed yet.  The offset is added to make the return
    address appear as it would within an IRQ ISR. */
    *pxTopOfStack = ( StackType_t ) pxCode + portINSTRUCTION_SIZE;
    pxTopOfStack--;

    *pxTopOfStack = ( StackType_t ) 0x00000000; /* R14 */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) pxOriginalTOS; /* Stack used when task starts goes in R13. */
    pxTopOfStack--;

    #ifdef portPRELOAD_TASK_REGISTERS
    {
        *pxTopOfStack = ( StackType_t ) 0x12121212; /* R12 */
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) 0x11111111; /* R11 */
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) 0x10101010; /* R10 */
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) 0x09090909; /* R9 */
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) 0x08080808; /* R8 */
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) 0x07070707; /* R7 */
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) 0x06060606; /* R6 */
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) 0x05050505; /* R5 */
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) 0x04040404; /* R4 */
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) 0x03030303; /* R3 */
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) 0x02020202; /* R2 */
        pxTopOfStack--;
        *pxTopOfStack = ( StackType_t ) 0x01010101; /* R1 */
        pxTopOfStack--;
    }
    #else
    {
        pxTopOfStack -= portSPACE_BETWEEN_TOS_AND_PARAMETERS;
    }
    #endif

    /* Function parameters are passed in R0. */
    *pxTopOfStack = ( StackType_t ) pvParameters; /* R0 */
    pxTopOfStack--;

    /* Set the status register for system mode, with interrupts enabled. */
    *pxTopOfStack = ( StackType_t ) ( ( _get_CPSR() & ~0xFF ) | portINITIAL_SPSR );

    if( ( ( uint32_t ) pxCode & 0x01UL ) != 0x00 )
    {
        /* The task will start in thumb mode. */
        *pxTopOfStack |= portTHUMB_MODE_BIT;
    }

    #ifdef __TI_VFP_SUPPORT__
    {
        pxTopOfStack--;

        /* The last thing on the stack is the tasks ulUsingFPU value, which by
        default is set to indicate that the stack frame does not include FPU
        registers. */
        *pxTopOfStack = pdFALSE;
    }
    #endif

    return pxTopOfStack;
}
```

**解说：** 这一段实现一个函数，把一组相关步骤封装成独立的执行单元。

## 片段 6: 函数 prvSetupTimerInterrupt

```c
/*-----------------------------------------------------------*/
static void prvSetupTimerInterrupt(void)
{
    /* Disable timer 0. */
    portRTI_GCTRL_REG &= 0xFFFFFFFEUL;

    /* Use the internal counter. */
    portRTI_TBCTRL_REG = 0x00000000U;

    /* COMPSEL0 will use the RTIFRC0 counter. */
    portRTI_COMPCTRL_REG = 0x00000000U;

    /* Initialise the counter and the prescale counter registers. */
    portRTI_CNT0_UC0_REG =  0x00000000U;
    portRTI_CNT0_FRC0_REG =  0x00000000U;

    /* Set Prescalar for RTI clock. */
    portRTI_CNT0_CPUC0_REG = 0x00000001U;
    portRTI_CNT0_COMP0_REG = ( configCPU_CLOCK_HZ / 2 ) / configTICK_RATE_HZ;
    portRTI_CNT0_UDCP0_REG = ( configCPU_CLOCK_HZ / 2 ) / configTICK_RATE_HZ;

    /* Clear interrupts. */
    portRTI_INTFLAG_REG =  0x0007000FU;
    portRTI_CLEARINTENA_REG = 0x00070F0FU;

    /* Enable the compare 0 interrupt. */
    portRTI_SETINTENA_REG = 0x00000001U;
    portRTI_GCTRL_REG |= 0x00000001U;
}
```

**解说：** 这一段实现函数 `prvSetupTimerInterrupt`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 7: 函数 xPortStartScheduler

```c
/*-----------------------------------------------------------*/
/*
 * See header file for description.
 */
BaseType_t xPortStartScheduler(void)
{
    /* Start the timer that generates the tick ISR. */
    prvSetupTimerInterrupt();

    /* Reset the critical section nesting count read to execute the first task. */
    ulCriticalNesting = 0;

    /* Start the first task.  This is done from portASM.asm as ARM mode must be
    used. */
    vPortStartFirstTask();

    /* Should not get here! */
    return pdFAIL;
}
```

**解说：** 这一段实现函数 `xPortStartScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 8: 函数 vPortEndScheduler

```c
/*-----------------------------------------------------------*/
/*
 * See header file for description.
 */
void vPortEndScheduler(void)
{
    /* Not implemented in ports where there is nothing to return to.
    Artificially force an assert. */
    configASSERT( ulCriticalNesting == 1000UL );
}
```

**解说：** 这一段实现函数 `vPortEndScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 9: 预处理配置 vPortNonPreemptiveTick

```c
/*-----------------------------------------------------------*/
#if configUSE_PREEMPTION == 0

    /* The cooperative scheduler requires a normal IRQ service routine to
     * simply increment the system tick. */
    __interrupt void vPortNonPreemptiveTick( void )
    {
        /* clear clock interrupt flag */
        portRTI_INTFLAG_REG = 0x00000001;

        /* Increment the tick count - this may make a delaying task ready
        to run - but a context switch is not performed. */
        xTaskIncrementTick();
    }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 10: 预处理配置 vPortPreemptiveTick

```c
 #else

    /*
     **************************************************************************
     * The preemptive scheduler ISR is written in assembler and can be found
     * in the portASM.asm file. This will only get used if portUSE_PREEMPTION
     * is set to 1 in portmacro.h
     **************************************************************************
     */
    void vPortPreemptiveTick( void );
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 11: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 12: 函数 vPortEnterCritical

```c
/*-----------------------------------------------------------*/
/*
 * Disable interrupts, and keep a count of the nesting depth.
 */
void vPortEnterCritical( void )
{
    /* Disable interrupts as per portDISABLE_INTERRUPTS(); */
    portDISABLE_INTERRUPTS();

    /* Now interrupts are disabled ulCriticalNesting can be accessed
    directly.  Increment ulCriticalNesting to keep a count of how many times
    portENTER_CRITICAL() has been called. */
    ulCriticalNesting++;
}
```

**解说：** 这一段实现函数 `vPortEnterCritical`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 13: 函数 vPortExitCritical

```c
/*-----------------------------------------------------------*/
/*
 * Decrement the critical nesting count, and if it has reached zero, re-enable
 * interrupts.
 */
void vPortExitCritical( void )
{
    if( ulCriticalNesting > 0 )
    {
        /* Decrement the nesting count as we are leaving a critical section. */
        ulCriticalNesting--;

        /* If the nesting level has reached zero then interrupts should be
        re-enabled. */
        if( ulCriticalNesting == 0 )
        {
            /* Enable interrupts as per portENABLE_INTERRUPTS(). */
            portENABLE_INTERRUPTS();
        }
    }
}
```

**解说：** 这一段实现函数 `vPortExitCritical`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 14: 预处理配置 vPortTaskUsesFPU

```c
/*-----------------------------------------------------------*/
#if __TI_VFP_SUPPORT__

    void vPortTaskUsesFPU( void )
    {
    extern void vPortInitialiseFPSCR( void );

        /* A task is registering the fact that it needs an FPU context.  Set the
        FPU flag (saved as part of the task context. */
        ulTaskHasFPUContext = pdTRUE;

        /* Initialise the floating point status register. */
        vPortInitialiseFPSCR();
    }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 15: 预处理配置

```c
#endif /* __TI_VFP_SUPPORT__ */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 16: 说明性注释

```c
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。
