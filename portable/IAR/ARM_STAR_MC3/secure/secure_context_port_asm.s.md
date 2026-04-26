# secure_context_port_asm.s 代码解说

源文件：`portable/IAR/ARM_STAR_MC3/secure/secure_context_port_asm.s`

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
    SECTION .text:CODE:NOROOT(2)
    THUMB
```

**解说：** 这一段是 `secure_context_port_asm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 3: 预处理配置

```asm
/* Including FreeRTOSConfig.h here will cause build errors if the header file
contains code not understood by the assembler - for example the 'extern' keyword.
To avoid errors place any such code inside a #ifdef __ICCARM__/#endif block so
the code is included in C files but excluded by the preprocessor in assembly
files (__ICCARM__ is defined by the IAR C compiler but not by the IAR assembler. */
#include "FreeRTOSConfig.h"
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 4: 代码片段 4

```asm
    PUBLIC SecureContext_LoadContextAsm
    PUBLIC SecureContext_SaveContextAsm
/*-----------------------------------------------------------*/
```

**解说：** 这一段是 `secure_context_port_asm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 5: 汇编标签 SecureContext_LoadContextAsm

```asm
SecureContext_LoadContextAsm:
    /* pxSecureContext value is in r0. */
    mrs r1, ipsr                        /* r1 = IPSR. */
    cbz r1, load_ctx_therad_mode        /* Do nothing if the processor is running in the Thread Mode. */
    ldmia r0!, {r1, r2}                 /* r1 = pxSecureContext->pucCurrentStackPointer, r2 = pxSecureContext->pucStackLimit. */
```

**解说：** 这一段是汇编标签 `SecureContext_LoadContextAsm` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 6: 预处理配置

```asm
#if ( configENABLE_MPU == 1 )
    ldmia r1!, {r3}                     /* Read CONTROL register value from task's stack. r3 = CONTROL. */
    msr control, r3                     /* CONTROL = r3. */
#endif /* configENABLE_MPU */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 7: 代码片段 7

```asm
    msr psplim, r2                      /* PSPLIM = r2. */
    msr psp, r1                         /* PSP = r1. */
```

**解说：** 这一段是 `secure_context_port_asm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 8: 汇编标签 load_ctx_therad_mode

```asm
    load_ctx_therad_mode:
        bx lr
/*-----------------------------------------------------------*/
```

**解说：** 这一段是汇编标签 `load_ctx_therad_mode` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 9: 汇编标签 SecureContext_SaveContextAsm

```asm
SecureContext_SaveContextAsm:
    /* pxSecureContext value is in r0. */
    mrs r1, ipsr                        /* r1 = IPSR. */
    cbz r1, save_ctx_therad_mode        /* Do nothing if the processor is running in the Thread Mode. */
    mrs r1, psp                         /* r1 = PSP. */
```

**解说：** 这一段是汇编标签 `SecureContext_SaveContextAsm` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 10: 预处理配置

```asm
#if ( ( configENABLE_FPU == 1 ) || ( configENABLE_MVE == 1 ) )
    vstmdb r1!, {s0}                    /* Trigger the deferred stacking of FPU registers. */
    vldmia r1!, {s0}                    /* Nullify the effect of the previous statement. */
#endif /* configENABLE_FPU || configENABLE_MVE */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 11: 预处理配置

```asm
#if ( configENABLE_MPU == 1 )
    mrs r2, control                     /* r2 = CONTROL. */
    stmdb r1!, {r2}                     /* Store CONTROL value on the stack. */
#endif /* configENABLE_MPU */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 12: 代码片段 12

```asm
    str r1, [r0]                        /* Save the top of stack in context. pxSecureContext->pucCurrentStackPointer = r1. */
    movs r1, #0                         /* r1 = securecontextNO_STACK. */
    msr psplim, r1                      /* PSPLIM = securecontextNO_STACK. */
    msr psp, r1                         /* PSP = securecontextNO_STACK i.e. No stack for thread mode until next task's context is loaded. */
```

**解说：** 这一段是 `secure_context_port_asm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 13: 汇编标签 save_ctx_therad_mode

```asm
    save_ctx_therad_mode:
        bx lr
/*-----------------------------------------------------------*/
```

**解说：** 这一段是汇编标签 `save_ctx_therad_mode` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 14: 代码片段 14

```asm
    END
```

**解说：** 这一段是 `secure_context_port_asm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。
