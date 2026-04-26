# port.c 代码解说

源文件：`portable/GCC/PPC405_Xilinx/port.c`

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

## 片段 2: 预处理配置 portCRITICAL_INTERRUPT_ENABLE

```c
/*-----------------------------------------------------------
* Implementation of functions defined in portable.h for the PPC405 port.
*----------------------------------------------------------*/
/* Scheduler includes. */
#include "FreeRTOS.h"
#include "task.h"

/* Library includes. */
#include "xtime_l.h"
#include "xintc.h"
#include "xintc_i.h"

/*-----------------------------------------------------------*/

/* Definitions to set the initial MSR of each task. */
#define portCRITICAL_INTERRUPT_ENABLE    ( 1UL << 17UL )
#define portEXTERNAL_INTERRUPT_ENABLE    ( 1UL << 15UL )
#define portMACHINE_CHECK_ENABLE         ( 1UL << 12UL )

#if configUSE_FPU == 1
    #define portAPU_PRESENT              ( 1UL << 25UL )
    #define portFCM_FPU_PRESENT          ( 1UL << 13UL )
#else
    #define portAPU_PRESENT              ( 0UL )
    #define portFCM_FPU_PRESENT          ( 0UL )
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 宏 portINITIAL_MSR

```c
#define portINITIAL_MSR                  ( portCRITICAL_INTERRUPT_ENABLE | portEXTERNAL_INTERRUPT_ENABLE | portMACHINE_CHECK_ENABLE | portAPU_PRESENT | portFCM_FPU_PRESENT )


extern const unsigned _SDA_BASE_;
```

**解说：** 这一段定义宏 `portINITIAL_MSR`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 4: 代码片段 4

```c
extern const unsigned _SDA2_BASE_;
/*-----------------------------------------------------------*/
/*
 * Setup the system timer to generate the tick interrupt.
 */
static void prvSetupTimerInterrupt( void );
/*
 * The handler for the tick interrupt - defined in portasm.s.
 */
extern void vPortTickISR( void );
/*
 * The handler for the yield function - defined in portasm.s.
 */
extern void vPortYield( void );
/*
 * Function to start the scheduler running by starting the highest
 * priority task that has thus far been created.
 */
extern void vPortStartFirstTask( void );
/*-----------------------------------------------------------*/
/* Structure used to hold the state of the interrupt controller. */
static XIntc xInterruptController;
```

**解说：** 这一段是 `port.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 5: 函数 pxPortInitialiseStack

```c
/*-----------------------------------------------------------*/
/*
 * Initialise the stack of a task to look exactly as if the task had been
 * interrupted.
 *
 * See the header file portable.h.
 */
StackType_t * pxPortInitialiseStack( StackType_t * pxTopOfStack,
                                     TaskFunction_t pxCode,
                                     void * pvParameters )
{
    /* Place a known value at the bottom of the stack for debugging. */
    *pxTopOfStack = 0xDEADBEEF;
    pxTopOfStack--;

    /* EABI stack frame. */
    pxTopOfStack -= 20; /* Previous backchain and LR, R31 to R4 inclusive. */

    /* Parameters in R13. */
    *pxTopOfStack = ( StackType_t ) &_SDA_BASE_; /* address of the first small data area */
    pxTopOfStack -= 10;

    /* Parameters in R3. */
    *pxTopOfStack = ( StackType_t ) pvParameters;
    pxTopOfStack--;

    /* Parameters in R2. */
    *pxTopOfStack = ( StackType_t ) &_SDA2_BASE_; /* address of the second small data area */
    pxTopOfStack--;

    /* R1 is the stack pointer so is omitted. */

    *pxTopOfStack = 0x10000001UL;                      /* R0. */
    pxTopOfStack--;
    *pxTopOfStack = 0x00000000UL;                      /* USPRG0. */
    pxTopOfStack--;
    *pxTopOfStack = 0x00000000UL;                      /* CR. */
    pxTopOfStack--;
    *pxTopOfStack = 0x00000000UL;                      /* XER. */
    pxTopOfStack--;
    *pxTopOfStack = 0x00000000UL;                      /* CTR. */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) vPortEndScheduler; /* LR. */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) pxCode;            /* SRR0. */
    pxTopOfStack--;
    *pxTopOfStack = portINITIAL_MSR;                   /* SRR1. */
    pxTopOfStack--;
    *pxTopOfStack = ( StackType_t ) vPortEndScheduler; /* Next LR. */
    pxTopOfStack--;
    *pxTopOfStack = 0x00000000UL;                      /* Backchain. */

    return pxTopOfStack;
}
```

**解说：** 这一段实现函数 `pxPortInitialiseStack`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 6: 函数 xPortStartScheduler

```c
/*-----------------------------------------------------------*/
BaseType_t xPortStartScheduler( void )
{
    prvSetupTimerInterrupt();
    XExc_RegisterHandler( XEXC_ID_SYSTEM_CALL, ( XExceptionHandler ) vPortYield, ( void * ) 0 );
    vPortStartFirstTask();

    /* Should not get here as the tasks are now running! */
    return pdFALSE;
}
```

**解说：** 这一段实现函数 `xPortStartScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 7: 函数 vPortEndScheduler

```c
/*-----------------------------------------------------------*/
void vPortEndScheduler( void )
{
    /* Not implemented. */
    for( ; ; )
    {
    }
}
```

**解说：** 这一段实现函数 `vPortEndScheduler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 8: 函数 prvSetupTimerInterrupt

```c
/*-----------------------------------------------------------*/
/*
 * Hardware initialisation to generate the RTOS tick.
 */
static void prvSetupTimerInterrupt( void )
{
    const uint32_t ulInterval = ( ( configCPU_CLOCK_HZ / configTICK_RATE_HZ ) - 1UL );

    XTime_PITClearInterrupt();
    XTime_FITClearInterrupt();
    XTime_WDTClearInterrupt();
    XTime_WDTDisableInterrupt();
    XTime_FITDisableInterrupt();

    XExc_RegisterHandler( XEXC_ID_PIT_INT, ( XExceptionHandler ) vPortTickISR, ( void * ) 0 );

    XTime_PITEnableAutoReload();
    XTime_PITSetInterval( ulInterval );
    XTime_PITEnableInterrupt();
}
```

**解说：** 这一段实现函数 `prvSetupTimerInterrupt`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 9: 函数 vPortISRHandler

```c
/*-----------------------------------------------------------*/
void vPortISRHandler( void * pvNullDoNotUse )
{
    uint32_t ulInterruptStatus, ulInterruptMask = 1UL;
    BaseType_t xInterruptNumber;
    XIntc_Config * pxInterruptController;
    XIntc_VectorTableEntry * pxTable;

    /* Just to remove compiler warning. */
    ( void ) pvNullDoNotUse;

    /* Get the configuration by using the device ID - in this case it is
     * assumed that only one interrupt controller is being used. */
    pxInterruptController = &XIntc_ConfigTable[ XPAR_XPS_INTC_0_DEVICE_ID ];

    /* Which interrupts are pending? */
    ulInterruptStatus = XIntc_mGetIntrStatus( pxInterruptController->BaseAddress );

    for( xInterruptNumber = 0; xInterruptNumber < XPAR_INTC_MAX_NUM_INTR_INPUTS; xInterruptNumber++ )
    {
        if( ulInterruptStatus & 0x01UL )
        {
            /* Clear the pending interrupt. */
            XIntc_mAckIntr( pxInterruptController->BaseAddress, ulInterruptMask );

            /* Call the registered handler. */
            pxTable = &( pxInterruptController->HandlerTable[ xInterruptNumber ] );
            pxTable->Handler( pxTable->CallBackRef );
        }

        /* Check the next interrupt. */
        ulInterruptMask <<= 0x01UL;
        ulInterruptStatus >>= 0x01UL;

        /* Have we serviced all interrupts? */
        if( ulInterruptStatus == 0UL )
        {
            break;
        }
    }
}
```

**解说：** 这一段实现函数 `vPortISRHandler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 10: 函数 vPortSetupInterruptController

```c
/*-----------------------------------------------------------*/
void vPortSetupInterruptController( void )
{
    extern void vPortISRWrapper( void );

    /* Perform all library calls necessary to initialise the exception table
     * and interrupt controller.  This assumes only one interrupt controller is in
     * use. */
    XExc_mDisableExceptions( XEXC_NON_CRITICAL );
    XExc_Init();

    /* The library functions save the context - we then jump to a wrapper to
     * save the stack into the TCB.  The wrapper then calls the handler defined
     * above. */
    XExc_RegisterHandler( XEXC_ID_NON_CRITICAL_INT, ( XExceptionHandler ) vPortISRWrapper, NULL );
    XIntc_Initialize( &xInterruptController, XPAR_XPS_INTC_0_DEVICE_ID );
    XIntc_Start( &xInterruptController, XIN_REAL_MODE );
}
```

**解说：** 这一段实现函数 `vPortSetupInterruptController`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 11: 函数 xPortInstallInterruptHandler

```c
/*-----------------------------------------------------------*/
BaseType_t xPortInstallInterruptHandler( uint8_t ucInterruptID,
                                         XInterruptHandler pxHandler,
                                         void * pvCallBackRef )
{
    BaseType_t xReturn = pdFAIL;

    /* This function is defined here so the scope of xInterruptController can
     * remain within this file. */

    if( XST_SUCCESS == XIntc_Connect( &xInterruptController, ucInterruptID, pxHandler, pvCallBackRef ) )
    {
        XIntc_Enable( &xInterruptController, ucInterruptID );
        xReturn = pdPASS;
    }

    return xReturn;
}
```

**解说：** 这一段实现函数 `xPortInstallInterruptHandler`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。
