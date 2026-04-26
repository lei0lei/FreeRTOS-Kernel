# portASM.S 代码解说

源文件：`portable/GCC/ARM_AARCH64_SRE/portASM.S`

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

## 片段 2: 代码片段 2

```asm
    .text
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 3: 代码片段 3

```asm
    /* Variables and functions. */
    .extern ullMaxAPIPriorityMask
    .extern pxCurrentTCB
    .extern vTaskSwitchContext
    .extern vApplicationIRQHandler
    .extern ullPortInterruptNesting
    .extern ullPortTaskHasFPUContext
    .extern ullCriticalNesting
    .extern ullPortYieldRequired
    .extern _freertos_vector_table
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 代码片段 4

```asm
    .global FreeRTOS_IRQ_Handler
    .global FreeRTOS_SWI_Handler
    .global vPortRestoreTaskContext
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 5: 代码片段 5

```asm

.macro portSAVE_CONTEXT
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 6: 代码片段 6

```asm
    /* Switch to use the EL0 stack pointer. */
    MSR     SPSEL, #0
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 7: 代码片段 7

```asm
    /* Save the entire context. */
    STP     X0, X1, [SP, #-0x10]!
    STP     X2, X3, [SP, #-0x10]!
    STP     X4, X5, [SP, #-0x10]!
    STP     X6, X7, [SP, #-0x10]!
    STP     X8, X9, [SP, #-0x10]!
    STP     X10, X11, [SP, #-0x10]!
    STP     X12, X13, [SP, #-0x10]!
    STP     X14, X15, [SP, #-0x10]!
    STP     X16, X17, [SP, #-0x10]!
    STP     X18, X19, [SP, #-0x10]!
    STP     X20, X21, [SP, #-0x10]!
    STP     X22, X23, [SP, #-0x10]!
    STP     X24, X25, [SP, #-0x10]!
    STP     X26, X27, [SP, #-0x10]!
    STP     X28, X29, [SP, #-0x10]!
    STP     X30, XZR, [SP, #-0x10]!
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 8: 预处理配置

```asm
    /* Save the SPSR. */
#if defined( GUEST )
    MRS     X3, SPSR_EL1
    MRS     X2, ELR_EL1
#else
    MRS     X3, SPSR_EL3
    /* Save the ELR. */
    MRS     X2, ELR_EL3
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 9: 代码片段 9

```asm
    STP     X2, X3, [SP, #-0x10]!
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 10: 代码片段 10

```asm
    /* Save the critical section nesting depth. */
    LDR     X0, ullCriticalNestingConst
    LDR     X3, [X0]
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 11: 代码片段 11

```asm
    /* Save the FPU context indicator. */
    LDR     X0, ullPortTaskHasFPUContextConst
    LDR     X2, [X0]
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 12: 代码片段 12

```asm
    /* Save the FPU context, if any (32 128-bit plus two 64-bit status registers). */
    CMP     X2, #0
    B.EQ    1f
    STP     Q0, Q1, [SP,#-0x20]!
    STP     Q2, Q3, [SP,#-0x20]!
    STP     Q4, Q5, [SP,#-0x20]!
    STP     Q6, Q7, [SP,#-0x20]!
    STP     Q8, Q9, [SP,#-0x20]!
    STP     Q10, Q11, [SP,#-0x20]!
    STP     Q12, Q13, [SP,#-0x20]!
    STP     Q14, Q15, [SP,#-0x20]!
    STP     Q16, Q17, [SP,#-0x20]!
    STP     Q18, Q19, [SP,#-0x20]!
    STP     Q20, Q21, [SP,#-0x20]!
    STP     Q22, Q23, [SP,#-0x20]!
    STP     Q24, Q25, [SP,#-0x20]!
    STP     Q26, Q27, [SP,#-0x20]!
    STP     Q28, Q29, [SP,#-0x20]!
    STP     Q30, Q31, [SP,#-0x20]!
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 13: 代码片段 13

```asm
    /* Even though upper 32 bits of FPSR and FPCR are reserved, save and restore the whole 64 bits to keep 16-byte SP alignement. */
    MRS     X9, FPSR
    MRS     X10, FPCR
    STP     X9, X10, [SP, #-0x10]!
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 14: 代码片段 14

```asm
1:
    /* Store the critical nesting count and FPU context indicator. */
    STP     X2, X3, [SP, #-0x10]!
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 15: 代码片段 15

```asm
    LDR     X0, pxCurrentTCBConst
    LDR     X1, [X0]
    MOV     X0, SP   /* Move SP into X0 for saving. */
    STR     X0, [X1]
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 16: 代码片段 16

```asm
    /* Switch to use the ELx stack pointer. */
    MSR     SPSEL, #1
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 17: 代码片段 17

```asm
    .endm
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 18: 代码片段 18

```asm
; /**********************************************************************/
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 19: 代码片段 19

```asm
.macro portRESTORE_CONTEXT
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 20: 代码片段 20

```asm
    /* Switch to use the EL0 stack pointer. */
    MSR     SPSEL, #0
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 21: 代码片段 21

```asm
    /* Set the SP to point to the stack of the task being restored. */
    LDR     X0, pxCurrentTCBConst
    LDR     X1, [X0]
    LDR     X0, [X1]
    MOV     SP, X0
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 22: 代码片段 22

```asm
    LDP     X2, X3, [SP], #0x10  /* Critical nesting and FPU context. */
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 23: 代码片段 23

```asm
    /* Set the PMR register to be correct for the current critical nesting
    depth. */
    LDR     X0, ullCriticalNestingConst /* X0 holds the address of ullCriticalNesting. */
    MOV     X1, #255                    /* X1 holds the unmask value. */
    CMP     X3, #0
    B.EQ    1f
    LDR     X6, ullMaxAPIPriorityMaskConst
    LDR     X1, [X6]                    /* X1 holds the mask value. */
1:
    MSR     s3_0_c4_c6_0, X1            /* Write the mask value to ICCPMR. s3_0_c4_c6_0 is ICC_PMR_EL1. */
    DSB     SY                          /* _RB_Barriers probably not required here. */
    ISB     SY
    STR     X3, [X0]                    /* Restore the task's critical nesting count. */
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 24: 代码片段 24

```asm
    /* Restore the FPU context indicator. */
    LDR     X0, ullPortTaskHasFPUContextConst
    STR     X2, [X0]
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 25: 代码片段 25

```asm
    /* Restore the FPU context, if any. */
    CMP     X2, #0
    B.EQ    1f
    LDP     X9, X10, [SP], #0x10
    LDP     Q30, Q31, [SP], #0x20
    LDP     Q28, Q29, [SP], #0x20
    LDP     Q26, Q27, [SP], #0x20
    LDP     Q24, Q25, [SP], #0x20
    LDP     Q22, Q23, [SP], #0x20
    LDP     Q20, Q21, [SP], #0x20
    LDP     Q18, Q19, [SP], #0x20
    LDP     Q16, Q17, [SP], #0x20
    LDP     Q14, Q15, [SP], #0x20
    LDP     Q12, Q13, [SP], #0x20
    LDP     Q10, Q11, [SP], #0x20
    LDP     Q8, Q9, [SP], #0x20
    LDP     Q6, Q7, [SP], #0x20
    LDP     Q4, Q5, [SP], #0x20
    LDP     Q2, Q3, [SP], #0x20
    LDP     Q0, Q1, [SP], #0x20
    MSR     FPSR, X9
    MSR     FPCR, X10
1:
    LDP     X2, X3, [SP], #0x10  /* SPSR and ELR. */
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 26: 预处理配置

```asm
#if defined( GUEST )
    /* Restore the SPSR. */
    MSR     SPSR_EL1, X3
    /* Restore the ELR. */
    MSR     ELR_EL1, X2
#else
    /* Restore the SPSR. */
    MSR     SPSR_EL3, X3 /*_RB_ Assumes started in EL3. */
    /* Restore the ELR. */
    MSR     ELR_EL3, X2
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 27: 代码片段 27

```asm
    LDP     X30, XZR, [SP], #0x10
    LDP     X28, X29, [SP], #0x10
    LDP     X26, X27, [SP], #0x10
    LDP     X24, X25, [SP], #0x10
    LDP     X22, X23, [SP], #0x10
    LDP     X20, X21, [SP], #0x10
    LDP     X18, X19, [SP], #0x10
    LDP     X16, X17, [SP], #0x10
    LDP     X14, X15, [SP], #0x10
    LDP     X12, X13, [SP], #0x10
    LDP     X10, X11, [SP], #0x10
    LDP     X8, X9, [SP], #0x10
    LDP     X6, X7, [SP], #0x10
    LDP     X4, X5, [SP], #0x10
    LDP     X2, X3, [SP], #0x10
    LDP     X0, X1, [SP], #0x10
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 28: 代码片段 28

```asm
    /* Switch to use the ELx stack pointer.  _RB_ Might not be required. */
    MSR     SPSEL, #1
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 29: 代码片段 29

```asm
    ERET
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 30: 代码片段 30

```asm
    .endm
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 31: 汇编标签 FreeRTOS_SWI_Handler

```asm

/******************************************************************************
 * FreeRTOS_SWI_Handler handler is used to perform a context switch.
 *****************************************************************************/
.align 8
.type FreeRTOS_SWI_Handler, %function
FreeRTOS_SWI_Handler:
    /* Save the context of the current task and select a new task to run. */
    portSAVE_CONTEXT
#if defined( GUEST )
    MRS     X0, ESR_EL1
#else
    MRS     X0, ESR_EL3
#endif
```

**解说：** 这一段是汇编标签 `FreeRTOS_SWI_Handler` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 32: 代码片段 32

```asm
    LSR     X1, X0, #26
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 33: 预处理配置

```asm
#if defined( GUEST )
    CMP     X1, #0x15   /* 0x15 = SVC instruction. */
#else
    CMP     X1, #0x17   /* 0x17 = SMC instruction. */
#endif
    B.NE    FreeRTOS_Abort
    BL      vTaskSwitchContext
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 34: 代码片段 34

```asm
    portRESTORE_CONTEXT
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 35: 汇编标签 FreeRTOS_Abort

```asm
FreeRTOS_Abort:
    /* Full ESR is in X0, exception class code is in X1. */
    B       .
```

**解说：** 这一段是汇编标签 `FreeRTOS_Abort` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 36: 汇编标签 vPortRestoreTaskContext

```asm
/******************************************************************************
 * vPortRestoreTaskContext is used to start the scheduler.
 *****************************************************************************/
.align 8
.type vPortRestoreTaskContext, %function
vPortRestoreTaskContext:
.set freertos_vector_base,  _freertos_vector_table
```

**解说：** 这一段是汇编标签 `vPortRestoreTaskContext` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 37: 代码片段 37

```asm
    /* Install the FreeRTOS interrupt handlers. */
    LDR     X1, =freertos_vector_base
#if defined( GUEST )
    MSR     VBAR_EL1, X1
#else
    MSR     VBAR_EL3, X1
#endif
    DSB     SY
    ISB     SY
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 38: 代码片段 38

```asm
    /* Start the first task. */
    portRESTORE_CONTEXT
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 39: 说明性注释

```asm

/******************************************************************************
 * FreeRTOS_IRQ_Handler handles IRQ entry and exit.
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：FreeRTOS_IRQ_Handler handles IRQ entry and exit.。

## 片段 40: 汇编标签 FreeRTOS_IRQ_Handler

```asm
 * This handler is supposed to be used only for IRQs and never for FIQs. Per ARM
 * GIC documentation [1], Group 0 interrupts are always signaled as FIQs. Since
 * this handler is only for IRQs, We can safely assume Group 1 while accessing
 * Interrupt Acknowledge and End Of Interrupt registers and therefore, use
 * ICC_IAR1_EL1 and ICC_EOIR1_EL1.
 *
 * [1] https://developer.arm.com/documentation/198123/0300/Arm-CoreLink-GIC-fundamentals
 *****************************************************************************/
.align 8
.type FreeRTOS_IRQ_Handler, %function
FreeRTOS_IRQ_Handler:
    /* Save volatile registers. */
    STP     X0, X1, [SP, #-0x10]!
    STP     X2, X3, [SP, #-0x10]!
    STP     X4, X5, [SP, #-0x10]!
    STP     X6, X7, [SP, #-0x10]!
    STP     X8, X9, [SP, #-0x10]!
    STP     X10, X11, [SP, #-0x10]!
    STP     X12, X13, [SP, #-0x10]!
    STP     X14, X15, [SP, #-0x10]!
    STP     X16, X17, [SP, #-0x10]!
    STP     X18, X19, [SP, #-0x10]!
    STP     X29, X30, [SP, #-0x10]!
```

**解说：** 这一段是汇编标签 `FreeRTOS_IRQ_Handler` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 41: 预处理配置

```asm
    /* Save the SPSR and ELR. */
#if defined( GUEST )
    MRS     X3, SPSR_EL1
    MRS     X2, ELR_EL1
#else
    MRS     X3, SPSR_EL3
    MRS     X2, ELR_EL3
#endif
    STP     X2, X3, [SP, #-0x10]!
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 42: 代码片段 42

```asm
    /* Increment the interrupt nesting counter. */
    LDR     X5, ullPortInterruptNestingConst
    LDR     X1, [X5]    /* Old nesting count in X1. */
    ADD     X6, X1, #1
    STR     X6, [X5]    /* Address of nesting count variable in X5. */
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 43: 代码片段 43

```asm
    /* Maintain the interrupt nesting information across the function call. */
    STP     X1, X5, [SP, #-0x10]!
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 44: 代码片段 44

```asm
    /* Read interrupt ID from the interrupt acknowledge register and store it
    in X0 for future parameter and interrupt clearing use. */
    MRS     X0, S3_0_C12_C12_0  /* S3_0_C12_C12_0 is ICC_IAR1_EL1. */
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 45: 代码片段 45

```asm
    /* Maintain the interrupt ID value across the function call. */
    STP     X0, X1, [SP, #-0x10]!
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 46: 代码片段 46

```asm
    /* Call the C handler. */
    BL vApplicationIRQHandler
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 47: 代码片段 47

```asm
    /* Disable interrupts. */
    MSR     DAIFSET, #2
    DSB     SY
    ISB     SY
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 48: 代码片段 48

```asm
    /* Restore the interrupt ID value. */
    LDP     X0, X1, [SP], #0x10
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 49: 代码片段 49

```asm
    /* End IRQ processing by writing interrupt ID value to the EOI register. */
    MSR     S3_0_C12_C12_1, X0  /* S3_0_C12_C12_1 is ICC_EOIR1_EL1. */
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 50: 代码片段 50

```asm
    /* Restore the critical nesting count. */
    LDP     X1, X5, [SP], #0x10
    STR     X1, [X5]
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 51: 代码片段 51

```asm
    /* Has interrupt nesting unwound? */
    CMP     X1, #0
    B.NE    Exit_IRQ_No_Context_Switch
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 52: 代码片段 52

```asm
    /* Is a context switch required? */
    LDR     X0, ullPortYieldRequiredConst
    LDR     X1, [X0]
    CMP     X1, #0
    B.EQ    Exit_IRQ_No_Context_Switch
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 53: 代码片段 53

```asm
    /* Reset ullPortYieldRequired to 0. */
    MOV     X2, #0
    STR     X2, [X0]
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 54: 代码片段 54

```asm
    /* Restore volatile registers. */
    LDP     X4, X5, [SP], #0x10  /* SPSR and ELR. */
#if defined( GUEST )
    MSR     SPSR_EL1, X5
    MSR     ELR_EL1, X4
#else
    MSR     SPSR_EL3, X5 /*_RB_ Assumes started in EL3. */
    MSR     ELR_EL3, X4
#endif
    DSB     SY
    ISB     SY
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 55: 代码片段 55

```asm
    LDP     X29, X30, [SP], #0x10
    LDP     X18, X19, [SP], #0x10
    LDP     X16, X17, [SP], #0x10
    LDP     X14, X15, [SP], #0x10
    LDP     X12, X13, [SP], #0x10
    LDP     X10, X11, [SP], #0x10
    LDP     X8, X9, [SP], #0x10
    LDP     X6, X7, [SP], #0x10
    LDP     X4, X5, [SP], #0x10
    LDP     X2, X3, [SP], #0x10
    LDP     X0, X1, [SP], #0x10
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 56: 代码片段 56

```asm
    /* Save the context of the current task and select a new task to run. */
    portSAVE_CONTEXT
    BL vTaskSwitchContext
    portRESTORE_CONTEXT
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 57: 汇编标签 Exit_IRQ_No_Context_Switch

```asm
Exit_IRQ_No_Context_Switch:
    /* Restore volatile registers. */
    LDP     X4, X5, [SP], #0x10  /* SPSR and ELR. */
#if defined( GUEST )
    MSR     SPSR_EL1, X5
    MSR     ELR_EL1, X4
#else
    MSR     SPSR_EL3, X5 /*_RB_ Assumes started in EL3. */
    MSR     ELR_EL3, X4
#endif
    DSB     SY
    ISB     SY
```

**解说：** 这一段是汇编标签 `Exit_IRQ_No_Context_Switch` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 58: 代码片段 58

```asm
    LDP     X29, X30, [SP], #0x10
    LDP     X18, X19, [SP], #0x10
    LDP     X16, X17, [SP], #0x10
    LDP     X14, X15, [SP], #0x10
    LDP     X12, X13, [SP], #0x10
    LDP     X10, X11, [SP], #0x10
    LDP     X8, X9, [SP], #0x10
    LDP     X6, X7, [SP], #0x10
    LDP     X4, X5, [SP], #0x10
    LDP     X2, X3, [SP], #0x10
    LDP     X0, X1, [SP], #0x10
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 59: 代码片段 59

```asm
    ERET
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 60: 说明性注释

```asm
/******************************************************************************
 * If the application provides an implementation of vApplicationIRQHandler(),
 * then it will get called directly without saving the FPU registers on
 * interrupt entry, and this weak implementation of
 * vApplicationIRQHandler() will not get called.
 *
 * If the application provides its own implementation of
 * vApplicationFPUSafeIRQHandler() then this implementation of
 * vApplicationIRQHandler() will be called, save the FPU registers, and then
 * call vApplicationFPUSafeIRQHandler().
 *
 * Therefore, if the application writer wants FPU registers to be saved on
 * interrupt entry their IRQ handler must be called
 * vApplicationFPUSafeIRQHandler(), and if the application writer does not want
 * FPU registers to be saved on interrupt entry their IRQ handler must be
 * called vApplicationIRQHandler().
 *****************************************************************************/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：If the application provides an implementation of vApplicationIRQHandler(), then it will get called directly without saving the FPU registers on interrupt entry, and this weak implementation of vApplicationIRQHandler() will not get called. I。

## 片段 61: 汇编标签 vApplicationIRQHandler

```asm
.align 8
.weak vApplicationIRQHandler
.type vApplicationIRQHandler, %function
vApplicationIRQHandler:
    /* Save LR and FP on the stack */
    STP     X29, X30, [SP, #-0x10]!
```

**解说：** 这一段是汇编标签 `vApplicationIRQHandler` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 62: 代码片段 62

```asm
    /* Save FPU registers (32 128-bits + 2 64-bits configuration and status registers) */
    STP     Q0, Q1, [SP,#-0x20]!
    STP     Q2, Q3, [SP,#-0x20]!
    STP     Q4, Q5, [SP,#-0x20]!
    STP     Q6, Q7, [SP,#-0x20]!
    STP     Q8, Q9, [SP,#-0x20]!
    STP     Q10, Q11, [SP,#-0x20]!
    STP     Q12, Q13, [SP,#-0x20]!
    STP     Q14, Q15, [SP,#-0x20]!
    STP     Q16, Q17, [SP,#-0x20]!
    STP     Q18, Q19, [SP,#-0x20]!
    STP     Q20, Q21, [SP,#-0x20]!
    STP     Q22, Q23, [SP,#-0x20]!
    STP     Q24, Q25, [SP,#-0x20]!
    STP     Q26, Q27, [SP,#-0x20]!
    STP     Q28, Q29, [SP,#-0x20]!
    STP     Q30, Q31, [SP,#-0x20]!
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 63: 代码片段 63

```asm
    /* Even though upper 32 bits of FPSR and FPCR are reserved, save and restore the whole 64 bits to keep 16-byte SP alignement. */
    MRS     X9, FPSR
    MRS     X10, FPCR
    STP     X9, X10, [SP, #-0x10]!
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 64: 代码片段 64

```asm
    /* Call the C handler. */
    BL vApplicationFPUSafeIRQHandler
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 65: 说明性注释

```asm
    /* Restore FPU registers */
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：Restore FPU registers。

## 片段 66: 代码片段 66

```asm
    LDP     X9, X10, [SP], #0x10
    LDP     Q30, Q31, [SP], #0x20
    LDP     Q28, Q29, [SP], #0x20
    LDP     Q26, Q27, [SP], #0x20
    LDP     Q24, Q25, [SP], #0x20
    LDP     Q22, Q23, [SP], #0x20
    LDP     Q20, Q21, [SP], #0x20
    LDP     Q18, Q19, [SP], #0x20
    LDP     Q16, Q17, [SP], #0x20
    LDP     Q14, Q15, [SP], #0x20
    LDP     Q12, Q13, [SP], #0x20
    LDP     Q10, Q11, [SP], #0x20
    LDP     Q8, Q9, [SP], #0x20
    LDP     Q6, Q7, [SP], #0x20
    LDP     Q4, Q5, [SP], #0x20
    LDP     Q2, Q3, [SP], #0x20
    LDP     Q0, Q1, [SP], #0x20
    MSR     FPSR, X9
    MSR     FPCR, X10
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 67: 代码片段 67

```asm
    /* Restore FP and LR */
    LDP     X29, X30, [SP], #0x10
    RET
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 68: 汇编标签 pxCurrentTCBConst

```asm
.align 8
pxCurrentTCBConst: .dword pxCurrentTCB
ullCriticalNestingConst: .dword ullCriticalNesting
ullPortTaskHasFPUContextConst: .dword ullPortTaskHasFPUContext
```

**解说：** 这一段是汇编标签 `pxCurrentTCBConst` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 69: 汇编标签 ullMaxAPIPriorityMaskConst

```asm
ullMaxAPIPriorityMaskConst: .dword ullMaxAPIPriorityMask
ullPortInterruptNestingConst: .dword ullPortInterruptNesting
ullPortYieldRequiredConst: .dword ullPortYieldRequired
```

**解说：** 这一段是汇编标签 `ullMaxAPIPriorityMaskConst` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 70: 代码片段 70

```asm
.end
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。
