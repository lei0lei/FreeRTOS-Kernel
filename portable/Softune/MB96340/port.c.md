# port.c 代码解说

源文件：`portable/Softune/MB96340/port.c`

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
#include "FreeRTOS.h"
#include "task.h"

/*-----------------------------------------------------------
 * Implementation of functions defined in portable.h for the 16FX port.
 *----------------------------------------------------------*/

/*
 * Get current value of DPR and ADB registers
 */
StackType_t xGet_DPR_ADB_bank( void );
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 代码片段 3

```c
/*
 * Get current value of DTB and PCB registers
 */
StackType_t xGet_DTB_PCB_bank( void );
/*
 * Sets up the periodic ISR used for the RTOS tick.  This uses RLT0, but
 * can be done using any given RLT.
 */
static void prvSetupRLT0Interrupt( void );
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 类型定义 TCB_t

```c
/*-----------------------------------------------------------*/
/*
 * We require the address of the pxCurrentTCB variable, but don't want to know
 * any details of its type.
 */
typedef void TCB_t;
```

**解说：** 这一段定义类型 `TCB_t`，把相关字段或取值组织成一个明确的数据结构，方便内核代码传递和维护状态。

## 片段 5: 代码片段 5

```c
extern volatile TCB_t * volatile pxCurrentTCB;
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 6: 预处理配置 portSAVE_CONTEXT

```c
/*-----------------------------------------------------------*/
/*
 * Macro to save a task context to the task stack. This macro  copies the
 * saved context (AH:AL, DPR:ADB, DTB:PCB , PC and PS) from  the   system
 * stack to task stack pointed by user stack pointer ( USP  for SMALL and
 * MEDIUM memory model amd USB:USP for COMPACT  and LARGE memory model ),
 * then  it pushes the general purpose registers RW0-RW7  on  to the task
 * stack. Finally the  resultant  stack  pointer  value is saved into the
 * task  control  block  so  it  can  be retrieved the next time the task
 * executes.
 */
#if( ( configMEMMODEL == portSMALL ) || ( configMEMMODEL == portMEDIUM ) )

    #define portSAVE_CONTEXT()                                          \
            {   __asm(" POPW  A ");                                     \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" PUSHW  A ");                                    \
                __asm(" OR   CCR,#H'20 ");                              \
                __asm(" POPW  A ");                                     \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" PUSHW  A ");                                    \
                __asm(" OR   CCR,#H'20 ");                              \
                __asm(" POPW  A ");                                     \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" PUSHW  A ");                                    \
                __asm(" OR   CCR,#H'20 ");                              \
                __asm(" POPW  A ");                                     \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" PUSHW  A ");                                    \
                __asm(" OR   CCR,#H'20 ");                              \
                __asm(" POPW  A ");                                     \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" PUSHW  A ");                                    \
                __asm(" OR   CCR,#H'20 ");                              \
                __asm(" POPW  A ");                                     \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" PUSHW  A ");                                    \
                __asm(" PUSHW (RW0,RW1,RW2,RW3,RW4,RW5,RW6,RW7) ");     \
                __asm(" MOVW A, _pxCurrentTCB ");                       \
                __asm(" MOVW A, SP ");                                  \
                __asm(" SWAPW ");                                       \
                __asm(" MOVW @AL, AH ");                                \
                __asm(" OR   CCR,#H'20 ");                              \
            }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 7: 宏 value

```c
/*
 * Macro to restore a task context from the task stack. This is
 * effectively the reverse of SAVE_CONTEXT(). First the stack pointer
 * value (USP for SMALL and MEDIUM memory model amd USB:USP for COMPACT
 * and LARGE memory model ) is loaded from the task  control block. Next
 * the value of all the general purpose registers RW0-RW7 is retrieved.
 * Finally it copies of the context ( AH:AL, DPR:ADB, DTB:PCB, PC and PS)
 * of the task to be executed upon RETI from user stack to system stack.
 */
    #define portRESTORE_CONTEXT()                                       \
            {   __asm(" MOVW A, _pxCurrentTCB ");                       \
                __asm(" MOVW A, @A ");                                  \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" MOVW SP, A ");                                  \
                __asm(" POPW (RW0,RW1,RW2,RW3,RW4,RW5,RW6,RW7) ");      \
                __asm(" POPW  A ");                                     \
                __asm(" OR   CCR,#H'20 ");                              \
                __asm(" PUSHW  A ");                                    \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" POPW  A ");                                     \
                __asm(" OR   CCR,#H'20 ");                              \
                __asm(" PUSHW  A ");                                    \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" POPW  A ");                                     \
                __asm(" OR   CCR,#H'20 ");                              \
                __asm(" PUSHW  A ");                                    \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" POPW  A ");                                     \
                __asm(" OR   CCR,#H'20 ");                              \
                __asm(" PUSHW  A ");                                    \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" POPW  A ");                                     \
                __asm(" OR   CCR,#H'20 ");                              \
                __asm(" PUSHW  A ");                                    \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" POPW  A ");                                     \
                __asm(" OR   CCR,#H'20 ");                              \
                __asm(" PUSHW  A ");                                    \
            }
```

**解说：** 这一段定义宏 `value`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 8: 预处理配置 portSAVE_CONTEXT

```c
#elif( ( configMEMMODEL == portCOMPACT ) || ( configMEMMODEL == portLARGE ) )

    #define portSAVE_CONTEXT()                                          \
            {   __asm(" POPW  A ");                                     \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" PUSHW  A ");                                    \
                __asm(" OR   CCR,#H'20 ");                              \
                __asm(" POPW  A ");                                     \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" PUSHW  A ");                                    \
                __asm(" OR   CCR,#H'20 ");                              \
                __asm(" POPW  A ");                                     \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" PUSHW  A ");                                    \
                __asm(" OR   CCR,#H'20 ");                              \
                __asm(" POPW  A ");                                     \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" PUSHW  A ");                                    \
                __asm(" OR   CCR,#H'20 ");                              \
                __asm(" POPW  A ");                                     \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" PUSHW  A ");                                    \
                __asm(" OR   CCR,#H'20 ");                              \
                __asm(" POPW  A ");                                     \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" PUSHW  A ");                                    \
                __asm(" PUSHW (RW0,RW1,RW2,RW3,RW4,RW5,RW6,RW7) ");     \
                __asm(" MOVL A, _pxCurrentTCB ");                       \
                __asm(" MOVL RL2, A ");                                 \
                __asm(" MOVW A, SP ");                                  \
                __asm(" MOVW @RL2+0, A ");                              \
                __asm(" MOV A, USB ");                                  \
                __asm(" MOV @RL2+2, A ");                               \
            }
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 9: 宏 portRESTORE_CONTEXT

```c
    #define portRESTORE_CONTEXT()                                       \
            {   __asm(" MOVL A, _pxCurrentTCB ");                       \
                __asm(" MOVL RL2, A ");                                 \
                __asm(" MOVW A, @RL2+0 ");                              \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" MOVW SP, A ");                                  \
                __asm(" MOV A, @RL2+2 ");                               \
                __asm(" MOV USB, A ");                                  \
                __asm(" POPW (RW0,RW1,RW2,RW3,RW4,RW5,RW6,RW7) ");      \
                __asm(" POPW  A ");                                     \
                __asm(" OR   CCR,#H'20 ");                              \
                __asm(" PUSHW  A ");                                    \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" POPW  A ");                                     \
                __asm(" OR   CCR,#H'20 ");                              \
                __asm(" PUSHW  A ");                                    \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" POPW  A ");                                     \
                __asm(" OR   CCR,#H'20 ");                              \
                __asm(" PUSHW  A ");                                    \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" POPW  A ");                                     \
                __asm(" OR   CCR,#H'20 ");                              \
                __asm(" PUSHW  A ");                                    \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" POPW  A ");                                     \
                __asm(" OR   CCR,#H'20 ");                              \
                __asm(" PUSHW  A ");                                    \
                __asm(" AND  CCR,#H'DF ");                              \
                __asm(" POPW  A ");                                     \
                __asm(" OR   CCR,#H'20 ");                              \
                __asm(" PUSHW  A ");                                    \
            }
```

**解说：** 这一段定义宏 `portRESTORE_CONTEXT`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 10: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 11: 预处理配置 _xGet_DPR_ADB_bank

```c
/*-----------------------------------------------------------*/
/*
 * Functions for obtaining the current value  of  DPR:ADB, DTB:PCB bank registers
 */
#pragma asm

        .GLOBAL    _xGet_DPR_ADB_bank
        .GLOBAL    _xGet_DTB_PCB_bank
        .SECTION   CODE, CODE, ALIGN=1

_xGet_DPR_ADB_bank:

    MOV A, DPR
    SWAP
    MOV A, ADB
    ORW A
    #if configMEMMODEL == portMEDIUM || configMEMMODEL == portLARGE
        RETP
    #elif configMEMMODEL == portSMALL || configMEMMODEL == portCOMPACT
        RET
    #endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 12: 代码片段 13

```c
_xGet_DTB_PCB_bank:

    MOV A, DTB
    SWAP
    MOV A, PCB
    ORW A
    #if configMEMMODEL == portMEDIUM || configMEMMODEL == portLARGE
        RETP
    #elif configMEMMODEL == portSMALL || configMEMMODEL == portCOMPACT
        RET
    #endif
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 13: 预处理配置

```c
#pragma endasm
/*-----------------------------------------------------------*/

/*
 * Initialise the stack of a task to look exactly as if a call to
 * portSAVE_CONTEXT had been called.
 *
 * See the header file portable.h.
 */
StackType_t *pxPortInitialiseStack( StackType_t *pxTopOfStack, TaskFunction_t pxCode, void *pvParameters )
{
    /* Place a few bytes of known values on the bottom of the stack.
    This is just useful for debugging. */
    *pxTopOfStack = 0x1111;
    pxTopOfStack--;
    *pxTopOfStack = 0x2222;
    pxTopOfStack--;
    *pxTopOfStack = 0x3333;
    pxTopOfStack--;

    /* Once the task is called the task  would  push  the  pointer to the
    parameter onto the stack. Hence here the pointer would be copied to the stack
    first.  When using the COMPACT or LARGE memory model the pointer would be 24
    bits, and when using the SMALL or MEDIUM memory model the pointer would be 16
    bits. */
    #if( ( configMEMMODEL == portCOMPACT ) || ( configMEMMODEL == portLARGE ) )
    {
        *pxTopOfStack = ( StackType_t ) ( ( uint32_t ) ( pvParameters ) >> 16 );
        pxTopOfStack--;
    }
    #endif

    *pxTopOfStack = ( StackType_t ) ( pvParameters );
    pxTopOfStack--;

    /* This is redundant push to the stack. This is required in order to introduce
    an offset so that the task accesses a parameter correctly that is passed on to
    the task stack. */
    #if( ( configMEMMODEL == portMEDIUM ) || ( configMEMMODEL == portLARGE ) )
    {
        *pxTopOfStack = ( xGet_DTB_PCB_bank() & 0xff00 ) | ( ( ( int32_t ) ( pxCode ) >> 16 ) & 0xff );
        pxTopOfStack--;
    }
    #endif

    /* This is redundant push to the stack. This is required in order to introduce
    an offset so the task correctly accesses the parameter passed on the task stack. */
    *pxTopOfStack = ( StackType_t ) ( pxCode );
    pxTopOfStack--;

    /* PS - User Mode, ILM=7, RB=0, Interrupts enabled,USP */
    *pxTopOfStack = 0xE0C0;
    pxTopOfStack--;

    /* PC */
    *pxTopOfStack = ( StackType_t ) ( pxCode );
    pxTopOfStack--;

    /* DTB | PCB */
    #if configMEMMODEL == portSMALL || configMEMMODEL == portCOMPACT
    {
        *pxTopOfStack = xGet_DTB_PCB_bank();
        pxTopOfStack--;
    }
    #endif

    /* DTB | PCB, in case of MEDIUM and LARGE memory models, PCB would be used
    along with PC to indicate the start address of the function. */
    #if( ( configMEMMODEL == portMEDIUM ) || ( configMEMMODEL == portLARGE ) )
    {
        *pxTopOfStack = ( xGet_DTB_PCB_bank() & 0xff00 ) | ( ( ( int32_t ) ( pxCode ) >> 16 ) & 0xff );
        pxTopOfStack--;
    }
    #endif

    /* DPR | ADB  */
    *pxTopOfStack = xGet_DPR_ADB_bank();
    pxTopOfStack--;

    /* AL */
    *pxTopOfStack = ( StackType_t ) 0x9999;
    pxTopOfStack--;

    /* AH */
    *pxTopOfStack = ( StackType_t ) 0xAAAA;
    pxTopOfStack--;

    /* Next the general purpose registers. */
    *pxTopOfStack = ( StackType_t ) 0x7777; /* RW7 */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x6666; /* RW6 */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x5555; /* RW5 */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x4444; /* RW4 */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x3333; /* RW3 */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x2222; /* RW2 */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x1111; /* RW1 */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) 0x8888; /* RW0 */

    return pxTopOfStack;
}
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 14: 函数 prvSetupRLT0Interrupt

```c
/*-----------------------------------------------------------*/
static void prvSetupRLT0Interrupt( void )
{
/* The peripheral clock divided by 16 is used by the timer. */
const uint16_t usReloadValue = ( uint16_t ) ( ( ( configCLKP1_CLOCK_HZ / configTICK_RATE_HZ ) / 16UL ) - 1UL );

    /* set reload value = 34999+1, TICK Interrupt after 10 ms @ 56MHz of CLKP1 */
    TMRLR0 = usReloadValue;

    /* prescaler 1:16, reload, interrupt enable, count enable, trigger */
    TMCSR0 = 0x041B;
}
```

**解说：** 这一段实现函数 `prvSetupRLT0Interrupt`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 15: 函数 xPortStartScheduler

```c
/*-----------------------------------------------------------*/
BaseType_t xPortStartScheduler( void )
{
    /* Setup the hardware to generate the tick. */
    prvSetupRLT0Interrupt();

    /* Restore the context of the first task that is going to run. */
    portRESTORE_CONTEXT();

    /* Simulate a function call end as generated by the compiler.  We will now
    jump to the start of the task the context of which we have just restored. */
    __asm(" reti ");


    /* Should not get here. */
    return pdTRUE;
}
```

**解说：** 这一段实现函数 `xPortStartScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 16: 函数 vPortEndScheduler

```c
/*-----------------------------------------------------------*/
void vPortEndScheduler( void )
{
    /* Not implemented - unlikely to ever be required as there is nothing to
    return to. */
}
```

**解说：** 这一段实现函数 `vPortEndScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 17: 预处理配置 prvRLT0_TICKISR

```c
/*-----------------------------------------------------------*/
/*
 * The interrupt service routine used depends on whether the pre-emptive
 * scheduler is being used or not.
 */
#if configUSE_PREEMPTION == 1

    /*
     * Tick ISR for preemptive scheduler.  We can use a __nosavereg attribute
     * as the context is to be saved by the portSAVE_CONTEXT() macro, not the
     * compiler generated code.  The tick count is incremented after the context
     * is saved.
     */
    __nosavereg __interrupt void prvRLT0_TICKISR( void )
    {
        /* Disable interrupts so that portSAVE_CONTEXT() is not interrupted */
        __DI();

        /* Save the context of the interrupted task. */
        portSAVE_CONTEXT();

        /* Enable interrupts */
        __EI();

        /* Clear RLT0 interrupt flag */
        TMCSR0_UF = 0;

        /* Increment the tick count then switch to the highest priority task
        that is ready to run. */
        if( xTaskIncrementTick() != pdFALSE )
        {
            vTaskSwitchContext();
        }

        /* Disable interrupts so that portRESTORE_CONTEXT() is not interrupted */
        __DI();

        /* Restore the context of the new task. */
        portRESTORE_CONTEXT();

        /* Enable interrupts */
        __EI();
    }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 18: 预处理配置 prvRLT0_TICKISR

```c
#else

    /*
     * Tick ISR for the cooperative scheduler.  All this does is increment the
     * tick count.  We don't need to switch context, this can only be done by
     * manual calls to taskYIELD();
     */
    __interrupt void prvRLT0_TICKISR( void )
    {
        /* Clear RLT0 interrupt flag */
        TMCSR0_UF = 0;

        xTaskIncrementTick();
    }
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 19: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 20: 函数 vPortYield

```c
/*-----------------------------------------------------------*/
/*
 * Manual context switch. We can use a __nosavereg attribute  as the context
 * is to be saved by the portSAVE_CONTEXT() macro, not the compiler generated
 * code.
 */
__nosavereg __interrupt void vPortYield( void )
{
    /* Save the context of the interrupted task. */
    portSAVE_CONTEXT();

    /* Switch to the highest priority task that is ready to run. */
    vTaskSwitchContext();

    /* Restore the context of the new task. */
    portRESTORE_CONTEXT();
}
```

**解说：** 这一段实现函数 `vPortYield`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 21: 函数 vPortYieldDelayed

```c
/*-----------------------------------------------------------*/
__nosavereg __interrupt void vPortYieldDelayed( void )
{
    /* Disable interrupts so that portSAVE_CONTEXT() is not interrupted */
    __DI();

    /* Save the context of the interrupted task. */
    portSAVE_CONTEXT();

    /* Enable interrupts */
    __EI();

    /* Clear delayed interrupt flag */
    __asm (" CLRB  03A4H:0 ");

    /* Switch to the highest priority task that is ready to run. */
    vTaskSwitchContext();

    /* Disable interrupts so that portSAVE_CONTEXT() is not interrupted */
    __DI();

    /* Restore the context of the new task. */
    portRESTORE_CONTEXT();

    /* Enable interrupts */
    __EI();
}
```

**解说：** 这一段实现函数 `vPortYieldDelayed`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 22: 说明性注释

```c
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。
