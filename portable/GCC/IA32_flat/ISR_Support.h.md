# ISR_Support.h 代码解说

源文件：`portable/GCC/IA32_flat/ISR_Support.h`

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

## 片段 2: 代码片段 2

```c
    .extern ulTopOfSystemStack
    .extern ulInterruptNesting

/*-----------------------------------------------------------*/

.macro portFREERTOS_INTERRUPT_ENTRY

    /* Save general purpose registers. */
    pusha

    /* If ulInterruptNesting is zero the rest of the task context will need
    saving and a stack switch might be required. */
    movl    ulInterruptNesting, %eax
    test    %eax, %eax
    jne     2f

    /* Interrupts are not nested, so save the rest of the task context. */
    .if configSUPPORT_FPU == 1

        /* If the task has a buffer allocated to save the FPU context then
        save the FPU context now. */
        movl    pucPortTaskFPUContextBuffer, %eax
        test    %eax, %eax
        je      1f
        fnsave  ( %eax ) /* Save FLOP context into ucTempFPUBuffer array. */
        fwait

        1:
        /* Save the address of the FPU context, if any. */
        push    pucPortTaskFPUContextBuffer

    .endif /* configSUPPORT_FPU */

    /* Find the TCB. */
    movl    pxCurrentTCB, %eax

    /* Stack location is first item in the TCB. */
    movl    %esp, (%eax)

    /* Switch stacks. */
    movl    ulTopOfSystemStack, %esp
    movl    %esp, %ebp

    2:
    /* Increment nesting count. */
    add     $1, ulInterruptNesting

.endm
/*-----------------------------------------------------------*/

.macro portINTERRUPT_EPILOGUE

    cli
    sub     $1, ulInterruptNesting

    /* If the nesting has unwound to zero. */
    movl    ulInterruptNesting, %eax
    test    %eax, %eax
    jne     2f

    /* If a yield was requested then select a new TCB now. */
    movl    ulPortYieldPending, %eax
    test    %eax, %eax
    je      1f
    movl    $0, ulPortYieldPending
    call    vTaskSwitchContext

    1:
    /* Stack location is first item in the TCB. */
    movl    pxCurrentTCB, %eax
    movl    (%eax), %esp

    .if configSUPPORT_FPU == 1

        /* Restore address of task's FPU context buffer. */
        pop     pucPortTaskFPUContextBuffer

        /* If the task has a buffer allocated in which its FPU context is saved,
        then restore it now. */
        movl    pucPortTaskFPUContextBuffer, %eax
        test    %eax, %eax
        je      1f
        frstor  ( %eax )
        1:
    .endif

    2:
    popa

.endm
/*-----------------------------------------------------------*/

.macro portFREERTOS_INTERRUPT_EXIT

    portINTERRUPT_EPILOGUE
    /* EOI. */
    movl    $0x00, (0xFEE000B0)
    iret

.endm
```

**解说：** 这一段是 `ISR_Support.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。
