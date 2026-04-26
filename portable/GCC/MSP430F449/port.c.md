# port.c 代码解说

源文件：`portable/GCC/MSP430F449/port.c`

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

## 片段 2: 预处理配置 portACLK_FREQUENCY_HZ

```c
/*
 *  Changes from V2.5.2
 *
 + usCriticalNesting now has a volatile qualifier.
 */
/* Standard includes. */
#include <stdlib.h>
#include <signal.h>

/* Scheduler includes. */
#include "FreeRTOS.h"
#include "task.h"

/*-----------------------------------------------------------
* Implementation of functions defined in portable.h for the MSP430 port.
*----------------------------------------------------------*/

/* Constants required for hardware setup.  The tick ISR runs off the ACLK,
 * not the MCLK. */
#define portACLK_FREQUENCY_HZ           ( ( TickType_t ) 32768 )
#define portINITIAL_CRITICAL_NESTING    ( ( uint16_t ) 10 )
#define portFLAGS_INT_ENABLED           ( ( StackType_t ) 0x08 )

/* We require the address of the pxCurrentTCB variable, but don't want to know
 * any details of its type. */
typedef void TCB_t;
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 代码片段 3

```c
extern volatile TCB_t * volatile pxCurrentTCB;
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 代码片段 4

```c
/* Most ports implement critical sections by placing the interrupt flags on
 * the stack before disabling interrupts.  Exiting the critical section is then
 * simply a case of popping the flags from the stack.  As mspgcc does not use
 * a frame pointer this cannot be done as modifying the stack will clobber all
 * the stack variables.  Instead each task maintains a count of the critical
 * section nesting depth.  Each time a critical section is entered the count is
 * incremented.  Each time a critical section is left the count is decremented -
 * with interrupts only being re-enabled if the count is zero.
 *
 * usCriticalNesting will get set to zero when the scheduler starts, but must
 * not be initialised to zero as this will cause problems during the startup
 * sequence. */
volatile uint16_t usCriticalNesting = portINITIAL_CRITICAL_NESTING;
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 5: 宏 portSAVE_CONTEXT

```c
/*-----------------------------------------------------------*/
/*
 * Macro to save a task context to the task stack.  This simply pushes all the
 * general purpose msp430 registers onto the stack, followed by the
 * usCriticalNesting value used by the task.  Finally the resultant stack
 * pointer value is saved into the task control block so it can be retrieved
 * the next time the task executes.
 */
#define portSAVE_CONTEXT()                               \
    asm volatile ( "push   r4                      \n\t" \
                   "push   r5                      \n\t" \
                   "push   r6                      \n\t" \
                   "push   r7                      \n\t" \
                   "push   r8                      \n\t" \
                   "push   r9                      \n\t" \
                   "push   r10                     \n\t" \
                   "push   r11                     \n\t" \
                   "push   r12                     \n\t" \
                   "push   r13                     \n\t" \
                   "push   r14                     \n\t" \
                   "push   r15                     \n\t" \
                   "mov.w  usCriticalNesting, r14  \n\t" \
                   "push   r14                     \n\t" \
                   "mov.w  pxCurrentTCB, r12       \n\t" \
                   "mov.w  r1, @r12                \n\t" \
                   );
```

**解说：** 这一段定义宏 `portSAVE_CONTEXT`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 6: 宏 portRESTORE_CONTEXT

```c
/*
 * Macro to restore a task context from the task stack.  This is effectively
 * the reverse of portSAVE_CONTEXT().  First the stack pointer value is
 * loaded from the task control block.  Next the value for usCriticalNesting
 * used by the task is retrieved from the stack - followed by the value of all
 * the general purpose msp430 registers.
 *
 * The bic instruction ensures there are no low power bits set in the status
 * register that is about to be popped from the stack.
 */
#define portRESTORE_CONTEXT()                            \
    asm volatile ( "mov.w  pxCurrentTCB, r12       \n\t" \
                   "mov.w  @r12, r1                \n\t" \
                   "pop    r15                     \n\t" \
                   "mov.w  r15, usCriticalNesting  \n\t" \
                   "pop    r15                     \n\t" \
                   "pop    r14                     \n\t" \
                   "pop    r13                     \n\t" \
                   "pop    r12                     \n\t" \
                   "pop    r11                     \n\t" \
                   "pop    r10                     \n\t" \
                   "pop    r9                      \n\t" \
                   "pop    r8                      \n\t" \
                   "pop    r7                      \n\t" \
                   "pop    r6                      \n\t" \
                   "pop    r5                      \n\t" \
                   "pop    r4                      \n\t" \
                   "bic    #(0xf0),0(r1)           \n\t" \
                   "reti                           \n\t" \
                   );
```

**解说：** 这一段定义宏 `portRESTORE_CONTEXT`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 7: 代码片段 7

```c
/*-----------------------------------------------------------*/
/*
 * Sets up the periodic ISR used for the RTOS tick.  This uses timer 0, but
 * could have alternatively used the watchdog timer or timer 1.
 */
static void prvSetupTimerInterrupt( void );
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 8: 函数 pxPortInitialiseStack

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
    /*
     *  Place a few bytes of known values on the bottom of the stack.
     *  This is just useful for debugging and can be included if required.
     *
     * pxTopOfStack = ( StackType_t ) 0x1111;
     *  pxTopOfStack--;
     * pxTopOfStack = ( StackType_t ) 0x2222;
     *  pxTopOfStack--;
     * pxTopOfStack = ( StackType_t ) 0x3333;
     *  pxTopOfStack--;
     */

    /* The msp430 automatically pushes the PC then SR onto the stack before
     * executing an ISR.  We want the stack to look just as if this has happened
     * so place a pointer to the start of the task on the stack first - followed
     * by the flags we want the task to use when it starts up. */
    *pxTopOfStack = ( StackType_t ) pxCode;
    pxTopOfStack--;
    *pxTopOfStack = portFLAGS_INT_ENABLED;
    pxTopOfStack--;

    /* Next the general purpose registers. */
    *pxTopOfStack = ( StackType_t ) 0x4444;
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x5555;
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x6666;
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x7777;
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x8888;
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x9999;
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0xaaaa;
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0xbbbb;
    pxTopOfStack--;
#ifdef __MSPGCC__
    *pxTopOfStack = ( StackType_t ) 0xcccc;
#else
    /* The MSP430 EABI expects the function parameter in R12. */
    *pxTopOfStack = ( StackType_t ) pvParameters;
#endif
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0xdddd;
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0xeeee;
    pxTopOfStack--;
#ifdef __MSPGCC__
    /* The mspgcc ABI expects the function parameter in R15. */
    *pxTopOfStack = ( StackType_t ) pvParameters;
#else
    *pxTopOfStack = ( StackType_t ) 0xffff;
#endif
    pxTopOfStack--;

    /* The code generated by the mspgcc compiler does not maintain separate
     * stack and frame pointers. The portENTER_CRITICAL macro cannot therefore
     * use the stack as per other ports.  Instead a variable is used to keep
     * track of the critical section nesting.  This variable has to be stored
     * as part of the task context and is initially set to zero. */
    *pxTopOfStack = ( StackType_t ) portNO_CRITICAL_SECTION_NESTING;

    /* Return a pointer to the top of the stack we have generated so this can
     * be stored in the task control block for the task. */
    return pxTopOfStack;
}
```

**解说：** 这一段实现函数 `pxPortInitialiseStack`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 9: 函数 xPortStartScheduler

```c
/*-----------------------------------------------------------*/
BaseType_t xPortStartScheduler( void )
{
    /* Setup the hardware to generate the tick.  Interrupts are disabled when
     * this function is called. */
    prvSetupTimerInterrupt();

    /* Restore the context of the first task that is going to run. */
    portRESTORE_CONTEXT();

    /* Should not get here as the tasks are now running! */
    return pdTRUE;
}
```

**解说：** 这一段实现函数 `xPortStartScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 10: 函数 vPortEndScheduler

```c
/*-----------------------------------------------------------*/
void vPortEndScheduler( void )
{
    /* It is unlikely that the MSP430 port will get stopped.  If required simply
     * disable the tick interrupt here. */
}
```

**解说：** 这一段实现函数 `vPortEndScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 11: 代码片段 11

```c
/*-----------------------------------------------------------*/
/*
 * Manual context switch called by portYIELD or taskYIELD.
 *
 * The first thing we do is save the registers so we can use a naked attribute.
 */
void vPortYield( void ) __attribute__( ( naked ) );
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 12: 函数 vPortYield

```c
void vPortYield( void )
{
    /* We want the stack of the task being saved to look exactly as if the task
     * was saved during a pre-emptive RTOS tick ISR.  Before calling an ISR the
     * msp430 places the status register onto the stack.  As this is a function
     * call and not an ISR we have to do this manually. */
    asm volatile ( "push    r2" );
    _DINT();

    /* Save the context of the current task. */
    portSAVE_CONTEXT();

    /* Switch to the highest priority task that is ready to run. */
    vTaskSwitchContext();

    /* Restore the context of the new task. */
    portRESTORE_CONTEXT();
}
```

**解说：** 这一段实现函数 `vPortYield`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 13: 函数 prvSetupTimerInterrupt

```c
/*-----------------------------------------------------------*/
/*
 * Hardware initialisation to generate the RTOS tick.  This uses timer 0
 * but could alternatively use the watchdog timer or timer 1.
 */
static void prvSetupTimerInterrupt( void )
{
    /* Ensure the timer is stopped. */
    TACTL = 0;

    /* Run the timer of the ACLK. */
    TACTL = TASSEL_1;

    /* Clear everything to start with. */
    TACTL |= TACLR;

    /* Set the compare match value according to the tick rate we want. */
    TACCR0 = portACLK_FREQUENCY_HZ / configTICK_RATE_HZ;

    /* Enable the interrupts. */
    TACCTL0 = CCIE;

    /* Start up clean. */
    TACTL |= TACLR;

    /* Up mode. */
    TACTL |= MC_1;
}
```

**解说：** 这一段实现函数 `prvSetupTimerInterrupt`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 14: 预处理配置 prvTickISR

```c
/*-----------------------------------------------------------*/
/*
 * The interrupt service routine used depends on whether the pre-emptive
 * scheduler is being used or not.
 */
#if configUSE_PREEMPTION == 1

/*
 * Tick ISR for preemptive scheduler.  We can use a naked attribute as
 * the context is saved at the start of vPortYieldFromTick().  The tick
 * count is incremented after the context is saved.
 */
    interrupt( TIMERA0_VECTOR ) void prvTickISR( void ) __attribute__( ( naked ) );
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 15: 函数 prvTickISR

```c
    interrupt( TIMERA0_VECTOR ) void prvTickISR( void )
    {
        /* Save the context of the interrupted task. */
        portSAVE_CONTEXT();

        /* Increment the tick count then switch to the highest priority task
         * that is ready to run. */
        if( xTaskIncrementTick() != pdFALSE )
        {
            vTaskSwitchContext();
        }

        /* Restore the context of the new task. */
        portRESTORE_CONTEXT();
    }
```

**解说：** 这一段实现函数 `prvTickISR`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 16: 预处理配置 prvTickISR

```c
#else /* if configUSE_PREEMPTION == 1 */

/*
 * Tick ISR for the cooperative scheduler.  All this does is increment the
 * tick count.  We don't need to switch context, this can only be done by
 * manual calls to taskYIELD();
 */
    interrupt( TIMERA0_VECTOR ) void prvTickISR( void );
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 17: 函数 prvTickISR

```c
    interrupt( TIMERA0_VECTOR ) void prvTickISR( void )
    {
        xTaskIncrementTick();
    }
```

**解说：** 这一段实现函数 `prvTickISR`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 18: 预处理配置

```c
#endif /* if configUSE_PREEMPTION == 1 */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。
