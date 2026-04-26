# ISR_Support.h 代码解说

源文件：`portable/IAR/STR75x/ISR_Support.h`

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

EXTERN pxCurrentTCB
EXTERN ulCriticalNesting

;
```

**解说：** 这一段是 `ISR_Support.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 2: 代码片段 2

```c
Context save and restore macro definitions
;
portSAVE_CONTEXT MACRO

;
Push R0 as we are going to use the register.
   STMDB SP !, {
    R0
}
Set R0 to point to the task stack pointer.
   STMDB SP, {
    SP
}
```

**解说：** 这一段是 `ISR_Support.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 3: 代码片段 6

```c
^
NOP
SUB SP, SP, # 4
LDMIA SP !, {
    R0
}
```

**解说：** 这一段是 `ISR_Support.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 代码片段 4

```c
;
Push the return address onto the stack.
          STMDB R0 !, {
           LR
       }
       Now we have saved LR we can use it instead of R0.
          MOV LR, R0

;
Pop R0 so we can save it onto the system mode stack.
   LDMIA SP !, {
    R0
}
Push all the system mode registers onto the task stack.
   STMDB LR, {
    R0 - LR
}
^
NOP
SUB LR, LR, # 60

;
Push the SPSR onto the task stack.
   MRS R0, SPSR
STMDB LR !, {
    R0
}
LDR R0, = ulCriticalNesting
          LDR R0, [ R0 ]
STMDB LR !, {
    R0
}
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 5: 代码片段 15

```c
Store the new top of stack

for the task.
   LDR R1, = pxCurrentTCB
             LDR R0, [ R1 ]
STR LR, [ R0 ]

ENDM


portRESTORE_CONTEXT MACRO

;
```

**解说：** 这一段是 `ISR_Support.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 6: 代码片段 16

```c
Set the LR to the task stack.
   LDR R1, = pxCurrentTCB
             LDR R0, [ R1 ]
LDR LR, [ R0 ]

;
```

**解说：** 这一段是 `ISR_Support.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 7: 代码片段 7

```c
The critical nesting depth is the first item on the stack.
   ;
Load it into the ulCriticalNesting variable.
   LDR R0, = ulCriticalNesting
             LDMFD LR !, {
    R1
}
STR R1, [ R0 ]

;
Get the SPSR from the stack.
   LDMFD LR !, {
    R0
}
MSR SPSR_cxsf, R0

;
```

**解说：** 这一段是 `ISR_Support.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 8: 代码片段 22

```c
Restore all system mode registers

for the task.
   LDMFD LR, {
    R0 - R14
}
```

**解说：** 这一段是 `ISR_Support.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 9: 代码片段 9

```c
^
NOP

;
Restore the return address.
          LDR LR, [ LR, # + 60 ]

;
And return -correcting the offset in the LR to obtain the
;
correct address.
   SUBS PC, LR, # 4

ENDM
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。
