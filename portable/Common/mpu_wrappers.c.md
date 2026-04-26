# mpu_wrappers.c 代码解说

源文件：`portable/Common/mpu_wrappers.c`

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

## 片段 2: 宏 MPU_WRAPPERS_INCLUDED_FROM_API_FILE

```c
/*
 * Implementation of the wrapper functions used to raise the processor privilege
 * before calling a standard FreeRTOS API function.
 */
/* Defining MPU_WRAPPERS_INCLUDED_FROM_API_FILE prevents task.h from redefining
 * all the API functions to use the MPU wrappers.  That should only be done when
 * task.h is included from an application file. */
#define MPU_WRAPPERS_INCLUDED_FROM_API_FILE

/* Scheduler includes. */
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "timers.h"
#include "event_groups.h"
#include "stream_buffer.h"
#include "mpu_prototypes.h"

#undef MPU_WRAPPERS_INCLUDED_FROM_API_FILE
/*-----------------------------------------------------------*/

#if ( ( portUSING_MPU_WRAPPERS == 1 ) && ( configUSE_MPU_WRAPPERS_V1 == 1 ) )

    #if ( configENABLE_ACCESS_CONTROL_LIST == 1 )
        #error Access control list is not available with this MPU wrapper. Please set configENABLE_ACCESS_CONTROL_LIST to 0.
    #endif
```

**解说：** 这一段定义宏 `MPU_WRAPPERS_INCLUDED_FROM_API_FILE`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 3: 预处理配置 MPU_xTaskCreate

```c
    #if ( configSUPPORT_DYNAMIC_ALLOCATION == 1 )
        BaseType_t MPU_xTaskCreate( TaskFunction_t pvTaskCode,
                                    const char * const pcName,
                                    const configSTACK_DEPTH_TYPE uxStackDepth,
                                    void * pvParameters,
                                    UBaseType_t uxPriority,
                                    TaskHandle_t * pxCreatedTask ) /* FREERTOS_SYSTEM_CALL */
        {
            BaseType_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                uxPriority = uxPriority & ~( portPRIVILEGE_BIT );
                portMEMORY_BARRIER();

                xReturn = xTaskCreate( pvTaskCode, pcName, uxStackDepth, pvParameters, uxPriority, pxCreatedTask );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xTaskCreate( pvTaskCode, pcName, uxStackDepth, pvParameters, uxPriority, pxCreatedTask );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 4: 预处理配置

```c
    #endif /* configSUPPORT_DYNAMIC_ALLOCATION */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 5: 预处理配置 MPU_xTaskCreateStatic

```c
/*-----------------------------------------------------------*/
    #if ( configSUPPORT_STATIC_ALLOCATION == 1 )
        TaskHandle_t MPU_xTaskCreateStatic( TaskFunction_t pxTaskCode,
                                            const char * const pcName,
                                            const configSTACK_DEPTH_TYPE uxStackDepth,
                                            void * const pvParameters,
                                            UBaseType_t uxPriority,
                                            StackType_t * const puxStackBuffer,
                                            StaticTask_t * const pxTaskBuffer ) /* FREERTOS_SYSTEM_CALL */
        {
            TaskHandle_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                uxPriority = uxPriority & ~( portPRIVILEGE_BIT );
                portMEMORY_BARRIER();

                xReturn = xTaskCreateStatic( pxTaskCode, pcName, uxStackDepth, pvParameters, uxPriority, puxStackBuffer, pxTaskBuffer );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xTaskCreateStatic( pxTaskCode, pcName, uxStackDepth, pvParameters, uxPriority, puxStackBuffer, pxTaskBuffer );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 6: 预处理配置

```c
    #endif /* configSUPPORT_STATIC_ALLOCATION */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 7: 预处理配置 MPU_vTaskDelete

```c
/*-----------------------------------------------------------*/
    #if ( INCLUDE_vTaskDelete == 1 )
        void MPU_vTaskDelete( TaskHandle_t pxTaskToDelete ) /* FREERTOS_SYSTEM_CALL */
        {
            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                vTaskDelete( pxTaskToDelete );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                vTaskDelete( pxTaskToDelete );
            }
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 8: 预处理配置

```c
    #endif /* if ( INCLUDE_vTaskDelete == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 9: 预处理配置 MPU_xTaskDelayUntil

```c
/*-----------------------------------------------------------*/
    #if ( INCLUDE_xTaskDelayUntil == 1 )
        BaseType_t MPU_xTaskDelayUntil( TickType_t * const pxPreviousWakeTime,
                                        TickType_t xTimeIncrement ) /* FREERTOS_SYSTEM_CALL */
        {
            BaseType_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xTaskDelayUntil( pxPreviousWakeTime, xTimeIncrement );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xTaskDelayUntil( pxPreviousWakeTime, xTimeIncrement );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 10: 预处理配置

```c
    #endif /* if ( INCLUDE_xTaskDelayUntil == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 11: 预处理配置 MPU_xTaskAbortDelay

```c
/*-----------------------------------------------------------*/
    #if ( INCLUDE_xTaskAbortDelay == 1 )
        BaseType_t MPU_xTaskAbortDelay( TaskHandle_t xTask ) /* FREERTOS_SYSTEM_CALL */
        {
            BaseType_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xTaskAbortDelay( xTask );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xTaskAbortDelay( xTask );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 12: 预处理配置

```c
    #endif /* if ( INCLUDE_xTaskAbortDelay == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 13: 预处理配置 MPU_vTaskDelay

```c
/*-----------------------------------------------------------*/
    #if ( INCLUDE_vTaskDelay == 1 )
        void MPU_vTaskDelay( TickType_t xTicksToDelay ) /* FREERTOS_SYSTEM_CALL */
        {
            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                vTaskDelay( xTicksToDelay );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                vTaskDelay( xTicksToDelay );
            }
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 14: 预处理配置

```c
    #endif /* if ( INCLUDE_vTaskDelay == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 15: 预处理配置 MPU_uxTaskPriorityGet

```c
/*-----------------------------------------------------------*/
    #if ( INCLUDE_uxTaskPriorityGet == 1 )
        UBaseType_t MPU_uxTaskPriorityGet( const TaskHandle_t pxTask ) /* FREERTOS_SYSTEM_CALL */
        {
            UBaseType_t uxReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                uxReturn = uxTaskPriorityGet( pxTask );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                uxReturn = uxTaskPriorityGet( pxTask );
            }

            return uxReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 16: 预处理配置

```c
    #endif /* if ( INCLUDE_uxTaskPriorityGet == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 17: 预处理配置 MPU_vTaskPrioritySet

```c
/*-----------------------------------------------------------*/
    #if ( INCLUDE_vTaskPrioritySet == 1 )
        void MPU_vTaskPrioritySet( TaskHandle_t pxTask,
                                   UBaseType_t uxNewPriority ) /* FREERTOS_SYSTEM_CALL */
        {
            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                vTaskPrioritySet( pxTask, uxNewPriority );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                vTaskPrioritySet( pxTask, uxNewPriority );
            }
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 18: 预处理配置

```c
    #endif /* if ( INCLUDE_vTaskPrioritySet == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 19: 预处理配置

```c
/*-----------------------------------------------------------*/
    #if ( INCLUDE_eTaskGetState == 1 )
        eTaskState MPU_eTaskGetState( TaskHandle_t pxTask ) /* FREERTOS_SYSTEM_CALL */
        {
            eTaskState eReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                eReturn = eTaskGetState( pxTask );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                eReturn = eTaskGetState( pxTask );
            }

            return eReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 20: 预处理配置

```c
    #endif /* if ( INCLUDE_eTaskGetState == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 21: 预处理配置 MPU_vTaskGetInfo

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_TRACE_FACILITY == 1 )
        void MPU_vTaskGetInfo( TaskHandle_t xTask,
                               TaskStatus_t * pxTaskStatus,
                               BaseType_t xGetFreeStackSpace,
                               eTaskState eState ) /* FREERTOS_SYSTEM_CALL */
        {
            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                vTaskGetInfo( xTask, pxTaskStatus, xGetFreeStackSpace, eState );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                vTaskGetInfo( xTask, pxTaskStatus, xGetFreeStackSpace, eState );
            }
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 22: 预处理配置

```c
    #endif /* if ( configUSE_TRACE_FACILITY == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 23: 预处理配置 MPU_xTaskGetIdleTaskHandle

```c
/*-----------------------------------------------------------*/
    #if ( INCLUDE_xTaskGetIdleTaskHandle == 1 )
        TaskHandle_t MPU_xTaskGetIdleTaskHandle( void ) /* FREERTOS_SYSTEM_CALL */
        {
            TaskHandle_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();
                xReturn = xTaskGetIdleTaskHandle();
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xTaskGetIdleTaskHandle();
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 24: 预处理配置

```c
    #endif /* if ( INCLUDE_xTaskGetIdleTaskHandle == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 25: 预处理配置 MPU_vTaskSuspend

```c
/*-----------------------------------------------------------*/
    #if ( INCLUDE_vTaskSuspend == 1 )
        void MPU_vTaskSuspend( TaskHandle_t pxTaskToSuspend ) /* FREERTOS_SYSTEM_CALL */
        {
            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                vTaskSuspend( pxTaskToSuspend );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                vTaskSuspend( pxTaskToSuspend );
            }
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 26: 预处理配置

```c
    #endif /* if ( INCLUDE_vTaskSuspend == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 27: 预处理配置 MPU_vTaskResume

```c
/*-----------------------------------------------------------*/
    #if ( INCLUDE_vTaskSuspend == 1 )
        void MPU_vTaskResume( TaskHandle_t pxTaskToResume ) /* FREERTOS_SYSTEM_CALL */
        {
            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                vTaskResume( pxTaskToResume );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                vTaskResume( pxTaskToResume );
            }
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 28: 预处理配置

```c
    #endif /* if ( INCLUDE_vTaskSuspend == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 29: 函数 MPU_vTaskSuspendAll

```c
/*-----------------------------------------------------------*/
    void MPU_vTaskSuspendAll( void ) /* FREERTOS_SYSTEM_CALL */
    {
        if( portIS_PRIVILEGED() == pdFALSE )
        {
            portRAISE_PRIVILEGE();
            portMEMORY_BARRIER();

            vTaskSuspendAll();
            portMEMORY_BARRIER();

            portRESET_PRIVILEGE();
            portMEMORY_BARRIER();
        }
        else
        {
            vTaskSuspendAll();
        }
    }
```

**解说：** 这一段实现函数 `MPU_vTaskSuspendAll`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 30: 函数 MPU_xTaskResumeAll

```c
/*-----------------------------------------------------------*/
    BaseType_t MPU_xTaskResumeAll( void ) /* FREERTOS_SYSTEM_CALL */
    {
        BaseType_t xReturn;

        if( portIS_PRIVILEGED() == pdFALSE )
        {
            portRAISE_PRIVILEGE();
            portMEMORY_BARRIER();

            xReturn = xTaskResumeAll();
            portMEMORY_BARRIER();

            portRESET_PRIVILEGE();
            portMEMORY_BARRIER();
        }
        else
        {
            xReturn = xTaskResumeAll();
        }

        return xReturn;
    }
```

**解说：** 这一段实现函数 `MPU_xTaskResumeAll`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 31: 函数 MPU_xTaskGetTickCount

```c
/*-----------------------------------------------------------*/
    TickType_t MPU_xTaskGetTickCount( void ) /* FREERTOS_SYSTEM_CALL */
    {
        TickType_t xReturn;

        if( portIS_PRIVILEGED() == pdFALSE )
        {
            portRAISE_PRIVILEGE();
            portMEMORY_BARRIER();

            xReturn = xTaskGetTickCount();
            portMEMORY_BARRIER();

            portRESET_PRIVILEGE();
            portMEMORY_BARRIER();
        }
        else
        {
            xReturn = xTaskGetTickCount();
        }

        return xReturn;
    }
```

**解说：** 这一段实现函数 `MPU_xTaskGetTickCount`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 32: 函数 MPU_uxTaskGetNumberOfTasks

```c
/*-----------------------------------------------------------*/
    UBaseType_t MPU_uxTaskGetNumberOfTasks( void ) /* FREERTOS_SYSTEM_CALL */
    {
        UBaseType_t uxReturn;

        if( portIS_PRIVILEGED() == pdFALSE )
        {
            portRAISE_PRIVILEGE();
            portMEMORY_BARRIER();

            uxReturn = uxTaskGetNumberOfTasks();
            portMEMORY_BARRIER();

            portRESET_PRIVILEGE();
            portMEMORY_BARRIER();
        }
        else
        {
            uxReturn = uxTaskGetNumberOfTasks();
        }

        return uxReturn;
    }
```

**解说：** 这一段实现函数 `MPU_uxTaskGetNumberOfTasks`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 33: 预处理配置 MPU_xTaskGetHandle

```c
/*-----------------------------------------------------------*/
    #if ( INCLUDE_xTaskGetHandle == 1 )
        TaskHandle_t MPU_xTaskGetHandle( const char * pcNameToQuery ) /* FREERTOS_SYSTEM_CALL */
        {
            TaskHandle_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xTaskGetHandle( pcNameToQuery );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xTaskGetHandle( pcNameToQuery );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 34: 预处理配置

```c
    #endif /* if ( INCLUDE_xTaskGetHandle == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 35: 预处理配置 MPU_vTaskListTasks

```c
/*-----------------------------------------------------------*/
    #if ( ( configUSE_TRACE_FACILITY == 1 ) && ( configUSE_STATS_FORMATTING_FUNCTIONS > 0 ) && ( configSUPPORT_DYNAMIC_ALLOCATION == 1 ) )
        void MPU_vTaskListTasks( char * pcWriteBuffer,
                                 size_t uxBufferLength ) /* FREERTOS_SYSTEM_CALL */
        {
            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                vTaskListTasks( pcWriteBuffer, uxBufferLength );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                vTaskListTasks( pcWriteBuffer, uxBufferLength );
            }
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 36: 预处理配置

```c
    #endif /* if ( ( configUSE_TRACE_FACILITY == 1 ) && ( configUSE_STATS_FORMATTING_FUNCTIONS > 0 ) && ( configSUPPORT_DYNAMIC_ALLOCATION == 1 ) ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 37: 预处理配置 MPU_vTaskGetRunTimeStatistics

```c
/*-----------------------------------------------------------*/
    #if ( ( configGENERATE_RUN_TIME_STATS == 1 ) && ( configUSE_STATS_FORMATTING_FUNCTIONS > 0 ) && ( configSUPPORT_DYNAMIC_ALLOCATION == 1 ) )
        void MPU_vTaskGetRunTimeStatistics( char * pcWriteBuffer,
                                            size_t uxBufferLength ) /* FREERTOS_SYSTEM_CALL */
        {
            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                vTaskGetRunTimeStatistics( pcWriteBuffer, uxBufferLength );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                vTaskGetRunTimeStatistics( pcWriteBuffer, uxBufferLength );
            }
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 38: 预处理配置

```c
    #endif /* if ( ( configGENERATE_RUN_TIME_STATS == 1 ) && ( configUSE_STATS_FORMATTING_FUNCTIONS > 0 ) && ( configSUPPORT_DYNAMIC_ALLOCATION == 1 ) ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 39: 预处理配置

```c
/*-----------------------------------------------------------*/
    #if ( ( configGENERATE_RUN_TIME_STATS == 1 ) && ( INCLUDE_xTaskGetIdleTaskHandle == 1 ) )
        configRUN_TIME_COUNTER_TYPE MPU_ulTaskGetIdleRunTimePercent( void ) /* FREERTOS_SYSTEM_CALL */
        {
            configRUN_TIME_COUNTER_TYPE xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = ulTaskGetIdleRunTimePercent();
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = ulTaskGetIdleRunTimePercent();
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 40: 预处理配置

```c
    #endif /* if ( ( configGENERATE_RUN_TIME_STATS == 1 ) && ( INCLUDE_xTaskGetIdleTaskHandle == 1 ) ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 41: 预处理配置

```c
/*-----------------------------------------------------------*/
    #if ( ( configGENERATE_RUN_TIME_STATS == 1 ) && ( INCLUDE_xTaskGetIdleTaskHandle == 1 ) )
        configRUN_TIME_COUNTER_TYPE MPU_ulTaskGetIdleRunTimeCounter( void ) /* FREERTOS_SYSTEM_CALL */
        {
            configRUN_TIME_COUNTER_TYPE xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = ulTaskGetIdleRunTimeCounter();
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = ulTaskGetIdleRunTimeCounter();
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 42: 预处理配置

```c
    #endif /* if ( ( configGENERATE_RUN_TIME_STATS == 1 ) && ( INCLUDE_xTaskGetIdleTaskHandle == 1 ) ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 43: 预处理配置 MPU_vTaskSetApplicationTaskTag

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_APPLICATION_TASK_TAG == 1 )
        void MPU_vTaskSetApplicationTaskTag( TaskHandle_t xTask,
                                             TaskHookFunction_t pxTagValue ) /* FREERTOS_SYSTEM_CALL */
        {
            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                vTaskSetApplicationTaskTag( xTask, pxTagValue );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                vTaskSetApplicationTaskTag( xTask, pxTagValue );
            }
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 44: 预处理配置

```c
    #endif /* if ( configUSE_APPLICATION_TASK_TAG == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 45: 预处理配置

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_APPLICATION_TASK_TAG == 1 )
        TaskHookFunction_t MPU_xTaskGetApplicationTaskTag( TaskHandle_t xTask ) /* FREERTOS_SYSTEM_CALL */
        {
            TaskHookFunction_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xTaskGetApplicationTaskTag( xTask );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xTaskGetApplicationTaskTag( xTask );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 46: 预处理配置

```c
    #endif /* if ( configUSE_APPLICATION_TASK_TAG == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 47: 预处理配置 MPU_vTaskSetThreadLocalStoragePointer

```c
/*-----------------------------------------------------------*/
    #if ( configNUM_THREAD_LOCAL_STORAGE_POINTERS != 0 )
        void MPU_vTaskSetThreadLocalStoragePointer( TaskHandle_t xTaskToSet,
                                                    BaseType_t xIndex,
                                                    void * pvValue ) /* FREERTOS_SYSTEM_CALL */
        {
            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                vTaskSetThreadLocalStoragePointer( xTaskToSet, xIndex, pvValue );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                vTaskSetThreadLocalStoragePointer( xTaskToSet, xIndex, pvValue );
            }
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 48: 预处理配置

```c
    #endif /* if ( configNUM_THREAD_LOCAL_STORAGE_POINTERS != 0 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 49: 预处理配置 MPU_pvTaskGetThreadLocalStoragePointer

```c
/*-----------------------------------------------------------*/
    #if ( configNUM_THREAD_LOCAL_STORAGE_POINTERS != 0 )
        void * MPU_pvTaskGetThreadLocalStoragePointer( TaskHandle_t xTaskToQuery,
                                                       BaseType_t xIndex ) /* FREERTOS_SYSTEM_CALL */
        {
            void * pvReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                pvReturn = pvTaskGetThreadLocalStoragePointer( xTaskToQuery, xIndex );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                pvReturn = pvTaskGetThreadLocalStoragePointer( xTaskToQuery, xIndex );
            }

            return pvReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 50: 预处理配置

```c
    #endif /* if ( configNUM_THREAD_LOCAL_STORAGE_POINTERS != 0 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 51: 预处理配置 MPU_xTaskCallApplicationTaskHook

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_APPLICATION_TASK_TAG == 1 )
        BaseType_t MPU_xTaskCallApplicationTaskHook( TaskHandle_t xTask,
                                                     void * pvParameter ) /* FREERTOS_SYSTEM_CALL */
        {
            BaseType_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xTaskCallApplicationTaskHook( xTask, pvParameter );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xTaskCallApplicationTaskHook( xTask, pvParameter );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 52: 预处理配置

```c
    #endif /* if ( configUSE_APPLICATION_TASK_TAG == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 53: 预处理配置 MPU_uxTaskGetSystemState

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_TRACE_FACILITY == 1 )
        UBaseType_t MPU_uxTaskGetSystemState( TaskStatus_t * pxTaskStatusArray,
                                              UBaseType_t uxArraySize,
                                              configRUN_TIME_COUNTER_TYPE * pulTotalRunTime ) /* FREERTOS_SYSTEM_CALL */
        {
            UBaseType_t uxReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                uxReturn = uxTaskGetSystemState( pxTaskStatusArray, uxArraySize, pulTotalRunTime );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                uxReturn = uxTaskGetSystemState( pxTaskStatusArray, uxArraySize, pulTotalRunTime );
            }

            return uxReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 54: 预处理配置

```c
    #endif /* if ( configUSE_TRACE_FACILITY == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 55: 函数 MPU_xTaskCatchUpTicks

```c
/*-----------------------------------------------------------*/
    BaseType_t MPU_xTaskCatchUpTicks( TickType_t xTicksToCatchUp ) /* FREERTOS_SYSTEM_CALL */
    {
        BaseType_t xReturn;

        if( portIS_PRIVILEGED() == pdFALSE )
        {
            portRAISE_PRIVILEGE();
            portMEMORY_BARRIER();

            xReturn = xTaskCatchUpTicks( xTicksToCatchUp );
            portMEMORY_BARRIER();

            portRESET_PRIVILEGE();
            portMEMORY_BARRIER();
        }
        else
        {
            xReturn = xTaskCatchUpTicks( xTicksToCatchUp );
        }

        return xReturn;
    }
```

**解说：** 这一段实现函数 `MPU_xTaskCatchUpTicks`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 56: 预处理配置 MPU_uxTaskGetStackHighWaterMark

```c
/*-----------------------------------------------------------*/
    #if ( INCLUDE_uxTaskGetStackHighWaterMark == 1 )
        UBaseType_t MPU_uxTaskGetStackHighWaterMark( TaskHandle_t xTask ) /* FREERTOS_SYSTEM_CALL */
        {
            UBaseType_t uxReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                uxReturn = uxTaskGetStackHighWaterMark( xTask );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                uxReturn = uxTaskGetStackHighWaterMark( xTask );
            }

            return uxReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 57: 预处理配置

```c
    #endif /* if ( INCLUDE_uxTaskGetStackHighWaterMark == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 58: 预处理配置

```c
/*-----------------------------------------------------------*/
    #if ( INCLUDE_uxTaskGetStackHighWaterMark2 == 1 )
        configSTACK_DEPTH_TYPE MPU_uxTaskGetStackHighWaterMark2( TaskHandle_t xTask ) /* FREERTOS_SYSTEM_CALL */
        {
            configSTACK_DEPTH_TYPE uxReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                uxReturn = uxTaskGetStackHighWaterMark2( xTask );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                uxReturn = uxTaskGetStackHighWaterMark2( xTask );
            }

            return uxReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 59: 预处理配置

```c
    #endif /* if ( INCLUDE_uxTaskGetStackHighWaterMark2 == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 60: 预处理配置 MPU_xTaskGetCurrentTaskHandle

```c
/*-----------------------------------------------------------*/
    #if ( ( INCLUDE_xTaskGetCurrentTaskHandle == 1 ) || ( configUSE_RECURSIVE_MUTEXES == 1 ) )
        TaskHandle_t MPU_xTaskGetCurrentTaskHandle( void ) /* FREERTOS_SYSTEM_CALL */
        {
            TaskHandle_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();
                xReturn = xTaskGetCurrentTaskHandle();
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xTaskGetCurrentTaskHandle();
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 61: 预处理配置

```c
    #endif /* if ( ( INCLUDE_xTaskGetCurrentTaskHandle == 1 ) || ( configUSE_RECURSIVE_MUTEXES == 1 ) ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 62: 预处理配置 MPU_xTaskGetSchedulerState

```c
/*-----------------------------------------------------------*/
    #if ( INCLUDE_xTaskGetSchedulerState == 1 )
        BaseType_t MPU_xTaskGetSchedulerState( void ) /* FREERTOS_SYSTEM_CALL */
        {
            BaseType_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xTaskGetSchedulerState();
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xTaskGetSchedulerState();
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 63: 预处理配置

```c
    #endif /* if ( INCLUDE_xTaskGetSchedulerState == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 64: 函数 MPU_vTaskSetTimeOutState

```c
/*-----------------------------------------------------------*/
    void MPU_vTaskSetTimeOutState( TimeOut_t * const pxTimeOut ) /* FREERTOS_SYSTEM_CALL */
    {
        if( portIS_PRIVILEGED() == pdFALSE )
        {
            portRAISE_PRIVILEGE();
            portMEMORY_BARRIER();

            vTaskSetTimeOutState( pxTimeOut );
            portMEMORY_BARRIER();

            portRESET_PRIVILEGE();
            portMEMORY_BARRIER();
        }
        else
        {
            vTaskSetTimeOutState( pxTimeOut );
        }
    }
```

**解说：** 这一段实现函数 `MPU_vTaskSetTimeOutState`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 65: 函数 MPU_xTaskCheckForTimeOut

```c
/*-----------------------------------------------------------*/
    BaseType_t MPU_xTaskCheckForTimeOut( TimeOut_t * const pxTimeOut,
                                         TickType_t * const pxTicksToWait ) /* FREERTOS_SYSTEM_CALL */
    {
        BaseType_t xReturn;

        if( portIS_PRIVILEGED() == pdFALSE )
        {
            portRAISE_PRIVILEGE();
            portMEMORY_BARRIER();

            xReturn = xTaskCheckForTimeOut( pxTimeOut, pxTicksToWait );
            portMEMORY_BARRIER();

            portRESET_PRIVILEGE();
            portMEMORY_BARRIER();
        }
        else
        {
            xReturn = xTaskCheckForTimeOut( pxTimeOut, pxTicksToWait );
        }

        return xReturn;
    }
```

**解说：** 这一段实现函数 `MPU_xTaskCheckForTimeOut`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 66: 预处理配置 MPU_xTaskGenericNotify

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_TASK_NOTIFICATIONS == 1 )
        BaseType_t MPU_xTaskGenericNotify( TaskHandle_t xTaskToNotify,
                                           UBaseType_t uxIndexToNotify,
                                           uint32_t ulValue,
                                           eNotifyAction eAction,
                                           uint32_t * pulPreviousNotificationValue ) /* FREERTOS_SYSTEM_CALL */
        {
            BaseType_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xTaskGenericNotify( xTaskToNotify, uxIndexToNotify, ulValue, eAction, pulPreviousNotificationValue );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xTaskGenericNotify( xTaskToNotify, uxIndexToNotify, ulValue, eAction, pulPreviousNotificationValue );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 67: 预处理配置

```c
    #endif /* if ( configUSE_TASK_NOTIFICATIONS == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 68: 预处理配置 MPU_xTaskGenericNotifyWait

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_TASK_NOTIFICATIONS == 1 )
        BaseType_t MPU_xTaskGenericNotifyWait( UBaseType_t uxIndexToWaitOn,
                                               uint32_t ulBitsToClearOnEntry,
                                               uint32_t ulBitsToClearOnExit,
                                               uint32_t * pulNotificationValue,
                                               TickType_t xTicksToWait ) /* FREERTOS_SYSTEM_CALL */
        {
            BaseType_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xTaskGenericNotifyWait( uxIndexToWaitOn, ulBitsToClearOnEntry, ulBitsToClearOnExit, pulNotificationValue, xTicksToWait );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xTaskGenericNotifyWait( uxIndexToWaitOn, ulBitsToClearOnEntry, ulBitsToClearOnExit, pulNotificationValue, xTicksToWait );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 69: 预处理配置

```c
    #endif /* if ( configUSE_TASK_NOTIFICATIONS == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 70: 预处理配置 MPU_ulTaskGenericNotifyTake

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_TASK_NOTIFICATIONS == 1 )
        uint32_t MPU_ulTaskGenericNotifyTake( UBaseType_t uxIndexToWaitOn,
                                              BaseType_t xClearCountOnExit,
                                              TickType_t xTicksToWait ) /* FREERTOS_SYSTEM_CALL */
        {
            uint32_t ulReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                ulReturn = ulTaskGenericNotifyTake( uxIndexToWaitOn, xClearCountOnExit, xTicksToWait );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                ulReturn = ulTaskGenericNotifyTake( uxIndexToWaitOn, xClearCountOnExit, xTicksToWait );
            }

            return ulReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 71: 预处理配置

```c
    #endif /* if ( configUSE_TASK_NOTIFICATIONS == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 72: 预处理配置 MPU_xTaskGenericNotifyStateClear

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_TASK_NOTIFICATIONS == 1 )
        BaseType_t MPU_xTaskGenericNotifyStateClear( TaskHandle_t xTask,
                                                     UBaseType_t uxIndexToClear ) /* FREERTOS_SYSTEM_CALL */
        {
            BaseType_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xTaskGenericNotifyStateClear( xTask, uxIndexToClear );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xTaskGenericNotifyStateClear( xTask, uxIndexToClear );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 73: 预处理配置

```c
    #endif /* if ( configUSE_TASK_NOTIFICATIONS == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 74: 预处理配置 MPU_ulTaskGenericNotifyValueClear

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_TASK_NOTIFICATIONS == 1 )
        uint32_t MPU_ulTaskGenericNotifyValueClear( TaskHandle_t xTask,
                                                    UBaseType_t uxIndexToClear,
                                                    uint32_t ulBitsToClear ) /* FREERTOS_SYSTEM_CALL */
        {
            uint32_t ulReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                ulReturn = ulTaskGenericNotifyValueClear( xTask, uxIndexToClear, ulBitsToClear );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                ulReturn = ulTaskGenericNotifyValueClear( xTask, uxIndexToClear, ulBitsToClear );
            }

            return ulReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 75: 预处理配置

```c
    #endif /* if ( configUSE_TASK_NOTIFICATIONS == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 76: 预处理配置 MPU_xQueueGenericCreate

```c
/*-----------------------------------------------------------*/
    #if ( configSUPPORT_DYNAMIC_ALLOCATION == 1 )
        QueueHandle_t MPU_xQueueGenericCreate( UBaseType_t uxQueueLength,
                                               UBaseType_t uxItemSize,
                                               uint8_t ucQueueType ) /* FREERTOS_SYSTEM_CALL */
        {
            QueueHandle_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xQueueGenericCreate( uxQueueLength, uxItemSize, ucQueueType );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xQueueGenericCreate( uxQueueLength, uxItemSize, ucQueueType );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 77: 预处理配置

```c
    #endif /* if ( configSUPPORT_DYNAMIC_ALLOCATION == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 78: 预处理配置 MPU_xQueueGenericCreateStatic

```c
/*-----------------------------------------------------------*/
    #if ( configSUPPORT_STATIC_ALLOCATION == 1 )
        QueueHandle_t MPU_xQueueGenericCreateStatic( const UBaseType_t uxQueueLength,
                                                     const UBaseType_t uxItemSize,
                                                     uint8_t * pucQueueStorage,
                                                     StaticQueue_t * pxStaticQueue,
                                                     const uint8_t ucQueueType ) /* FREERTOS_SYSTEM_CALL */
        {
            QueueHandle_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xQueueGenericCreateStatic( uxQueueLength, uxItemSize, pucQueueStorage, pxStaticQueue, ucQueueType );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xQueueGenericCreateStatic( uxQueueLength, uxItemSize, pucQueueStorage, pxStaticQueue, ucQueueType );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 79: 预处理配置

```c
    #endif /* if ( configSUPPORT_STATIC_ALLOCATION == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 80: 函数 MPU_xQueueGenericReset

```c
/*-----------------------------------------------------------*/
    BaseType_t MPU_xQueueGenericReset( QueueHandle_t pxQueue,
                                       BaseType_t xNewQueue ) /* FREERTOS_SYSTEM_CALL */
    {
        BaseType_t xReturn;

        if( portIS_PRIVILEGED() == pdFALSE )
        {
            portRAISE_PRIVILEGE();
            portMEMORY_BARRIER();

            xReturn = xQueueGenericReset( pxQueue, xNewQueue );
            portMEMORY_BARRIER();

            portRESET_PRIVILEGE();
            portMEMORY_BARRIER();
        }
        else
        {
            xReturn = xQueueGenericReset( pxQueue, xNewQueue );
        }

        return xReturn;
    }
```

**解说：** 这一段实现函数 `MPU_xQueueGenericReset`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 81: 函数 MPU_xQueueGenericSend

```c
/*-----------------------------------------------------------*/
    BaseType_t MPU_xQueueGenericSend( QueueHandle_t xQueue,
                                      const void * const pvItemToQueue,
                                      TickType_t xTicksToWait,
                                      BaseType_t xCopyPosition ) /* FREERTOS_SYSTEM_CALL */
    {
        BaseType_t xReturn;

        if( portIS_PRIVILEGED() == pdFALSE )
        {
            portRAISE_PRIVILEGE();
            portMEMORY_BARRIER();

            xReturn = xQueueGenericSend( xQueue, pvItemToQueue, xTicksToWait, xCopyPosition );
            portMEMORY_BARRIER();

            portRESET_PRIVILEGE();
            portMEMORY_BARRIER();
        }
        else
        {
            xReturn = xQueueGenericSend( xQueue, pvItemToQueue, xTicksToWait, xCopyPosition );
        }

        return xReturn;
    }
```

**解说：** 这一段实现函数 `MPU_xQueueGenericSend`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 82: 函数 MPU_uxQueueMessagesWaiting

```c
/*-----------------------------------------------------------*/
    UBaseType_t MPU_uxQueueMessagesWaiting( const QueueHandle_t pxQueue ) /* FREERTOS_SYSTEM_CALL */
    {
        UBaseType_t uxReturn;

        if( portIS_PRIVILEGED() == pdFALSE )
        {
            portRAISE_PRIVILEGE();
            portMEMORY_BARRIER();

            uxReturn = uxQueueMessagesWaiting( pxQueue );
            portMEMORY_BARRIER();

            portRESET_PRIVILEGE();
            portMEMORY_BARRIER();
        }
        else
        {
            uxReturn = uxQueueMessagesWaiting( pxQueue );
        }

        return uxReturn;
    }
```

**解说：** 这一段实现函数 `MPU_uxQueueMessagesWaiting`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 83: 函数 MPU_uxQueueSpacesAvailable

```c
/*-----------------------------------------------------------*/
    UBaseType_t MPU_uxQueueSpacesAvailable( const QueueHandle_t xQueue ) /* FREERTOS_SYSTEM_CALL */
    {
        UBaseType_t uxReturn;

        if( portIS_PRIVILEGED() == pdFALSE )
        {
            portRAISE_PRIVILEGE();
            portMEMORY_BARRIER();

            uxReturn = uxQueueSpacesAvailable( xQueue );
            portMEMORY_BARRIER();

            portRESET_PRIVILEGE();
            portMEMORY_BARRIER();
        }
        else
        {
            uxReturn = uxQueueSpacesAvailable( xQueue );
        }

        return uxReturn;
    }
```

**解说：** 这一段实现函数 `MPU_uxQueueSpacesAvailable`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 84: 函数 MPU_xQueueReceive

```c
/*-----------------------------------------------------------*/
    BaseType_t MPU_xQueueReceive( QueueHandle_t pxQueue,
                                  void * const pvBuffer,
                                  TickType_t xTicksToWait ) /* FREERTOS_SYSTEM_CALL */
    {
        BaseType_t xReturn;

        if( portIS_PRIVILEGED() == pdFALSE )
        {
            portRAISE_PRIVILEGE();
            portMEMORY_BARRIER();

            xReturn = xQueueReceive( pxQueue, pvBuffer, xTicksToWait );
            portMEMORY_BARRIER();

            portRESET_PRIVILEGE();
            portMEMORY_BARRIER();
        }
        else
        {
            xReturn = xQueueReceive( pxQueue, pvBuffer, xTicksToWait );
        }

        return xReturn;
    }
```

**解说：** 这一段实现函数 `MPU_xQueueReceive`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 85: 函数 MPU_xQueuePeek

```c
/*-----------------------------------------------------------*/
    BaseType_t MPU_xQueuePeek( QueueHandle_t xQueue,
                               void * const pvBuffer,
                               TickType_t xTicksToWait ) /* FREERTOS_SYSTEM_CALL */
    {
        BaseType_t xReturn;

        if( portIS_PRIVILEGED() == pdFALSE )
        {
            portRAISE_PRIVILEGE();
            portMEMORY_BARRIER();

            xReturn = xQueuePeek( xQueue, pvBuffer, xTicksToWait );
            portMEMORY_BARRIER();

            portRESET_PRIVILEGE();
            portMEMORY_BARRIER();
        }
        else
        {
            xReturn = xQueuePeek( xQueue, pvBuffer, xTicksToWait );
        }

        return xReturn;
    }
```

**解说：** 这一段实现函数 `MPU_xQueuePeek`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 86: 函数 MPU_xQueueSemaphoreTake

```c
/*-----------------------------------------------------------*/
    BaseType_t MPU_xQueueSemaphoreTake( QueueHandle_t xQueue,
                                        TickType_t xTicksToWait ) /* FREERTOS_SYSTEM_CALL */
    {
        BaseType_t xReturn;

        if( portIS_PRIVILEGED() == pdFALSE )
        {
            portRAISE_PRIVILEGE();
            portMEMORY_BARRIER();

            xReturn = xQueueSemaphoreTake( xQueue, xTicksToWait );
            portMEMORY_BARRIER();

            portRESET_PRIVILEGE();
            portMEMORY_BARRIER();
        }
        else
        {
            xReturn = xQueueSemaphoreTake( xQueue, xTicksToWait );
        }

        return xReturn;
    }
```

**解说：** 这一段实现函数 `MPU_xQueueSemaphoreTake`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 87: 预处理配置 MPU_xQueueGetMutexHolder

```c
/*-----------------------------------------------------------*/
    #if ( ( configUSE_MUTEXES == 1 ) && ( INCLUDE_xSemaphoreGetMutexHolder == 1 ) )
        TaskHandle_t MPU_xQueueGetMutexHolder( QueueHandle_t xSemaphore ) /* FREERTOS_SYSTEM_CALL */
        {
            void * xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xQueueGetMutexHolder( xSemaphore );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xQueueGetMutexHolder( xSemaphore );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 88: 预处理配置

```c
    #endif /* if ( ( configUSE_MUTEXES == 1 ) && ( INCLUDE_xSemaphoreGetMutexHolder == 1 ) ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 89: 预处理配置 MPU_xQueueCreateMutex

```c
/*-----------------------------------------------------------*/
    #if ( ( configUSE_MUTEXES == 1 ) && ( configSUPPORT_DYNAMIC_ALLOCATION == 1 ) )
        QueueHandle_t MPU_xQueueCreateMutex( const uint8_t ucQueueType ) /* FREERTOS_SYSTEM_CALL */
        {
            QueueHandle_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xQueueCreateMutex( ucQueueType );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xQueueCreateMutex( ucQueueType );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 90: 预处理配置

```c
    #endif /* if ( ( configUSE_MUTEXES == 1 ) && ( configSUPPORT_DYNAMIC_ALLOCATION == 1 ) ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 91: 预处理配置 MPU_xQueueCreateMutexStatic

```c
/*-----------------------------------------------------------*/
    #if ( ( configUSE_MUTEXES == 1 ) && ( configSUPPORT_STATIC_ALLOCATION == 1 ) )
        QueueHandle_t MPU_xQueueCreateMutexStatic( const uint8_t ucQueueType,
                                                   StaticQueue_t * pxStaticQueue ) /* FREERTOS_SYSTEM_CALL */
        {
            QueueHandle_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xQueueCreateMutexStatic( ucQueueType, pxStaticQueue );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xQueueCreateMutexStatic( ucQueueType, pxStaticQueue );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 92: 预处理配置

```c
    #endif /* if ( ( configUSE_MUTEXES == 1 ) && ( configSUPPORT_STATIC_ALLOCATION == 1 ) ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 93: 预处理配置 MPU_xQueueCreateCountingSemaphore

```c
/*-----------------------------------------------------------*/
    #if ( ( configUSE_COUNTING_SEMAPHORES == 1 ) && ( configSUPPORT_DYNAMIC_ALLOCATION == 1 ) )
        QueueHandle_t MPU_xQueueCreateCountingSemaphore( UBaseType_t uxCountValue,
                                                         UBaseType_t uxInitialCount ) /* FREERTOS_SYSTEM_CALL */
        {
            QueueHandle_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xQueueCreateCountingSemaphore( uxCountValue, uxInitialCount );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xQueueCreateCountingSemaphore( uxCountValue, uxInitialCount );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 94: 预处理配置

```c
    #endif /* if ( ( configUSE_COUNTING_SEMAPHORES == 1 ) && ( configSUPPORT_DYNAMIC_ALLOCATION == 1 ) ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 95: 预处理配置 MPU_xQueueCreateCountingSemaphoreStatic

```c
/*-----------------------------------------------------------*/
    #if ( ( configUSE_COUNTING_SEMAPHORES == 1 ) && ( configSUPPORT_STATIC_ALLOCATION == 1 ) )

        QueueHandle_t MPU_xQueueCreateCountingSemaphoreStatic( const UBaseType_t uxMaxCount,
                                                               const UBaseType_t uxInitialCount,
                                                               StaticQueue_t * pxStaticQueue ) /* FREERTOS_SYSTEM_CALL */
        {
            QueueHandle_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xQueueCreateCountingSemaphoreStatic( uxMaxCount, uxInitialCount, pxStaticQueue );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xQueueCreateCountingSemaphoreStatic( uxMaxCount, uxInitialCount, pxStaticQueue );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 96: 预处理配置

```c
    #endif /* if ( ( configUSE_COUNTING_SEMAPHORES == 1 ) && ( configSUPPORT_STATIC_ALLOCATION == 1 ) ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 97: 预处理配置 MPU_xQueueTakeMutexRecursive

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_RECURSIVE_MUTEXES == 1 )
        BaseType_t MPU_xQueueTakeMutexRecursive( QueueHandle_t xMutex,
                                                 TickType_t xBlockTime ) /* FREERTOS_SYSTEM_CALL */
        {
            BaseType_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xQueueTakeMutexRecursive( xMutex, xBlockTime );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xQueueTakeMutexRecursive( xMutex, xBlockTime );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 98: 预处理配置

```c
    #endif /* if ( configUSE_RECURSIVE_MUTEXES == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 99: 预处理配置 MPU_xQueueGiveMutexRecursive

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_RECURSIVE_MUTEXES == 1 )
        BaseType_t MPU_xQueueGiveMutexRecursive( QueueHandle_t xMutex ) /* FREERTOS_SYSTEM_CALL */
        {
            BaseType_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xQueueGiveMutexRecursive( xMutex );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xQueueGiveMutexRecursive( xMutex );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 100: 预处理配置

```c
    #endif /* if ( configUSE_RECURSIVE_MUTEXES == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 101: 预处理配置

```c
/*-----------------------------------------------------------*/
    #if ( ( configUSE_QUEUE_SETS == 1 ) && ( configSUPPORT_DYNAMIC_ALLOCATION == 1 ) )
        QueueSetHandle_t MPU_xQueueCreateSet( UBaseType_t uxEventQueueLength ) /* FREERTOS_SYSTEM_CALL */
        {
            QueueSetHandle_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xQueueCreateSet( uxEventQueueLength );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xQueueCreateSet( uxEventQueueLength );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 102: 预处理配置

```c
    #endif /* if ( ( configUSE_QUEUE_SETS == 1 ) && ( configSUPPORT_DYNAMIC_ALLOCATION == 1 ) ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 103: 预处理配置

```c
/*-----------------------------------------------------------*/
    #if ( ( configUSE_QUEUE_SETS == 1 ) && ( configSUPPORT_STATIC_ALLOCATION == 1 ) )
        QueueSetHandle_t MPU_xQueueCreateSetStatic( const UBaseType_t uxEventQueueLength,
                                                    uint8_t * pucQueueStorage,
                                                    StaticQueue_t * pxStaticQueue ) /* FREERTOS_SYSTEM_CALL */
        {
            QueueSetHandle_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xQueueCreateSetStatic( uxEventQueueLength, pucQueueStorage, pxStaticQueue );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xQueueCreateSetStatic( uxEventQueueLength, pucQueueStorage, pxStaticQueue );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 104: 预处理配置

```c
    #endif /* if ( ( configUSE_QUEUE_SETS == 1 ) && ( configSUPPORT_STATIC_ALLOCATION == 1 ) ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 105: 预处理配置

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_QUEUE_SETS == 1 )
        QueueSetMemberHandle_t MPU_xQueueSelectFromSet( QueueSetHandle_t xQueueSet,
                                                        TickType_t xBlockTimeTicks ) /* FREERTOS_SYSTEM_CALL */
        {
            QueueSetMemberHandle_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xQueueSelectFromSet( xQueueSet, xBlockTimeTicks );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xQueueSelectFromSet( xQueueSet, xBlockTimeTicks );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 106: 预处理配置

```c
    #endif /* if ( configUSE_QUEUE_SETS == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 107: 预处理配置 MPU_xQueueAddToSet

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_QUEUE_SETS == 1 )
        BaseType_t MPU_xQueueAddToSet( QueueSetMemberHandle_t xQueueOrSemaphore,
                                       QueueSetHandle_t xQueueSet ) /* FREERTOS_SYSTEM_CALL */
        {
            BaseType_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xQueueAddToSet( xQueueOrSemaphore, xQueueSet );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xQueueAddToSet( xQueueOrSemaphore, xQueueSet );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 108: 预处理配置

```c
    #endif /* if ( configUSE_QUEUE_SETS == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 109: 预处理配置 MPU_xQueueRemoveFromSet

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_QUEUE_SETS == 1 )
        BaseType_t MPU_xQueueRemoveFromSet( QueueSetMemberHandle_t xQueueOrSemaphore,
                                            QueueSetHandle_t xQueueSet ) /* FREERTOS_SYSTEM_CALL */
        {
            BaseType_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xQueueRemoveFromSet( xQueueOrSemaphore, xQueueSet );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xQueueRemoveFromSet( xQueueOrSemaphore, xQueueSet );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 110: 预处理配置

```c
    #endif /* if ( configUSE_QUEUE_SETS == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 111: 预处理配置 MPU_vQueueAddToRegistry

```c
/*-----------------------------------------------------------*/
    #if configQUEUE_REGISTRY_SIZE > 0
        void MPU_vQueueAddToRegistry( QueueHandle_t xQueue,
                                      const char * pcName ) /* FREERTOS_SYSTEM_CALL */
        {
            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                vQueueAddToRegistry( xQueue, pcName );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                vQueueAddToRegistry( xQueue, pcName );
            }
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 112: 预处理配置

```c
    #endif /* if configQUEUE_REGISTRY_SIZE > 0 */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 113: 预处理配置 MPU_vQueueUnregisterQueue

```c
/*-----------------------------------------------------------*/
    #if configQUEUE_REGISTRY_SIZE > 0
        void MPU_vQueueUnregisterQueue( QueueHandle_t xQueue ) /* FREERTOS_SYSTEM_CALL */
        {
            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                vQueueUnregisterQueue( xQueue );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                vQueueUnregisterQueue( xQueue );
            }
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 114: 预处理配置

```c
    #endif /* if configQUEUE_REGISTRY_SIZE > 0 */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 115: 预处理配置 MPU_pcQueueGetName

```c
/*-----------------------------------------------------------*/
    #if configQUEUE_REGISTRY_SIZE > 0
        const char * MPU_pcQueueGetName( QueueHandle_t xQueue ) /* FREERTOS_SYSTEM_CALL */
        {
            const char * pcReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                pcReturn = pcQueueGetName( xQueue );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                pcReturn = pcQueueGetName( xQueue );
            }

            return pcReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 116: 预处理配置

```c
    #endif /* if configQUEUE_REGISTRY_SIZE > 0 */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 117: 函数 MPU_vQueueDelete

```c
/*-----------------------------------------------------------*/
    void MPU_vQueueDelete( QueueHandle_t xQueue ) /* FREERTOS_SYSTEM_CALL */
    {
        if( portIS_PRIVILEGED() == pdFALSE )
        {
            portRAISE_PRIVILEGE();
            portMEMORY_BARRIER();

            vQueueDelete( xQueue );
            portMEMORY_BARRIER();

            portRESET_PRIVILEGE();
            portMEMORY_BARRIER();
        }
        else
        {
            vQueueDelete( xQueue );
        }
    }
```

**解说：** 这一段实现函数 `MPU_vQueueDelete`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 118: 预处理配置 MPU_pvTimerGetTimerID

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_TIMERS == 1 )
        void * MPU_pvTimerGetTimerID( const TimerHandle_t xTimer ) /* FREERTOS_SYSTEM_CALL */
        {
            void * pvReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                pvReturn = pvTimerGetTimerID( xTimer );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                pvReturn = pvTimerGetTimerID( xTimer );
            }

            return pvReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 119: 预处理配置

```c
    #endif /* if ( configUSE_TIMERS == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 120: 预处理配置 MPU_vTimerSetTimerID

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_TIMERS == 1 )
        void MPU_vTimerSetTimerID( TimerHandle_t xTimer,
                                   void * pvNewID ) /* FREERTOS_SYSTEM_CALL */
        {
            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                vTimerSetTimerID( xTimer, pvNewID );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                vTimerSetTimerID( xTimer, pvNewID );
            }
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 121: 预处理配置

```c
    #endif /* if ( configUSE_TIMERS == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 122: 预处理配置 MPU_xTimerIsTimerActive

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_TIMERS == 1 )
        BaseType_t MPU_xTimerIsTimerActive( TimerHandle_t xTimer ) /* FREERTOS_SYSTEM_CALL */
        {
            BaseType_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xTimerIsTimerActive( xTimer );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xTimerIsTimerActive( xTimer );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 123: 预处理配置

```c
    #endif /* if ( configUSE_TIMERS == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 124: 预处理配置 MPU_xTimerGetTimerDaemonTaskHandle

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_TIMERS == 1 )
        TaskHandle_t MPU_xTimerGetTimerDaemonTaskHandle( void ) /* FREERTOS_SYSTEM_CALL */
        {
            TaskHandle_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xTimerGetTimerDaemonTaskHandle();
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xTimerGetTimerDaemonTaskHandle();
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 125: 预处理配置

```c
    #endif /* if ( configUSE_TIMERS == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 126: 预处理配置 MPU_vTimerSetReloadMode

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_TIMERS == 1 )
        void MPU_vTimerSetReloadMode( TimerHandle_t xTimer,
                                      const BaseType_t xAutoReload ) /* FREERTOS_SYSTEM_CALL */
        {
            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                vTimerSetReloadMode( xTimer, xAutoReload );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                vTimerSetReloadMode( xTimer, xAutoReload );
            }
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 127: 预处理配置

```c
    #endif /* if ( configUSE_TIMERS == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 128: 预处理配置 MPU_uxTimerGetReloadMode

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_TIMERS == 1 )
        UBaseType_t MPU_uxTimerGetReloadMode( TimerHandle_t xTimer )
        {
            UBaseType_t uxReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                uxReturn = uxTimerGetReloadMode( xTimer );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                uxReturn = uxTimerGetReloadMode( xTimer );
            }

            return uxReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 129: 预处理配置

```c
    #endif /* if ( configUSE_TIMERS == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 130: 预处理配置 MPU_pcTimerGetName

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_TIMERS == 1 )
        const char * MPU_pcTimerGetName( TimerHandle_t xTimer ) /* FREERTOS_SYSTEM_CALL */
        {
            const char * pcReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                pcReturn = pcTimerGetName( xTimer );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                pcReturn = pcTimerGetName( xTimer );
            }

            return pcReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 131: 预处理配置

```c
    #endif /* if ( configUSE_TIMERS == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 132: 预处理配置 MPU_xTimerGetPeriod

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_TIMERS == 1 )
        TickType_t MPU_xTimerGetPeriod( TimerHandle_t xTimer ) /* FREERTOS_SYSTEM_CALL */
        {
            TickType_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xTimerGetPeriod( xTimer );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xTimerGetPeriod( xTimer );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 133: 预处理配置

```c
    #endif /* if ( configUSE_TIMERS == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 134: 预处理配置 MPU_xTimerGetExpiryTime

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_TIMERS == 1 )
        TickType_t MPU_xTimerGetExpiryTime( TimerHandle_t xTimer ) /* FREERTOS_SYSTEM_CALL */
        {
            TickType_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xTimerGetExpiryTime( xTimer );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xTimerGetExpiryTime( xTimer );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 135: 预处理配置

```c
    #endif /* if ( configUSE_TIMERS == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 136: 预处理配置 MPU_xTimerGenericCommandFromTask

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_TIMERS == 1 )
        BaseType_t MPU_xTimerGenericCommandFromTask( TimerHandle_t xTimer,
                                                     const BaseType_t xCommandID,
                                                     const TickType_t xOptionalValue,
                                                     BaseType_t * const pxHigherPriorityTaskWoken,
                                                     const TickType_t xTicksToWait ) /* FREERTOS_SYSTEM_CALL */
        {
            BaseType_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xTimerGenericCommandFromTask( xTimer, xCommandID, xOptionalValue, pxHigherPriorityTaskWoken, xTicksToWait );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xTimerGenericCommandFromTask( xTimer, xCommandID, xOptionalValue, pxHigherPriorityTaskWoken, xTicksToWait );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 137: 预处理配置

```c
    #endif /* if ( configUSE_TIMERS == 1 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 138: 预处理配置

```c
/*-----------------------------------------------------------*/
    #if ( ( configSUPPORT_DYNAMIC_ALLOCATION == 1 ) && ( configUSE_EVENT_GROUPS == 1 ) )
        EventGroupHandle_t MPU_xEventGroupCreate( void ) /* FREERTOS_SYSTEM_CALL */
        {
            EventGroupHandle_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xEventGroupCreate();
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xEventGroupCreate();
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 139: 预处理配置

```c
    #endif /* #if ( ( configSUPPORT_DYNAMIC_ALLOCATION == 1 ) && ( configUSE_EVENT_GROUPS == 1 ) ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 140: 预处理配置

```c
/*-----------------------------------------------------------*/
    #if ( ( configSUPPORT_STATIC_ALLOCATION == 1 ) && ( configUSE_EVENT_GROUPS == 1 ) )
        EventGroupHandle_t MPU_xEventGroupCreateStatic( StaticEventGroup_t * pxEventGroupBuffer ) /* FREERTOS_SYSTEM_CALL */
        {
            EventGroupHandle_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xEventGroupCreateStatic( pxEventGroupBuffer );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xEventGroupCreateStatic( pxEventGroupBuffer );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 141: 预处理配置

```c
    #endif /* #if ( ( configSUPPORT_STATIC_ALLOCATION == 1 ) && ( configUSE_EVENT_GROUPS == 1 ) ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 142: 预处理配置

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_EVENT_GROUPS == 1 )
        EventBits_t MPU_xEventGroupWaitBits( EventGroupHandle_t xEventGroup,
                                             const EventBits_t uxBitsToWaitFor,
                                             const BaseType_t xClearOnExit,
                                             const BaseType_t xWaitForAllBits,
                                             TickType_t xTicksToWait ) /* FREERTOS_SYSTEM_CALL */
        {
            EventBits_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xEventGroupWaitBits( xEventGroup, uxBitsToWaitFor, xClearOnExit, xWaitForAllBits, xTicksToWait );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xEventGroupWaitBits( xEventGroup, uxBitsToWaitFor, xClearOnExit, xWaitForAllBits, xTicksToWait );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 143: 预处理配置

```c
    #endif /* #if ( configUSE_EVENT_GROUPS == 1 ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 144: 预处理配置

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_EVENT_GROUPS == 1 )
        EventBits_t MPU_xEventGroupClearBits( EventGroupHandle_t xEventGroup,
                                              const EventBits_t uxBitsToClear ) /* FREERTOS_SYSTEM_CALL */
        {
            EventBits_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xEventGroupClearBits( xEventGroup, uxBitsToClear );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xEventGroupClearBits( xEventGroup, uxBitsToClear );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 145: 预处理配置

```c
    #endif /* #if ( configUSE_EVENT_GROUPS == 1 ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 146: 预处理配置

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_EVENT_GROUPS == 1 )
        EventBits_t MPU_xEventGroupSetBits( EventGroupHandle_t xEventGroup,
                                            const EventBits_t uxBitsToSet ) /* FREERTOS_SYSTEM_CALL */
        {
            EventBits_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xEventGroupSetBits( xEventGroup, uxBitsToSet );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xEventGroupSetBits( xEventGroup, uxBitsToSet );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 147: 预处理配置

```c
    #endif /* #if ( configUSE_EVENT_GROUPS == 1 ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 148: 预处理配置

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_EVENT_GROUPS == 1 )
        EventBits_t MPU_xEventGroupSync( EventGroupHandle_t xEventGroup,
                                         const EventBits_t uxBitsToSet,
                                         const EventBits_t uxBitsToWaitFor,
                                         TickType_t xTicksToWait ) /* FREERTOS_SYSTEM_CALL */
        {
            EventBits_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xEventGroupSync( xEventGroup, uxBitsToSet, uxBitsToWaitFor, xTicksToWait );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xEventGroupSync( xEventGroup, uxBitsToSet, uxBitsToWaitFor, xTicksToWait );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 149: 预处理配置

```c
    #endif /* #if ( configUSE_EVENT_GROUPS == 1 ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 150: 预处理配置 MPU_vEventGroupDelete

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_EVENT_GROUPS == 1 )
        void MPU_vEventGroupDelete( EventGroupHandle_t xEventGroup ) /* FREERTOS_SYSTEM_CALL */
        {
            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                vEventGroupDelete( xEventGroup );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                vEventGroupDelete( xEventGroup );
            }
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 151: 预处理配置

```c
    #endif /* #if ( configUSE_EVENT_GROUPS == 1 ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 152: 预处理配置 MPU_xStreamBufferSend

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_STREAM_BUFFERS == 1 )
        size_t MPU_xStreamBufferSend( StreamBufferHandle_t xStreamBuffer,
                                      const void * pvTxData,
                                      size_t xDataLengthBytes,
                                      TickType_t xTicksToWait ) /* FREERTOS_SYSTEM_CALL */
        {
            size_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xStreamBufferSend( xStreamBuffer, pvTxData, xDataLengthBytes, xTicksToWait );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xStreamBufferSend( xStreamBuffer, pvTxData, xDataLengthBytes, xTicksToWait );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 153: 预处理配置

```c
    #endif /* #if ( configUSE_STREAM_BUFFERS == 1 ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 154: 预处理配置 MPU_xStreamBufferNextMessageLengthBytes

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_STREAM_BUFFERS == 1 )
        size_t MPU_xStreamBufferNextMessageLengthBytes( StreamBufferHandle_t xStreamBuffer ) /* FREERTOS_SYSTEM_CALL */
        {
            size_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xStreamBufferNextMessageLengthBytes( xStreamBuffer );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xStreamBufferNextMessageLengthBytes( xStreamBuffer );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 155: 预处理配置

```c
    #endif /* #if ( configUSE_STREAM_BUFFERS == 1 ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 156: 预处理配置 MPU_xStreamBufferReceive

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_STREAM_BUFFERS == 1 )
        size_t MPU_xStreamBufferReceive( StreamBufferHandle_t xStreamBuffer,
                                         void * pvRxData,
                                         size_t xBufferLengthBytes,
                                         TickType_t xTicksToWait ) /* FREERTOS_SYSTEM_CALL */
        {
            size_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xStreamBufferReceive( xStreamBuffer, pvRxData, xBufferLengthBytes, xTicksToWait );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xStreamBufferReceive( xStreamBuffer, pvRxData, xBufferLengthBytes, xTicksToWait );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 157: 预处理配置

```c
    #endif /* #if ( configUSE_STREAM_BUFFERS == 1 ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 158: 预处理配置 MPU_vStreamBufferDelete

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_STREAM_BUFFERS == 1 )
        void MPU_vStreamBufferDelete( StreamBufferHandle_t xStreamBuffer ) /* FREERTOS_SYSTEM_CALL */
        {
            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                vStreamBufferDelete( xStreamBuffer );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                vStreamBufferDelete( xStreamBuffer );
            }
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 159: 预处理配置

```c
    #endif /* #if ( configUSE_STREAM_BUFFERS == 1 ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 160: 预处理配置 MPU_xStreamBufferIsFull

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_STREAM_BUFFERS == 1 )
        BaseType_t MPU_xStreamBufferIsFull( StreamBufferHandle_t xStreamBuffer ) /* FREERTOS_SYSTEM_CALL */
        {
            BaseType_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xStreamBufferIsFull( xStreamBuffer );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xStreamBufferIsFull( xStreamBuffer );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 161: 预处理配置

```c
    #endif /* #if ( configUSE_STREAM_BUFFERS == 1 ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 162: 预处理配置 MPU_xStreamBufferIsEmpty

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_STREAM_BUFFERS == 1 )
        BaseType_t MPU_xStreamBufferIsEmpty( StreamBufferHandle_t xStreamBuffer ) /* FREERTOS_SYSTEM_CALL */
        {
            BaseType_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xStreamBufferIsEmpty( xStreamBuffer );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xStreamBufferIsEmpty( xStreamBuffer );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 163: 预处理配置

```c
    #endif /* #if ( configUSE_STREAM_BUFFERS == 1 ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 164: 预处理配置 MPU_xStreamBufferReset

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_STREAM_BUFFERS == 1 )
        BaseType_t MPU_xStreamBufferReset( StreamBufferHandle_t xStreamBuffer ) /* FREERTOS_SYSTEM_CALL */
        {
            BaseType_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xStreamBufferReset( xStreamBuffer );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xStreamBufferReset( xStreamBuffer );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 165: 预处理配置

```c
    #endif /* #if ( configUSE_STREAM_BUFFERS == 1 ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 166: 预处理配置 MPU_xStreamBufferSpacesAvailable

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_STREAM_BUFFERS == 1 )
        size_t MPU_xStreamBufferSpacesAvailable( StreamBufferHandle_t xStreamBuffer ) /* FREERTOS_SYSTEM_CALL */
        {
            size_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();
                xReturn = xStreamBufferSpacesAvailable( xStreamBuffer );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xStreamBufferSpacesAvailable( xStreamBuffer );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 167: 预处理配置

```c
    #endif /* #if ( configUSE_STREAM_BUFFERS == 1 ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 168: 预处理配置 MPU_xStreamBufferBytesAvailable

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_STREAM_BUFFERS == 1 )
        size_t MPU_xStreamBufferBytesAvailable( StreamBufferHandle_t xStreamBuffer ) /* FREERTOS_SYSTEM_CALL */
        {
            size_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xStreamBufferBytesAvailable( xStreamBuffer );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xStreamBufferBytesAvailable( xStreamBuffer );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 169: 预处理配置

```c
    #endif /* #if ( configUSE_STREAM_BUFFERS == 1 ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 170: 预处理配置 MPU_xStreamBufferSetTriggerLevel

```c
/*-----------------------------------------------------------*/
    #if ( configUSE_STREAM_BUFFERS == 1 )
        BaseType_t MPU_xStreamBufferSetTriggerLevel( StreamBufferHandle_t xStreamBuffer,
                                                     size_t xTriggerLevel ) /* FREERTOS_SYSTEM_CALL */
        {
            BaseType_t xReturn;

            if( portIS_PRIVILEGED() == pdFALSE )
            {
                portRAISE_PRIVILEGE();
                portMEMORY_BARRIER();

                xReturn = xStreamBufferSetTriggerLevel( xStreamBuffer, xTriggerLevel );
                portMEMORY_BARRIER();

                portRESET_PRIVILEGE();
                portMEMORY_BARRIER();
            }
            else
            {
                xReturn = xStreamBufferSetTriggerLevel( xStreamBuffer, xTriggerLevel );
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 171: 预处理配置

```c
    #endif /* #if ( configUSE_STREAM_BUFFERS == 1 ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 172: 预处理配置

```c
/*-----------------------------------------------------------*/
    #if ( ( configSUPPORT_DYNAMIC_ALLOCATION == 1 ) && ( configUSE_STREAM_BUFFERS == 1 ) )
        StreamBufferHandle_t MPU_xStreamBufferGenericCreate( size_t xBufferSizeBytes,
                                                             size_t xTriggerLevelBytes,
                                                             BaseType_t xStreamBufferType,
                                                             StreamBufferCallbackFunction_t pxSendCompletedCallback,
                                                             StreamBufferCallbackFunction_t pxReceiveCompletedCallback ) /* FREERTOS_SYSTEM_CALL */
        {
            StreamBufferHandle_t xReturn;

            /**
             * Stream buffer application level callback functionality is disabled for MPU
             * enabled ports.
             */
            configASSERT( ( pxSendCompletedCallback == NULL ) &&
                          ( pxReceiveCompletedCallback == NULL ) );

            if( ( pxSendCompletedCallback == NULL ) &&
                ( pxReceiveCompletedCallback == NULL ) )
            {
                if( portIS_PRIVILEGED() == pdFALSE )
                {
                    portRAISE_PRIVILEGE();
                    portMEMORY_BARRIER();

                    xReturn = xStreamBufferGenericCreate( xBufferSizeBytes,
                                                          xTriggerLevelBytes,
                                                          xStreamBufferType,
                                                          NULL,
                                                          NULL );
                    portMEMORY_BARRIER();

                    portRESET_PRIVILEGE();
                    portMEMORY_BARRIER();
                }
                else
                {
                    xReturn = xStreamBufferGenericCreate( xBufferSizeBytes,
                                                          xTriggerLevelBytes,
                                                          xStreamBufferType,
                                                          NULL,
                                                          NULL );
                }
            }
            else
            {
                traceSTREAM_BUFFER_CREATE_FAILED( xStreamBufferType );
                xReturn = NULL;
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 173: 预处理配置

```c
    #endif /* #if ( ( configSUPPORT_DYNAMIC_ALLOCATION == 1 ) && ( configUSE_STREAM_BUFFERS == 1 ) ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 174: 预处理配置

```c
/*-----------------------------------------------------------*/
    #if ( ( configSUPPORT_STATIC_ALLOCATION == 1 ) && ( configUSE_STREAM_BUFFERS == 1 ) )
        StreamBufferHandle_t MPU_xStreamBufferGenericCreateStatic( size_t xBufferSizeBytes,
                                                                   size_t xTriggerLevelBytes,
                                                                   BaseType_t xStreamBufferType,
                                                                   uint8_t * const pucStreamBufferStorageArea,
                                                                   StaticStreamBuffer_t * const pxStaticStreamBuffer,
                                                                   StreamBufferCallbackFunction_t pxSendCompletedCallback,
                                                                   StreamBufferCallbackFunction_t pxReceiveCompletedCallback ) /* FREERTOS_SYSTEM_CALL */
        {
            StreamBufferHandle_t xReturn;

            /**
             * Stream buffer application level callback functionality is disabled for MPU
             * enabled ports.
             */
            configASSERT( ( pxSendCompletedCallback == NULL ) &&
                          ( pxReceiveCompletedCallback == NULL ) );

            if( ( pxSendCompletedCallback == NULL ) &&
                ( pxReceiveCompletedCallback == NULL ) )
            {
                if( portIS_PRIVILEGED() == pdFALSE )
                {
                    portRAISE_PRIVILEGE();
                    portMEMORY_BARRIER();

                    xReturn = xStreamBufferGenericCreateStatic( xBufferSizeBytes,
                                                                xTriggerLevelBytes,
                                                                xStreamBufferType,
                                                                pucStreamBufferStorageArea,
                                                                pxStaticStreamBuffer,
                                                                NULL,
                                                                NULL );
                    portMEMORY_BARRIER();

                    portRESET_PRIVILEGE();
                    portMEMORY_BARRIER();
                }
                else
                {
                    xReturn = xStreamBufferGenericCreateStatic( xBufferSizeBytes,
                                                                xTriggerLevelBytes,
                                                                xStreamBufferType,
                                                                pucStreamBufferStorageArea,
                                                                pxStaticStreamBuffer,
                                                                NULL,
                                                                NULL );
                }
            }
            else
            {
                traceSTREAM_BUFFER_CREATE_STATIC_FAILED( xReturn, xStreamBufferType );
                xReturn = NULL;
            }

            return xReturn;
        }
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 175: 预处理配置

```c
    #endif /* #if ( ( configSUPPORT_STATIC_ALLOCATION == 1 ) && ( configUSE_STREAM_BUFFERS == 1 ) ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 176: 预处理配置 MPU_FunctionName

```c
/*-----------------------------------------------------------*/
/* Functions that the application writer wants to execute in privileged mode
 * can be defined in application_defined_privileged_functions.h.  The functions
 * must take the same format as those above whereby the privilege state on exit
 * equals the privilege state on entry.  For example:
 *
 * void MPU_FunctionName( [parameters ] ) FREERTOS_SYSTEM_CALL;
 * void MPU_FunctionName( [parameters ] )
 * {
 *      if( portIS_PRIVILEGED() == pdFALSE )
 *      {
 *          portRAISE_PRIVILEGE();
 *          portMEMORY_BARRIER();
 *
 *          FunctionName( [parameters ] );
 *          portMEMORY_BARRIER();
 *
 *          portRESET_PRIVILEGE();
 *          portMEMORY_BARRIER();
 *      }
 *      else
 *      {
 *          FunctionName( [parameters ] );
 *      }
 * }
 */
    #if configINCLUDE_APPLICATION_DEFINED_PRIVILEGED_FUNCTIONS == 1
        #include "application_defined_privileged_functions.h"
    #endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 177: 预处理配置

```c
/*-----------------------------------------------------------*/
#endif /* #if ( ( portUSING_MPU_WRAPPERS == 1 ) && ( configUSE_MPU_WRAPPERS_V1 == 1 ) ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 178: 说明性注释

```c
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。
