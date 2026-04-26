# os_wrapper_freertos.c 代码解说

源文件：`portable/ThirdParty/GCC/ARM_TFM/os_wrapper_freertos.c`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 文件头和许可证

```c
/*
 * Copyright (c) 2019-2024, Arm Limited. All rights reserved.
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
 */
```

**解说：** 这一段是文件头，说明项目归属、许可证和免责条款；它告诉使用者这个文件按 MIT 许可证发布。

## 片段 2: 预处理配置

```c
/*
 * This file contains the implementation of APIs which are defined in
 * \interface/include/os_wrapper/mutex.h by TF-M(tag: TF-Mv2.0.0).
 * The implementation is based on FreeRTOS mutex type semaphore.
 */
#include "os_wrapper/mutex.h"

#include "FreeRTOS.h"
#include "semphr.h"
#include "mpu_wrappers.h"

#if ( configSUPPORT_STATIC_ALLOCATION == 1 )

/*
 * In the static allocation, the RAM is required to hold the semaphore's
 * state.
 */
    StaticSemaphore_t xSecureMutexBuffer;
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 4: 函数 os_wrapper_mutex_create

```c
void * os_wrapper_mutex_create( void )
{
    SemaphoreHandle_t xMutexHandle = NULL;

    #if ( configSUPPORT_DYNAMIC_ALLOCATION == 1 )
        xMutexHandle = xSemaphoreCreateMutex();
    #elif ( configSUPPORT_STATIC_ALLOCATION == 1 )
        xMutexHandle = xSemaphoreCreateMutexStatic( &xSecureMutexBuffer );
    #endif
    return ( void * ) xMutexHandle;
}
```

**解说：** 这一段实现函数 `os_wrapper_mutex_create`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 5: 函数 os_wrapper_mutex_acquire

```c
/*-----------------------------------------------------------*/
uint32_t os_wrapper_mutex_acquire( void * handle,
                                   uint32_t timeout )
{
    BaseType_t xRet;

    if( !handle )
    {
        return OS_WRAPPER_ERROR;
    }

    xRet = xSemaphoreTake( ( SemaphoreHandle_t ) handle,
                           ( timeout == OS_WRAPPER_WAIT_FOREVER ) ?
                           portMAX_DELAY : ( TickType_t ) timeout );

    if( xRet != pdPASS )
    {
        return OS_WRAPPER_ERROR;
    }
    else
    {
        return OS_WRAPPER_SUCCESS;
    }
}
```

**解说：** 这一段实现函数 `os_wrapper_mutex_acquire`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 6: 函数 os_wrapper_mutex_release

```c
/*-----------------------------------------------------------*/
uint32_t os_wrapper_mutex_release( void * handle )
{
    BaseType_t xRet;

    if( !handle )
    {
        return OS_WRAPPER_ERROR;
    }

    xRet = xSemaphoreGive( ( SemaphoreHandle_t ) handle );

    if( xRet != pdPASS )
    {
        return OS_WRAPPER_ERROR;
    }
    else
    {
        return OS_WRAPPER_SUCCESS;
    }
}
```

**解说：** 这一段实现函数 `os_wrapper_mutex_release`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 7: 函数 os_wrapper_mutex_delete

```c
/*-----------------------------------------------------------*/
uint32_t os_wrapper_mutex_delete( void * handle )
{
    vSemaphoreDelete( ( SemaphoreHandle_t ) handle );

    return OS_WRAPPER_SUCCESS;
}
```

**解说：** 这一段实现函数 `os_wrapper_mutex_delete`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 8: 说明性注释

```c
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。
