# secure_init.c 代码解说

源文件：`portable/GCC/ARM_CM52/secure/secure_init.c`

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

## 片段 2: 预处理配置 SecureInit_DePrioritizeNSExceptions

```c
/* Standard includes. */
#include <stdint.h>

/* Secure init includes. */
#include "secure_init.h"

/* Secure port macros. */
#include "secure_port_macros.h"

/**
 * @brief Constants required to manipulate the SCB.
 */
#define secureinitSCB_AIRCR                 ( ( volatile uint32_t * ) 0xe000ed0c )  /* Application Interrupt and Reset Control Register. */
#define secureinitSCB_AIRCR_VECTKEY_POS     ( 16UL )
#define secureinitSCB_AIRCR_VECTKEY_MASK    ( 0xFFFFUL << secureinitSCB_AIRCR_VECTKEY_POS )
#define secureinitSCB_AIRCR_PRIS_POS        ( 14UL )
#define secureinitSCB_AIRCR_PRIS_MASK       ( 1UL << secureinitSCB_AIRCR_PRIS_POS )

/**
 * @brief Constants required to manipulate the FPU.
 */
#define secureinitFPCCR                     ( ( volatile uint32_t * ) 0xe000ef34 )  /* Floating Point Context Control Register. */
#define secureinitFPCCR_LSPENS_POS          ( 29UL )
#define secureinitFPCCR_LSPENS_MASK         ( 1UL << secureinitFPCCR_LSPENS_POS )
#define secureinitFPCCR_TS_POS              ( 26UL )
#define secureinitFPCCR_TS_MASK             ( 1UL << secureinitFPCCR_TS_POS )

#define secureinitNSACR                     ( ( volatile uint32_t * ) 0xe000ed8c )  /* Non-secure Access Control Register. */
#define secureinitNSACR_CP10_POS            ( 10UL )
#define secureinitNSACR_CP10_MASK           ( 1UL << secureinitNSACR_CP10_POS )
#define secureinitNSACR_CP11_POS            ( 11UL )
#define secureinitNSACR_CP11_MASK           ( 1UL << secureinitNSACR_CP11_POS )
/*-----------------------------------------------------------*/

secureportNON_SECURE_CALLABLE void SecureInit_DePrioritizeNSExceptions( void )
{
    uint32_t ulIPSR;

    /* Read the Interrupt Program Status Register (IPSR) value. */
    secureportREAD_IPSR( ulIPSR );

    /* Do nothing if the processor is running in the Thread Mode. IPSR is zero
     * when the processor is running in the Thread Mode. */
    if( ulIPSR != 0 )
    {
        *( secureinitSCB_AIRCR ) = ( *( secureinitSCB_AIRCR ) & ~( secureinitSCB_AIRCR_VECTKEY_MASK | secureinitSCB_AIRCR_PRIS_MASK ) ) |
                                   ( ( 0x05FAUL << secureinitSCB_AIRCR_VECTKEY_POS ) & secureinitSCB_AIRCR_VECTKEY_MASK ) |
                                   ( ( 0x1UL << secureinitSCB_AIRCR_PRIS_POS ) & secureinitSCB_AIRCR_PRIS_MASK );
    }
}
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 函数 SecureInit_EnableNSFPUAccess

```c
/*-----------------------------------------------------------*/
secureportNON_SECURE_CALLABLE void SecureInit_EnableNSFPUAccess( void )
{
    uint32_t ulIPSR;

    /* Read the Interrupt Program Status Register (IPSR) value. */
    secureportREAD_IPSR( ulIPSR );

    /* Do nothing if the processor is running in the Thread Mode. IPSR is zero
     * when the processor is running in the Thread Mode. */
    if( ulIPSR != 0 )
    {
        /* CP10 = 1 ==> Non-secure access to the Floating Point Unit is
         * permitted. CP11 should be programmed to the same value as CP10. */
        *( secureinitNSACR ) |= ( secureinitNSACR_CP10_MASK | secureinitNSACR_CP11_MASK );

        /* LSPENS = 0 ==> LSPEN is writable from non-secure state. This ensures
         * that we can enable/disable lazy stacking in port.c file. */
        *( secureinitFPCCR ) &= ~( secureinitFPCCR_LSPENS_MASK );

        /* TS = 1 ==> Treat FP registers as secure i.e. callee saved FP
         * registers (S16-S31) are also pushed to stack on exception entry and
         * restored on exception return. */
        *( secureinitFPCCR ) |= ( secureinitFPCCR_TS_MASK );
    }
}
```

**解说：** 这一段实现函数 `SecureInit_EnableNSFPUAccess`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 4: 说明性注释

```c
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。
