# port.c 代码解说

源文件：`portable/MPLAB/PIC32MX/port.c`

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
 * Implementation of functions defined in portable.h for the PIC32MX port.
  *----------------------------------------------------------*/
#ifndef __XC
    #error This port is designed to work with XC32.  Please update your C compiler version.
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 3: 预处理配置 portTIMER_PRESCALE

```c
/* Scheduler include files. */
#include "FreeRTOS.h"
#include "task.h"

/* Hardware specifics. */
#define portTIMER_PRESCALE  8
#define portPRESCALE_BITS   1

/* Bits within various registers. */
#define portIE_BIT                      ( 0x00000001 )
#define portEXL_BIT                     ( 0x00000002 )

/* Bits within the CAUSE register. */
#define portCORE_SW_0                   ( 0x00000100 )
#define portCORE_SW_1                   ( 0x00000200 )

/* The EXL bit is set to ensure interrupts do not occur while the context of
the first task is being restored. */
#define portINITIAL_SR                  ( portIE_BIT | portEXL_BIT )

/*
By default port.c generates its tick interrupt from TIMER1.  The user can
override this behaviour by:
    1: Providing their own implementation of vApplicationSetupTickTimerInterrupt(),
       which is the function that configures the timer.  The function is defined
       as a weak symbol in this file so if the same function name is used in the
       application code then the version in the application code will be linked
       into the application in preference to the version defined in this file.
    2: Define configTICK_INTERRUPT_VECTOR to the vector number of the timer used
       to generate the tick interrupt.  For example, when timer 1 is used then
       configTICK_INTERRUPT_VECTOR is set to _TIMER_1_VECTOR.
       configTICK_INTERRUPT_VECTOR should be defined in FreeRTOSConfig.h.
    3: Define configCLEAR_TICK_TIMER_INTERRUPT() to clear the interrupt in the
       timer used to generate the tick interrupt.  For example, when timer 1 is
       used configCLEAR_TICK_TIMER_INTERRUPT() is defined to
       IFS0CLR = _IFS0_T1IF_MASK.
*/
#ifndef configTICK_INTERRUPT_VECTOR
    #define configTICK_INTERRUPT_VECTOR _TIMER_1_VECTOR
    #define configCLEAR_TICK_TIMER_INTERRUPT() IFS0CLR = _IFS0_T1IF_MASK
#else
    #ifndef configCLEAR_TICK_TIMER_INTERRUPT
        #error If configTICK_INTERRUPT_VECTOR is defined in application code then configCLEAR_TICK_TIMER_INTERRUPT must also be defined in application code.
    #endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 4: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 5: 预处理配置 portTASK_RETURN_ADDRESS

```c
/* Let the user override the pre-loading of the initial RA with the address of
prvTaskExitError() in case it messes up unwinding of the stack in the
debugger - in which case configTASK_RETURN_ADDRESS can be defined as 0 (NULL). */
#ifdef configTASK_RETURN_ADDRESS
    #define portTASK_RETURN_ADDRESS configTASK_RETURN_ADDRESS
#else
    #define portTASK_RETURN_ADDRESS prvTaskExitError
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 6: 预处理配置 portISR_STACK_FILL_BYTE

```c
/* Set configCHECK_FOR_STACK_OVERFLOW to 3 to add ISR stack checking to task
stack checking.  A problem in the ISR stack will trigger an assert, not call the
stack overflow hook function (because the stack overflow hook is specific to a
task stack, not the ISR stack). */
#if( configCHECK_FOR_STACK_OVERFLOW > 2 )

    /* Don't use 0xa5 as the stack fill bytes as that is used by the kernel for
    the task stacks, and so will legitimately appear in many positions within
    the ISR stack. */
    #define portISR_STACK_FILL_BYTE 0xee

    static const uint8_t ucExpectedStackBytes[] = {
                                    portISR_STACK_FILL_BYTE, portISR_STACK_FILL_BYTE, portISR_STACK_FILL_BYTE, portISR_STACK_FILL_BYTE,     \
                                    portISR_STACK_FILL_BYTE, portISR_STACK_FILL_BYTE, portISR_STACK_FILL_BYTE, portISR_STACK_FILL_BYTE,     \
                                    portISR_STACK_FILL_BYTE, portISR_STACK_FILL_BYTE, portISR_STACK_FILL_BYTE, portISR_STACK_FILL_BYTE,     \
                                    portISR_STACK_FILL_BYTE, portISR_STACK_FILL_BYTE, portISR_STACK_FILL_BYTE, portISR_STACK_FILL_BYTE,     \
                                    portISR_STACK_FILL_BYTE, portISR_STACK_FILL_BYTE, portISR_STACK_FILL_BYTE, portISR_STACK_FILL_BYTE };   \

    #define portCHECK_ISR_STACK() configASSERT( ( memcmp( ( void * ) xISRStack, ( void * ) ucExpectedStackBytes, sizeof( ucExpectedStackBytes ) ) == 0 ) )
#else
    /* Define the function away. */
    #define portCHECK_ISR_STACK()
#endif /* configCHECK_FOR_STACK_OVERFLOW > 2 */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 7: 代码片段 7

```c
/*-----------------------------------------------------------*/
/*
 * Place the prototype here to ensure the interrupt vector is correctly installed.
 * Note that because the interrupt is written in assembly, the IPL setting in the
 * following line of code has no effect.  The interrupt priority is set by the
 * call to ConfigIntTimer1() in vApplicationSetupTickTimerInterrupt().
 */
extern void __attribute__( (interrupt(IPL1AUTO), vector( configTICK_INTERRUPT_VECTOR ))) vPortTickInterruptHandler( void );
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 8: 代码片段 8

```c
/*
 * The software interrupt handler that performs the yield.  Note that, because
 * the interrupt is written in assembly, the IPL setting in the following line of
 * code has no effect.  The interrupt priority is set by the call to
 * mConfigIntCoreSW0() in xPortStartScheduler().
 */
void __attribute__( (interrupt(IPL1AUTO), vector(_CORE_SOFTWARE_0_VECTOR))) vPortYieldISR( void );
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 9: 代码片段 9

```c
/*
 * Used to catch tasks that attempt to return from their implementing function.
 */
static void prvTaskExitError( void );
/*-----------------------------------------------------------*/
/* Records the interrupt nesting depth.  This is initialised to one as it is
decremented to 0 when the first task starts. */
volatile UBaseType_t uxInterruptNesting = 0x01;
/* Stores the task stack pointer when a switch is made to use the system stack. */
UBaseType_t uxSavedTaskStackPointer = 0;
/* The stack used by interrupt service routines that cause a context switch. */
__attribute__ ((aligned(8))) StackType_t xISRStack[ configISR_STACK_SIZE ] = { 0 };
/* The top of stack value ensures there is enough space to store 6 registers on
the callers stack, as some functions seem to want to do this. */
const StackType_t * const xISRStackTop = &( xISRStack[ ( configISR_STACK_SIZE & ~portBYTE_ALIGNMENT_MASK ) - 8 ] );
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 10: 函数实现

```c
/*-----------------------------------------------------------*/
/*
 * See header file for description.
 */
StackType_t *pxPortInitialiseStack( StackType_t *pxTopOfStack, TaskFunction_t pxCode, void *pvParameters )
{
    /* Ensure 8 byte alignment is maintained when the context is popped from
     * stack. The size of the context is 33 words (132 bytes). */
    pxTopOfStack--;
    pxTopOfStack--;

    *pxTopOfStack = (StackType_t) 0xDEADBEEF;
    pxTopOfStack--;

    *pxTopOfStack = (StackType_t) 0x12345678;   /* Word to which the stack pointer will be left pointing after context restore. */
    pxTopOfStack--;

    *pxTopOfStack = (StackType_t) _CP0_GET_CAUSE();
    pxTopOfStack--;

    *pxTopOfStack = (StackType_t) portINITIAL_SR;/* CP0_STATUS */
    pxTopOfStack--;

    *pxTopOfStack = (StackType_t) pxCode;       /* CP0_EPC */
    pxTopOfStack--;

    *pxTopOfStack = (StackType_t) portTASK_RETURN_ADDRESS;  /* ra */
    pxTopOfStack -= 15;

    *pxTopOfStack = (StackType_t) pvParameters; /* Parameters to pass in. */
    pxTopOfStack -= 15;

    return pxTopOfStack;
}
```

**解说：** 这一段实现一个函数，把一组相关步骤封装成独立的执行单元。

## 片段 11: 函数 prvTaskExitError

```c
/*-----------------------------------------------------------*/
static void prvTaskExitError( void )
{
    /* A function that implements a task must not exit or attempt to return to
    its caller as there is nothing to return to.  If a task wants to exit it
    should instead call vTaskDelete( NULL ).

    Artificially force an assert() to be triggered if configASSERT() is
    defined, then stop here so application writers can catch the error. */
    configASSERT( uxSavedTaskStackPointer == 0UL );
    portDISABLE_INTERRUPTS();
    for( ;; );
}
```

**解说：** 这一段实现函数 `prvTaskExitError`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 12: 函数 vApplicationSetupTickTimerInterrupt

```c
/*-----------------------------------------------------------*/
/*
 * Setup a timer for a regular tick.  This function uses peripheral timer 1.
 * The function is declared weak so an application writer can use a different
 * timer by redefining this implementation.  If a different timer is used then
 * configTICK_INTERRUPT_VECTOR must also be defined in FreeRTOSConfig.h to
 * ensure the RTOS provided tick interrupt handler is installed on the correct
 * vector number.  When Timer 1 is used the vector number is defined as
 * _TIMER_1_VECTOR.
 */
__attribute__(( weak )) void vApplicationSetupTickTimerInterrupt( void )
{
const uint32_t ulCompareMatch = ( (configPERIPHERAL_CLOCK_HZ / portTIMER_PRESCALE) / configTICK_RATE_HZ ) - 1;

    T1CON = 0x0000;
    T1CONbits.TCKPS = portPRESCALE_BITS;
    PR1 = ulCompareMatch;
    IPC1bits.T1IP = configKERNEL_INTERRUPT_PRIORITY;

    /* Clear the interrupt as a starting condition. */
    IFS0bits.T1IF = 0;

    /* Enable the interrupt. */
    IEC0bits.T1IE = 1;

    /* Start the timer. */
    T1CONbits.TON = 1;
}
```

**解说：** 这一段实现函数 `vApplicationSetupTickTimerInterrupt`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 13: 函数 vPortEndScheduler

```c
/*-----------------------------------------------------------*/
void vPortEndScheduler(void)
{
    /* Not implemented in ports where there is nothing to return to.
    Artificially force an assert. */
    configASSERT( uxInterruptNesting == 1000UL );
}
```

**解说：** 这一段实现函数 `vPortEndScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 14: 函数 xPortStartScheduler

```c
/*-----------------------------------------------------------*/
BaseType_t xPortStartScheduler( void )
{
extern void vPortStartFirstTask( void );
extern void *pxCurrentTCB;

    #if ( configCHECK_FOR_STACK_OVERFLOW > 2 )
    {
        /* Fill the ISR stack to make it easy to asses how much is being used. */
        memset( ( void * ) xISRStack, portISR_STACK_FILL_BYTE, sizeof( xISRStack ) );
    }
    #endif /* configCHECK_FOR_STACK_OVERFLOW > 2 */

    /* Clear the software interrupt flag. */
    IFS0CLR = _IFS0_CS0IF_MASK;

    /* Set software timer priority. */
    IPC0CLR = _IPC0_CS0IP_MASK;
    IPC0SET = ( configKERNEL_INTERRUPT_PRIORITY << _IPC0_CS0IP_POSITION );

    /* Enable software interrupt. */
    IEC0CLR = _IEC0_CS0IE_MASK;
    IEC0SET = 1 << _IEC0_CS0IE_POSITION;

    /* Setup the timer to generate the tick.  Interrupts will have been
    disabled by the time we get here. */
    vApplicationSetupTickTimerInterrupt();

    /* Kick off the highest priority task that has been created so far.
    Its stack location is loaded into uxSavedTaskStackPointer. */
    uxSavedTaskStackPointer = *( UBaseType_t * ) pxCurrentTCB;
    vPortStartFirstTask();

    /* Should never get here as the tasks will now be executing!  Call the task
    exit error function to prevent compiler warnings about a static function
    not being called in the case that the application writer overrides this
    functionality by defining configTASK_RETURN_ADDRESS. */
    prvTaskExitError();

    return pdFALSE;
}
```

**解说：** 这一段实现函数 `xPortStartScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 15: 函数 vPortIncrementTick

```c
/*-----------------------------------------------------------*/
void vPortIncrementTick( void )
{
UBaseType_t uxSavedStatus;

    uxSavedStatus = uxPortSetInterruptMaskFromISR();
    {
        if( xTaskIncrementTick() != pdFALSE )
        {
            /* Pend a context switch. */
            _CP0_BIS_CAUSE( portCORE_SW_0 );
        }
    }
    vPortClearInterruptMaskFromISR( uxSavedStatus );

    /* Look for the ISR stack getting near or past its limit. */
    portCHECK_ISR_STACK();

    /* Clear timer interrupt. */
    configCLEAR_TICK_TIMER_INTERRUPT();
}
```

**解说：** 这一段实现函数 `vPortIncrementTick`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 16: 函数 uxPortSetInterruptMaskFromISR

```c
/*-----------------------------------------------------------*/
UBaseType_t uxPortSetInterruptMaskFromISR( void )
{
UBaseType_t uxSavedStatusRegister;

    __builtin_disable_interrupts();
    uxSavedStatusRegister = _CP0_GET_STATUS() | 0x01;
    /* This clears the IPL bits, then sets them to
    configMAX_SYSCALL_INTERRUPT_PRIORITY.  This function should not be called
    from an interrupt that has a priority above
    configMAX_SYSCALL_INTERRUPT_PRIORITY so, when used correctly, the action
    can only result in the IPL being unchanged or raised, and therefore never
    lowered. */
    _CP0_SET_STATUS( ( ( uxSavedStatusRegister & ( ~portALL_IPL_BITS ) ) ) | ( configMAX_SYSCALL_INTERRUPT_PRIORITY << portIPL_SHIFT ) );

    return uxSavedStatusRegister;
}
```

**解说：** 这一段实现函数 `uxPortSetInterruptMaskFromISR`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 17: 函数 vPortClearInterruptMaskFromISR

```c
/*-----------------------------------------------------------*/
void vPortClearInterruptMaskFromISR( UBaseType_t uxSavedStatusRegister )
{
    _CP0_SET_STATUS( uxSavedStatusRegister );
}
```

**解说：** 这一段实现函数 `vPortClearInterruptMaskFromISR`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 18: 说明性注释

```c
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。
