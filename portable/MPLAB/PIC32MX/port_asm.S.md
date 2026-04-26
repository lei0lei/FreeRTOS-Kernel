# port_asm.S 代码解说

源文件：`portable/MPLAB/PIC32MX/port_asm.S`

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
#include <xc.h>
#include <sys/asm.h>
#include "ISR_Support.h"
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 代码片段 3

```asm

    .set    nomips16
    .set    noreorder
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 代码片段 4

```asm
    .extern pxCurrentTCB
    .extern vTaskSwitchContext
    .extern vPortIncrementTick
    .extern xISRStackTop
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 5: 代码片段 5

```asm
    .global vPortStartFirstTask
    .global vPortYieldISR
    .global vPortTickInterruptHandler
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 6: 说明性注释

```asm

/******************************************************************/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：/。

## 片段 7: 代码片段 7

```asm
    .set        noreorder
    .set        noat
    .ent        vPortTickInterruptHandler
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 8: 汇编标签 vPortTickInterruptHandler

```asm
vPortTickInterruptHandler:
```

**解说：** 这一段是汇编标签 `vPortTickInterruptHandler` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 9: 代码片段 9

```asm
    portSAVE_CONTEXT
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 10: 代码片段 10

```asm
    jal         vPortIncrementTick
    nop
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 11: 代码片段 11

```asm
    portRESTORE_CONTEXT
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 12: 代码片段 12

```asm
    .end vPortTickInterruptHandler
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 13: 说明性注释

```asm
/******************************************************************/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：/。

## 片段 14: 代码片段 14

```asm
    .set        noreorder
    .set        noat
    .ent        vPortStartFirstTask
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 15: 汇编标签 vPortStartFirstTask

```asm
vPortStartFirstTask:
```

**解说：** 这一段是汇编标签 `vPortStartFirstTask` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 16: 代码片段 16

```asm
    /* Simply restore the context of the highest priority task that has been
    created so far. */
    portRESTORE_CONTEXT
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 17: 代码片段 17

```asm
    .end vPortStartFirstTask
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 19: 说明性注释

```asm
/*******************************************************************/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：/。

## 片段 20: 代码片段 20

```asm
    .set        noreorder
    .set        noat
    .ent        vPortYieldISR
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 21: 汇编标签 vPortYieldISR

```asm
vPortYieldISR:
```

**解说：** 这一段是汇编标签 `vPortYieldISR` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 22: 代码片段 22

```asm
    /* Make room for the context. First save the current status so it can be
    manipulated. */
    addiu       sp, sp, -portCONTEXT_SIZE
    mfc0        k1, _CP0_STATUS
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 23: 代码片段 23

```asm
    /* Also save s6 and s5 so they can be used.  Any nesting interrupts should
    maintain the values of these registers across the ISR. */
    sw          s6, 44(sp)
    sw          s5, 40(sp)
    sw          k1, portSTATUS_STACK_LOCATION(sp)
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 24: 代码片段 24

```asm
    /* Prepare to re-enabled interrupt above the kernel priority. */
    ins         k1, zero, 10, 6
    ori         k1, k1, ( configMAX_SYSCALL_INTERRUPT_PRIORITY << 10 )
    ins         k1, zero, 1, 4
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 25: 代码片段 25

```asm
    /* s5 is used as the frame pointer. */
    add         s5, zero, sp
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 26: 代码片段 26

```asm
    /* Swap to the system stack.  This is not conditional on the nesting
    count as this interrupt is always the lowest priority and therefore
    the nesting is always 0. */
    la          sp, xISRStackTop
    lw          sp, (sp)
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 27: 代码片段 27

```asm
    /* Set the nesting count. */
    la          k0, uxInterruptNesting
    addiu       s6, zero, 1
    sw          s6, 0(k0)
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 28: 代码片段 28

```asm
    /* s6 holds the EPC value, this is saved with the rest of the context
    after interrupts are enabled. */
    mfc0        s6, _CP0_EPC
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 29: 代码片段 29

```asm
    /* Re-enable interrupts above configMAX_SYSCALL_INTERRUPT_PRIORITY. */
    mtc0        k1, _CP0_STATUS
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 30: 代码片段 30

```asm
    /* Save the context into the space just created.  s6 is saved again
    here as it now contains the EPC value. */
    sw          ra, 120(s5)
    sw          s8, 116(s5)
    sw          t9, 112(s5)
    sw          t8, 108(s5)
    sw          t7, 104(s5)
    sw          t6, 100(s5)
    sw          t5, 96(s5)
    sw          t4, 92(s5)
    sw          t3, 88(s5)
    sw          t2, 84(s5)
    sw          t1, 80(s5)
    sw          t0, 76(s5)
    sw          a3, 72(s5)
    sw          a2, 68(s5)
    sw          a1, 64(s5)
    sw          a0, 60(s5)
    sw          v1, 56(s5)
    sw          v0, 52(s5)
    sw          s7, 48(s5)
    sw          s6, portEPC_STACK_LOCATION(s5)
    /* s5 and s6 has already been saved. */
    sw          s4, 36(s5)
    sw          s3, 32(s5)
    sw          s2, 28(s5)
    sw          s1, 24(s5)
    sw          s0, 20(s5)
    sw          $1, 16(s5)
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 31: 代码片段 31

```asm
    /* s7 is used as a scratch register as this should always be saved across
    nesting interrupts. */
    mfhi        s7
    sw          s7, 12(s5)
    mflo        s7
    sw          s7, 8(s5)
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 32: 代码片段 32

```asm
    /* Save the stack pointer to the task. */
    la          s7, pxCurrentTCB
    lw          s7, (s7)
    sw          s5, (s7)
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 33: 代码片段 33

```asm
    /* Set the interrupt mask to the max priority that can use the API.  The
    yield handler will only be called at configKERNEL_INTERRUPT_PRIORITY which
    is below configMAX_SYSCALL_INTERRUPT_PRIORITY - so this can only ever
    raise the IPL value and never lower it. */
    di
    ehb
    mfc0        s7, _CP0_STATUS
    ins         s7, zero, 10, 6
    ori         s6, s7, ( configMAX_SYSCALL_INTERRUPT_PRIORITY << 10 ) | 1
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 34: 代码片段 34

```asm
    /* This mtc0 re-enables interrupts, but only above
    configMAX_SYSCALL_INTERRUPT_PRIORITY. */
    mtc0        s6, _CP0_STATUS
    ehb
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 35: 代码片段 35

```asm
    /* Clear the software interrupt in the core. */
    mfc0        s6, _CP0_CAUSE
    ins         s6, zero, 8, 1
    mtc0        s6, _CP0_CAUSE
    ehb
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 36: 代码片段 36

```asm
    /* Clear the interrupt in the interrupt controller. */
    la          s6, IFS0CLR
    addiu       s4, zero, 2
    sw          s4, (s6)
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 37: 代码片段 37

```asm
    jal         vTaskSwitchContext
    nop
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 38: 代码片段 38

```asm
    /* Clear the interrupt mask again.  The saved status value is still in s7. */
    mtc0        s7, _CP0_STATUS
    ehb
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 39: 代码片段 39

```asm
    /* Restore the stack pointer from the TCB. */
    la          s0, pxCurrentTCB
    lw          s0, (s0)
    lw          s5, (s0)
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 40: 代码片段 40

```asm
    /* Restore the rest of the context. */
    lw          s0, 8(s5)
    mtlo        s0
    lw          s0, 12(s5)
    mthi        s0
    lw          $1, 16(s5)
    lw          s0, 20(s5)
    lw          s1, 24(s5)
    lw          s2, 28(s5)
    lw          s3, 32(s5)
    lw          s4, 36(s5)
    /* s5 is loaded later. */
    lw          s6, 44(s5)
    lw          s7, 48(s5)
    lw          v0, 52(s5)
    lw          v1, 56(s5)
    lw          a0, 60(s5)
    lw          a1, 64(s5)
    lw          a2, 68(s5)
    lw          a3, 72(s5)
    lw          t0, 76(s5)
    lw          t1, 80(s5)
    lw          t2, 84(s5)
    lw          t3, 88(s5)
    lw          t4, 92(s5)
    lw          t5, 96(s5)
    lw          t6, 100(s5)
    lw          t7, 104(s5)
    lw          t8, 108(s5)
    lw          t9, 112(s5)
    lw          s8, 116(s5)
    lw          ra, 120(s5)
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 41: 代码片段 41

```asm
    /* Protect access to the k registers, and others. */
    di
    ehb
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 42: 代码片段 42

```asm
    /* Set nesting back to zero.  As the lowest priority interrupt this
    interrupt cannot have nested. */
    la          k0, uxInterruptNesting
    sw          zero, 0(k0)
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 43: 代码片段 43

```asm
    /* Switch back to use the real stack pointer. */
    add         sp, zero, s5
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 44: 代码片段 44

```asm
    /* Restore the real s5 value. */
    lw          s5, 40(sp)
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 45: 代码片段 45

```asm
    /* Pop the status and epc values. */
    lw          k1, portSTATUS_STACK_LOCATION(sp)
    lw          k0, portEPC_STACK_LOCATION(sp)
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 46: 代码片段 46

```asm
    /* Remove stack frame. */
    addiu       sp, sp, portCONTEXT_SIZE
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 47: 代码片段 47

```asm
    mtc0        k1, _CP0_STATUS
    mtc0        k0, _CP0_EPC
    ehb
    eret
    nop
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 48: 代码片段 48

```asm
    .end        vPortYieldISR
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。
