# portASM.s 代码解说

源文件：`portable/RVDS/ARM_CA9/portASM.s`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 代码片段 1

```asm
;/*
; * FreeRTOS Kernel <DEVELOPMENT BRANCH>
; * Copyright (C) 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
; *
; * SPDX-License-Identifier: MIT
; *
; * Permission is hereby granted, free of charge, to any person obtaining a copy of
; * this software and associated documentation files (the "Software"), to deal in
; * the Software without restriction, including without limitation the rights to
; * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
; * the Software, and to permit persons to whom the Software is furnished to do so,
; * subject to the following conditions:
; *
; * The above copyright notice and this permission notice shall be included in all
; * copies or substantial portions of the Software.
; *
; * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
; * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
; * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
; * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
; * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
; * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
; *
; * https://www.FreeRTOS.org
; * https://github.com/FreeRTOS
; *
; */
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 2: 代码片段 2

```asm
    INCLUDE portmacro.inc
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 3: 代码片段 3

```asm
    IMPORT  vApplicationIRQHandler
    IMPORT  vTaskSwitchContext
    IMPORT  ulPortYieldRequired
    IMPORT  ulPortInterruptNesting
    IMPORT  vTaskSwitchContext
    IMPORT  ulICCIAR
    IMPORT  ulICCEOIR
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 代码片段 4

```asm
    EXPORT  FreeRTOS_SWI_Handler
    EXPORT  FreeRTOS_IRQ_Handler
    EXPORT  vPortRestoreTaskContext
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 5: 代码片段 5

```asm
    ARM
    AREA    PORT_ASM, CODE, READONLY
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 6: 代码片段 6

```asm

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; SVC handler is used to yield a task.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
FreeRTOS_SWI_Handler
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 7: 代码片段 7

```asm
    PRESERVE8
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 8: 代码片段 8

```asm
    ; Save the context of the current task and select a new task to run.
    portSAVE_CONTEXT
    LDR R0, =vTaskSwitchContext
    BLX R0
    portRESTORE_CONTEXT
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 9: 代码片段 9

```asm
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; vPortRestoreTaskContext is used to start the scheduler.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
vPortRestoreTaskContext
    ; Switch to system mode
    CPS     #SYS_MODE
    portRESTORE_CONTEXT
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 10: 代码片段 10

```asm
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; PL390 GIC interrupt handler
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
FreeRTOS_IRQ_Handler
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 11: 代码片段 11

```asm
    ; Return to the interrupted instruction.
    SUB     lr, lr, #4
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 12: 代码片段 12

```asm
    ; Push the return address and SPSR
    PUSH    {lr}
    MRS     lr, SPSR
    PUSH    {lr}
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 13: 代码片段 13

```asm
    ; Change to supervisor mode to allow reentry.
    CPS     #SVC_MODE
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 14: 代码片段 14

```asm
    ; Push used registers.
    PUSH    {r0-r4, r12}
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 15: 代码片段 15

```asm
    ; Increment nesting count.  r3 holds the address of ulPortInterruptNesting
    ; for future use.  r1 holds the original ulPortInterruptNesting value for
    ; future use.
    LDR     r3, =ulPortInterruptNesting
    LDR     r1, [r3]
    ADD     r4, r1, #1
    STR     r4, [r3]
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 16: 代码片段 16

```asm
    ; Read value from the interrupt acknowledge register, which is stored in r0
    ; for future parameter and interrupt clearing use.
    LDR     r2, =ulICCIAR
    LDR     r0, [r2]
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 17: 代码片段 17

```asm
    ; Ensure bit 2 of the stack pointer is clear.  r2 holds the bit 2 value for
    ; future use.  _RB_ Does this ever actually need to be done provided the
    ; start of the stack is 8-byte aligned?
    MOV     r2, sp
    AND     r2, r2, #4
    SUB     sp, sp, r2
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 18: 代码片段 18

```asm
    ; Call the interrupt handler.  r4 is pushed to maintain alignment.
    PUSH    {r0-r4, lr}
    LDR     r1, =vApplicationIRQHandler
    BLX     r1
    POP     {r0-r4, lr}
    ADD     sp, sp, r2
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 19: 代码片段 19

```asm
    CPSID   i
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 20: 代码片段 20

```asm
    ; Write the value read from ICCIAR to ICCEOIR
    LDR     r4, =ulICCEOIR
    STR     r0, [r4]
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 21: 代码片段 21

```asm
    ; Restore the old nesting count
    STR     r1, [r3]
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 22: 代码片段 22

```asm
    ; A context switch is never performed if the nesting count is not 0
    CMP     r1, #0
    BNE     exit_without_switch
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 23: 代码片段 23

```asm
    ; Did the interrupt request a context switch?  r1 holds the address of
    ; ulPortYieldRequired and r0 the value of ulPortYieldRequired for future
    ; use.
    LDR     r1, =ulPortYieldRequired
    LDR     r0, [r1]
    CMP     r0, #0
    BNE     switch_before_exit
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 24: 代码片段 24

```asm
exit_without_switch
    ; No context switch.  Restore used registers, LR_irq and SPSR before
    ; returning.
    POP     {r0-r4, r12}
    CPS     #IRQ_MODE
    POP     {LR}
    MSR     SPSR_cxsf, LR
    POP     {LR}
    MOVS    PC, LR
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 25: 代码片段 25

```asm
switch_before_exit
    ; A context switch is to be performed.  Clear the context switch pending
    ; flag.
    MOV     r0, #0
    STR     r0, [r1]
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 26: 代码片段 26

```asm
    ; Restore used registers, LR-irq and SPSR before saving the context
    ; to the task stack.
    POP     {r0-r4, r12}
    CPS     #IRQ_MODE
    POP     {LR}
    MSR     SPSR_cxsf, LR
    POP     {LR}
    portSAVE_CONTEXT
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 27: 代码片段 27

```asm
    ; Call the function that selects the new task to execute.
    ; vTaskSwitchContext() if vTaskSwitchContext() uses LDRD or STRD
    ; instructions, or 8 byte aligned stack allocated data.  LR does not need
    ; saving as a new LR will be loaded by portRESTORE_CONTEXT anyway.
    LDR     r0, =vTaskSwitchContext
    BLX     r0
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 28: 代码片段 28

```asm
    ; Restore the context of, and branch to, the task selected to execute next.
    portRESTORE_CONTEXT
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 29: 代码片段 29

```asm

    END
```

**解说：** 这一段是 `portASM.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。
