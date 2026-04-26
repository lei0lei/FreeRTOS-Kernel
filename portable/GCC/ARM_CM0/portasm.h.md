# portasm.h 代码解说

源文件：`portable/GCC/ARM_CM0/portasm.h`

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

## 片段 2: 预处理配置 vRestoreContextOfFirstTask

```c
#ifndef __PORT_ASM_H__
#define __PORT_ASM_H__

/* Scheduler includes. */
#include "FreeRTOS.h"

/* MPU wrappers includes. */
#include "mpu_wrappers.h"

/**
 * @brief Restore the context of the first task so that the first task starts
 * executing.
 */
void vRestoreContextOfFirstTask( void ) __attribute__( ( naked ) ) PRIVILEGED_FUNCTION;
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 代码片段 3

```c
/**
 * @brief Checks whether or not the processor is privileged.
 *
 * @return 1 if the processor is already privileged, 0 otherwise.
 */
BaseType_t xIsPrivileged( void ) __attribute__( ( naked ) );
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 4: 代码片段 4

```c
/**
 * @brief Raises the privilege level by clearing the bit 0 of the CONTROL
 * register.
 *
 * @note This is a privileged function and should only be called from the kernel
 * code.
 *
 * Bit 0 of the CONTROL register defines the privilege level of Thread Mode.
 *  Bit[0] = 0 --> The processor is running privileged
 *  Bit[0] = 1 --> The processor is running unprivileged.
 */
void vRaisePrivilege( void ) __attribute__( ( naked ) ) PRIVILEGED_FUNCTION;
```

**解说：** 这一段是 `portasm.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 5: 代码片段 5

```c
/**
 * @brief Lowers the privilege level by setting the bit 0 of the CONTROL
 * register.
 *
 * Bit 0 of the CONTROL register defines the privilege level of Thread Mode.
 *  Bit[0] = 0 --> The processor is running privileged
 *  Bit[0] = 1 --> The processor is running unprivileged.
 */
void vResetPrivilege( void ) __attribute__( ( naked ) );
```

**解说：** 这一段是 `portasm.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 6: 代码片段 6

```c
/**
 * @brief Starts the first task.
 */
void vStartFirstTask( void ) __attribute__( ( naked ) ) PRIVILEGED_FUNCTION;
/**
 * @brief Disables interrupts.
 */
uint32_t ulSetInterruptMask( void ) __attribute__( ( naked ) ) PRIVILEGED_FUNCTION;
/**
 * @brief Enables interrupts.
 */
void vClearInterruptMask( uint32_t ulMask ) __attribute__( ( naked ) ) PRIVILEGED_FUNCTION;
/**
 * @brief PendSV Exception handler.
 */
void PendSV_Handler( void ) __attribute__( ( naked ) ) PRIVILEGED_FUNCTION;
/**
 * @brief SVC Handler.
 */
void SVC_Handler( void ) __attribute__( ( naked ) ) PRIVILEGED_FUNCTION;
```

**解说：** 这一段是 `portasm.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 7: 预处理配置

```c
#endif /* __PORT_ASM_H__ */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。
