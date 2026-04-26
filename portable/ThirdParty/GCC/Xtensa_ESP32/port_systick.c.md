# port_systick.c 代码解说

源文件：`portable/ThirdParty/GCC/Xtensa_ESP32/port_systick.c`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 文件头和许可证

```c
/*
 * SPDX-FileCopyrightText: 2017-2022 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Apache-2.0
 */
```

**解说：** 这一段是文件头，说明项目归属、许可证和免责条款；它告诉使用者这个文件按 MIT 许可证发布。

## 片段 2: 预处理配置

```c
#include <stdlib.h>
#include <string.h>
#include "soc/cpu.h"
#include "FreeRTOS.h"
#include "task.h"
#include "esp_intr_alloc.h"
#include "esp_err.h"
#include "esp_log.h"
#include "sdkconfig.h"
#ifdef CONFIG_FREERTOS_SYSTICK_USES_SYSTIMER
    #include "soc/periph_defs.h"
    #include "soc/system_reg.h"
    #include "hal/systimer_hal.h"
    #include "hal/systimer_ll.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 预处理配置

```c
#ifdef CONFIG_PM_TRACE
    #include "esp_private/pm_trace.h"
#endif //CONFIG_PM_TRACE
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 4: 代码片段 4

```c
BaseType_t xPortSysTickHandler( void );
```

**解说：** 这一段是 `port_systick.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 5: 预处理配置 _frxt_tick_timer_init

```c
#ifdef CONFIG_FREERTOS_SYSTICK_USES_CCOUNT
    extern void _frxt_tick_timer_init( void );
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 6: 代码片段 6

```c
    extern void _xt_tick_divisor_init( void );
```

**解说：** 这一段是 `port_systick.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 7: 预处理配置 SYSTICK_INTR_ID

```c
    #ifdef CONFIG_FREERTOS_CORETIMER_0
        #define SYSTICK_INTR_ID    ( ETS_INTERNAL_TIMER0_INTR_SOURCE + ETS_INTERNAL_INTR_SOURCE_OFF )
    #endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 8: 预处理配置 SYSTICK_INTR_ID

```c
    #ifdef CONFIG_FREERTOS_CORETIMER_1
        #define SYSTICK_INTR_ID    ( ETS_INTERNAL_TIMER1_INTR_SOURCE + ETS_INTERNAL_INTR_SOURCE_OFF )
    #endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 9: 函数 vPortSetupTimer

```c
/**
 * @brief Initialize CCONT timer to generate the tick interrupt
 *
 */
    void vPortSetupTimer( void )
    {
        /* Init the tick divisor value */
        _xt_tick_divisor_init();

        _frxt_tick_timer_init();
    }
```

**解说：** 这一段实现函数 `vPortSetupTimer`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 10: 预处理配置

```c
#elif CONFIG_FREERTOS_SYSTICK_USES_SYSTIMER

    _Static_assert( SOC_CPU_CORES_NUM <= SOC_SYSTIMER_ALARM_NUM - 1, "the number of cores must match the number of core alarms in SYSTIMER" );
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 11: 代码片段 11

```c
    void SysTickIsrHandler( void * arg );
    static uint32_t s_handled_systicks[ portNUM_PROCESSORS ] = { 0 };
```

**解说：** 这一段是 `port_systick.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 12: 宏 vPortSetupTimer

```c
    #define SYSTICK_INTR_ID    ( ETS_SYSTIMER_TARGET0_EDGE_INTR_SOURCE )

/**
 * @brief Set up the systimer peripheral to generate the tick interrupt
 *
 * Both timer alarms are configured in periodic mode.
 * It is done at the same time so SysTicks for both CPUs occur at the same time or very close.
 * Shifts a time of triggering interrupts for core 0 and core 1.
 */
    void vPortSetupTimer( void )
    {
        unsigned cpuid = xPortGetCoreID();

        #ifdef CONFIG_FREERTOS_CORETIMER_SYSTIMER_LVL3
            const unsigned level = ESP_INTR_FLAG_LEVEL3;
        #else
            const unsigned level = ESP_INTR_FLAG_LEVEL1;
        #endif
        /* Systimer HAL layer object */
        static systimer_hal_context_t systimer_hal;
        /* set system timer interrupt vector */
        ESP_ERROR_CHECK( esp_intr_alloc( ETS_SYSTIMER_TARGET0_EDGE_INTR_SOURCE + cpuid, ESP_INTR_FLAG_IRAM | level, SysTickIsrHandler, &systimer_hal, NULL ) );

        if( cpuid == 0 )
        {
            systimer_hal_init( &systimer_hal );
            systimer_ll_set_counter_value( systimer_hal.dev, SYSTIMER_LL_COUNTER_OS_TICK, 0 );
            systimer_ll_apply_counter_value( systimer_hal.dev, SYSTIMER_LL_COUNTER_OS_TICK );

            for( cpuid = 0; cpuid < SOC_CPU_CORES_NUM; cpuid++ )
            {
                systimer_hal_counter_can_stall_by_cpu( &systimer_hal, SYSTIMER_LL_COUNTER_OS_TICK, cpuid, false );
            }

            for( cpuid = 0; cpuid < portNUM_PROCESSORS; ++cpuid )
            {
                uint32_t alarm_id = SYSTIMER_LL_ALARM_OS_TICK_CORE0 + cpuid;

                /* configure the timer */
                systimer_hal_connect_alarm_counter( &systimer_hal, alarm_id, SYSTIMER_LL_COUNTER_OS_TICK );
                systimer_hal_set_alarm_period( &systimer_hal, alarm_id, 1000000UL / CONFIG_FREERTOS_HZ );
                systimer_hal_select_alarm_mode( &systimer_hal, alarm_id, SYSTIMER_ALARM_MODE_PERIOD );
                systimer_hal_counter_can_stall_by_cpu( &systimer_hal, SYSTIMER_LL_COUNTER_OS_TICK, cpuid, true );

                if( cpuid == 0 )
                {
                    systimer_hal_enable_alarm_int( &systimer_hal, alarm_id );
                    systimer_hal_enable_counter( &systimer_hal, SYSTIMER_LL_COUNTER_OS_TICK );
                    #ifndef CONFIG_FREERTOS_UNICORE
                        /* SysTick of core 0 and core 1 are shifted by half of period */
                        systimer_hal_counter_value_advance( &systimer_hal, SYSTIMER_LL_COUNTER_OS_TICK, 1000000UL / CONFIG_FREERTOS_HZ / 2 );
                    #endif
                }
            }
        }
        else
        {
            uint32_t alarm_id = SYSTIMER_LL_ALARM_OS_TICK_CORE0 + cpuid;
            systimer_hal_enable_alarm_int( &systimer_hal, alarm_id );
        }
    }
```

**解说：** 这一段定义宏 `vPortSetupTimer`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 13: 函数 SysTickIsrHandler

```c
/**
 * @brief Systimer interrupt handler.
 *
 * The Systimer interrupt for SysTick works in periodic mode no need to calc the next alarm.
 * If a timer interrupt is ever serviced more than one tick late, it is necessary to process multiple ticks.
 */
    IRAM_ATTR void SysTickIsrHandler( void * arg )
    {
        uint32_t cpuid = xPortGetCoreID();
        systimer_hal_context_t * systimer_hal = ( systimer_hal_context_t * ) arg;

        #ifdef CONFIG_PM_TRACE
            ESP_PM_TRACE_ENTER( TICK, cpuid );
        #endif

        uint32_t alarm_id = SYSTIMER_LL_ALARM_OS_TICK_CORE0 + cpuid;

        do
        {
            systimer_ll_clear_alarm_int( systimer_hal->dev, alarm_id );

            uint32_t diff = systimer_hal_get_counter_value( systimer_hal, SYSTIMER_LL_COUNTER_OS_TICK ) / systimer_ll_get_alarm_period( systimer_hal->dev, alarm_id ) - s_handled_systicks[ cpuid ];

            if( diff > 0 )
            {
                if( s_handled_systicks[ cpuid ] == 0 )
                {
                    s_handled_systicks[ cpuid ] = diff;
                    diff = 1;
                }
                else
                {
                    s_handled_systicks[ cpuid ] += diff;
                }

                do
                {
                    xPortSysTickHandler();
                } while( --diff );
            }
        } while( systimer_ll_is_alarm_int_fired( systimer_hal->dev, alarm_id ) );

        #ifdef CONFIG_PM_TRACE
            ESP_PM_TRACE_EXIT( TICK, cpuid );
        #endif
    }
```

**解说：** 这一段实现函数 `SysTickIsrHandler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 14: 预处理配置

```c
#endif // CONFIG_FREERTOS_SYSTICK_USES_CCOUNT
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 15: 函数 xPortSysTickHandler

```c
/**
 * @brief Handler of SysTick
 *
 * The function is called from:
 *  - _frxt_timer_int for xtensa with CONFIG_FREERTOS_SYSTICK_USES_CCOUNT
 *  - SysTickIsrHandler for xtensa with CONFIG_FREERTOS_SYSTICK_USES_SYSTIMER
 *  - SysTickIsrHandler for riscv
 */
BaseType_t xPortSysTickHandler( void )
{
    portbenchmarkIntLatency();
    traceISR_ENTER( SYSTICK_INTR_ID );
    BaseType_t ret = xTaskIncrementTick();

    if( ret != pdFALSE )
    {
        traceISR_EXIT_TO_SCHEDULER();
        portYIELD_FROM_ISR();
    }
    else
    {
        traceISR_EXIT();
    }

    return ret;
}
```

**解说：** 这一段实现函数 `xPortSysTickHandler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。
