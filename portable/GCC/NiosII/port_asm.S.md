# port_asm.S 代码解说

源文件：`portable/GCC/NiosII/port_asm.S`

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
.extern     vTaskSwitchContext
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 3: 代码片段 3

```asm
.set noat
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 预处理配置

```asm
# Exported to start the first task.
.globl restore_sp_from_pxCurrentTCB
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 5: 预处理配置

```asm
# Entry point for exceptions.
.section .exceptions.entry.user, "xa"
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 6: 汇编标签 save_context

```asm
# Save the entire context of a task.
save_context:
    addi    sp, sp, -116        # Create space on the stack.
    stw     ra, 0(sp)
                                # Leave a gap for muldiv 0
    stw     at, 8(sp)
    stw     r2, 12(sp)
    stw     r3, 16(sp)
    stw     r4, 20(sp)
    stw     r5, 24(sp)
    stw     r6, 28(sp)
    stw     r7, 32(sp)
    stw     r8, 36(sp)
    stw     r9, 40(sp)
    stw     r10, 44(sp)
    stw     r11, 48(sp)
    stw     r12, 52(sp)
    stw     r13, 56(sp)
    stw     r14, 60(sp)
    stw     r15, 64(sp)
    rdctl   r5, estatus         # Save the eStatus
    stw     r5, 68(sp)
    addi    r15, ea, -4         # Instruction that caused exception
    stw     r15, 72(sp)         # Save as EA
    stw     r16, 76(sp)         # Save the remaining registers
    stw     r17, 80(sp)
    stw     r18, 84(sp)
    stw     r19, 88(sp)
    stw     r20, 92(sp)
    stw     r21, 96(sp)
    stw     r22, 100(sp)
    stw     r23, 104(sp)
    stw     gp, 108(sp)
    stw     fp, 112(sp)
```

**解说：** 这一段是汇编标签 `save_context` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 7: 汇编标签 save_sp_to_pxCurrentTCB

```asm
save_sp_to_pxCurrentTCB:
    movia   et, pxCurrentTCB    # Load the address of the pxCurrentTCB pointer
    ldw     et, (et)            # Load the value of the pxCurrentTCB pointer
    stw     sp, (et)            # Store the stack pointer into the top of the TCB
```

**解说：** 这一段是汇编标签 `save_sp_to_pxCurrentTCB` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 8: 代码片段 8

```asm
    br      irq_test_user       # skip the section .exceptions.entry
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 9: 汇编标签 irq_test_user

```asm
    .section .exceptions.irqtest, "xa"
irq_test_user:
```

**解说：** 这一段是汇编标签 `irq_test_user` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 10: 汇编标签 restore_sp_from_pxCurrentTCB

```asm
    .section .exceptions.exit.user, "xa"
restore_sp_from_pxCurrentTCB:
    movia   et, pxCurrentTCB        # Load the address of the pxCurrentTCB pointer
    ldw     et, (et)                # Load the value of the pxCurrentTCB pointer
    ldw     sp, (et)                # Load the stack pointer with the top value of the TCB
```

**解说：** 这一段是汇编标签 `restore_sp_from_pxCurrentTCB` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 11: 汇编标签 restore_context

```asm
restore_context:
    ldw     ra, 0(sp)       # Restore the registers.
                            # Leave a gap for muldiv 0.
    ldw     at, 8(sp)
    ldw     r2, 12(sp)
    ldw     r3, 16(sp)
    ldw     r4, 20(sp)
    ldw     r5, 24(sp)
    ldw     r6, 28(sp)
    ldw     r7, 32(sp)
    ldw     r8, 36(sp)
    ldw     r9, 40(sp)
    ldw     r10, 44(sp)
    ldw     r11, 48(sp)
    ldw     r12, 52(sp)
    ldw     r13, 56(sp)
    ldw     r14, 60(sp)
    ldw     r15, 64(sp)
    ldw     et, 68(sp)      # Load the eStatus
    wrctl   estatus, et     # Write the eStatus
    ldw     ea, 72(sp)      # Load the Program Counter
    ldw     r16, 76(sp)
    ldw     r17, 80(sp)
    ldw     r18, 84(sp)
    ldw     r19, 88(sp)
    ldw     r20, 92(sp)
    ldw     r21, 96(sp)
    ldw     r22, 100(sp)
    ldw     r23, 104(sp)
    ldw     gp, 108(sp)
    ldw     fp, 112(sp)
    addi    sp, sp, 116     # Release stack space
```

**解说：** 这一段是汇编标签 `restore_context` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 12: 代码片段 12

```asm
    eret                    # Return to address ea, loading eStatus into Status.
```

**解说：** 这一段是 `port_asm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 13: 汇编标签 soft_exceptions

```asm
    .section .exceptions.soft, "xa"
soft_exceptions:
    movhi   r3, 0x003b              /* upper half of trap opcode */
    ori     r3, r3, 0x683a          /* lower half of trap opcode */
    beq     r2, r3, call_scheduler
    br      exceptions_unknown_user         # its something else
```

**解说：** 这一段是汇编标签 `soft_exceptions` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 14: 汇编标签 call_scheduler

```asm
call_scheduler:
    stw     ea, 72(sp)                      # EA is PC+4 so will skip over instruction causing exception
    movia   r15, vTaskSwitchContext         # Pick the next context - use long call version in place of "call"
    callr   r15
    br      restore_sp_from_pxCurrentTCB    # Switch in the task context and restore.
```

**解说：** 这一段是汇编标签 `call_scheduler` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 15: 汇编标签 exceptions_unknown_user

```asm
    .section .exceptions.unknown.user
exceptions_unknown_user:
```

**解说：** 这一段是汇编标签 `exceptions_unknown_user` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。
