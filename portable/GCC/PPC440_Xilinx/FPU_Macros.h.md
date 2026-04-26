# FPU_Macros.h 代码解说

源文件：`portable/GCC/PPC440_Xilinx/FPU_Macros.h`

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

## 片段 2: 宏 vPortSaveFPURegisters

```c
/* When switching out a task, if the task tag contains a buffer address then
 * save the flop context into the buffer. */
#define traceTASK_SWITCHED_OUT()                                         \
    if( pxCurrentTCB->pxTaskTag != NULL )                                \
    {                                                                    \
        extern void vPortSaveFPURegisters( void * );                     \
        vPortSaveFPURegisters( ( void * ) ( pxCurrentTCB->pxTaskTag ) ); \
    }
```

**解说：** 这一段定义宏 `vPortSaveFPURegisters`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 3: 宏 vPortRestoreFPURegisters

```c
/* When switching in a task, if the task tag contains a buffer address then
 * load the flop context from the buffer. */
#define traceTASK_SWITCHED_IN()                                             \
    if( pxCurrentTCB->pxTaskTag != NULL )                                   \
    {                                                                       \
        extern void vPortRestoreFPURegisters( void * );                     \
        vPortRestoreFPURegisters( ( void * ) ( pxCurrentTCB->pxTaskTag ) ); \
    }
```

**解说：** 这一段定义宏 `vPortRestoreFPURegisters`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。
