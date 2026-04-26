# port_common.c 代码解说

源文件：`portable/ThirdParty/GCC/Xtensa_ESP32/port_common.c`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 文件头和许可证

```c
/*
 * SPDX-FileCopyrightText: 2022 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Apache-2.0
 */
```

**解说：** 这一段是文件头，说明项目归属、许可证和免责条款；它告诉使用者这个文件按 MIT 许可证发布。

## 片段 2: 预处理配置

```c
#include <string.h>
#include "FreeRTOS.h"
#include "task.h"
#include "portmacro.h"
#include "esp_system.h"
#include "esp_heap_caps_init.h"
#include "esp_int_wdt.h"
#include "esp_task_wdt.h"
#include "esp_task.h"
#include "esp_private/crosscore_int.h"
#include "esp_private/startup_internal.h" /* Required by g_spiram_ok. [refactor-todo] for g_spiram_ok */
#include "esp_log.h"
#include "soc/soc_memory_types.h"
#include "soc/dport_access.h"
#include "sdkconfig.h"
#include "esp_freertos_hooks.h"

#if CONFIG_IDF_TARGET_ESP32
    #include "esp32/spiram.h"
#elif CONFIG_IDF_TARGET_ESP32S2
    #include "esp32s2/spiram.h"
#elif CONFIG_IDF_TARGET_ESP32S3
    #include "esp32s3/spiram.h"
#elif CONFIG_IDF_TARGET_ESP32C3 || CONFIG_IDF_TARGET_ESP32H2
/* SPIRAM is not supported on ESP32-C3 */
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 预处理配置

```c
#if CONFIG_SPIRAM_MALLOC_RESERVE_INTERNAL
    static const char * TAG = "cpu_start";
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 4: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 5: 代码片段 5

```c
/* Architecture-agnostic parts of the FreeRTOS ESP-IDF port layer can go here.
 *
 * The actual call flow will be to call esp_startup_start_app() in <ARCH>/port.c,
 * which will then call esp_startup_start_app_common()
 */
/* Duplicate of inaccessible xSchedulerRunning; needed at startup to avoid counting nesting */
volatile unsigned port_xSchedulerRunning[ portNUM_PROCESSORS ] = { 0 };
```

**解说：** 这一段是 `port_common.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 6: 预处理配置

```c
/* For now, running FreeRTOS on one core and a bare metal on the other (or other OSes) */
/* is not supported. For now CONFIG_FREERTOS_UNICORE and CONFIG_ESP_SYSTEM_SINGLE_CORE_MODE */
/* should mirror each other's values. */
/* */
/* And since this should be true, we can just check for CONFIG_FREERTOS_UNICORE. */
#if CONFIG_FREERTOS_UNICORE != CONFIG_ESP_SYSTEM_SINGLE_CORE_MODE
    #error "FreeRTOS and system configuration mismatch regarding the use of multiple cores."
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 7: 代码片段 7

```c
static void main_task( void * args );
```

**解说：** 这一段是 `port_common.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 8: 预处理配置 esp_gdbstub_init

```c
#ifdef CONFIG_ESP_SYSTEM_GDBSTUB_RUNTIME
    void esp_gdbstub_init( void );
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 9: 预处理配置

```c
#endif // CONFIG_ESP_SYSTEM_GDBSTUB_RUNTIME
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 10: 代码片段 10

```c
extern void app_main( void );
```

**解说：** 这一段是 `port_common.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 11: 函数 esp_startup_start_app_common

```c
void esp_startup_start_app_common( void )
{
    #if CONFIG_ESP_INT_WDT
        esp_int_wdt_init();
        /*Initialize the interrupt watch dog for CPU0. */
        esp_int_wdt_cpu_init();
    #endif

    esp_crosscore_int_init();

    #ifdef CONFIG_ESP_SYSTEM_GDBSTUB_RUNTIME
        esp_gdbstub_init();
    #endif // CONFIG_ESP_SYSTEM_GDBSTUB_RUNTIME

    portBASE_TYPE res = xTaskCreatePinnedToCore( &main_task, "main",
                                                 ESP_TASK_MAIN_STACK, NULL,
                                                 ESP_TASK_MAIN_PRIO, NULL, ESP_TASK_MAIN_CORE );
    assert( res == pdTRUE );
    ( void ) res;
}
```

**解说：** 这一段实现函数 `esp_startup_start_app_common`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 12: 预处理配置

```c
#if !CONFIG_FREERTOS_UNICORE
    static volatile bool s_other_cpu_startup_done = false;
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 13: 函数实现

```c
    static bool other_cpu_startup_idle_hook_cb( void )
    {
        s_other_cpu_startup_done = true;
        return true;
    }
```

**解说：** 这一段实现一个函数，把一组相关步骤封装成独立的执行单元。

## 片段 14: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 15: 函数 main_task

```c
static void main_task( void * args )
{
    #if !CONFIG_FREERTOS_UNICORE
        /* Wait for FreeRTOS initialization to finish on other core, before replacing its startup stack */
        esp_register_freertos_idle_hook_for_cpu( other_cpu_startup_idle_hook_cb, !xPortGetCoreID() );

        while( !s_other_cpu_startup_done )
        {
        }
        esp_deregister_freertos_idle_hook_for_cpu( other_cpu_startup_idle_hook_cb, !xPortGetCoreID() );
    #endif

    /* [refactor-todo] check if there is a way to move the following block to esp_system startup */
    heap_caps_enable_nonos_stack_heaps();

    /* Now we have startup stack RAM available for heap, enable any DMA pool memory */
    #if CONFIG_SPIRAM_MALLOC_RESERVE_INTERNAL
        if( g_spiram_ok )
        {
            esp_err_t r = esp_spiram_reserve_dma_pool( CONFIG_SPIRAM_MALLOC_RESERVE_INTERNAL );

            if( r != ESP_OK )
            {
                ESP_EARLY_LOGE( TAG, "Could not reserve internal/DMA pool (error 0x%x)", r );
                abort();
            }
        }
    #endif /* if CONFIG_SPIRAM_MALLOC_RESERVE_INTERNAL */

    /*Initialize task wdt if configured to do so */
    #ifdef CONFIG_ESP_TASK_WDT_PANIC
        ESP_ERROR_CHECK( esp_task_wdt_init( CONFIG_ESP_TASK_WDT_TIMEOUT_S, true ) );
    #elif CONFIG_ESP_TASK_WDT
        ESP_ERROR_CHECK( esp_task_wdt_init( CONFIG_ESP_TASK_WDT_TIMEOUT_S, false ) );
    #endif

    /*Add IDLE 0 to task wdt */
    #ifdef CONFIG_ESP_TASK_WDT_CHECK_IDLE_TASK_CPU0
        TaskHandle_t idle_0 = xTaskGetIdleTaskHandleForCPU( 0 );

        if( idle_0 != NULL )
        {
            ESP_ERROR_CHECK( esp_task_wdt_add( idle_0 ) );
        }
    #endif
    /*Add IDLE 1 to task wdt */
    #ifdef CONFIG_ESP_TASK_WDT_CHECK_IDLE_TASK_CPU1
        TaskHandle_t idle_1 = xTaskGetIdleTaskHandleForCPU( 1 );

        if( idle_1 != NULL )
        {
            ESP_ERROR_CHECK( esp_task_wdt_add( idle_1 ) );
        }
    #endif

    app_main();
    vTaskDelete( NULL );
}
```

**解说：** 这一段实现函数 `main_task`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 16: 函数实现

```c
/* -------------------- Heap Related ----------------------- */
bool xPortCheckValidTCBMem( const void * ptr )
{
    return esp_ptr_internal( ptr ) && esp_ptr_byte_accessible( ptr );
}
```

**解说：** 这一段实现一个函数，把一组相关步骤封装成独立的执行单元。

## 片段 17: 函数实现

```c
bool xPortcheckValidStackMem( const void * ptr )
{
    #ifdef CONFIG_SPIRAM_ALLOW_STACK_EXTERNAL_MEMORY
        return esp_ptr_byte_accessible( ptr );
    #else
        return esp_ptr_internal( ptr ) && esp_ptr_byte_accessible( ptr );
    #endif
}
```

**解说：** 这一段实现一个函数，把一组相关步骤封装成独立的执行单元。
