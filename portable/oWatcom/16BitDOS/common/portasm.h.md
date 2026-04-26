# portasm.h 代码解说

源文件：`portable/oWatcom/16BitDOS/common/portasm.h`

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

## 片段 2: 类型定义 TCB_t

```c
typedef void TCB_t;
```

**解说：** 这一段定义类型 `TCB_t`，把相关字段或取值组织成一个明确的数据结构，方便内核代码传递和维护状态。

## 片段 3: 代码片段 3

```c
extern volatile TCB_t * volatile pxCurrentTCB;
extern void vTaskSwitchContext( void );
```

**解说：** 这一段是 `portasm.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 代码片段 5

```c
/*
 * Saves the stack pointer for one task into its TCB, calls
 * vTaskSwitchContext() to update the TCB being used, then restores the stack
 * from the new TCB read to run the task.
 */
void portSWITCH_CONTEXT( void );
```

**解说：** 这一段是 `portasm.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 5: 代码片段 6

```c
/*
 * Load the stack pointer from the TCB of the task which is going to be first
 * to execute.  Then force an IRET so the registers and IP are popped off the
 * stack.
 */
void portFIRST_CONTEXT( void );
```

**解说：** 这一段是 `portasm.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 6: 预处理配置

```c
/* There are slightly different versions depending on whether you are building
to include debugger information.  If debugger information is used then there
are a couple of extra bytes left of the ISR stack (presumably for use by the
debugger).  The true stack pointer is then stored in the bp register.  We add
2 to the stack pointer to remove the extra bytes before we restore our context. */
#ifdef DEBUG_BUILD

    #pragma aux portSWITCH_CONTEXT =    "mov    ax, seg pxCurrentTCB"                                                       \
                                        "mov    ds, ax"                                                                     \
                                        "les    bx, pxCurrentTCB"           /* Save the stack pointer into the TCB. */      \
                                        "mov    es:0x2[ bx ], ss"                                                           \
                                        "mov    es:[ bx ], sp"                                                              \
                                        "call   vTaskSwitchContext"         /* Perform the switch. */                       \
                                        "mov    ax, seg pxCurrentTCB"       /* Restore the stack pointer from the TCB. */   \
                                        "mov    ds, ax"                                                                     \
                                        "les    bx, dword ptr pxCurrentTCB"                                                 \
                                        "mov    ss, es:[ bx + 2 ]"                                                          \
                                        "mov    sp, es:[ bx ]"                                                              \
                                        "mov    bp, sp"                     /* Prepare the bp register for the restoration of the SP in the compiler generated portion of the ISR */    \
                                        "add    bp, 0x0002"



    #pragma aux portFIRST_CONTEXT =     "mov    ax, seg pxCurrentTCB"           \
                                        "mov    ds, ax"                         \
                                        "les    bx, dword ptr pxCurrentTCB"     \
                                        "mov    ss, es:[ bx + 2 ]"              \
                                        "mov    sp, es:[ bx ]"                  \
                                        "add    sp, 0x0002"                     /* Remove the extra bytes that exist in debug builds before restoring the context. */ \
                                        "pop    ax"                             \
                                        "pop    ax"                             \
                                        "pop    es"                             \
                                        "pop    ds"                             \
                                        "popa"                                  \
                                        "iret"
#else

    #pragma aux portSWITCH_CONTEXT =    "mov    ax, seg pxCurrentTCB"                                                       \
                                        "mov    ds, ax"                                                                     \
                                        "les    bx, pxCurrentTCB"           /* Save the stack pointer into the TCB. */      \
                                        "mov    es:0x2[ bx ], ss"                                                           \
                                        "mov    es:[ bx ], sp"                                                              \
                                        "call   vTaskSwitchContext"         /* Perform the switch. */                       \
                                        "mov    ax, seg pxCurrentTCB"       /* Restore the stack pointer from the TCB. */   \
                                        "mov    ds, ax"                                                                     \
                                        "les    bx, dword ptr pxCurrentTCB"                                                 \
                                        "mov    ss, es:[ bx + 2 ]"                                                          \
                                        "mov    sp, es:[ bx ]"


    #pragma aux portFIRST_CONTEXT =     "mov    ax, seg pxCurrentTCB"           \
                                        "mov    ds, ax"                         \
                                        "les    bx, dword ptr pxCurrentTCB"     \
                                        "mov    ss, es:[ bx + 2 ]"              \
                                        "mov    sp, es:[ bx ]"                  \
                                        "pop    ax"                             \
                                        "pop    ax"                             \
                                        "pop    es"                             \
                                        "pop    ds"                             \
                                        "popa"                                  \
                                        "iret"
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。
