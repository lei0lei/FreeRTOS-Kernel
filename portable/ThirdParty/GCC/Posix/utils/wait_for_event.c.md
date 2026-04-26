# wait_for_event.c 代码解说

源文件：`portable/ThirdParty/GCC/Posix/utils/wait_for_event.c`

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

## 片段 2: 预处理配置 event

```c
#include <pthread.h>
#include <stdlib.h>
#include <errno.h>

#include "wait_for_event.h"

struct event
{
    pthread_mutex_t mutex;
    pthread_mutexattr_t mutexattr;
    pthread_cond_t cond;
    bool event_triggered;
};
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 函数 event_create

```c
/*-----------------------------------------------------------*/
struct event * event_create( void )
{
    struct event * ev = malloc( sizeof( struct event ) );

    if( ev != NULL )
    {
        ev->event_triggered = false;
        pthread_mutexattr_init( &ev->mutexattr );
        #ifndef __APPLE__
            pthread_mutexattr_setrobust( &ev->mutexattr, PTHREAD_MUTEX_ROBUST );
        #endif
        pthread_mutex_init( &ev->mutex, &ev->mutexattr );
        pthread_cond_init( &ev->cond, NULL );
    }

    return ev;
}
```

**解说：** 这一段实现函数 `event_create`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 4: 函数 event_delete

```c
/*-----------------------------------------------------------*/
void event_delete( struct event * ev )
{
    pthread_mutex_destroy( &ev->mutex );
    pthread_mutexattr_destroy( &ev->mutexattr );
    pthread_cond_destroy( &ev->cond );
    free( ev );
}
```

**解说：** 这一段实现函数 `event_delete`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 5: 函数 event

```c
/*-----------------------------------------------------------*/
bool event_wait( struct event * ev )
{
    if( pthread_mutex_lock( &ev->mutex ) == EOWNERDEAD )
    {
        #ifndef __APPLE__
            /* If the thread owning the mutex died, make the mutex consistent. */
            pthread_mutex_consistent( &ev->mutex );
        #endif
    }

    while( ev->event_triggered == false )
    {
        pthread_cond_wait( &ev->cond, &ev->mutex );
    }

    ev->event_triggered = false;
    pthread_mutex_unlock( &ev->mutex );
    return true;
}
```

**解说：** 这一段实现函数 `event`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 6: 函数 event

```c
/*-----------------------------------------------------------*/
bool event_wait_timed( struct event * ev,
                       time_t ms )
{
    struct timespec ts;
    int ret = 0;

    clock_gettime( CLOCK_REALTIME, &ts );
    ts.tv_sec += ms / 1000;
    ts.tv_nsec += ( ( ms % 1000 ) * 1000000 );
    if( pthread_mutex_lock( &ev->mutex ) == EOWNERDEAD )
    {
        #ifndef __APPLE__
            /* If the thread owning the mutex died, make the mutex consistent. */
            pthread_mutex_consistent( &ev->mutex );
        #endif
    }

    while( ( ev->event_triggered == false ) && ( ret == 0 ) )
    {
        ret = pthread_cond_timedwait( &ev->cond, &ev->mutex, &ts );

        if( ( ret == -1 ) && ( errno == ETIMEDOUT ) )
        {
            return false;
        }
    }

    ev->event_triggered = false;
    pthread_mutex_unlock( &ev->mutex );
    return true;
}
```

**解说：** 这一段实现函数 `event`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 7: 函数 event_signal

```c
/*-----------------------------------------------------------*/
void event_signal( struct event * ev )
{
    if( pthread_mutex_lock( &ev->mutex ) == EOWNERDEAD )
    {
        #ifndef __APPLE__
            /* If the thread owning the mutex died, make the mutex consistent. */
            pthread_mutex_consistent( &ev->mutex );
        #endif
    }
    ev->event_triggered = true;
    pthread_cond_signal( &ev->cond );
    pthread_mutex_unlock( &ev->mutex );
}
```

**解说：** 这一段实现函数 `event_signal`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 8: 说明性注释

```c
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。
