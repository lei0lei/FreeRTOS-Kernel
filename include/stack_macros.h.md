# stack_macros.h 代码解说

源文件：`include/stack_macros.h`

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

## 片段 2: 预处理配置 STACK_MACROS_H

```c
#ifndef STACK_MACROS_H
#define STACK_MACROS_H

/*
 * Call the stack overflow hook function if the stack of the task being swapped
 * out is currently overflowed, or looks like it might have overflowed in the
 * past.
 *
 * Setting configCHECK_FOR_STACK_OVERFLOW to 1 will cause the macro to check
 * the current stack state only - comparing the current top of stack value to
 * the stack limit.  Setting configCHECK_FOR_STACK_OVERFLOW to greater than 1
 * will also cause the last few stack bytes to be checked to ensure the value
 * to which the bytes were set when the task was created have not been
 * overwritten.  Note this second test does not guarantee that an overflowed
 * stack will always be recognised.
 */

/*-----------------------------------------------------------*/

/*
 * portSTACK_LIMIT_PADDING is a number of extra words to consider to be in
 * use on the stack.
 */
#ifndef portSTACK_LIMIT_PADDING
    #define portSTACK_LIMIT_PADDING    0
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 3: 预处理配置 taskCHECK_FOR_STACK_OVERFLOW

```c
/* Stack overflow check is not straight forward to implement for MPU ports
 * because of the following reasons:
 * 1. The context is stored in TCB and as a result, pxTopOfStack member points
 *    to the context location in TCB.
 * 2. System calls are executed on a separate privileged only stack.
 *
 * It is still okay because an MPU region is used to protect task stack which
 * means task stack overflow will trigger an MPU fault for unprivileged tasks.
 * Additionally, architectures with hardware stack overflow checking support
 * (such as Armv8-M) will trigger a fault when a task's stack overflows.
 */
#if ( ( configCHECK_FOR_STACK_OVERFLOW == 1 ) && ( portSTACK_GROWTH < 0 ) && ( portUSING_MPU_WRAPPERS != 1 ) )

/* Only the current stack state is to be checked. */
    #define taskCHECK_FOR_STACK_OVERFLOW()                                                      \
    do                                                                                          \
    {                                                                                           \
        /* Is the currently saved stack pointer within the stack limit? */                      \
        if( pxCurrentTCB->pxTopOfStack <= pxCurrentTCB->pxStack + portSTACK_LIMIT_PADDING )     \
        {                                                                                       \
            char * pcOverflowTaskName = pxCurrentTCB->pcTaskName;                               \
            vApplicationStackOverflowHook( ( TaskHandle_t ) pxCurrentTCB, pcOverflowTaskName ); \
        }                                                                                       \
    } while( 0 )

#endif /* configCHECK_FOR_STACK_OVERFLOW == 1 */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 4: 预处理配置 taskCHECK_FOR_STACK_OVERFLOW

```c
/*-----------------------------------------------------------*/
#if ( ( configCHECK_FOR_STACK_OVERFLOW == 1 ) && ( portSTACK_GROWTH > 0 ) && ( portUSING_MPU_WRAPPERS != 1 ) )

/* Only the current stack state is to be checked. */
    #define taskCHECK_FOR_STACK_OVERFLOW()                                                       \
    do                                                                                           \
    {                                                                                            \
        /* Is the currently saved stack pointer within the stack limit? */                       \
        if( pxCurrentTCB->pxTopOfStack >= pxCurrentTCB->pxEndOfStack - portSTACK_LIMIT_PADDING ) \
        {                                                                                        \
            char * pcOverflowTaskName = pxCurrentTCB->pcTaskName;                                \
            vApplicationStackOverflowHook( ( TaskHandle_t ) pxCurrentTCB, pcOverflowTaskName );  \
        }                                                                                        \
    } while( 0 )

#endif /* configCHECK_FOR_STACK_OVERFLOW == 1 */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 5: 预处理配置 taskCHECK_FOR_STACK_OVERFLOW

```c
/*-----------------------------------------------------------*/
#if ( ( configCHECK_FOR_STACK_OVERFLOW > 1 ) && ( portSTACK_GROWTH < 0 ) && ( portUSING_MPU_WRAPPERS != 1 ) )

    #define taskCHECK_FOR_STACK_OVERFLOW()                                                       \
    do                                                                                           \
    {                                                                                            \
        const uint32_t * const pulStack = ( uint32_t * ) pxCurrentTCB->pxStack;                  \
        const uint32_t ulCheckValue = ( uint32_t ) 0xa5a5a5a5U;                                  \
                                                                                                 \
        if( ( pxCurrentTCB->pxTopOfStack <= pxCurrentTCB->pxStack + portSTACK_LIMIT_PADDING ) || \
            ( pulStack[ 0 ] != ulCheckValue ) ||                                                 \
            ( pulStack[ 1 ] != ulCheckValue ) ||                                                 \
            ( pulStack[ 2 ] != ulCheckValue ) ||                                                 \
            ( pulStack[ 3 ] != ulCheckValue ) )                                                  \
        {                                                                                        \
            char * pcOverflowTaskName = pxCurrentTCB->pcTaskName;                                \
            vApplicationStackOverflowHook( ( TaskHandle_t ) pxCurrentTCB, pcOverflowTaskName );  \
        }                                                                                        \
    } while( 0 )

#endif /* #if( configCHECK_FOR_STACK_OVERFLOW > 1 ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 6: 预处理配置 taskCHECK_FOR_STACK_OVERFLOW

```c
/*-----------------------------------------------------------*/
#if ( ( configCHECK_FOR_STACK_OVERFLOW > 1 ) && ( portSTACK_GROWTH > 0 ) && ( portUSING_MPU_WRAPPERS != 1 ) )

    #define taskCHECK_FOR_STACK_OVERFLOW()                                                                                                \
    do                                                                                                                                    \
    {                                                                                                                                     \
        int8_t * pcEndOfStack = ( int8_t * ) pxCurrentTCB->pxEndOfStack;                                                                  \
        static const uint8_t ucExpectedStackBytes[] = { tskSTACK_FILL_BYTE, tskSTACK_FILL_BYTE, tskSTACK_FILL_BYTE, tskSTACK_FILL_BYTE,   \
                                                        tskSTACK_FILL_BYTE, tskSTACK_FILL_BYTE, tskSTACK_FILL_BYTE, tskSTACK_FILL_BYTE,   \
                                                        tskSTACK_FILL_BYTE, tskSTACK_FILL_BYTE, tskSTACK_FILL_BYTE, tskSTACK_FILL_BYTE,   \
                                                        tskSTACK_FILL_BYTE, tskSTACK_FILL_BYTE, tskSTACK_FILL_BYTE, tskSTACK_FILL_BYTE,   \
                                                        tskSTACK_FILL_BYTE, tskSTACK_FILL_BYTE, tskSTACK_FILL_BYTE, tskSTACK_FILL_BYTE }; \
                                                                                                                                          \
        pcEndOfStack -= sizeof( ucExpectedStackBytes );                                                                                   \
                                                                                                                                          \
        if( ( pxCurrentTCB->pxTopOfStack >= pxCurrentTCB->pxEndOfStack - portSTACK_LIMIT_PADDING ) ||                                     \
            ( memcmp( ( void * ) pcEndOfStack, ( void * ) ucExpectedStackBytes, sizeof( ucExpectedStackBytes ) ) != 0 ) )                 \
        {                                                                                                                                 \
            char * pcOverflowTaskName = pxCurrentTCB->pcTaskName;                                                                         \
            vApplicationStackOverflowHook( ( TaskHandle_t ) pxCurrentTCB, pcOverflowTaskName );                                           \
        }                                                                                                                                 \
    } while( 0 )

#endif /* #if( configCHECK_FOR_STACK_OVERFLOW > 1 ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 7: 预处理配置 taskCHECK_FOR_STACK_OVERFLOW

```c
/*-----------------------------------------------------------*/
/* Remove stack overflow macro if not being used. */
#ifndef taskCHECK_FOR_STACK_OVERFLOW
    #define taskCHECK_FOR_STACK_OVERFLOW()
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 8: 预处理配置

```c
#endif /* STACK_MACROS_H */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。
