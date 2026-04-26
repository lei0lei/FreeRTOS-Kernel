# ISR_Support.h 代码解说

源文件：`portable/IAR/78K0R/ISR_Support.h`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 代码片段 1

```c
; /*
   * ; * FreeRTOS Kernel <DEVELOPMENT BRANCH>
   * ; * Copyright (C) 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
   * ; *
   * ; * SPDX-License-Identifier: MIT
   * ; *
   * ; * Permission is hereby granted, free of charge, to any person obtaining a copy of
   * ; * this software and associated documentation files (the "Software"), to deal in
   * ; * the Software without restriction, including without limitation the rights to
   * ; * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
   * ; * the Software, and to permit persons to whom the Software is furnished to do so,
   * ; * subject to the following conditions:
   * ; *
   * ; * The above copyright notice and this permission notice shall be included in all
   * ; * copies or substantial portions of the Software.
   * ; *
   * ; * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   * ; * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
   * ; * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
   * ; * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
   * ; * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
   * ; * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
   * ; *
   * ; * https://www.FreeRTOS.org
   * ; * https://github.com/FreeRTOS
   * ; *
   * ; */

#include "FreeRTOSConfig.h"

;
```

**解说：** 这一段是 `ISR_Support.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 2: 代码片段 2

```c
Variables used by scheduler
;
------------------------------------------------------------------------------
EXTERN pxCurrentTCB
EXTERN usCriticalNesting

;
------------------------------------------------------------------------------
;
portSAVE_CONTEXT MACRO
;
Saves the context of the general purpose registers, CS and ES( only in far
                                                               ;
                                                               memory mode ) registers the usCriticalNesting Value and the Stack Pointer
;
of the active Task onto the task stack
;
------------------------------------------------------------------------------
portSAVE_CONTEXT MACRO

PUSH AX;
Save AX Register to stack.
   PUSH HL
MOV A, CS;
Save CS register.
   XCH A, X
MOV A, ES;
Save ES register.
   PUSH AX
PUSH DE;
Save the remaining general purpose registers.
   PUSH BC
MOVW AX, usCriticalNesting;
Save the usCriticalNesting value.
   PUSH AX
MOVW AX, pxCurrentTCB;
```

**解说：** 这一段是 `ISR_Support.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 3: 代码片段 14

```c
Save the Stack pointer.
   MOVW HL, AX
MOVW AX, SP
        MOVW[ HL ], AX
        ENDM
;
```

**解说：** 这一段是 `ISR_Support.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 代码片段 4

```c
------------------------------------------------------------------------------

;
------------------------------------------------------------------------------
;
portRESTORE_CONTEXT MACRO
;
Restores the task Stack Pointer then use this to restore usCriticalNesting,
;
general purpose registers and the CS and ES( only in far memory mode )
;
of the selected task from the task stack
;
------------------------------------------------------------------------------
portRESTORE_CONTEXT MACRO
MOVW AX, pxCurrentTCB;
Restore the Stack pointer.
   MOVW HL, AX
MOVW AX, [ HL ]
MOVW SP, AX
POP AX;
Restore usCriticalNesting value.
   MOVW usCriticalNesting, AX
POP BC;
Restore the necessary general purpose registers.
   POP DE
POP AX;
Restore the ES register.
   MOV ES, A
XCH A, X;
Restore the CS register.
   MOV CS, A
POP HL;
Restore general purpose register HL.
   POP AX;
Restore AX.
   ENDM
;
------------------------------------------------------------------------------
```

**解说：** 这一段是 `ISR_Support.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。
