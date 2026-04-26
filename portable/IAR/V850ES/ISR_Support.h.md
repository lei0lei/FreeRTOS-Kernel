# ISR_Support.h 代码解说

源文件：`portable/IAR/V850ES/ISR_Support.h`

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
EXTERN pxCurrentTCB
EXTERN usCriticalNesting

#include "FreeRTOSConfig.h"

;
```

**解说：** 这一段是 `ISR_Support.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 3: 代码片段 3

```c
Context save and restore macro definitions
;
portSAVE_CONTEXT MACRO

    add - 0x0C, sp;
prepare stack to save necessary values
st.w lp, 8[ sp ];
store LP to stack
    stsr    0, r31
    st.w lp, 4[ sp ];
store EIPC to stack
    stsr    1, lp
    st.w lp, 0[ sp ];
store EIPSW to stack
#if configDATA_MODE == 1; Using the Tiny data model
prepare {
    r20, r21, r22, r23, r24, r25, r26, r27, r28, r29, r30
}, 76, sp;
```

**解说：** 这一段是 `ISR_Support.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 代码片段 9

```c
save general purpose registers
sst.w r19, 72[ ep ]
sst.w r18, 68[ ep ]
sst.w r17, 64[ ep ]
sst.w r16, 60[ ep ]
sst.w r15, 56[ ep ]
sst.w r14, 52[ ep ]
sst.w r13, 48[ ep ]
sst.w r12, 44[ ep ]
sst.w r11, 40[ ep ]
sst.w r10, 36[ ep ]
sst.w r9, 32[ ep ]
sst.w r8, 28[ ep ]
sst.w r7, 24[ ep ]
sst.w r6, 20[ ep ]
sst.w r5, 16[ ep ]
sst.w r4, 12[ ep ]
#else; Using the Small / Large data model
prepare {
    r20, r21, r22, r23, r24, r26, r27, r28, r29, r30
}, 72, sp;
```

**解说：** 这一段是 `ISR_Support.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 5: 代码片段 10

```c
save general purpose registers
sst.w r19, 68[ ep ]
sst.w r18, 64[ ep ]
sst.w r17, 60[ ep ]
sst.w r16, 56[ ep ]
sst.w r15, 52[ ep ]
sst.w r14, 48[ ep ]
sst.w r13, 44[ ep ]
sst.w r12, 40[ ep ]
sst.w r11, 36[ ep ]
sst.w r10, 32[ ep ]
sst.w r9, 28[ ep ]
sst.w r8, 24[ ep ]
sst.w r7, 20[ ep ]
sst.w r6, 16[ ep ]
sst.w r5, 12[ ep ]
#endif /* configDATA_MODE */
```

**解说：** 这一段是 `ISR_Support.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 6: 代码片段 6

```c
sst.w r2, 8[ ep ]
sst.w r1, 4[ ep ]
MOVHI hi1( usCriticalNesting ), r0, r1;
save usCriticalNesting value to stack
ld.w lw1( usCriticalNesting )[ r1 ], r2
sst.w r2, 0[ ep ]
MOVHI hi1( pxCurrentTCB ), r0, r1;
```

**解说：** 这一段是 `ISR_Support.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 7: 代码片段 13

```c
save SP to top of current TCB
ld.w lw1( pxCurrentTCB )[ r1 ], r2
st.w sp, 0[ r2 ]
ENDM


portRESTORE_CONTEXT MACRO

MOVHI hi1( pxCurrentTCB ), r0, r1;
```

**解说：** 这一段是 `ISR_Support.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 8: 代码片段 8

```c
get Stackpointer address
ld.w lw1( pxCurrentTCB )[ r1 ], sp
MOV sp, r1
ld.w    0[ r1 ], sp;
load stackpointer
MOV sp, ep;
set stack pointer to element pointer
sld.w   0[ ep ], r1;
load usCriticalNesting value from stack
MOVHI hi1( usCriticalNesting ), r0, r2
st.w r1, lw1( usCriticalNesting )[ r2 ]
sld.w   4[ ep ], r1;
```

**解说：** 这一段是 `ISR_Support.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 9: 代码片段 18

```c
restore general purpose registers
sld.w   8[ ep ], r2
#if configDATA_MODE == 1; Using Tiny data model
    sld.w   12[ ep ], r4
    sld.w   16[ ep ], r5
    sld.w   20[ ep ], r6
    sld.w   24[ ep ], r7
    sld.w   28[ ep ], r8
    sld.w   32[ ep ], r9
    sld.w   36[ ep ], r10
    sld.w   40[ ep ], r11
    sld.w   44[ ep ], r12
    sld.w   48[ ep ], r13
    sld.w   52[ ep ], r14
    sld.w   56[ ep ], r15
    sld.w   60[ ep ], r16
    sld.w   64[ ep ], r17
    sld.w   68[ ep ], r18
    sld.w   72[ ep ], r19
    dispose 76, {
        r20, r21, r22, r23, r24, r25, r26, r27, r28, r29, r30
    }
```

**解说：** 这一段是 `ISR_Support.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 10: 预处理配置

```c
#else; Using Small / Large data model
    sld.w   12[ ep ], r5
    sld.w   16[ ep ], r6
    sld.w   20[ ep ], r7
    sld.w   24[ ep ], r8
    sld.w   28[ ep ], r9
    sld.w   32[ ep ], r10
    sld.w   36[ ep ], r11
    sld.w   40[ ep ], r12
    sld.w   44[ ep ], r13
    sld.w   48[ ep ], r14
    sld.w   52[ ep ], r15
    sld.w   56[ ep ], r16
    sld.w   60[ ep ], r17
    sld.w   64[ ep ], r18
    sld.w   68[ ep ], r19
    dispose 72, {
        r20, r21, r22, r23, r24, r26, r27, r28, r29, r30
    }
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 11: 预处理配置

```c
#endif /* configDATA_MODE */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 12: 代码片段 12

```c
ld.w    0[ sp ], lp;
restore EIPSW from stack
ldsr lp, 1
ld.w    4[ sp ], lp;
restore EIPC from stack
ldsr lp, 0
ld.w    8[ sp ], lp;
restore LP from stack
    add     0x0C, sp;
set SP to right position

RETI

ENDM
```

**解说：** 这一段是 `ISR_Support.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。
