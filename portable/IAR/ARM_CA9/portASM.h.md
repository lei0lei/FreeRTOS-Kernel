# portASM.h 代码解说

源文件：`portable/IAR/ARM_CA9/portASM.h`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 代码片段 1

```c
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

    EXTERN  vTaskSwitchContext
    EXTERN  ulCriticalNesting
    EXTERN  pxCurrentTCB
    EXTERN  ulPortTaskHasFPUContext
    EXTERN  ulAsmAPIPriorityMask

portSAVE_CONTEXT macro

    ; Save the LR and SPSR onto the system mode stack before switching to
    ; system mode to save the remaining system mode registers
    SRSDB   sp!, #SYS_MODE
    CPS     #SYS_MODE
    PUSH    {R0-R12, R14}
```

**解说：** 这一段是 `portASM.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 2: 代码片段 2

```c
    ; Push the critical nesting count
    LDR     R2, =ulCriticalNesting
    LDR     R1, [R2]
    PUSH    {R1}
```

**解说：** 这一段是 `portASM.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 3: 代码片段 3

```c
    ; Does the task have a floating point context that needs saving?  If
    ; ulPortTaskHasFPUContext is 0 then no.
    LDR     R2, =ulPortTaskHasFPUContext
    LDR     R3, [R2]
    CMP     R3, #0

    ; Save the floating point context, if any
    FMRXNE  R1,  FPSCR
    VPUSHNE {D0-D15}
```

**解说：** 这一段是 `portASM.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 代码片段 4

```c
    VPUSHNE {D16-D31}
    PUSHNE  {R1}
    ; Save ulPortTaskHasFPUContext itself
    PUSH    {R3}
```

**解说：** 这一段是 `portASM.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 5: 代码片段 7

```c
    ; Save the stack pointer in the TCB
    LDR     R0, =pxCurrentTCB
    LDR     R1, [R0]
    STR     SP, [R1]

    endm

; /**********************************************************************/

portRESTORE_CONTEXT macro

    ; Set the SP to point to the stack of the task being restored.
    LDR     R0, =pxCurrentTCB
    LDR     R1, [R0]
    LDR     SP, [R1]

    ; Is there a floating point context to restore?  If the restored
    ; ulPortTaskHasFPUContext is zero then no.
    LDR     R0, =ulPortTaskHasFPUContext
    POP     {R1}
```

**解说：** 这一段是 `portASM.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 6: 代码片段 6

```c
    STR     R1, [R0]
    CMP     R1, #0

    ; Restore the floating point context, if any
    POPNE   {R0}
    VPOPNE  {D16-D31}
    VPOPNE  {D0-D15}
    VMSRNE  FPSCR, R0

    ; Restore the critical section nesting depth
    LDR     R0, =ulCriticalNesting
    POP     {R1}
```

**解说：** 这一段是 `portASM.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 7: 代码片段 12

```c
    STR     R1, [R0]

    ; Ensure the priority mask is correct for the critical nesting depth
    LDR     R2, =portICCPMR_PRIORITY_MASK_REGISTER_ADDRESS
    CMP     R1, #0
    MOVEQ   R4, #255
    LDRNE   R4, =( configMAX_API_CALL_INTERRUPT_PRIORITY << portPRIORITY_SHIFT )
    STR     R4, [r2]

    ; Restore all system mode registers other than the SP (which is already
    ; being used)
    POP     {R0-R12, R14}
```

**解说：** 这一段是 `portASM.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 8: 代码片段 8

```c
    ; Return to the task code, loading CPSR on the way.
    RFEIA   sp!

    endm
```

**解说：** 这一段是 `portASM.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。
