# atomic.h 代码解说

源文件：`include/atomic.h`

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

## 片段 2: 预处理配置 ATOMIC_H

```c
/**
 * @file atomic.h
 * @brief FreeRTOS atomic operation support.
 *
 * This file implements atomic functions by disabling interrupts globally.
 * Implementations with architecture specific atomic instructions can be
 * provided under each compiler directory.
 *
 * The atomic interface can be used in FreeRTOS tasks on all FreeRTOS ports. It
 * can also be used in Interrupt Service Routines (ISRs) on FreeRTOS ports that
 * support nested interrupts (i.e. portHAS_NESTED_INTERRUPTS is set to 1). The
 * atomic interface must not be used in ISRs on FreeRTOS ports that do not
 * support nested interrupts (i.e. portHAS_NESTED_INTERRUPTS is set to 0)
 * because ISRs on these ports cannot be interrupted and therefore, do not need
 * atomics in ISRs.
 */
#ifndef ATOMIC_H
#define ATOMIC_H

#ifndef INC_FREERTOS_H
    #error "include FreeRTOS.h must appear in source files before include atomic.h"
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 3: 预处理配置 ATOMIC_ENTER_CRITICAL

```c
/* Standard includes. */
#include <stdint.h>

/* *INDENT-OFF* */
#ifdef __cplusplus
    extern "C" {
#endif
/* *INDENT-ON* */

/*
 * Port specific definitions -- entering/exiting critical section.
 * Refer template -- ./lib/FreeRTOS/portable/Compiler/Arch/portmacro.h
 *
 * Every call to ATOMIC_EXIT_CRITICAL() must be closely paired with
 * ATOMIC_ENTER_CRITICAL().
 *
 */
#if ( portHAS_NESTED_INTERRUPTS == 1 )

/* Nested interrupt scheme is supported in this port. */
    #define ATOMIC_ENTER_CRITICAL() \
    UBaseType_t uxCriticalSectionType = portSET_INTERRUPT_MASK_FROM_ISR()

    #define ATOMIC_EXIT_CRITICAL() \
    portCLEAR_INTERRUPT_MASK_FROM_ISR( uxCriticalSectionType )

#else

/* Nested interrupt scheme is NOT supported in this port. */
    #define ATOMIC_ENTER_CRITICAL()    portENTER_CRITICAL()
    #define ATOMIC_EXIT_CRITICAL()     portEXIT_CRITICAL()

#endif /* portSET_INTERRUPT_MASK_FROM_ISR() */

/*
 * Port specific definition -- "always inline".
 * Inline is compiler specific, and may not always get inlined depending on your
 * optimization level.  Also, inline is considered as performance optimization
 * for atomic.  Thus, if portFORCE_INLINE is not provided by portmacro.h,
 * instead of resulting error, simply define it away.
 */
#ifndef portFORCE_INLINE
    #define portFORCE_INLINE
#endif

#define ATOMIC_COMPARE_AND_SWAP_SUCCESS    0x1U     /**< Compare and swap succeeded, swapped. */
#define ATOMIC_COMPARE_AND_SWAP_FAILURE    0x0U     /**< Compare and swap failed, did not swap. */

/*----------------------------- Swap && CAS ------------------------------*/

/**
 * Atomic compare-and-swap
 *
 * @brief Performs an atomic compare-and-swap operation on the specified values.
 *
 * @param[in, out] pulDestination  Pointer to memory location from where value is
 *                               to be loaded and checked.
 * @param[in] ulExchange         If condition meets, write this value to memory.
 * @param[in] ulComparand        Swap condition.
 *
 * @return Unsigned integer of value 1 or 0. 1 for swapped, 0 for not swapped.
 *
 * @note This function only swaps *pulDestination with ulExchange, if previous
 *       *pulDestination value equals ulComparand.
 */
static portFORCE_INLINE uint32_t Atomic_CompareAndSwap_u32( uint32_t volatile * pulDestination,
                                                            uint32_t ulExchange,
                                                            uint32_t ulComparand )
{
    uint32_t ulReturnValue;

    ATOMIC_ENTER_CRITICAL();
    {
        if( *pulDestination == ulComparand )
        {
            *pulDestination = ulExchange;
            ulReturnValue = ATOMIC_COMPARE_AND_SWAP_SUCCESS;
        }
        else
        {
            ulReturnValue = ATOMIC_COMPARE_AND_SWAP_FAILURE;
        }
    }
    ATOMIC_EXIT_CRITICAL();

    return ulReturnValue;
}
/*-----------------------------------------------------------*/

/**
 * Atomic swap (pointers)
 *
 * @brief Atomically sets the address pointed to by *ppvDestination to the value
 *        of *pvExchange.
 *
 * @param[in, out] ppvDestination  Pointer to memory location from where a pointer
 *                                 value is to be loaded and written back to.
 * @param[in] pvExchange           Pointer value to be written to *ppvDestination.
 *
 * @return The initial value of *ppvDestination.
 */
static portFORCE_INLINE void * Atomic_SwapPointers_p32( void * volatile * ppvDestination,
                                                        void * pvExchange )
{
    void * pReturnValue;

    ATOMIC_ENTER_CRITICAL();
    {
        pReturnValue = *ppvDestination;
        *ppvDestination = pvExchange;
    }
    ATOMIC_EXIT_CRITICAL();

    return pReturnValue;
}
/*-----------------------------------------------------------*/

/**
 * Atomic compare-and-swap (pointers)
 *
 * @brief Performs an atomic compare-and-swap operation on the specified pointer
 *        values.
 *
 * @param[in, out] ppvDestination  Pointer to memory location from where a pointer
 *                                 value is to be loaded and checked.
 * @param[in] pvExchange           If condition meets, write this value to memory.
 * @param[in] pvComparand          Swap condition.
 *
 * @return Unsigned integer of value 1 or 0. 1 for swapped, 0 for not swapped.
 *
 * @note This function only swaps *ppvDestination with pvExchange, if previous
 *       *ppvDestination value equals pvComparand.
 */
static portFORCE_INLINE uint32_t Atomic_CompareAndSwapPointers_p32( void * volatile * ppvDestination,
                                                                    void * pvExchange,
                                                                    void * pvComparand )
{
    uint32_t ulReturnValue = ATOMIC_COMPARE_AND_SWAP_FAILURE;

    ATOMIC_ENTER_CRITICAL();
    {
        if( *ppvDestination == pvComparand )
        {
            *ppvDestination = pvExchange;
            ulReturnValue = ATOMIC_COMPARE_AND_SWAP_SUCCESS;
        }
    }
    ATOMIC_EXIT_CRITICAL();

    return ulReturnValue;
}


/*----------------------------- Arithmetic ------------------------------*/

/**
 * Atomic add
 *
 * @brief Atomically adds count to the value of the specified pointer points to.
 *
 * @param[in,out] pulAddend  Pointer to memory location from where value is to be
 *                         loaded and written back to.
 * @param[in] ulCount      Value to be added to *pulAddend.
 *
 * @return previous *pulAddend value.
 */
static portFORCE_INLINE uint32_t Atomic_Add_u32( uint32_t volatile * pulAddend,
                                                 uint32_t ulCount )
{
    uint32_t ulCurrent;

    ATOMIC_ENTER_CRITICAL();
    {
        ulCurrent = *pulAddend;
        *pulAddend += ulCount;
    }
    ATOMIC_EXIT_CRITICAL();

    return ulCurrent;
}
/*-----------------------------------------------------------*/

/**
 * Atomic subtract
 *
 * @brief Atomically subtracts count from the value of the specified pointer
 *        pointers to.
 *
 * @param[in,out] pulAddend  Pointer to memory location from where value is to be
 *                         loaded and written back to.
 * @param[in] ulCount      Value to be subtract from *pulAddend.
 *
 * @return previous *pulAddend value.
 */
static portFORCE_INLINE uint32_t Atomic_Subtract_u32( uint32_t volatile * pulAddend,
                                                      uint32_t ulCount )
{
    uint32_t ulCurrent;

    ATOMIC_ENTER_CRITICAL();
    {
        ulCurrent = *pulAddend;
        *pulAddend -= ulCount;
    }
    ATOMIC_EXIT_CRITICAL();

    return ulCurrent;
}
/*-----------------------------------------------------------*/

/**
 * Atomic increment
 *
 * @brief Atomically increments the value of the specified pointer points to.
 *
 * @param[in,out] pulAddend  Pointer to memory location from where value is to be
 *                         loaded and written back to.
 *
 * @return *pulAddend value before increment.
 */
static portFORCE_INLINE uint32_t Atomic_Increment_u32( uint32_t volatile * pulAddend )
{
    uint32_t ulCurrent;

    ATOMIC_ENTER_CRITICAL();
    {
        ulCurrent = *pulAddend;
        *pulAddend += 1;
    }
    ATOMIC_EXIT_CRITICAL();

    return ulCurrent;
}
/*-----------------------------------------------------------*/

/**
 * Atomic decrement
 *
 * @brief Atomically decrements the value of the specified pointer points to
 *
 * @param[in,out] pulAddend  Pointer to memory location from where value is to be
 *                         loaded and written back to.
 *
 * @return *pulAddend value before decrement.
 */
static portFORCE_INLINE uint32_t Atomic_Decrement_u32( uint32_t volatile * pulAddend )
{
    uint32_t ulCurrent;

    ATOMIC_ENTER_CRITICAL();
    {
        ulCurrent = *pulAddend;
        *pulAddend -= 1;
    }
    ATOMIC_EXIT_CRITICAL();

    return ulCurrent;
}

/*----------------------------- Bitwise Logical ------------------------------*/

/**
 * Atomic OR
 *
 * @brief Performs an atomic OR operation on the specified values.
 *
 * @param [in, out] pulDestination  Pointer to memory location from where value is
 *                                to be loaded and written back to.
 * @param [in] ulValue            Value to be ORed with *pulDestination.
 *
 * @return The original value of *pulDestination.
 */
static portFORCE_INLINE uint32_t Atomic_OR_u32( uint32_t volatile * pulDestination,
                                                uint32_t ulValue )
{
    uint32_t ulCurrent;

    ATOMIC_ENTER_CRITICAL();
    {
        ulCurrent = *pulDestination;
        *pulDestination |= ulValue;
    }
    ATOMIC_EXIT_CRITICAL();

    return ulCurrent;
}
/*-----------------------------------------------------------*/

/**
 * Atomic AND
 *
 * @brief Performs an atomic AND operation on the specified values.
 *
 * @param [in, out] pulDestination  Pointer to memory location from where value is
 *                                to be loaded and written back to.
 * @param [in] ulValue            Value to be ANDed with *pulDestination.
 *
 * @return The original value of *pulDestination.
 */
static portFORCE_INLINE uint32_t Atomic_AND_u32( uint32_t volatile * pulDestination,
                                                 uint32_t ulValue )
{
    uint32_t ulCurrent;

    ATOMIC_ENTER_CRITICAL();
    {
        ulCurrent = *pulDestination;
        *pulDestination &= ulValue;
    }
    ATOMIC_EXIT_CRITICAL();

    return ulCurrent;
}
/*-----------------------------------------------------------*/

/**
 * Atomic NAND
 *
 * @brief Performs an atomic NAND operation on the specified values.
 *
 * @param [in, out] pulDestination  Pointer to memory location from where value is
 *                                to be loaded and written back to.
 * @param [in] ulValue            Value to be NANDed with *pulDestination.
 *
 * @return The original value of *pulDestination.
 */
static portFORCE_INLINE uint32_t Atomic_NAND_u32( uint32_t volatile * pulDestination,
                                                  uint32_t ulValue )
{
    uint32_t ulCurrent;

    ATOMIC_ENTER_CRITICAL();
    {
        ulCurrent = *pulDestination;
        *pulDestination = ~( ulCurrent & ulValue );
    }
    ATOMIC_EXIT_CRITICAL();

    return ulCurrent;
}
/*-----------------------------------------------------------*/

/**
 * Atomic XOR
 *
 * @brief Performs an atomic XOR operation on the specified values.
 *
 * @param [in, out] pulDestination  Pointer to memory location from where value is
 *                                to be loaded and written back to.
 * @param [in] ulValue            Value to be XORed with *pulDestination.
 *
 * @return The original value of *pulDestination.
 */
static portFORCE_INLINE uint32_t Atomic_XOR_u32( uint32_t volatile * pulDestination,
                                                 uint32_t ulValue )
{
    uint32_t ulCurrent;

    ATOMIC_ENTER_CRITICAL();
    {
        ulCurrent = *pulDestination;
        *pulDestination ^= ulValue;
    }
    ATOMIC_EXIT_CRITICAL();

    return ulCurrent;
}

/* *INDENT-OFF* */
#ifdef __cplusplus
    }
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 4: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 5: 预处理配置

```c
/* *INDENT-ON* */
#endif /* ATOMIC_H */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。
