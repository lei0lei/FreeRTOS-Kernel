# portasm.S 代码解说

源文件：`portable/ThirdParty/CDK/T-HEAD_CK802/portasm.S`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 文件头和许可证

```asm
/*
 * Copyright (C) 2017 C-SKY Microsystems Co., Ltd. All rights reserved.
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
 */
```

**解说：** 这一段是文件头，说明项目归属、许可证和免责条款；它告诉使用者这个文件按 MIT 许可证发布。

## 片段 2: 说明性注释

```asm
//#include <csi_config.h>
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：include <csi_config.h>。

## 片段 3: 汇编标签 vPortStartTask

```asm
/********************************************************************
 * Functions: vPortStartTask
 *
 ********************************************************************/
.global vPortStartTask
.type   vPortStartTask, %function
vPortStartTask:
    psrclr   ie
    lrw      r4, pxCurrentTCB
    ld.w     r4, (r4)                // the current task stack pointer is the first member
    ld.w     sp, (r4)
```

**解说：** 这一段是汇编标签 `vPortStartTask` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 4: 代码片段 4

```asm
    ldw      r0, (sp, 64)
    mtcr     r0, epc
    ldw      r0, (sp, 60)
    mtcr     r0, epsr
    ldw      r15, (sp, 56)
    ldm      r0-r13, (sp)
    addi     sp, 68
    rte
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 5: 汇编标签 vPortYield

```asm
/********************************************************************
 * Functions: vPortYield
 *
 ********************************************************************/
.global vPortYield
.type   vPortYield, %function
vPortYield:
    psrclr  ee
    subi    sp, 68
    stm     r0-r13, (sp)
    stw     r15, (sp, 56)
    mfcr    r0, psr
    bseti   r0, 8
    stw     r0, (sp, 60)
    stw     r15, (sp, 64)
```

**解说：** 这一段是汇编标签 `vPortYield` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 6: 代码片段 6

```asm
    lrw     r2, pxCurrentTCB
    ld.w    r3, (r2)
    st.w    sp, (r3)
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 7: 代码片段 7

```asm
    jbsr    vTaskSwitchContext
    lrw     r4, pxCurrentTCB
    ld.w    r4, (r4)
    ld.w    sp, (r4)
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 8: 代码片段 8

```asm
    ldw     r0, (sp, 64)
    mtcr    r0, epc
    ldw     r0, (sp, 60)
    mtcr    r0, epsr
    ldw     r15, (sp, 56)
    ldm     r0-r13, (sp)
    addi    sp, 68
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 9: 代码片段 9

```asm
    rte
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 10: 汇编标签 NOVIC_IRQ_Default_Handler

```asm
/********************************************************************
 * Functions: NOVIC_IRQ_Default_Handler
 *
 ********************************************************************/
.global NOVIC_IRQ_Default_Handler
.type   NOVIC_IRQ_Default_Handler, %function
NOVIC_IRQ_Default_Handler:
    psrset  ee
    subi    sp, 68
    stm     r0-r13, (sp)
    stw     r15, (sp, 56)
    mfcr    r0, epsr
    stw     r0, (sp, 60)
    mfcr    r0, epc
    stw     r0, (sp, 64)
```

**解说：** 这一段是汇编标签 `NOVIC_IRQ_Default_Handler` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 11: 代码片段 11

```asm
    lrw     r7, pxCurrentTCB
    ldw     r7, (r7)
    stw     sp, (r7)
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 12: 代码片段 12

```asm
    lrw     sp, g_top_irqstack
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 13: 代码片段 13

```asm
    lrw     r1, g_irqvector
    mfcr    r0, psr
    lsri    r0, 16
    sextb   r0
    subi    r0, 32
    lsli    r0, 2
    add     r1, r0
    ldw     r1, (r1)
    lsri    r0, 2
    jsr     r1
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 14: 代码片段 14

```asm
    lrw     r7, pxCurrentTCB
    ldw     r7, (r7)
    ldw     sp, (r7)
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 15: 代码片段 15

```asm
    ldw     r0, (sp, 64)
    mtcr    r0, epc
    ldw     r0, (sp, 60)
    mtcr    r0, epsr
    ldm     r0-r13, (sp)
    ldw     r15, (sp, 56)
    addi    sp, 68
    rte
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。
