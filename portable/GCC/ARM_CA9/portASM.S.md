# portASM.S 代码解说

源文件：`portable/GCC/ARM_CA9/portASM.S`

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
    .eabi_attribute Tag_ABI_align_preserved, 1
    .text
    .arm
```

**解说：** 这一段是文件头，说明项目归属、许可证和免责条款；它告诉使用者这个文件按 MIT 许可证发布。

## 片段 2: 代码片段 2

```asm
    .set SYS_MODE,  0x1f
    .set SVC_MODE,  0x13
    .set IRQ_MODE,  0x12
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 3: 代码片段 3

```asm
    /* Hardware registers addresses. */
    .extern ulICCIARAddress
    .extern ulICCEOIRAddress
    .extern ulICCPMRAddress
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 代码片段 4

```asm
    /* Variables and functions. */
    .extern ulMaxAPIPriorityMask
    .extern _freertos_vector_table
    .extern pxCurrentTCB
    .extern vTaskSwitchContext
    .extern vApplicationIRQHandler
    .extern ulPortInterruptNesting
    .extern ulPortTaskHasFPUContext
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 5: 代码片段 5

```asm
    .global FreeRTOS_IRQ_Handler
    .global FreeRTOS_SWI_Handler
    .global vPortRestoreTaskContext
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 7: 代码片段 7

```asm

.macro portSAVE_CONTEXT
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 8: 代码片段 8

```asm
    /* Save the LR and SPSR onto the system mode stack before switching to
    system mode to save the remaining system mode registers. */
    SRSDB   sp!, #SYS_MODE
    CPS     #SYS_MODE
    PUSH    {R0-R12, R14}
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 9: 代码片段 9

```asm
    /* Push the critical nesting count. */
    LDR     R2, ulCriticalNestingConst
    LDR     R1, [R2]
    PUSH    {R1}
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 10: 代码片段 10

```asm
    /* Does the task have a floating point context that needs saving?  If
    ulPortTaskHasFPUContext is 0 then no. */
    LDR     R2, ulPortTaskHasFPUContextConst
    LDR     R3, [R2]
    CMP     R3, #0
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 11: 代码片段 11

```asm
    /* Save the floating point context, if any. */
    FMRXNE  R1,  FPSCR
    PUSHNE  {R1}
    VPUSHNE {D0-D15}
    VPUSHNE {D16-D31}
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 12: 代码片段 12

```asm
    /* Save ulPortTaskHasFPUContext itself. */
    PUSH    {R3}
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 13: 代码片段 13

```asm
    /* Save the stack pointer in the TCB. */
    LDR     R0, pxCurrentTCBConst
    LDR     R1, [R0]
    STR     SP, [R1]
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 14: 代码片段 14

```asm
    .endm
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 15: 代码片段 15

```asm
; /**********************************************************************/
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 16: 代码片段 16

```asm
.macro portRESTORE_CONTEXT
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 17: 代码片段 17

```asm
    /* Set the SP to point to the stack of the task being restored. */
    LDR     R0, pxCurrentTCBConst
    LDR     R1, [R0]
    LDR     SP, [R1]
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 18: 代码片段 18

```asm
    /* Is there a floating point context to restore?  If the restored
    ulPortTaskHasFPUContext is zero then no. */
    LDR     R0, ulPortTaskHasFPUContextConst
    POP     {R1}
    STR     R1, [R0]
    CMP     R1, #0
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 19: 代码片段 19

```asm
    /* Restore the floating point context, if any. */
    VPOPNE  {D16-D31}
    VPOPNE  {D0-D15}
    POPNE   {R0}
    VMSRNE  FPSCR, R0
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 20: 代码片段 20

```asm
    /* Restore the critical section nesting depth. */
    LDR     R0, ulCriticalNestingConst
    POP     {R1}
    STR     R1, [R0]
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 21: 代码片段 21

```asm
    /* Ensure the priority mask is correct for the critical nesting depth. */
    LDR     R2, ulICCPMRConst
    LDR     R2, [R2]
    CMP     R1, #0
    MOVEQ   R4, #255
    LDRNE   R4, ulMaxAPIPriorityMaskConst
    LDRNE   R4, [R4]
    STR     R4, [R2]
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 22: 代码片段 22

```asm
    /* Restore all system mode registers other than the SP (which is already
    being used). */
    POP     {R0-R12, R14}
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 23: 代码片段 23

```asm
    /* Return to the task code, loading CPSR on the way. */
    RFEIA   sp!
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 24: 代码片段 24

```asm
    .endm
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 26: 汇编标签 FreeRTOS_SWI_Handler

```asm

/******************************************************************************
 * SVC handler is used to start the scheduler.
 *****************************************************************************/
.align 4
.type FreeRTOS_SWI_Handler, %function
FreeRTOS_SWI_Handler:
    /* Save the context of the current task and select a new task to run. */
    portSAVE_CONTEXT
```

**解说：** 这一段是汇编标签 `FreeRTOS_SWI_Handler` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 27: 代码片段 27

```asm
    /* Ensure bit 2 of the stack pointer is clear. */
    MOV     r2, sp
    AND     r2, r2, #4
    SUB     sp, sp, r2
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 28: 代码片段 28

```asm
    LDR R0, vTaskSwitchContextConst
    BLX R0
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 29: 代码片段 29

```asm
    portRESTORE_CONTEXT
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 30: 汇编标签 vPortRestoreTaskContext

```asm

/******************************************************************************
 * vPortRestoreTaskContext is used to start the scheduler.
 *****************************************************************************/
.type vPortRestoreTaskContext, %function
vPortRestoreTaskContext:
    /* Switch to system mode. */
    CPS     #SYS_MODE
    portRESTORE_CONTEXT
```

**解说：** 这一段是汇编标签 `vPortRestoreTaskContext` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 31: 汇编标签 FreeRTOS_IRQ_Handler

```asm
.align 4
.type FreeRTOS_IRQ_Handler, %function
FreeRTOS_IRQ_Handler:
    /* Return to the interrupted instruction. */
    SUB     lr, lr, #4
```

**解说：** 这一段是汇编标签 `FreeRTOS_IRQ_Handler` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 32: 代码片段 32

```asm
    /* Push the return address and SPSR. */
    PUSH    {lr}
    MRS     lr, SPSR
    PUSH    {lr}
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 33: 代码片段 33

```asm
    /* Change to supervisor mode to allow reentry. */
    CPS     #SVC_MODE
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 34: 代码片段 34

```asm
    /* Push used registers. */
    PUSH    {r0-r4, r12}
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 35: 代码片段 35

```asm
    /* Increment nesting count.  r3 holds the address of ulPortInterruptNesting
    for future use.  r1 holds the original ulPortInterruptNesting value for
    future use. */
    LDR     r3, ulPortInterruptNestingConst
    LDR     r1, [r3]
    ADD     r4, r1, #1
    STR     r4, [r3]
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 36: 代码片段 36

```asm
    /* Read value from the interrupt acknowledge register, which is stored in r0
    for future parameter and interrupt clearing use. */
    LDR     r2, ulICCIARConst
    LDR     r2, [r2]
    LDR     r0, [r2]
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 37: 代码片段 37

```asm
    /* Ensure bit 2 of the stack pointer is clear.  r2 holds the bit 2 value for
    future use.  _RB_ Does this ever actually need to be done provided the start
    of the stack is 8-byte aligned? */
    MOV     r2, sp
    AND     r2, r2, #4
    SUB     sp, sp, r2
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 38: 代码片段 38

```asm
    /* Call the interrupt handler.  r4 pushed to maintain alignment. */
    PUSH    {r0-r4, lr}
    LDR     r1, vApplicationIRQHandlerConst
    BLX     r1
    POP     {r0-r4, lr}
    ADD     sp, sp, r2
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 39: 代码片段 39

```asm
    CPSID   i
    DSB
    ISB
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 40: 代码片段 40

```asm
    /* Write the value read from ICCIAR to ICCEOIR. */
    LDR     r4, ulICCEOIRConst
    LDR     r4, [r4]
    STR     r0, [r4]
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 41: 代码片段 41

```asm
    /* Restore the old nesting count. */
    STR     r1, [r3]
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 42: 代码片段 42

```asm
    /* A context switch is never performed if the nesting count is not 0. */
    CMP     r1, #0
    BNE     exit_without_switch
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 43: 代码片段 43

```asm
    /* Did the interrupt request a context switch?  r1 holds the address of
    ulPortYieldRequired and r0 the value of ulPortYieldRequired for future
    use. */
    LDR     r1, =ulPortYieldRequired
    LDR     r0, [r1]
    CMP     r0, #0
    BNE     switch_before_exit
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 44: 汇编标签 exit_without_switch

```asm
exit_without_switch:
    /* No context switch.  Restore used registers, LR_irq and SPSR before
    returning. */
    POP     {r0-r4, r12}
    CPS     #IRQ_MODE
    POP     {LR}
    MSR     SPSR_cxsf, LR
    POP     {LR}
    MOVS    PC, LR
```

**解说：** 这一段是汇编标签 `exit_without_switch` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 45: 汇编标签 switch_before_exit

```asm
switch_before_exit:
    /* A context switch is to be performed.  Clear the context switch pending
    flag. */
    MOV     r0, #0
    STR     r0, [r1]
```

**解说：** 这一段是汇编标签 `switch_before_exit` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 46: 代码片段 46

```asm
    /* Restore used registers, LR-irq and SPSR before saving the context
    to the task stack. */
    POP     {r0-r4, r12}
    CPS     #IRQ_MODE
    POP     {LR}
    MSR     SPSR_cxsf, LR
    POP     {LR}
    portSAVE_CONTEXT
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 47: 代码片段 47

```asm
    /* Call the function that selects the new task to execute.
    vTaskSwitchContext() if vTaskSwitchContext() uses LDRD or STRD
    instructions, or 8 byte aligned stack allocated data.  LR does not need
    saving as a new LR will be loaded by portRESTORE_CONTEXT anyway.
    Ensure bit 2 of the stack pointer is clear.  r2 holds the bit 2 value for
    future use. */
    MOV     r2, sp
    AND     r2, r2, #4
    SUB     sp, sp, r2
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 48: 代码片段 48

```asm
    LDR     R0, vTaskSwitchContextConst
    BLX     R0
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 49: 代码片段 49

```asm
    /* Restore the context of, and branch to, the task selected to execute
    next. */
    portRESTORE_CONTEXT
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 50: 说明性注释

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

## 片段 51: 汇编标签 vApplicationIRQHandler

```asm
.align 4
.weak vApplicationIRQHandler
.type vApplicationIRQHandler, %function
vApplicationIRQHandler:
    PUSH    {LR}
    FMRX    R1,  FPSCR
    VPUSH   {D0-D7}
    VPUSH   {D16-D31}
    PUSH    {R1}
```

**解说：** 这一段是汇编标签 `vApplicationIRQHandler` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 52: 代码片段 52

```asm
    LDR     r1, vApplicationFPUSafeIRQHandlerConst
    BLX     r1
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 53: 代码片段 53

```asm
    POP     {R0}
    VPOP    {D16-D31}
    VPOP    {D0-D7}
    VMSR    FPSCR, R0
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 54: 代码片段 54

```asm
    POP {PC}
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 55: 汇编标签 ulICCIARConst

```asm

ulICCIARConst:  .word ulICCIARAddress
ulICCEOIRConst: .word ulICCEOIRAddress
ulICCPMRConst: .word ulICCPMRAddress
pxCurrentTCBConst: .word pxCurrentTCB
ulCriticalNestingConst: .word ulCriticalNesting
ulPortTaskHasFPUContextConst: .word ulPortTaskHasFPUContext
ulMaxAPIPriorityMaskConst: .word ulMaxAPIPriorityMask
vTaskSwitchContextConst: .word vTaskSwitchContext
vApplicationIRQHandlerConst: .word vApplicationIRQHandler
ulPortInterruptNestingConst: .word ulPortInterruptNesting
vApplicationFPUSafeIRQHandlerConst: .word vApplicationFPUSafeIRQHandler
```

**解说：** 这一段是汇编标签 `ulICCIARConst` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 56: 代码片段 56

```asm
.end
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。
