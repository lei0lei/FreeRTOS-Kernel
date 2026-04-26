# port.c 代码解说

源文件：`portable/ThirdParty/GCC/Posix/port.c`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 文件头和许可证

```c
/*
 * FreeRTOS Kernel <DEVELOPMENT BRANCH>
 * Copyright (C) 2020 Cambridge Consultants Ltd.
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

## 片段 2: 预处理配置 _GNU_SOURCE

```c
/*-----------------------------------------------------------
* Implementation of functions defined in portable.h for the Posix port.
*
* Each task has a pthread which eases use of standard debuggers
* (allowing backtraces of tasks etc). Threads for tasks that are not
* running are blocked in sigwait().
*
* Task switch is done by resuming the thread for the next task by
* signaling the condition variable and then waiting on a condition variable
* with the current thread.
*
* The timer interrupt uses SIGALRM and care is taken to ensure that
* the signal handler runs only on the thread for the current task.
*
* Use of part of the standard C library requires care as some
* functions can take pthread mutexes internally which can result in
* deadlocks as the FreeRTOS kernel can switch tasks while they're
* holding a pthread mutex.
*
* stdio (printf() and friends) should be called from a single task
* only or serialized with a FreeRTOS primitive such as a binary
* semaphore or mutex.
*
* Note: When using LLDB (the default debugger on macOS) with this port,
* suppress SIGUSR1 to prevent debugger interference. This can be
* done by adding the following line to ~/.lldbinit:
* `process handle SIGUSR1 -n true -p false -s false`
*----------------------------------------------------------*/
#ifdef __linux__
    #define _GNU_SOURCE
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 3: 预处理配置 SIG_RESUME

```c
#include "portmacro.h"
#include <errno.h>
#include <pthread.h>
#include <limits.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <sys/times.h>
#include <time.h>
#include <unistd.h>

/* Scheduler includes. */
#include "FreeRTOS.h"
#include "task.h"
#include "timers.h"
#include "utils/wait_for_event.h"
/*-----------------------------------------------------------*/

#define SIG_RESUME    SIGUSR1

typedef struct THREAD
{
    pthread_t pthread;
    TaskFunction_t pxCode;
    void * pvParams;
    BaseType_t xDying;
    struct event * ev;
} Thread_t;
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 4: 函数 prvGetThreadFromTask

```c
/*
 * The additional per-thread data is stored at the beginning of the
 * task's stack.
 */
static inline Thread_t * prvGetThreadFromTask( TaskHandle_t xTask )
{
    StackType_t * pxTopOfStack = *( StackType_t ** ) xTask;

    return ( Thread_t * ) ( pxTopOfStack + 1 );
}
```

**解说：** 这一段实现函数 `prvGetThreadFromTask`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 5: 代码片段 5

```c
/*-----------------------------------------------------------*/
static pthread_once_t hSigSetupThread = PTHREAD_ONCE_INIT;
static pthread_once_t hThreadKeyOnce = PTHREAD_ONCE_INIT;
static sigset_t xAllSignals;
static sigset_t xSchedulerOriginalSignalMask;
static pthread_t hMainThread = ( pthread_t ) NULL;
static volatile BaseType_t uxCriticalNesting;
static BaseType_t xSchedulerEnd = pdFALSE;
static pthread_t hTimerTickThread;
static bool xTimerTickThreadShouldRun;
static uint64_t prvStartTimeNs;
static pthread_key_t xThreadKey = 0;
/*-----------------------------------------------------------*/
static void prvSetupSignalsAndSchedulerPolicy( void );
static void prvSetupTimerInterrupt( void );
static void * prvWaitForStart( void * pvParams );
static void prvSwitchThread( Thread_t * xThreadToResume,
                             Thread_t * xThreadToSuspend );
static void prvSuspendSelf( Thread_t * thread );
static void prvResumeThread( Thread_t * xThreadId );
static void vPortSystemTickHandler( int sig );
static void vPortStartFirstTask( void );
static void prvPortYieldFromISR( void );
static void prvThreadKeyDestructor( void * pvData );
static void prvInitThreadKey( void );
static void prvMarkAsFreeRTOSThread( void );
static BaseType_t prvIsFreeRTOSThread( void );
static void prvDestroyThreadKey( void );
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 6: 函数 prvThreadKeyDestructor

```c
/*-----------------------------------------------------------*/
static void prvThreadKeyDestructor( void * pvData )
{
    free( pvData );
}
```

**解说：** 这一段实现函数 `prvThreadKeyDestructor`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 7: 函数 prvInitThreadKey

```c
/*-----------------------------------------------------------*/
static void prvInitThreadKey( void )
{
    pthread_key_create( &xThreadKey, prvThreadKeyDestructor );
    /* Destroy xThreadKey when the process exits. */
    atexit( prvDestroyThreadKey );
}
```

**解说：** 这一段实现函数 `prvInitThreadKey`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 8: 函数 prvMarkAsFreeRTOSThread

```c
/*-----------------------------------------------------------*/
static void prvMarkAsFreeRTOSThread( void )
{
    uint8_t * pucThreadData = NULL;

    ( void ) pthread_once( &hThreadKeyOnce, prvInitThreadKey );

    pucThreadData = malloc( 1 );
    configASSERT( pucThreadData != NULL );

    *pucThreadData = 1;

    pthread_setspecific( xThreadKey, pucThreadData );
}
```

**解说：** 这一段实现函数 `prvMarkAsFreeRTOSThread`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 9: 函数 prvIsFreeRTOSThread

```c
/*-----------------------------------------------------------*/
static BaseType_t prvIsFreeRTOSThread( void )
{
    uint8_t * pucThreadData = NULL;
    BaseType_t xRet = pdFALSE;

    ( void ) pthread_once( &hThreadKeyOnce, prvInitThreadKey );

    pucThreadData = ( uint8_t * ) pthread_getspecific( xThreadKey );

    if( ( pucThreadData != NULL ) && ( *pucThreadData == 1 ) )
    {
        xRet = pdTRUE;
    }

    return xRet;
}
```

**解说：** 这一段实现函数 `prvIsFreeRTOSThread`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 10: 函数 prvDestroyThreadKey

```c
/*-----------------------------------------------------------*/
static void prvDestroyThreadKey( void )
{
    pthread_key_delete( xThreadKey );
}
```

**解说：** 这一段实现函数 `prvDestroyThreadKey`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 11: 代码片段 11

```c
/*-----------------------------------------------------------*/
static void prvFatalError( const char * pcCall,
                           int iErrno ) __attribute__( ( __noreturn__ ) );
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 12: 函数 prvFatalError

```c
void prvFatalError( const char * pcCall,
                    int iErrno )
{
    fprintf( stderr, "%s: %s\n", pcCall, strerror( iErrno ) );
    abort();
}
```

**解说：** 这一段实现函数 `prvFatalError`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 13: 函数 prvPortSetCurrentThreadName

```c
/*-----------------------------------------------------------*/
static void prvPortSetCurrentThreadName( const char * pxThreadName )
{
    #ifdef __APPLE__
        pthread_setname_np( pxThreadName );
    #else
        pthread_setname_np( pthread_self(), pxThreadName );
    #endif
}
```

**解说：** 这一段实现函数 `prvPortSetCurrentThreadName`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 14: 函数 pxPortInitialiseStack

```c
/*-----------------------------------------------------------*/
/*
 * See header file for description.
 */
StackType_t * pxPortInitialiseStack( StackType_t * pxTopOfStack,
                                     StackType_t * pxEndOfStack,
                                     TaskFunction_t pxCode,
                                     void * pvParameters )
{
    Thread_t * thread;
    pthread_attr_t xThreadAttributes;
    size_t ulStackSize;
    int iRet;

    ( void ) pthread_once( &hSigSetupThread, prvSetupSignalsAndSchedulerPolicy );

    /*
     * Store the additional thread data at the start of the stack.
     */
    thread = ( Thread_t * ) ( pxTopOfStack + 1 ) - 1;
    pxTopOfStack = ( StackType_t * ) thread - 1;

    /* Ensure that there is enough space to store Thread_t on the stack. */
    ulStackSize = ( size_t ) ( pxTopOfStack + 1 - pxEndOfStack ) * sizeof( *pxTopOfStack );
    configASSERT( ulStackSize > sizeof( Thread_t ) );
    ( void ) ulStackSize; /* suppress set but not used warning */

    thread->pxCode = pxCode;
    thread->pvParams = pvParameters;
    thread->xDying = pdFALSE;

    pthread_attr_init( &xThreadAttributes );

    thread->ev = event_create();

    vPortEnterCritical();

    iRet = pthread_create( &thread->pthread, &xThreadAttributes,
                           prvWaitForStart, thread );

    if( iRet != 0 )
    {
        prvFatalError( "pthread_create", iRet );
    }

    vPortExitCritical();

    return pxTopOfStack;
}
```

**解说：** 这一段实现函数 `pxPortInitialiseStack`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 15: 函数 vPortStartFirstTask

```c
/*-----------------------------------------------------------*/
void vPortStartFirstTask( void )
{
    Thread_t * pxFirstThread = prvGetThreadFromTask( xTaskGetCurrentTaskHandle() );

    /* Start the first task. */
    prvResumeThread( pxFirstThread );
}
```

**解说：** 这一段实现函数 `vPortStartFirstTask`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 16: 函数 xPortStartScheduler

```c
/*-----------------------------------------------------------*/
/*
 * See header file for description.
 */
BaseType_t xPortStartScheduler( void )
{
    int iSignal;
    sigset_t xSignals;

    hMainThread = pthread_self();
    prvPortSetCurrentThreadName( "Scheduler" );

    /* Start the timer that generates the tick ISR(SIGALRM).
     * Interrupts are disabled here already. */
    prvSetupTimerInterrupt();

    /*
     * Block SIG_RESUME before starting any tasks so the main thread can sigwait on it.
     * To sigwait on an unblocked signal is undefined.
     * https://pubs.opengroup.org/onlinepubs/009604499/functions/sigwait.html
     */
    sigemptyset( &xSignals );
    sigaddset( &xSignals, SIG_RESUME );
    ( void ) pthread_sigmask( SIG_BLOCK, &xSignals, NULL );

    /* Start the first task. */
    vPortStartFirstTask();

    /* Wait until signaled by vPortEndScheduler(). */
    while( xSchedulerEnd != pdTRUE )
    {
        sigwait( &xSignals, &iSignal );
    }

    /*
     * clear out the variable that is used to end the scheduler, otherwise
     * subsequent scheduler restarts will end immediately.
     */
    xSchedulerEnd = pdFALSE;

    /* Reset pthread_once_t, needed to restart the scheduler again.
     * memset the internal struct members for MacOS/Linux Compatibility */
    #if __APPLE__
        hSigSetupThread.__sig = _PTHREAD_ONCE_SIG_init;
        hThreadKeyOnce.__sig = _PTHREAD_ONCE_SIG_init;
        memset( ( void * ) &hSigSetupThread.__opaque, 0, sizeof( hSigSetupThread.__opaque ) );
        memset( ( void * ) &hThreadKeyOnce.__opaque, 0, sizeof( hThreadKeyOnce.__opaque ) );
    #else /* Linux PTHREAD library*/
        hSigSetupThread = ( pthread_once_t ) PTHREAD_ONCE_INIT;
        hThreadKeyOnce = ( pthread_once_t ) PTHREAD_ONCE_INIT;
    #endif /* __APPLE__*/

    /* Restore original signal mask. */
    ( void ) pthread_sigmask( SIG_SETMASK, &xSchedulerOriginalSignalMask, NULL );

    return 0;
}
```

**解说：** 这一段实现函数 `xPortStartScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 17: 函数 vPortEndScheduler

```c
/*-----------------------------------------------------------*/
void vPortEndScheduler( void )
{
    Thread_t * pxCurrentThread;
    BaseType_t xIsFreeRTOSThread;

    /* Stop the timer tick thread. */
    xTimerTickThreadShouldRun = false;
    pthread_join( hTimerTickThread, NULL );

    /* Check whether the current thread is a FreeRTOS thread.
     * This has to happen before the scheduler is signaled to exit
     * its loop to prevent data races on the thread key. */
    xIsFreeRTOSThread = prvIsFreeRTOSThread();

    /* Signal the scheduler to exit its loop. */
    xSchedulerEnd = pdTRUE;
    ( void ) pthread_kill( hMainThread, SIG_RESUME );

    /* Waiting to be deleted here. */
    if( xIsFreeRTOSThread == pdTRUE )
    {
        pxCurrentThread = prvGetThreadFromTask( xTaskGetCurrentTaskHandle() );
        event_wait( pxCurrentThread->ev );
    }

    pthread_testcancel();
}
```

**解说：** 这一段实现函数 `vPortEndScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 18: 函数 vPortEnterCritical

```c
/*-----------------------------------------------------------*/
void vPortEnterCritical( void )
{
    if( uxCriticalNesting == 0 )
    {
        vPortDisableInterrupts();
    }

    uxCriticalNesting++;
}
```

**解说：** 这一段实现函数 `vPortEnterCritical`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 19: 函数 vPortExitCritical

```c
/*-----------------------------------------------------------*/
void vPortExitCritical( void )
{
    uxCriticalNesting--;

    /* If we have reached 0 then re-enable the interrupts. */
    if( uxCriticalNesting == 0 )
    {
        vPortEnableInterrupts();
    }
}
```

**解说：** 这一段实现函数 `vPortExitCritical`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 20: 函数 prvPortYieldFromISR

```c
/*-----------------------------------------------------------*/
static void prvPortYieldFromISR( void )
{
    Thread_t * xThreadToSuspend;
    Thread_t * xThreadToResume;

    xThreadToSuspend = prvGetThreadFromTask( xTaskGetCurrentTaskHandle() );

    vTaskSwitchContext();

    xThreadToResume = prvGetThreadFromTask( xTaskGetCurrentTaskHandle() );

    prvSwitchThread( xThreadToResume, xThreadToSuspend );
}
```

**解说：** 这一段实现函数 `prvPortYieldFromISR`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 21: 函数 vPortYield

```c
/*-----------------------------------------------------------*/
void vPortYield( void )
{
    /* This must never be called from outside of a FreeRTOS-owned thread, or
     * the thread could get stuck in a suspended state. */
    configASSERT( prvIsFreeRTOSThread() == pdTRUE );

    vPortEnterCritical();

    prvPortYieldFromISR();

    vPortExitCritical();
}
```

**解说：** 这一段实现函数 `vPortYield`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 22: 函数 vPortDisableInterrupts

```c
/*-----------------------------------------------------------*/
void vPortDisableInterrupts( void )
{
    if( prvIsFreeRTOSThread() == pdTRUE )
    {
        pthread_sigmask( SIG_BLOCK, &xAllSignals, NULL );
    }
}
```

**解说：** 这一段实现函数 `vPortDisableInterrupts`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 23: 函数 vPortEnableInterrupts

```c
/*-----------------------------------------------------------*/
void vPortEnableInterrupts( void )
{
    if( prvIsFreeRTOSThread() == pdTRUE )
    {
        pthread_sigmask( SIG_UNBLOCK, &xAllSignals, NULL );
    }
}
```

**解说：** 这一段实现函数 `vPortEnableInterrupts`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 24: 函数 xPortSetInterruptMask

```c
/*-----------------------------------------------------------*/
UBaseType_t xPortSetInterruptMask( void )
{
    /* Interrupts are always disabled inside ISRs (signals
     * handlers). */
    return ( UBaseType_t ) 0;
}
```

**解说：** 这一段实现函数 `xPortSetInterruptMask`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 25: 函数 vPortClearInterruptMask

```c
/*-----------------------------------------------------------*/
void vPortClearInterruptMask( UBaseType_t uxMask )
{
    ( void ) uxMask;
}
```

**解说：** 这一段实现函数 `vPortClearInterruptMask`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 26: 函数 prvGetTimeNs

```c
/*-----------------------------------------------------------*/
static uint64_t prvGetTimeNs( void )
{
    struct timespec t;

    clock_gettime( CLOCK_MONOTONIC, &t );

    return ( uint64_t ) t.tv_sec * ( uint64_t ) 1000000000UL + ( uint64_t ) t.tv_nsec;
}
```

**解说：** 这一段实现函数 `prvGetTimeNs`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 27: 函数 prvTimerTickHandler

```c
/*-----------------------------------------------------------*/
/* commented as part of the code below in vPortSystemTickHandler,
 * to adjust timing according to full demo requirements */
/* static uint64_t prvTickCount; */
static void * prvTimerTickHandler( void * arg )
{
    ( void ) arg;

    prvMarkAsFreeRTOSThread();

    prvPortSetCurrentThreadName( "Scheduler timer" );

    while( xTimerTickThreadShouldRun )
    {
        /*
         * signal to the active task to cause tick handling or
         * preemption (if enabled)
         */
        Thread_t * thread = prvGetThreadFromTask( xTaskGetCurrentTaskHandle() );
        pthread_kill( thread->pthread, SIGALRM );
        usleep( portTICK_RATE_MICROSECONDS );
    }

    return NULL;
}
```

**解说：** 这一段实现函数 `prvTimerTickHandler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 28: 函数 prvSetupTimerInterrupt

```c
/*-----------------------------------------------------------*/
/*
 * Setup the systick timer to generate the tick interrupts at the required
 * frequency.
 */
void prvSetupTimerInterrupt( void )
{
    xTimerTickThreadShouldRun = true;
    pthread_create( &hTimerTickThread, NULL, prvTimerTickHandler, NULL );

    prvStartTimeNs = prvGetTimeNs();
}
```

**解说：** 这一段实现函数 `prvSetupTimerInterrupt`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 29: 函数 vPortSystemTickHandler

```c
/*-----------------------------------------------------------*/
static void vPortSystemTickHandler( int sig )
{
    if( prvIsFreeRTOSThread() == pdTRUE )
    {
        Thread_t * pxThreadToSuspend;
        Thread_t * pxThreadToResume;

        ( void ) sig;

        uxCriticalNesting++; /* Signals are blocked in this signal handler. */

        pxThreadToSuspend = prvGetThreadFromTask( xTaskGetCurrentTaskHandle() );

        if( xTaskIncrementTick() != pdFALSE )
        {
            /* Select Next Task. */
            vTaskSwitchContext();

            pxThreadToResume = prvGetThreadFromTask( xTaskGetCurrentTaskHandle() );

            prvSwitchThread( pxThreadToResume, pxThreadToSuspend );
        }

        uxCriticalNesting--;
    }
    else
    {
        fprintf( stderr, "vPortSystemTickHandler called from non-FreeRTOS thread\n" );
    }
}
```

**解说：** 这一段实现函数 `vPortSystemTickHandler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 30: 函数 vPortThreadDying

```c
/*-----------------------------------------------------------*/
void vPortThreadDying( void * pxTaskToDelete,
                       volatile BaseType_t * pxPendYield )
{
    Thread_t * pxThread = prvGetThreadFromTask( pxTaskToDelete );

    ( void ) pxPendYield;

    pxThread->xDying = pdTRUE;
}
```

**解说：** 这一段实现函数 `vPortThreadDying`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 31: 函数 vPortCancelThread

```c
/*-----------------------------------------------------------*/
void vPortCancelThread( void * pxTaskToDelete )
{
    Thread_t * pxThreadToCancel = prvGetThreadFromTask( pxTaskToDelete );

    /*
     * The thread has already been suspended so it can be safely cancelled.
     */
    pthread_cancel( pxThreadToCancel->pthread );
    event_signal( pxThreadToCancel->ev );
    pthread_join( pxThreadToCancel->pthread, NULL );
    event_delete( pxThreadToCancel->ev );
}
```

**解说：** 这一段实现函数 `vPortCancelThread`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 32: 函数 prvWaitForStart

```c
/*-----------------------------------------------------------*/
static void * prvWaitForStart( void * pvParams )
{
    Thread_t * pxThread = pvParams;

    prvMarkAsFreeRTOSThread();

    prvSuspendSelf( pxThread );

    /* Resumed for the first time, unblocks all signals. */
    uxCriticalNesting = 0;
    vPortEnableInterrupts();

    /* Set thread name */
    prvPortSetCurrentThreadName( pcTaskGetName( xTaskGetCurrentTaskHandle() ) );

    /* Call the task's entry point. */
    pxThread->pxCode( pxThread->pvParams );

    /* A function that implements a task must not exit or attempt to return to
     * its caller as there is nothing to return to. If a task wants to exit it
     * should instead call vTaskDelete( NULL ). Artificially force an assert()
     * to be triggered if configASSERT() is defined, so application writers can
     * catch the error. */
    configASSERT( pdFALSE );

    return NULL;
}
```

**解说：** 这一段实现函数 `prvWaitForStart`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 33: 函数 prvSwitchThread

```c
/*-----------------------------------------------------------*/
static void prvSwitchThread( Thread_t * pxThreadToResume,
                             Thread_t * pxThreadToSuspend )
{
    BaseType_t uxSavedCriticalNesting;

    if( pxThreadToSuspend != pxThreadToResume )
    {
        /*
         * Switch tasks.
         *
         * The critical section nesting is per-task, so save it on the
         * stack of the current (suspending thread), restoring it when
         * we switch back to this task.
         */
        uxSavedCriticalNesting = uxCriticalNesting;

        prvResumeThread( pxThreadToResume );

        if( pxThreadToSuspend->xDying == pdTRUE )
        {
            pthread_exit( NULL );
        }

        prvSuspendSelf( pxThreadToSuspend );

        uxCriticalNesting = uxSavedCriticalNesting;
    }
}
```

**解说：** 这一段实现函数 `prvSwitchThread`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 34: 函数 prvSuspendSelf

```c
/*-----------------------------------------------------------*/
static void prvSuspendSelf( Thread_t * thread )
{
    /*
     * Suspend this thread by waiting for a pthread_cond_signal event.
     *
     * A suspended thread must not handle signals (interrupts) so
     * all signals must be blocked by calling this from:
     *
     * - Inside a critical section (vPortEnterCritical() /
     *   vPortExitCritical()).
     *
     * - From a signal handler that has all signals masked.
     *
     * - A thread with all signals blocked with pthread_sigmask().
     */
    event_wait( thread->ev );
    pthread_testcancel();
}
```

**解说：** 这一段实现函数 `prvSuspendSelf`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 35: 函数 prvResumeThread

```c
/*-----------------------------------------------------------*/
static void prvResumeThread( Thread_t * xThreadId )
{
    if( pthread_self() != xThreadId->pthread )
    {
        event_signal( xThreadId->ev );
    }
}
```

**解说：** 这一段实现函数 `prvResumeThread`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 36: 函数 prvSetupSignalsAndSchedulerPolicy

```c
/*-----------------------------------------------------------*/
static void prvSetupSignalsAndSchedulerPolicy( void )
{
    struct sigaction sigtick;
    int iRet;

    hMainThread = pthread_self();

    /* Initialise common signal masks. */
    sigfillset( &xAllSignals );

    /* Don't block SIGINT so this can be used to break into GDB while
     * in a critical section. */
    sigdelset( &xAllSignals, SIGINT );

    /*
     * Block all signals in this thread so all new threads
     * inherits this mask.
     *
     * When a thread is resumed for the first time, all signals
     * will be unblocked.
     */
    ( void ) pthread_sigmask( SIG_SETMASK,
                              &xAllSignals,
                              &xSchedulerOriginalSignalMask );

    sigtick.sa_flags = 0;
    sigtick.sa_handler = vPortSystemTickHandler;
    sigfillset( &sigtick.sa_mask );

    iRet = sigaction( SIGALRM, &sigtick, NULL );

    if( iRet == -1 )
    {
        prvFatalError( "sigaction", errno );
    }
}
```

**解说：** 这一段实现函数 `prvSetupSignalsAndSchedulerPolicy`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 37: 函数 ulPortGetRunTime

```c
/*-----------------------------------------------------------*/
uint32_t ulPortGetRunTime( void )
{
    struct tms xTimes;

    times( &xTimes );

    return ( uint32_t ) xTimes.tms_utime;
}
```

**解说：** 这一段实现函数 `ulPortGetRunTime`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 38: 说明性注释

```c
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。
