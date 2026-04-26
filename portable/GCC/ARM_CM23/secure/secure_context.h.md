# secure_context.h 代码解说

源文件：`portable/GCC/ARM_CM23/secure/secure_context.h`

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

## 片段 2: 预处理配置 __SECURE_CONTEXT_H__

```c
#ifndef __SECURE_CONTEXT_H__
#define __SECURE_CONTEXT_H__

/* Standard includes. */
#include <stdint.h>

/* FreeRTOS includes. */
#include "FreeRTOSConfig.h"

/**
 * @brief PSP value when no secure context is loaded.
 */
#define securecontextNO_STACK              0x0

/**
 * @brief Invalid context ID.
 */
#define securecontextINVALID_CONTEXT_ID    0UL
/*-----------------------------------------------------------*/

/**
 * @brief Structure to represent a secure context.
 *
 * @note Since stack grows down, pucStackStart is the highest address while
 * pucStackLimit is the first address of the allocated memory.
 */
typedef struct SecureContext
{
    uint8_t * pucCurrentStackPointer; /**< Current value of stack pointer (PSP). */
    uint8_t * pucStackLimit;          /**< Last location of the stack memory (PSPLIM). */
    uint8_t * pucStackStart;          /**< First location of the stack memory. */
    void * pvTaskHandle;              /**< Task handle of the task this context is associated with. */
} SecureContext_t;
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 类型定义 SecureContextHandle_t

```c
/*-----------------------------------------------------------*/
/**
 * @brief Opaque handle for a secure context.
 */
typedef uint32_t SecureContextHandle_t;
```

**解说：** 这一段定义类型 `SecureContextHandle_t`，把相关字段或取值组织成一个明确的数据结构，方便内核代码传递和维护状态。

## 片段 4: 代码片段 4

```c
/*-----------------------------------------------------------*/
/**
 * @brief Initializes the secure context management system.
 *
 * PSP is set to NULL and therefore a task must allocate and load a context
 * before calling any secure side function in the thread mode.
 *
 * @note This function must be called in the handler mode. It is no-op if called
 * in the thread mode.
 */
void SecureContext_Init( void );
```

**解说：** 这一段是 `secure_context.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 5: 预处理配置

```c
/**
 * @brief Allocates a context on the secure side.
 *
 * @note This function must be called in the handler mode. It is no-op if called
 * in the thread mode.
 *
 * @param[in] ulSecureStackSize Size of the stack to allocate on secure side.
 * @param[in] ulIsTaskPrivileged 1 if the calling task is privileged, 0 otherwise.
 *
 * @return Opaque context handle if context is successfully allocated, NULL
 * otherwise.
 */
#if ( configENABLE_MPU == 1 )
    SecureContextHandle_t SecureContext_AllocateContext( uint32_t ulSecureStackSize,
                                                         uint32_t ulIsTaskPrivileged,
                                                         void * pvTaskHandle );
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 6: 预处理配置

```c
#else /* configENABLE_MPU */
    SecureContextHandle_t SecureContext_AllocateContext( uint32_t ulSecureStackSize,
                                                         void * pvTaskHandle );
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 7: 预处理配置

```c
#endif /* configENABLE_MPU */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 8: 代码片段 8

```c
/**
 * @brief Frees the given context.
 *
 * @note This function must be called in the handler mode. It is no-op if called
 * in the thread mode.
 *
 * @param[in] xSecureContextHandle Context handle corresponding to the
 * context to be freed.
 */
void SecureContext_FreeContext( SecureContextHandle_t xSecureContextHandle,
                                void * pvTaskHandle );
```

**解说：** 这一段是 `secure_context.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 9: 代码片段 9

```c
/**
 * @brief Loads the given context.
 *
 * @note This function must be called in the handler mode. It is no-op if called
 * in the thread mode.
 *
 * @param[in] xSecureContextHandle Context handle corresponding to the context
 * to be loaded.
 */
void SecureContext_LoadContext( SecureContextHandle_t xSecureContextHandle,
                                void * pvTaskHandle );
```

**解说：** 这一段是 `secure_context.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 10: 代码片段 10

```c
/**
 * @brief Saves the given context.
 *
 * @note This function must be called in the handler mode. It is no-op if called
 * in the thread mode.
 *
 * @param[in] xSecureContextHandle Context handle corresponding to the context
 * to be saved.
 */
void SecureContext_SaveContext( SecureContextHandle_t xSecureContextHandle,
                                void * pvTaskHandle );
```

**解说：** 这一段是 `secure_context.h` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 11: 预处理配置

```c
#endif /* __SECURE_CONTEXT_H__ */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。
