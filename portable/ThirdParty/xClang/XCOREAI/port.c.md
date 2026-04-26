# port.c 代码解说

源文件：`portable/ThirdParty/xClang/XCOREAI/port.c`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 预处理配置

```c
/* Copyright (c) 2019, XMOS Ltd, All rights reserved */
/* Scheduler includes. */
#include "FreeRTOS.h"
#include "task.h"
#include <string.h>
#include <xs1.h>
#include <xcore/hwtimer.h>
#include <xcore/triggerable.h>

static hwtimer_t xKernelTimer;
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 2: 代码片段 2

```c
uint32_t ulPortYieldRequired[ portMAX_CORE_COUNT ] = { pdFALSE };
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 3: 代码片段 3

```c
/* When this port was designed, it was assumed that pxCurrentTCBs would always
   exist and that it would always be an array containing pointers to the current
   TCBs for each core. In v11, this is not the case; if we are only running one
   core, the symbol is pxCurrentTCB instead. Therefore, this port adds a layer
   of indirection - we populate this pointer-to-pointer in the RTOS kernel entry
   function below. This makes this port agnostic to whether it is running on SMP
   or singlecore RTOS. */
void ** xcorePvtTCBContainer;
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 函数 vIntercoreInterruptISR

```c
/*-----------------------------------------------------------*/
void vIntercoreInterruptISR( void )
{
    int xCoreID;

/*	debug_printf( "In KCALL: %u\n", ulData ); */
    xCoreID = rtos_core_id_get();
    ulPortYieldRequired[ xCoreID ] = pdTRUE;
}
```

**解说：** 这一段实现函数 `vIntercoreInterruptISR`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 5: 函数实现

```c
/*-----------------------------------------------------------*/
DEFINE_RTOS_INTERRUPT_CALLBACK( pxKernelTimerISR, pvData )
{
    uint32_t ulLastTrigger;
    uint32_t ulNow;
    int xCoreID;
    UBaseType_t uxSavedInterruptStatus;

    xCoreID = 0;

    configASSERT( xCoreID == rtos_core_id_get() );

    /* Need the next interrupt to be scheduled relative to
     * the current trigger time, rather than the current
     * time. */
    ulLastTrigger = hwtimer_get_trigger_time( xKernelTimer );

    /* Check to see if the ISR is late. If it is, we don't
     * want to schedule the next interrupt to be in the past. */
    ulNow = hwtimer_get_time( xKernelTimer );

    if( ulNow - ulLastTrigger >= configCPU_CLOCK_HZ / configTICK_RATE_HZ )
    {
        ulLastTrigger = ulNow;
    }

    ulLastTrigger += configCPU_CLOCK_HZ / configTICK_RATE_HZ;
    hwtimer_change_trigger_time( xKernelTimer, ulLastTrigger );

    #if configUPDATE_RTOS_TIME_FROM_TICK_ISR == 1
        rtos_time_increment( RTOS_TICK_PERIOD( configTICK_RATE_HZ ) );
    #endif

    uxSavedInterruptStatus = taskENTER_CRITICAL_FROM_ISR();

    if( xTaskIncrementTick() != pdFALSE )
    {
        ulPortYieldRequired[ xCoreID ] = pdTRUE;
    }

    taskEXIT_CRITICAL_FROM_ISR( uxSavedInterruptStatus );
}
```

**解说：** 这一段实现一个函数，把一组相关步骤封装成独立的执行单元。

## 片段 6: 函数 vPortYieldOtherCore

```c
/*-----------------------------------------------------------*/
void vPortYieldOtherCore( int xOtherCoreID )
{
    int xCoreID;

    /*
     * This function must be called from within a critical section.
     */

    xCoreID = rtos_core_id_get();

/*	debug_printf("%d->%d\n", xCoreID, xOtherCoreID); */

/*	debug_printf("Yield core %d from %d\n", xOtherCoreID, xCoreID ); */

    rtos_irq( xOtherCoreID, xCoreID );
}
```

**解说：** 这一段实现函数 `vPortYieldOtherCore`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 7: 函数 prvCoreInit

```c
/*-----------------------------------------------------------*/
static int prvCoreInit( void )
{
    int xCoreID;

    xCoreID = rtos_core_register();
    debug_printf( "Logical Core %d initializing as FreeRTOS Core %d\n", get_logical_core_id(), xCoreID );

    asm volatile (
        "ldap r11, kexcept\n\t"
        "set kep, r11\n\t"
        :
        :
        : "r11"
        );

    rtos_irq_enable( configNUMBER_OF_CORES );

    /*
     * All threads wait here until all have enabled IRQs
     */
    while( rtos_irq_ready() == pdFALSE )
    {
    }

    if( xCoreID == 0 )
    {
        uint32_t ulNow;
        ulNow = hwtimer_get_time( xKernelTimer );
/*		debug_printf( "The time is now (%u)\n", ulNow ); */

        ulNow += configCPU_CLOCK_HZ / configTICK_RATE_HZ;

        triggerable_setup_interrupt_callback( xKernelTimer, NULL, RTOS_INTERRUPT_CALLBACK( pxKernelTimerISR ) );
        hwtimer_set_trigger_time( xKernelTimer, ulNow );
        triggerable_enable_trigger( xKernelTimer );
    }

    return xCoreID;
}
```

**解说：** 这一段实现函数 `prvCoreInit`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 8: 函数 vApplicationCoreInitHook

```c
/*-----------------------------------------------------------*/
DEFINE_RTOS_KERNEL_ENTRY( void, vPortStartSchedulerOnCore, void )
{
    int xCoreID;

    xCoreID = prvCoreInit();

    #if ( configUSE_CORE_INIT_HOOK == 1 )
    {
        extern void vApplicationCoreInitHook( BaseType_t xCoreID );

        vApplicationCoreInitHook( xCoreID );
    }
    #endif

    /* Populate the TCBContainer depending on whether we're singlecore or SMP */
    #if ( configNUMBER_OF_CORES == 1 )
    {
        asm volatile (
            "ldaw %0, dp[pxCurrentTCB]\n\t"
            : "=r"(xcorePvtTCBContainer)
            : /* no inputs */
            : /* no clobbers */
            );
    }
    #else
    {
        asm volatile (
            "ldaw %0, dp[pxCurrentTCBs]\n\t"
            : "=r"(xcorePvtTCBContainer)
            : /* no inputs */
            : /* no clobbers */
            );
    }

    #endif

    debug_printf( "FreeRTOS Core %d initialized\n", xCoreID );

    /*
     * Restore the context of the first thread
     * to run and jump into it.
     */
    asm volatile (
        "mov r6, %0\n\t"                       /* R6 must be the FreeRTOS core ID. In singlecore this is always 0. */
        "ldw r5, dp[xcorePvtTCBContainer]\n\t" /* R5 must be the TCB list which is indexed by R6 */
        "bu _freertos_restore_ctx\n\t"
        :                                /* no outputs */
        : "r" ( xCoreID )
        : "r5", "r6"
        );
}
```

**解说：** 这一段实现函数 `vApplicationCoreInitHook`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 9: 函数 pxPortInitialiseStack

```c
/*-----------------------------------------------------------*/
/*-----------------------------------------------------------*/
/* Public functions required by all ports below:             */
/*-----------------------------------------------------------*/
/*
 * See header file for description.
 */
StackType_t * pxPortInitialiseStack( StackType_t * pxTopOfStack,
                                     TaskFunction_t pxCode,
                                     void * pvParameters )
{
    /*debug_printf( "Top of stack was %p for task %p\n", pxTopOfStack, pxCode ); */

    /*
     * Grow the thread's stack by portTHREAD_CONTEXT_STACK_GROWTH
     * so we can push the context onto it.
     */
    pxTopOfStack -= portTHREAD_CONTEXT_STACK_GROWTH;

    uint32_t dp;
    uint32_t cp;

    /*
     * We need to get the current CP and DP pointers.
     */
    asm volatile (
        "ldaw r11, cp[0]\n\t"      /* get CP into R11 */
        "mov %0, r11\n\t"          /* get R11 (CP) into cp */
        "ldaw r11, dp[0]\n\t"      /* get DP into R11 */
        "mov %1, r11\n\t"          /* get R11 (DP) into dp */
        : "=r" ( cp ), "=r" ( dp ) /* output 0 is cp, output 1 is dp */
        :                          /* there are no inputs */
        : "r11"                    /* R11 gets clobbered */
        );

    /*
     * Push the thread context onto the stack.
     * Saved PC will point to the new thread's
     * entry pointer.
     * Interrupts will default to enabled.
     * KEDI is also set to enable dual issue mode
     * upon kernel entry.
     */
    pxTopOfStack[ 1 ] = ( StackType_t ) pxCode;       /* SP[1]  := SPC */
    pxTopOfStack[ 2 ] = XS1_SR_IEBLE_MASK
                        | XS1_SR_KEDI_MASK;           /* SP[2]  := SSR */
    pxTopOfStack[ 3 ] = 0x00000000;                   /* SP[3]  := SED */
    pxTopOfStack[ 4 ] = 0x00000000;                   /* SP[4]  := ET */
    pxTopOfStack[ 5 ] = dp;                           /* SP[5]  := DP */
    pxTopOfStack[ 6 ] = cp;                           /* SP[6]  := CP */
    pxTopOfStack[ 7 ] = 0x00000000;                   /* SP[7]  := LR */
    pxTopOfStack[ 8 ] = ( StackType_t ) pvParameters; /* SP[8]  := R0 */
    pxTopOfStack[ 9 ] = 0x01010101;                   /* SP[9]  := R1 */
    pxTopOfStack[ 10 ] = 0x02020202;                  /* SP[10] := R2 */
    pxTopOfStack[ 11 ] = 0x03030303;                  /* SP[11] := R3 */
    pxTopOfStack[ 12 ] = 0x04040404;                  /* SP[12] := R4 */
    pxTopOfStack[ 13 ] = 0x05050505;                  /* SP[13] := R5 */
    pxTopOfStack[ 14 ] = 0x06060606;                  /* SP[14] := R6 */
    pxTopOfStack[ 15 ] = 0x07070707;                  /* SP[15] := R7 */
    pxTopOfStack[ 16 ] = 0x08080808;                  /* SP[16] := R8 */
    pxTopOfStack[ 17 ] = 0x09090909;                  /* SP[17] := R9 */
    pxTopOfStack[ 18 ] = 0x10101010;                  /* SP[18] := R10 */
    pxTopOfStack[ 19 ] = 0x11111111;                  /* SP[19] := R11 */
    pxTopOfStack[ 20 ] = 0x00000000;                  /* SP[20] := vH and vSR */
    memset( &pxTopOfStack[ 21 ], 0, 32 );             /* SP[21 - 28] := vR   */
    memset( &pxTopOfStack[ 29 ], 1, 32 );             /* SP[29 - 36] := vD   */
    memset( &pxTopOfStack[ 37 ], 2, 32 );             /* SP[37 - 44] := vC   */

    /*debug_printf( "Top of stack is now %p for task %p\n", pxTopOfStack, pxCode ); */

    /*
     * Returns the new top of the stack
     */
    return pxTopOfStack;
}
```

**解说：** 这一段实现函数 `pxPortInitialiseStack`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 10: 代码片段 10

```c
/*-----------------------------------------------------------*/
void vPortStartSMPScheduler( void );
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 11: 函数 xPortStartScheduler

```c
/*
 * See header file for description.
 */
BaseType_t xPortStartScheduler( void )
{
    if( ( configNUMBER_OF_CORES > portMAX_CORE_COUNT ) || ( configNUMBER_OF_CORES <= 0 ) )
    {
        return pdFAIL;
    }

    rtos_locks_initialize();
    xKernelTimer = hwtimer_alloc();

    vPortStartSMPScheduler();

    return pdPASS;
}
```

**解说：** 这一段实现函数 `xPortStartScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 12: 函数 vPortEndScheduler

```c
/*-----------------------------------------------------------*/
void vPortEndScheduler( void )
{
    /* Do not implement. */
}
```

**解说：** 这一段实现函数 `vPortEndScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 13: 说明性注释

```c
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。
