# secure_context_port.c 代码解说

源文件：`portable/GCC/ARM_CM33/secure/secure_context_port.c`

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

## 片段 2: 预处理配置 SecureContext_LoadContextAsm

```c
/* Secure context includes. */
#include "secure_context.h"

/* Secure port macros. */
#include "secure_port_macros.h"

void SecureContext_LoadContextAsm( SecureContext_t * pxSecureContext ) __attribute__( ( naked ) );
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 代码片段 3

```c
void SecureContext_SaveContextAsm( SecureContext_t * pxSecureContext ) __attribute__( ( naked ) );
```

**解说：** 这一段是 `secure_context_port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 函数 SecureContext_LoadContextAsm

```c
void SecureContext_LoadContextAsm( SecureContext_t * pxSecureContext )
{
    /* pxSecureContext value is in r0. */
    __asm volatile
    (
        " .syntax unified                   \n"
        "                                   \n"
        " mrs r1, ipsr                      \n" /* r1 = IPSR. */
        " cbz r1, load_ctx_therad_mode      \n" /* Do nothing if the processor is running in the Thread Mode. */
        " ldmia r0!, {r1, r2}               \n" /* r1 = pxSecureContext->pucCurrentStackPointer, r2 = pxSecureContext->pucStackLimit. */
        "                                   \n"
        #if ( configENABLE_MPU == 1 )
            " ldmia r1!, {r3}               \n" /* Read CONTROL register value from task's stack. r3 = CONTROL. */
            " msr control, r3               \n" /* CONTROL = r3. */
        #endif /* configENABLE_MPU */
        "                                   \n"
        " msr psplim, r2                    \n" /* PSPLIM = r2. */
        " msr psp, r1                       \n" /* PSP = r1. */
        "                                   \n"
        " load_ctx_therad_mode:             \n"
        "    bx lr                          \n"
        "                                   \n"
        ::: "r0", "r1", "r2"
    );
}
```

**解说：** 这一段实现函数 `SecureContext_LoadContextAsm`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 5: 函数 SecureContext_SaveContextAsm

```c
/*-----------------------------------------------------------*/
void SecureContext_SaveContextAsm( SecureContext_t * pxSecureContext )
{
    /* pxSecureContext value is in r0. */
    __asm volatile
    (
        " .syntax unified                   \n"
        "                                   \n"
        " mrs r1, ipsr                      \n" /* r1 = IPSR. */
        " cbz r1, save_ctx_therad_mode      \n" /* Do nothing if the processor is running in the Thread Mode. */
        " mrs r1, psp                       \n" /* r1 = PSP. */
        "                                   \n"
        #if ( ( configENABLE_FPU == 1 ) || ( configENABLE_MVE == 1 ) )
            " vstmdb r1!, {s0}              \n" /* Trigger the deferred stacking of FPU registers. */
            " vldmia r1!, {s0}              \n" /* Nullify the effect of the previous statement. */
        #endif /* configENABLE_FPU || configENABLE_MVE */
        "                                   \n"
        #if ( configENABLE_MPU == 1 )
            " mrs r2, control               \n" /* r2 = CONTROL. */
            " stmdb r1!, {r2}               \n" /* Store CONTROL value on the stack. */
        #endif /* configENABLE_MPU */
        "                                   \n"
        " str r1, [r0]                      \n" /* Save the top of stack in context. pxSecureContext->pucCurrentStackPointer = r1. */
        " movs r1, %0                       \n" /* r1 = securecontextNO_STACK. */
        " msr psplim, r1                    \n" /* PSPLIM = securecontextNO_STACK. */
        " msr psp, r1                       \n" /* PSP = securecontextNO_STACK i.e. No stack for thread mode until next task's context is loaded. */
        "                                   \n"
        " save_ctx_therad_mode:             \n"
        "    bx lr                          \n"
        "                                   \n"
        ::"i" ( securecontextNO_STACK ) : "r1", "memory"
    );
}
```

**解说：** 这一段实现函数 `SecureContext_SaveContextAsm`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 6: 说明性注释

```c
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。
