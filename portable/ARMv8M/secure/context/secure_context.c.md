# secure_context.c 代码解说

源文件：`portable/ARMv8M/secure/context/secure_context.c`

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

## 片段 2: 预处理配置 securecontextCONTROL_VALUE_PRIVILEGED

```c
/* Secure context includes. */
#include "secure_context.h"

/* Secure heap includes. */
#include "secure_heap.h"

/* Secure port macros. */
#include "secure_port_macros.h"

/**
 * @brief CONTROL value for privileged tasks.
 *
 * Bit[0] - 0 --> Thread mode is privileged.
 * Bit[1] - 1 --> Thread mode uses PSP.
 */
#define securecontextCONTROL_VALUE_PRIVILEGED      0x02

/**
 * @brief CONTROL value for un-privileged tasks.
 *
 * Bit[0] - 1 --> Thread mode is un-privileged.
 * Bit[1] - 1 --> Thread mode uses PSP.
 */
#define securecontextCONTROL_VALUE_UNPRIVILEGED    0x03

/**
 * @brief Size of stack seal values in bytes.
 */
#define securecontextSTACK_SEAL_SIZE               8

/**
 * @brief Stack seal value as recommended by ARM.
 */
#define securecontextSTACK_SEAL_VALUE              0xFEF5EDA5

/**
 * @brief Maximum number of secure contexts.
 */
#ifndef secureconfigMAX_SECURE_CONTEXTS
    #define secureconfigMAX_SECURE_CONTEXTS    8UL
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 代码片段 3

```c
/*-----------------------------------------------------------*/
/**
 * @brief Pre-allocated array of secure contexts.
 */
SecureContext_t xSecureContexts[ secureconfigMAX_SECURE_CONTEXTS ];
```

**解说：** 这一段是 `secure_context.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 代码片段 4

```c
/*-----------------------------------------------------------*/
/**
 * @brief Get a free secure context for a task from the secure context pool (xSecureContexts).
 *
 * This function ensures that only one secure context is allocated for a task.
 *
 * @param[in] pvTaskHandle The task handle for which the secure context is allocated.
 *
 * @return Index of a free secure context in the xSecureContexts array.
 */
static uint32_t ulGetSecureContext( void * pvTaskHandle );
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 5: 代码片段 5

```c
/**
 * @brief Return the secure context to the secure context pool (xSecureContexts).
 *
 * @param[in] ulSecureContextIndex Index of the context in the xSecureContexts array.
 */
static void vReturnSecureContext( uint32_t ulSecureContextIndex );
```

**解说：** 这一段是 `secure_context.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 6: 代码片段 6

```c
/* These are implemented in assembly. */
extern void SecureContext_LoadContextAsm( SecureContext_t * pxSecureContext );
extern void SecureContext_SaveContextAsm( SecureContext_t * pxSecureContext );
```

**解说：** 这一段是 `secure_context.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 7: 函数 ulGetSecureContext

```c
/*-----------------------------------------------------------*/
static uint32_t ulGetSecureContext( void * pvTaskHandle )
{
    /* Start with invalid index. */
    uint32_t i, ulSecureContextIndex = secureconfigMAX_SECURE_CONTEXTS;

    for( i = 0; i < secureconfigMAX_SECURE_CONTEXTS; i++ )
    {
        if( ( xSecureContexts[ i ].pucCurrentStackPointer == NULL ) &&
            ( xSecureContexts[ i ].pucStackLimit == NULL ) &&
            ( xSecureContexts[ i ].pucStackStart == NULL ) &&
            ( xSecureContexts[ i ].pvTaskHandle == NULL ) &&
            ( ulSecureContextIndex == secureconfigMAX_SECURE_CONTEXTS ) )
        {
            ulSecureContextIndex = i;
        }
        else if( xSecureContexts[ i ].pvTaskHandle == pvTaskHandle )
        {
            /* A task can only have one secure context. Do not allocate a second
             * context for the same task. */
            ulSecureContextIndex = secureconfigMAX_SECURE_CONTEXTS;
            break;
        }
    }

    return ulSecureContextIndex;
}
```

**解说：** 这一段实现函数 `ulGetSecureContext`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 8: 函数 vReturnSecureContext

```c
/*-----------------------------------------------------------*/
static void vReturnSecureContext( uint32_t ulSecureContextIndex )
{
    xSecureContexts[ ulSecureContextIndex ].pucCurrentStackPointer = NULL;
    xSecureContexts[ ulSecureContextIndex ].pucStackLimit = NULL;
    xSecureContexts[ ulSecureContextIndex ].pucStackStart = NULL;
    xSecureContexts[ ulSecureContextIndex ].pvTaskHandle = NULL;
}
```

**解说：** 这一段实现函数 `vReturnSecureContext`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 9: 函数 SecureContext_Init

```c
/*-----------------------------------------------------------*/
secureportNON_SECURE_CALLABLE void SecureContext_Init( void )
{
    uint32_t ulIPSR, i;
    static uint32_t ulSecureContextsInitialized = 0;

    /* Read the Interrupt Program Status Register (IPSR) value. */
    secureportREAD_IPSR( ulIPSR );

    /* Do nothing if the processor is running in the Thread Mode. IPSR is zero
     * when the processor is running in the Thread Mode. */
    if( ( ulIPSR != 0 ) && ( ulSecureContextsInitialized == 0 ) )
    {
        /* Ensure to initialize secure contexts only once. */
        ulSecureContextsInitialized = 1;

        /* No stack for thread mode until a task's context is loaded. */
        secureportSET_PSPLIM( securecontextNO_STACK );
        secureportSET_PSP( securecontextNO_STACK );

        /* Initialize all secure contexts. */
        for( i = 0; i < secureconfigMAX_SECURE_CONTEXTS; i++ )
        {
            xSecureContexts[ i ].pucCurrentStackPointer = NULL;
            xSecureContexts[ i ].pucStackLimit = NULL;
            xSecureContexts[ i ].pucStackStart = NULL;
            xSecureContexts[ i ].pvTaskHandle = NULL;
        }

        #if ( configENABLE_MPU == 1 )
        {
            /* Configure thread mode to use PSP and to be unprivileged. */
            secureportSET_CONTROL( securecontextCONTROL_VALUE_UNPRIVILEGED );
        }
        #else /* configENABLE_MPU */
        {
            /* Configure thread mode to use PSP and to be privileged. */
            secureportSET_CONTROL( securecontextCONTROL_VALUE_PRIVILEGED );
        }
        #endif /* configENABLE_MPU */
    }
}
```

**解说：** 这一段实现函数 `SecureContext_Init`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 10: 预处理配置

```c
/*-----------------------------------------------------------*/
#if ( configENABLE_MPU == 1 )
    secureportNON_SECURE_CALLABLE SecureContextHandle_t SecureContext_AllocateContext( uint32_t ulSecureStackSize,
                                                                                       uint32_t ulIsTaskPrivileged,
                                                                                       void * pvTaskHandle )
#else /* configENABLE_MPU */
    secureportNON_SECURE_CALLABLE SecureContextHandle_t SecureContext_AllocateContext( uint32_t ulSecureStackSize,
                                                                                       void * pvTaskHandle )
#endif /* configENABLE_MPU */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 11: 函数 Register

```c
{
    uint8_t * pucStackMemory = NULL;
    uint8_t * pucStackLimit;
    uint32_t ulIPSR, ulSecureContextIndex;
    SecureContextHandle_t xSecureContextHandle = securecontextINVALID_CONTEXT_ID;

    #if ( configENABLE_MPU == 1 )
        uint32_t * pulCurrentStackPointer = NULL;
    #endif /* configENABLE_MPU */

    /* Read the Interrupt Program Status Register (IPSR) and Process Stack Limit
     * Register (PSPLIM) value. */
    secureportREAD_IPSR( ulIPSR );
    secureportREAD_PSPLIM( pucStackLimit );

    /* Do nothing if the processor is running in the Thread Mode. IPSR is zero
     * when the processor is running in the Thread Mode.
     * Also do nothing, if a secure context us already loaded. PSPLIM is set to
     * securecontextNO_STACK when no secure context is loaded. */
    if( ( ulIPSR != 0 ) && ( pucStackLimit == securecontextNO_STACK ) )
    {
        /* Obtain a free secure context. */
        ulSecureContextIndex = ulGetSecureContext( pvTaskHandle );

        /* Were we able to get a free context? */
        if( ulSecureContextIndex < secureconfigMAX_SECURE_CONTEXTS )
        {
            /* Allocate the stack space if possible. */
            if( ulSecureStackSize > ( UINT32_MAX - securecontextSTACK_SEAL_SIZE ) )
            {
                pucStackMemory = NULL;
            }
            else
            {
                pucStackMemory = pvPortMalloc( ulSecureStackSize + securecontextSTACK_SEAL_SIZE );
            }

            if( pucStackMemory != NULL )
            {
                /* Since stack grows down, the starting point will be the last
                * location. Note that this location is next to the last
                * allocated byte for stack (excluding the space for seal values)
                * because the hardware decrements the stack pointer before
                * writing i.e. if stack pointer is 0x2, a push operation will
                * decrement the stack pointer to 0x1 and then write at 0x1. */
                xSecureContexts[ ulSecureContextIndex ].pucStackStart = pucStackMemory + ulSecureStackSize;

                /* Seal the created secure process stack. */
                *( uint32_t * ) ( pucStackMemory + ulSecureStackSize ) = securecontextSTACK_SEAL_VALUE;
                *( uint32_t * ) ( pucStackMemory + ulSecureStackSize + 4 ) = securecontextSTACK_SEAL_VALUE;

                /* The stack cannot go beyond this location. This value is
                 * programmed in the PSPLIM register on context switch.*/
                xSecureContexts[ ulSecureContextIndex ].pucStackLimit = pucStackMemory;

                xSecureContexts[ ulSecureContextIndex ].pvTaskHandle = pvTaskHandle;

                #if ( configENABLE_MPU == 1 )
                {
                    /* Store the correct CONTROL value for the task on the stack.
                     * This value is programmed in the CONTROL register on
                     * context switch. */
                    pulCurrentStackPointer = ( uint32_t * ) xSecureContexts[ ulSecureContextIndex ].pucStackStart;
                    pulCurrentStackPointer--;

                    if( ulIsTaskPrivileged )
                    {
                        *( pulCurrentStackPointer ) = securecontextCONTROL_VALUE_PRIVILEGED;
                    }
                    else
                    {
                        *( pulCurrentStackPointer ) = securecontextCONTROL_VALUE_UNPRIVILEGED;
                    }

                    /* Store the current stack pointer. This value is programmed in
                     * the PSP register on context switch. */
                    xSecureContexts[ ulSecureContextIndex ].pucCurrentStackPointer = ( uint8_t * ) pulCurrentStackPointer;
                }
                #else /* configENABLE_MPU */
                {
                    /* Current SP is set to the starting of the stack. This
                     * value programmed in the PSP register on context switch. */
                    xSecureContexts[ ulSecureContextIndex ].pucCurrentStackPointer = xSecureContexts[ ulSecureContextIndex ].pucStackStart;
                }
                #endif /* configENABLE_MPU */

                /* Ensure to never return 0 as a valid context handle. */
                xSecureContextHandle = ulSecureContextIndex + 1UL;
            }
        }
    }

    return xSecureContextHandle;
}
```

**解说：** 这一段实现函数 `Register`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 12: 函数 SecureContext_FreeContext

```c
/*-----------------------------------------------------------*/
secureportNON_SECURE_CALLABLE void SecureContext_FreeContext( SecureContextHandle_t xSecureContextHandle,
                                                              void * pvTaskHandle )
{
    uint32_t ulIPSR, ulSecureContextIndex;

    /* Read the Interrupt Program Status Register (IPSR) value. */
    secureportREAD_IPSR( ulIPSR );

    /* Do nothing if the processor is running in the Thread Mode. IPSR is zero
     * when the processor is running in the Thread Mode. */
    if( ulIPSR != 0 )
    {
        /* Only free if a valid context handle is passed. */
        if( ( xSecureContextHandle > 0UL ) && ( xSecureContextHandle <= secureconfigMAX_SECURE_CONTEXTS ) )
        {
            ulSecureContextIndex = xSecureContextHandle - 1UL;

            /* Ensure that the secure context being deleted is associated with
             * the task. */
            if( xSecureContexts[ ulSecureContextIndex ].pvTaskHandle == pvTaskHandle )
            {
                /* Free the stack space. */
                vPortFree( xSecureContexts[ ulSecureContextIndex ].pucStackLimit );

                /* Return the secure context back to the free secure contexts pool. */
                vReturnSecureContext( ulSecureContextIndex );
            }
        }
    }
}
```

**解说：** 这一段实现函数 `SecureContext_FreeContext`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 13: 函数 SecureContext_LoadContext

```c
/*-----------------------------------------------------------*/
secureportNON_SECURE_CALLABLE void SecureContext_LoadContext( SecureContextHandle_t xSecureContextHandle,
                                                              void * pvTaskHandle )
{
    uint8_t * pucStackLimit;
    uint32_t ulSecureContextIndex;

    if( ( xSecureContextHandle > 0UL ) && ( xSecureContextHandle <= secureconfigMAX_SECURE_CONTEXTS ) )
    {
        ulSecureContextIndex = xSecureContextHandle - 1UL;

        secureportREAD_PSPLIM( pucStackLimit );

        /* Ensure that no secure context is loaded and the task is loading it's
         * own context. */
        if( ( pucStackLimit == securecontextNO_STACK ) &&
            ( xSecureContexts[ ulSecureContextIndex ].pvTaskHandle == pvTaskHandle ) )
        {
            SecureContext_LoadContextAsm( &( xSecureContexts[ ulSecureContextIndex ] ) );
        }
    }
}
```

**解说：** 这一段实现函数 `SecureContext_LoadContext`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 14: 函数 SecureContext_SaveContext

```c
/*-----------------------------------------------------------*/
secureportNON_SECURE_CALLABLE void SecureContext_SaveContext( SecureContextHandle_t xSecureContextHandle,
                                                              void * pvTaskHandle )
{
    uint8_t * pucStackLimit;
    uint32_t ulSecureContextIndex;

    if( ( xSecureContextHandle > 0UL ) && ( xSecureContextHandle <= secureconfigMAX_SECURE_CONTEXTS ) )
    {
        ulSecureContextIndex = xSecureContextHandle - 1UL;

        secureportREAD_PSPLIM( pucStackLimit );

        /* Ensure that task's context is loaded and the task is saving it's own
         * context. */
        if( ( xSecureContexts[ ulSecureContextIndex ].pucStackLimit == pucStackLimit ) &&
            ( xSecureContexts[ ulSecureContextIndex ].pvTaskHandle == pvTaskHandle ) )
        {
            SecureContext_SaveContextAsm( &( xSecureContexts[ ulSecureContextIndex ] ) );
        }
    }
}
```

**解说：** 这一段实现函数 `SecureContext_SaveContext`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 15: 说明性注释

```c
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。
