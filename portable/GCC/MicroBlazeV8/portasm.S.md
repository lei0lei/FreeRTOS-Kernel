# portasm.S 代码解说

源文件：`portable/GCC/MicroBlazeV8/portasm.S`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 文件头和许可证

```asm
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

```asm
/* FreeRTOS includes. */
#include "FreeRTOSConfig.h"
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 预处理配置

```asm
/* Xilinx library includes. */
#include "microblaze_exceptions_g.h"
#include "xparameters.h"
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 4: 预处理配置 portCONTEXT_SIZE

```asm
/* The context is oversized to allow functions called from the ISR to write
back into the caller stack. */
#if( XPAR_MICROBLAZE_USE_FPU != 0 )
    #define portCONTEXT_SIZE 136
    #define portMINUS_CONTEXT_SIZE -136
#else
    #define portCONTEXT_SIZE 132
    #define portMINUS_CONTEXT_SIZE -132
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 5: 宏 portR31_OFFSET

```asm
/* Offsets from the stack pointer at which saved registers are placed. */
#define portR31_OFFSET  4
#define portR30_OFFSET  8
#define portR29_OFFSET  12
#define portR28_OFFSET  16
#define portR27_OFFSET  20
#define portR26_OFFSET  24
#define portR25_OFFSET  28
#define portR24_OFFSET  32
#define portR23_OFFSET  36
#define portR22_OFFSET  40
#define portR21_OFFSET  44
#define portR20_OFFSET  48
#define portR19_OFFSET  52
#define portR18_OFFSET  56
#define portR17_OFFSET  60
#define portR16_OFFSET  64
#define portR15_OFFSET  68
#define portR14_OFFSET  72
#define portR13_OFFSET  76
#define portR12_OFFSET  80
#define portR11_OFFSET  84
#define portR10_OFFSET  88
#define portR9_OFFSET   92
#define portR8_OFFSET   96
#define portR7_OFFSET   100
#define portR6_OFFSET   104
#define portR5_OFFSET   108
#define portR4_OFFSET   112
#define portR3_OFFSET   116
#define portR2_OFFSET   120
#define portCRITICAL_NESTING_OFFSET 124
#define portMSR_OFFSET 128
#define portFSR_OFFSET 132
```

**解说：** 这一段定义宏 `portR31_OFFSET`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 6: 代码片段 6

```asm
    .extern pxCurrentTCB
    .extern XIntc_DeviceInterruptHandler
    .extern vTaskSwitchContext
    .extern uxCriticalNesting
    .extern pulISRStack
    .extern ulTaskSwitchRequested
    .extern vPortExceptionHandler
    .extern pulStackPointerOnFunctionEntry
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 7: 代码片段 7

```asm
    .global _interrupt_handler
    .global VPortYieldASM
    .global vPortStartFirstTask
    .global vPortExceptionHandlerEntry
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 8: 代码片段 8

```asm

.macro portSAVE_CONTEXT
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 9: 代码片段 9

```asm
    /* Make room for the context on the stack. */
    addik r1, r1, portMINUS_CONTEXT_SIZE
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 10: 代码片段 10

```asm
    /* Stack general registers. */
    swi r31, r1, portR31_OFFSET
    swi r30, r1, portR30_OFFSET
    swi r29, r1, portR29_OFFSET
    swi r28, r1, portR28_OFFSET
    swi r27, r1, portR27_OFFSET
    swi r26, r1, portR26_OFFSET
    swi r25, r1, portR25_OFFSET
    swi r24, r1, portR24_OFFSET
    swi r23, r1, portR23_OFFSET
    swi r22, r1, portR22_OFFSET
    swi r21, r1, portR21_OFFSET
    swi r20, r1, portR20_OFFSET
    swi r19, r1, portR19_OFFSET
    swi r18, r1, portR18_OFFSET
    swi r17, r1, portR17_OFFSET
    swi r16, r1, portR16_OFFSET
    swi r15, r1, portR15_OFFSET
    /* R14 is saved later as it needs adjustment if a yield is performed. */
    swi r13, r1, portR13_OFFSET
    swi r12, r1, portR12_OFFSET
    swi r11, r1, portR11_OFFSET
    swi r10, r1, portR10_OFFSET
    swi r9, r1, portR9_OFFSET
    swi r8, r1, portR8_OFFSET
    swi r7, r1, portR7_OFFSET
    swi r6, r1, portR6_OFFSET
    swi r5, r1, portR5_OFFSET
    swi r4, r1, portR4_OFFSET
    swi r3, r1, portR3_OFFSET
    swi r2, r1, portR2_OFFSET
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 11: 代码片段 11

```asm
    /* Stack the critical section nesting value. */
    lwi r18, r0, uxCriticalNesting
    swi r18, r1, portCRITICAL_NESTING_OFFSET
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 12: 代码片段 12

```asm
    /* Stack MSR. */
    mfs r18, rmsr
    swi r18, r1, portMSR_OFFSET
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 13: 预处理配置

```asm
    #if( XPAR_MICROBLAZE_USE_FPU != 0 )
        /* Stack FSR. */
        mfs r18, rfsr
        swi r18, r1, portFSR_OFFSET
    #endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 14: 代码片段 14

```asm
    /* Save the top of stack value to the TCB. */
    lwi r3, r0, pxCurrentTCB
    sw  r1, r0, r3
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 15: 代码片段 15

```asm
    .endm
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 16: 代码片段 16

```asm
.macro portRESTORE_CONTEXT
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 17: 代码片段 17

```asm
    /* Load the top of stack value from the TCB. */
    lwi r18, r0, pxCurrentTCB
    lw  r1, r0, r18
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 18: 代码片段 18

```asm
    /* Restore the general registers. */
    lwi r31, r1, portR31_OFFSET
    lwi r30, r1, portR30_OFFSET
    lwi r29, r1, portR29_OFFSET
    lwi r28, r1, portR28_OFFSET
    lwi r27, r1, portR27_OFFSET
    lwi r26, r1, portR26_OFFSET
    lwi r25, r1, portR25_OFFSET
    lwi r24, r1, portR24_OFFSET
    lwi r23, r1, portR23_OFFSET
    lwi r22, r1, portR22_OFFSET
    lwi r21, r1, portR21_OFFSET
    lwi r20, r1, portR20_OFFSET
    lwi r19, r1, portR19_OFFSET
    lwi r17, r1, portR17_OFFSET
    lwi r16, r1, portR16_OFFSET
    lwi r15, r1, portR15_OFFSET
    lwi r14, r1, portR14_OFFSET
    lwi r13, r1, portR13_OFFSET
    lwi r12, r1, portR12_OFFSET
    lwi r11, r1, portR11_OFFSET
    lwi r10, r1, portR10_OFFSET
    lwi r9, r1, portR9_OFFSET
    lwi r8, r1, portR8_OFFSET
    lwi r7, r1, portR7_OFFSET
    lwi r6, r1, portR6_OFFSET
    lwi r5, r1, portR5_OFFSET
    lwi r4, r1, portR4_OFFSET
    lwi r3, r1, portR3_OFFSET
    lwi r2, r1, portR2_OFFSET
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 19: 代码片段 19

```asm
    /* Reload the rmsr from the stack. */
    lwi r18, r1, portMSR_OFFSET
    mts rmsr, r18
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 20: 预处理配置

```asm
    #if( XPAR_MICROBLAZE_USE_FPU != 0 )
        /* Reload the FSR from the stack. */
        lwi r18, r1, portFSR_OFFSET
        mts rfsr, r18
    #endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 21: 代码片段 21

```asm
    /* Load the critical nesting value. */
    lwi r18, r1, portCRITICAL_NESTING_OFFSET
    swi r18, r0, uxCriticalNesting
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 22: 代码片段 22

```asm
    /* Test the critical nesting value.  If it is non zero then the task last
    exited the running state using a yield.  If it is zero, then the task
    last exited the running state through an interrupt. */
    xori r18, r18, 0
    bnei r18, exit_from_yield
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 23: 代码片段 23

```asm
    /* r18 was being used as a temporary.  Now restore its true value from the
    stack. */
    lwi r18, r1, portR18_OFFSET
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 24: 代码片段 24

```asm
    /* Remove the stack frame. */
    addik r1, r1, portCONTEXT_SIZE
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 25: 代码片段 25

```asm
    /* Return using rtid so interrupts are re-enabled as this function is
    exited. */
    rtid r14, 0
    or r0, r0, r0
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 26: 代码片段 26

```asm
    .endm
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 27: 汇编标签 exit_from_yield

```asm
/* This function is used to exit portRESTORE_CONTEXT() if the task being
returned to last left the Running state by calling taskYIELD() (rather than
being preempted by an interrupt). */
    .text
    .align  4
exit_from_yield:
```

**解说：** 这一段是汇编标签 `exit_from_yield` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 28: 代码片段 28

```asm
    /* r18 was being used as a temporary.  Now restore its true value from the
    stack. */
    lwi r18, r1, portR18_OFFSET
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 29: 代码片段 29

```asm
    /* Remove the stack frame. */
    addik r1, r1, portCONTEXT_SIZE
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 30: 代码片段 30

```asm
    /* Return to the task. */
    rtsd r14, 0
    or r0, r0, r0
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 31: 汇编标签 _interrupt_handler

```asm

    .text
    .align  4
_interrupt_handler:
```

**解说：** 这一段是汇编标签 `_interrupt_handler` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 32: 代码片段 32

```asm
    portSAVE_CONTEXT
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 33: 代码片段 33

```asm
    /* Stack the return address. */
    swi r14, r1, portR14_OFFSET
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 34: 代码片段 34

```asm
    /* Switch to the ISR stack. */
    lwi r1, r0, pulISRStack
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 35: 代码片段 35

```asm
    /* The parameter to the interrupt handler. */
    ori r5, r0, configINTERRUPT_CONTROLLER_TO_USE
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 36: 代码片段 36

```asm
    /* Execute any pending interrupts. */
    bralid r15, XIntc_DeviceInterruptHandler
    or r0, r0, r0
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 37: 代码片段 37

```asm
    /* See if a new task should be selected to execute. */
    lwi r18, r0, ulTaskSwitchRequested
    or r18, r18, r0
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 38: 代码片段 38

```asm
    /* If ulTaskSwitchRequested is already zero, then jump straight to
    restoring the task that is already in the Running state. */
    beqi r18, task_switch_not_requested
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 39: 代码片段 39

```asm
    /* Set ulTaskSwitchRequested back to zero as a task switch is about to be
    performed. */
    swi r0, r0, ulTaskSwitchRequested
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 40: 代码片段 40

```asm
    /* ulTaskSwitchRequested was not 0 when tested.  Select the next task to
    execute. */
    bralid r15, vTaskSwitchContext
    or r0, r0, r0
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 41: 汇编标签 task_switch_not_requested

```asm
task_switch_not_requested:
```

**解说：** 这一段是汇编标签 `task_switch_not_requested` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 42: 代码片段 42

```asm
    /* Restore the context of the next task scheduled to execute. */
    portRESTORE_CONTEXT
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 43: 汇编标签 VPortYieldASM

```asm

    .text
    .align  4
VPortYieldASM:
```

**解说：** 这一段是汇编标签 `VPortYieldASM` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 44: 代码片段 44

```asm
    portSAVE_CONTEXT
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 45: 代码片段 45

```asm
    /* Modify the return address so a return is done to the instruction after
    the call to VPortYieldASM. */
    addi r14, r14, 8
    swi r14, r1, portR14_OFFSET
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 46: 代码片段 46

```asm
    /* Switch to use the ISR stack. */
    lwi r1, r0, pulISRStack
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 47: 代码片段 47

```asm
    /* Select the next task to execute. */
    bralid r15, vTaskSwitchContext
    or r0, r0, r0
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 48: 代码片段 48

```asm
    /* Restore the context of the next task scheduled to execute. */
    portRESTORE_CONTEXT
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 49: 汇编标签 vPortStartFirstTask

```asm
    .text
    .align  4
vPortStartFirstTask:
```

**解说：** 这一段是汇编标签 `vPortStartFirstTask` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 50: 代码片段 50

```asm
    portRESTORE_CONTEXT
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 52: 预处理配置

```asm
#if ( MICROBLAZE_EXCEPTIONS_ENABLED == 1 ) && ( configINSTALL_EXCEPTION_HANDLERS == 1 )
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 53: 汇编标签 vPortExceptionHandlerEntry

```asm
    .text
    .align 4
vPortExceptionHandlerEntry:
```

**解说：** 这一段是汇编标签 `vPortExceptionHandlerEntry` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 54: 代码片段 54

```asm
    /* Take a copy of the stack pointer before vPortExecptionHandler is called,
    storing its value prior to the function stack frame being created. */
    swi r1, r0, pulStackPointerOnFunctionEntry
    bralid r15, vPortExceptionHandler
    or r0, r0, r0
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 55: 预处理配置

```asm
#endif /* ( MICROBLAZE_EXCEPTIONS_ENABLED == 1 ) && ( configINSTALL_EXCEPTION_HANDLERS == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。
