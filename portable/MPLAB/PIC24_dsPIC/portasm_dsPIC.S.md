# portasm_dsPIC.S 代码解说

源文件：`portable/MPLAB/PIC24_dsPIC/portasm_dsPIC.S`

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
#if defined( __dsPIC30F__ ) || defined( __dsPIC33F__ )
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 3: 代码片段 3

```asm
        .global _vPortYield
        .extern _vTaskSwitchContext
        .extern uxCriticalNesting
```

**解说：** 这一段是 `portasm_dsPIC.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 汇编标签 _vPortYield

```asm
_vPortYield:
```

**解说：** 这一段是汇编标签 `_vPortYield` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 5: 代码片段 5

```asm
        PUSH    SR                      /* Save the SR used by the task.... */
        PUSH    W0                      /* ....then disable interrupts. */
        MOV     #32, W0
        MOV     W0, SR
        PUSH    W1                      /* Save registers to the stack. */
        PUSH.D  W2
        PUSH.D  W4
        PUSH.D  W6
        PUSH.D  W8
        PUSH.D  W10
        PUSH.D  W12
        PUSH    W14
        PUSH    RCOUNT
        PUSH    TBLPAG
        PUSH    ACCAL
        PUSH    ACCAH
        PUSH    ACCAU
        PUSH    ACCBL
        PUSH    ACCBH
        PUSH    ACCBU
        PUSH    DCOUNT
        PUSH    DOSTARTL
        PUSH    DOSTARTH
        PUSH    DOENDL
        PUSH    DOENDH
```

**解说：** 这一段是 `portasm_dsPIC.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 6: 代码片段 6

```asm

        PUSH    CORCON
        PUSH    PSVPAG
        MOV     _uxCriticalNesting, W0      /* Save the critical nesting counter for the task. */
        PUSH    W0
        MOV     _pxCurrentTCB, W0           /* Save the new top of stack into the TCB. */
        MOV     W15, [W0]
```

**解说：** 这一段是 `portasm_dsPIC.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 7: 代码片段 7

```asm
        call    _vTaskSwitchContext
```

**解说：** 这一段是 `portasm_dsPIC.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 8: 代码片段 8

```asm
        MOV     _pxCurrentTCB, W0           /* Restore the stack pointer for the task. */
        MOV     [W0], W15
        POP     W0                          /* Restore the critical nesting counter for the task. */
        MOV     W0, _uxCriticalNesting
        POP     PSVPAG
        POP     CORCON
        POP     DOENDH
        POP     DOENDL
        POP     DOSTARTH
        POP     DOSTARTL
        POP     DCOUNT
        POP     ACCBU
        POP     ACCBH
        POP     ACCBL
        POP     ACCAU
        POP     ACCAH
        POP     ACCAL
        POP     TBLPAG
        POP     RCOUNT                      /* Restore the registers from the stack. */
        POP     W14
        POP.D   W12
        POP.D   W10
        POP.D   W8
        POP.D   W6
        POP.D   W4
        POP.D   W2
        POP.D   W0
        POP     SR
```

**解说：** 这一段是 `portasm_dsPIC.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 9: 代码片段 9

```asm
        return
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 10: 代码片段 10

```asm
        .end
```

**解说：** 这一段是 `portasm_dsPIC.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 11: 预处理配置

```asm
#endif /* defined( __dsPIC30F__ ) || defined( __dsPIC33F__ ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。
