# freertos_tls.c 代码解说

源文件：`portable/ThirdParty/GCC/ARC_EM_HS/freertos_tls.c`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 文件头和许可证

```c
/*
 * FreeRTOS Kernel <DEVELOPMENT BRANCH>
 * Copyright (C) 2020 Synopsys, Inc. or its affiliates.  All Rights Reserved.
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

## 片段 2: 预处理配置 TLS_DEBUG

```c
#if defined( __MW__ )

    #include <stdint.h>
    #include <stdlib.h>
    #include <string.h>

    #include "FreeRTOS.h"

    #include "queue.h"
    #include "semphr.h"
    #include "task.h"

    #include "arc/arc_exception.h"
    #include "embARC_toolchain.h"
    #include "embARC_debug.h"

    #ifdef ENABLE_FREERTOS_TLS_DEBUG
        #define TLS_DEBUG( fmt, ... )    EMBARC_PRINTF( fmt, ## __VA_ARGS__ )
    #else
        #define TLS_DEBUG( fmt, ... )
    #endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 代码片段 3

```c
/*
 * Runtime routines to execute constructors and
 * destructors for task local storage.
 */
    extern void __mw_run_tls_dtor();
    extern void __mw_run_tls_ctor();
    extern uint32_t exc_nest_count;
/*
 * Linker generated symbols to mark .tls section addresses
 * first byte .. last byte
 */
    extern char _ftls[], _etls[];
```

**解说：** 这一段是 `freertos_tls.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 预处理配置 executable_requires_tls_section

```c
    #pragma weak _ftls
    #pragma weak _etls

    void executable_requires_tls_section( void )
    {
        #if _ARC
            for( ; ; )
            {
                _flag( 1 );
                _nop();
                _nop();
                _nop();
                _nop();
                _nop();
            }
        #endif
    }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 5: 预处理配置

```c
    #pragma off_inline(executable_requires_tls_section);
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 6: 预处理配置

```c
    #pragma alias(executable_requires_tls_section, "executable_requires_.tls_section");
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 7: 函数 init_task_tls

```c
    static void * init_task_tls( void )
    {
        uint32_t len = ( uint32_t ) ( _etls - _ftls );
        void * tls = NULL;

        #if FREERTOS_HEAP_SEL == 3
        #warning "FreeRTOS TLS support is not compatible with heap 3 solution(FREERTOS_HEAP_SEL=3)!"
        #warning "You can change FREERTOS_HEAP_SEL in freertos.mk to select other heap solution."
        #else
            tls = pvPortMalloc( len );
        #endif

        if( tls )
        {
            TLS_DEBUG( "Malloc task tls:%dbytes\r\n", len );
            memcpy( tls, _ftls, len );
            __mw_run_tls_ctor(); /* Run constructors */
        }

        return tls;
    }
```

**解说：** 这一段实现函数 `init_task_tls`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 8: 函数 free_task_tls

```c
    static void free_task_tls( void * pxTCB )
    {
        TaskHandle_t task2free = ( TaskHandle_t ) pxTCB;

        if( task2free != NULL )
        {
            void * tls = pvTaskGetThreadLocalStoragePointer( task2free, 0 );

            if( tls )
            {
                TLS_DEBUG( "Free task tls\r\n" );
                __mw_run_tls_dtor();
                vPortFree( tls );
                vTaskSetThreadLocalStoragePointer( task2free, 0, NULL );
            }
        }
    }
```

**解说：** 这一段实现函数 `free_task_tls`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 9: 函数 task_end_hook

```c
    void task_end_hook( void * pxTCB )
    {
        free_task_tls( pxTCB );
    }
```

**解说：** 这一段实现函数 `task_end_hook`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 10: 函数 get_isr_tls

```c
    static void * get_isr_tls( void )
    {
        /* In an ISR */
        static int first = 1;

        if( _Rarely( first ) )
        {
            first = 0;
            __mw_run_tls_ctor(); /* Run constructors */
        }

        return ( void * ) _ftls;
    }
```

**解说：** 这一段实现函数 `get_isr_tls`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 11: 预处理配置 get_task_tls

```c
    #pragma off_inline(get_isr_tls)

    static void * get_task_tls( void )
    {
        TaskHandle_t cur_task;

        cur_task = xTaskGetCurrentTaskHandle();

        if( cur_task == NULL )
        {
            return get_isr_tls();
        }

        void * tls = pvTaskGetThreadLocalStoragePointer( cur_task, 0 );

        if( tls == NULL )
        {
            tls = init_task_tls();

            if( tls )
            {
                vTaskSetThreadLocalStoragePointer( cur_task, 0, tls );
            }
            else
            {
                tls = get_isr_tls();
            }
        }

        return tls;
    }
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 12: 预处理配置

```c
    #pragma off_inline(get_task_tls)

    #if _ARC /* for ARC XCALLs need to preserve flags */
        extern void * _Preserve_flags _mwget_tls( void );
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 13: 预处理配置

```c
    #endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 14: 函数 _mwget_tls

```c
/*
 * Back end gens calls to find local data for this task
 */
    void * _mwget_tls( void )
    {
        if( _ftls == ( char * ) 0 )
        {
            executable_requires_tls_section();
        }

        if( exc_nest_count > 0 ) /* In ISR */
        {
            return get_isr_tls();
        }
        else /* In Task */
        {
            return get_task_tls();
        }
    }
```

**解说：** 这一段实现函数 `_mwget_tls`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 15: 类型定义 _lock_t

```c
/* simple interface of thread safe */
    typedef xSemaphoreHandle _lock_t;
```

**解说：** 这一段定义类型 `_lock_t`，把相关字段或取值组织成一个明确的数据结构，方便内核代码传递和维护状态。

## 片段 16: 预处理配置

```c
    #if configUSE_RECURSIVE_MUTEXES != 1
        #error "configUSE_RECURSIVE_MUTEXES in FreeRTOSConfig.h need to 1"
    #endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 17: 函数 _mwmutex_create

```c
    void _mwmutex_create( _lock_t * mutex_ptr )
    {
        *mutex_ptr = xSemaphoreCreateRecursiveMutex();
    }
```

**解说：** 这一段实现函数 `_mwmutex_create`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 18: 函数 _mwmutex_delete

```c
    void _mwmutex_delete( _lock_t * mutex_ptr )
    {
        if( ( *mutex_ptr ) != NULL )
        {
            vSemaphoreDelete( *mutex_ptr );
        }
    }
```

**解说：** 这一段实现函数 `_mwmutex_delete`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 19: 函数 _mwmutex_lock

```c
    void _mwmutex_lock( _lock_t mutex )
    {
        if( ( mutex ) != NULL )
        {
            while( xSemaphoreTakeRecursive( mutex, portMAX_DELAY ) != pdTRUE )
            {
            }
        }
    }
```

**解说：** 这一段实现函数 `_mwmutex_lock`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 20: 函数 _mwmutex_unlock

```c
    void _mwmutex_unlock( _lock_t mutex )
    {
        if( ( mutex ) != NULL )
        {
            xSemaphoreGiveRecursive( mutex );
        }
    }
```

**解说：** 这一段实现函数 `_mwmutex_unlock`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 21: 预处理配置

```c
#else /* if defined( __MW__ ) */

#endif /* __MW__ */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。
