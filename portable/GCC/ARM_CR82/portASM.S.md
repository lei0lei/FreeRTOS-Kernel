# portASM.S 代码解说

源文件：`portable/GCC/ARM_CR82/portASM.S`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 文件头和许可证

```asm
/*
 * FreeRTOS Kernel <DEVELOPMENT BRANCH>
 * Copyright (C) 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * Copyright 2025-2026 Arm Limited and/or its affiliates
 * <open-source-office@arm.com>
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

## 片段 2: 说明性注释

```asm
/*
 * This file is tailored for ARM Cortex-R82 with SMP enabled.
 * It includes macros and functions for saving/restoring task context,
 * handling interrupts, and supporting multi-core operations.
 */
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：This file is tailored for ARM Cortex-R82 with SMP enabled. It includes macros and functions for saving/restoring task context, handling interrupts, and supporting multi-core operations.。

## 片段 3: 预处理配置

```asm
#include "FreeRTOSConfig.h"
#include "portmacro.h"
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 4: 宏 MPU_WRAPPERS_INCLUDED_FROM_API_FILE

```asm
/* Defining MPU_WRAPPERS_INCLUDED_FROM_API_FILE ensures that PRIVILEGED_FUNCTION
 * is defined correctly and privileged functions are placed in correct sections. */
#define MPU_WRAPPERS_INCLUDED_FROM_API_FILE
```

**解说：** 这一段定义宏 `MPU_WRAPPERS_INCLUDED_FROM_API_FILE`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 5: 预处理配置

```asm
/* System call numbers includes. */
#include "mpu_syscall_numbers.h"
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 6: 预处理配置

```asm
/* MPU_WRAPPERS_INCLUDED_FROM_API_FILE is needed to be defined only for the
 * header files. */
#undef MPU_WRAPPERS_INCLUDED_FROM_API_FILE
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 7: 代码片段 7

```asm
.text
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 8: 预处理配置

```asm
/* Variables and functions. */
#if ( configNUMBER_OF_CORES == 1 )
   .extern pxCurrentTCB
   .extern ullCriticalNesting
   .extern ullPortInterruptNesting
#else /* #if ( configNUMBER_OF_CORES == 1 ) */
   .extern pxCurrentTCBs
   .extern ullCriticalNestings
   .extern ullPortInterruptNestings
#endif
   .extern vTaskSwitchContext
   .extern vApplicationIRQHandler
   .extern ullPortTaskHasFPUContext
   .extern ullPortYieldRequired
   .extern _freertos_vector_table
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 9: 预处理配置

```asm
#if ( configENABLE_MPU == 1 )
   .extern xPortIsTaskPrivileged
   .extern vSystemCallEnter
   .extern vSystemCallExit
   .extern vRequestSystemCallExit
   .extern uxSystemCallImplementations
#endif /* #if ( configENABLE_MPU == 1 ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 10: 代码片段 10

```asm
   .global FreeRTOS_IRQ_Handler
   .global FreeRTOS_SWI_Handler
   .global vPortSaveTaskContext
   .global vPortRestoreTaskContext
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 11: 预处理配置

```asm
#if ( configENABLE_MPU == 1 )
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 12: 代码片段 12

```asm
   .macro portLOAD_MPU_REGIONS_ADDRESSES
MOV     X3, # portSTACK_REGION                      /* Task's first programmed region is its stack region as the first four MPU regions are already programmed.*/
MOV     X4, # configTOTAL_MPU_REGIONS - 1           /* Upper limit = configTOTAL_MPU_REGIONS - 1 */
1 :
    CMP     X3, X4                                  /* Compare i with ( configTOTAL_MPU_REGIONS - 1 ) */
    B.GT    2f                                      /* if i > ( configTOTAL_MPU_REGIONS - 1 ), exit loop */
    MSR     PRSELR_EL1, X3                          /* Program PRSELR_EL1. */
    ISB                                             /* Ensure PRSELR selection takes effect before registers access. */
    LDP     X1, X2, [ X0 ], # 0x10                  /* Retrieve ullPrbarEl1 and ullPrlarEl1r */
    MSR     PRBAR_EL1, X1                           /* Program PRBAR_EL1. */
    MSR     PRLAR_EL1, X2                           /* Program PRLAR_EL1. */
    ADD     X3, X3, # 1                             /* i++ */
    B       1b
2 :
    DSB     SY
    ISB
   .endm
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 13: 代码片段 13

```asm
   .macro portSTORE_MPU_REGIONS_ADDRESSES
MOV     X3, # portSTACK_REGION                      /* Task's first programmed region is its stack region as the first four MPU regions are already programmed.*/
MOV     X4, # configTOTAL_MPU_REGIONS - 1           /* Upper limit = configTOTAL_MPU_REGIONS - 1 */
1 :
    CMP     X3, X4                                  /* Compare i with ( configTOTAL_MPU_REGIONS - 1 ) */
    B.GT    2f                                      /* if i > ( configTOTAL_MPU_REGIONS - 1 ), exit loop */
    MSR     PRSELR_EL1, X3                          /* Program PRSELR_EL1. */
    ISB                                             /* Ensure PRSELR selection takes effect before registers access. */
    MRS     X1, PRBAR_EL1                           /* Retrieve PRBAR_EL1. */
    MRS     X2, PRLAR_EL1                           /* Retrieve PRLAR_EL1. */
    STP     X1, X2, [ X0 ], # 0x10                  /* Store PRBAR_EL1 and PRLAR_EL1 in ullPrbarEl1 and ullPrlarEl1r */
    ADD     X3, X3, # 1                             /* i++ */
    B       1b
2 :
    /* No additional barrier required after reading PR* registers. */
   .endm
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 14: 预处理配置

```asm
#endif /* #if ( configENABLE_MPU == 1 ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 15: 说明性注释

```asm
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。

## 片段 16: 代码片段 16

```asm
   .macro savefuncontextgpregs
/* Save function context general-purpose registers. */
STP X0, X1, [ SP, # - 0x10 ] !
STP X2, X3, [ SP, # - 0x10 ] !
STP X4, X5, [ SP, # - 0x10 ] !
STP X6, X7, [ SP, # - 0x10 ] !
STP X8, X9, [ SP, # - 0x10 ] !
STP X10, X11, [ SP, # - 0x10 ] !
STP X12, X13, [ SP, # - 0x10 ] !
STP X14, X15, [ SP, # - 0x10 ] !
STP X16, X17, [ SP, # - 0x10 ] !
STP X18, X29, [ SP, # - 0x10 ] !
STR X30, [ SP, # - 0x10 ] !
   .endm
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 17: 说明性注释

```asm
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。

## 片段 18: 代码片段 18

```asm
   .macro savesyscallcontextgpregs
/* Save system call context general-purpose registers. */
STP X4, X5, [ SP, # - 0x10 ] !
STP X6, X7, [ SP, # - 0x10 ] !
STP X8, X9, [ SP, # - 0x10 ] !
STP X10, X11, [ SP, # - 0x10 ] !
STP X12, X13, [ SP, # - 0x10 ] !
STP X14, X15, [ SP, # - 0x10 ] !
STP X16, X17, [ SP, # - 0x10 ] !
STP X18, X29, [ SP, # - 0x10 ] !
   .endm
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 19: 说明性注释

```asm
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。

## 片段 20: 代码片段 20

```asm
   .macro restorefuncontextgpregs
/* Restore function context general-purpose registers. */
LDR X30, [ SP ], # 0x10
LDP X18, X29, [ SP ], # 0x10
LDP X16, X17, [ SP ], # 0x10
LDP X14, X15, [ SP ], # 0x10
LDP X12, X13, [ SP ], # 0x10
LDP X10, X11, [ SP ], # 0x10
LDP X8, X9, [ SP ], # 0x10
LDP X6, X7, [ SP ], # 0x10
LDP X4, X5, [ SP ], # 0x10
LDP X2, X3, [ SP ], # 0x10
LDP X0, X1, [ SP ], # 0x10
   .endm
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 21: 说明性注释

```asm
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。

## 片段 22: 代码片段 22

```asm
   .macro restorefuncontextgpregexceptx0
/* Restore function context general-purpose registers while discarding old X0. */
LDR X30, [ SP ], # 0x10
LDP X18, X29, [ SP ], # 0x10
LDP X16, X17, [ SP ], # 0x10
LDP X14, X15, [ SP ], # 0x10
LDP X12, X13, [ SP ], # 0x10
LDP X10, X11, [ SP ], # 0x10
LDP X8, X9, [ SP ], # 0x10
LDP X6, X7, [ SP ], # 0x10
LDP X4, X5, [ SP ], # 0x10
LDP X2, X3, [ SP ], # 0x10
LDP XZR, X1, [ SP ], # 0x10
   .endm
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 23: 说明性注释

```asm
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。

## 片段 24: 代码片段 24

```asm
   .macro restoresyscallcontextgpregs
/* Restore system call context general-purpose registers. */
LDP X18, X29, [ SP ], # 0x10
LDP X16, X17, [ SP ], # 0x10
LDP X14, X15, [ SP ], # 0x10
LDP X12, X13, [ SP ], # 0x10
LDP X10, X11, [ SP ], # 0x10
LDP X8, X9, [ SP ], # 0x10
LDP X6, X7, [ SP ], # 0x10
LDP X4, X5, [ SP ], # 0x10
   .endm
/*-----------------------------------------------------------*/
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 25: 代码片段 25

```asm
   .macro saveallgpregisters
/* Save all general-purpose registers on stack. */
STP X0, X1, [ SP, # - 0x10 ] !
STP X2, X3, [ SP, # - 0x10 ] !
STP X4, X5, [ SP, # - 0x10 ] !
STP X6, X7, [ SP, # - 0x10 ] !
STP X8, X9, [ SP, # - 0x10 ] !
STP X10, X11, [ SP, # - 0x10 ] !
STP X12, X13, [ SP, # - 0x10 ] !
STP X14, X15, [ SP, # - 0x10 ] !
STP X16, X17, [ SP, # - 0x10 ] !
STP X18, X19, [ SP, # - 0x10 ] !
STP X20, X21, [ SP, # - 0x10 ] !
STP X22, X23, [ SP, # - 0x10 ] !
STP X24, X25, [ SP, # - 0x10 ] !
STP X26, X27, [ SP, # - 0x10 ] !
STP X28, X29, [ SP, # - 0x10 ] !
STP X30, XZR, [ SP, # - 0x10 ] !
   .endm
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 26: 说明性注释

```asm
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。

## 片段 27: 代码片段 27

```asm
   .macro restoreallgpregisters
/* Restore all general-purpose registers from stack. */
LDP X30, XZR, [ SP ], # 0x10
LDP X28, X29, [ SP ], # 0x10
LDP X26, X27, [ SP ], # 0x10
LDP X24, X25, [ SP ], # 0x10
LDP X22, X23, [ SP ], # 0x10
LDP X20, X21, [ SP ], # 0x10
LDP X18, X19, [ SP ], # 0x10
LDP X16, X17, [ SP ], # 0x10
LDP X14, X15, [ SP ], # 0x10
LDP X12, X13, [ SP ], # 0x10
LDP X10, X11, [ SP ], # 0x10
LDP X8, X9, [ SP ], # 0x10
LDP X6, X7, [ SP ], # 0x10
LDP X4, X5, [ SP ], # 0x10
LDP X2, X3, [ SP ], # 0x10
LDP X0, X1, [ SP ], # 0x10
   .endm
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 28: 说明性注释

```asm
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。

## 片段 29: 代码片段 29

```asm
   .macro savefloatregisters
/* Save floating-point registers and configuration/status registers. */
STP Q0, Q1, [ SP, # - 0x20 ] !
STP Q2, Q3, [ SP, # - 0x20 ] !
STP Q4, Q5, [ SP, # - 0x20 ] !
STP Q6, Q7, [ SP, # - 0x20 ] !
STP Q8, Q9, [ SP, # - 0x20 ] !
STP Q10, Q11, [ SP, # - 0x20 ] !
STP Q12, Q13, [ SP, # - 0x20 ] !
STP Q14, Q15, [ SP, # - 0x20 ] !
STP Q16, Q17, [ SP, # - 0x20 ] !
STP Q18, Q19, [ SP, # - 0x20 ] !
STP Q20, Q21, [ SP, # - 0x20 ] !
STP Q22, Q23, [ SP, # - 0x20 ] !
STP Q24, Q25, [ SP, # - 0x20 ] !
STP Q26, Q27, [ SP, # - 0x20 ] !
STP Q28, Q29, [ SP, # - 0x20 ] !
STP Q30, Q31, [ SP, # - 0x20 ] !
MRS X9, FPSR
MRS X10, FPCR
STP W9, W10, [ SP, # - 0x10 ] !
   .endm
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 30: 说明性注释

```asm
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。

## 片段 31: 代码片段 31

```asm
   .macro restorefloatregisters
/* Restore floating-point registers and configuration/status registers. */
LDP W9, W10, [ SP ], # 0x10
MSR FPSR, X9
MSR FPCR, X10
LDP Q30, Q31, [ SP ], # 0x20
LDP Q28, Q29, [ SP ], # 0x20
LDP Q26, Q27, [ SP ], # 0x20
LDP Q24, Q25, [ SP ], # 0x20
LDP Q22, Q23, [ SP ], # 0x20
LDP Q20, Q21, [ SP ], # 0x20
LDP Q18, Q19, [ SP ], # 0x20
LDP Q16, Q17, [ SP ], # 0x20
LDP Q14, Q15, [ SP ], # 0x20
LDP Q12, Q13, [ SP ], # 0x20
LDP Q10, Q11, [ SP ], # 0x20
LDP Q8, Q9, [ SP ], # 0x20
LDP Q6, Q7, [ SP ], # 0x20
LDP Q4, Q5, [ SP ], # 0x20
LDP Q2, Q3, [ SP ], # 0x20
LDP Q0, Q1, [ SP ], # 0x20
   .endm
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 32: 说明性注释

```asm
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。

## 片段 33: 代码片段 33

```asm
   .macro portSAVE_CONTEXT
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 34: 预处理配置

```asm
#if ( configENABLE_MPU == 1 )
   /* Switch to use the EL1 stack pointer. */
   MSR SPSEL, # 1
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 35: 代码片段 35

```asm
   /* Store X0-X4 as they are being used to save the user allocated task stack and to program the MPU */
   STP X0, X1,  [ SP, # - 0x10 ] !
   STP X2, X3, [ SP, # - 0x10 ] !
   STR X4, [ SP, # - 0x10 ] !
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 36: 代码片段 36

```asm
   /* Switch to use the EL0 stack pointer. */
   MSR SPSEL, # 0
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 37: 预处理配置

```asm
   /* Store user allocated task stack and use ullContext as the SP */
   #if ( configNUMBER_OF_CORES == 1 )
      adrp    X0, pxCurrentTCB
      add     X0, X0, :lo12:pxCurrentTCB   /* X0 = &pxCurrentTCB */
   #else
      adrp    X0, pxCurrentTCBs
      add     X0, X0, :lo12:pxCurrentTCBs  /* X0 = &pxCurrentTCBs */
      /* Get the core ID to index the TCB correctly. */
      MRS X2, MPIDR_EL1  /* Read the Multiprocessor Affinity Register */
      AND X2, X2, # 0xff /* Extract Aff0 which contains the core ID */
      LSL X2, X2, # 3    /* Scale the core ID to the size of a pointer (64-bit system) */
      ADD X0, X0, X2     /* Add the offset for the current core's TCB pointer */
   #endif
   LDR X1, [ X0 ]
   ADD X1, X1, #8         /* X1 = X1 + 8, X1 now points to ullTaskUnprivilegedSP in TCB. */
   MOV X0, SP
   STR X0, [ X1 ]         /* Save ullTaskUnprivilegedSP on task's TCB */
   SUB X1, X1, #8         /* X1 = X1 - 8, X1 now points to pxTopOfStack in TCB. */
   LDR X1, [ X1 ]
   MOV SP, X1             /* Use pxTopOfStack ( ullContext ) as the SP. */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 38: 代码片段 38

```asm
   savefuncontextgpregs
   #if ( configNUMBER_OF_CORES > 1 )
      MRS X1, ELR_EL1       /* Save ELR_EL1 before calling xPortIsTaskPrivileged which would change its value in case of multicore */
      STR X1, [ SP, # - 0x10 ] !
   #endif
   BL xPortIsTaskPrivileged
   #if ( configNUMBER_OF_CORES > 1 )
      LDR X1, [ SP ], # 0x10
      MSR ELR_EL1, X1
   #endif
   CBNZ X0, 3f               /* If task is privileged, skip saving MPU context. */
   #if ( configNUMBER_OF_CORES == 1 )
      adrp    X0, pxCurrentTCB
      add     X0, X0, :lo12:pxCurrentTCB   /* X0 = &pxCurrentTCB */
   #else
      adrp    X0, pxCurrentTCBs
      add     X0, X0, :lo12:pxCurrentTCBs  /* X0 = &pxCurrentTCBs */
      /* Get the core ID to index the TCB correctly. */
      MRS X2, MPIDR_EL1  /* Read the Multiprocessor Affinity Register */
      AND X2, X2, # 0xff /* Extract Aff0 which contains the core ID */
      LSL X2, X2, # 3    /* Scale the core ID to the size of a pointer (64-bit system) */
      ADD X0, X0, X2     /* Add the offset for the current core's TCB pointer */
   #endif
   LDR X0, [ X0 ]
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 39: 代码片段 39

```asm
   ADD X0, X0, #16         /* X0 = X0 + 16. X0 now points to MAIR_EL1 in TCB. */
   MRS X1, MAIR_EL1        /* X1 = MAIR_EL1. */
   STR X1, [ X0 ], # 0x8   /* Store MAIR_EL1 in TCB, X0 = X0 + 8. */
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 40: 代码片段 40

```asm
   portSTORE_MPU_REGIONS_ADDRESSES /* Store MPU region addresses onto TCB. */
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 41: 代码片段 41

```asm
3 :
   restorefuncontextgpregs
   MSR SPSEL, # 1
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 42: 代码片段 42

```asm
   /* Restore X0-X4. */
   LDR X4, [ SP ], # 0x10
   LDP X2, X3, [ SP ], # 0x10
   LDP X0, X1, [ SP ], # 0x10
#endif /* #if ( configENABLE_MPU == 1 ) */
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 43: 代码片段 43

```asm
MSR SPSEL, # 0
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 44: 代码片段 44

```asm
/* Save the entire context. */
saveallgpregisters
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 45: 代码片段 45

```asm
/* Save the SPSR and ELR values. */
MRS X3, SPSR_EL1
MRS X2, ELR_EL1
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 46: 代码片段 46

```asm
STP X2, X3, [ SP, # - 0x10 ] !
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 47: 预处理配置

```asm
/* Save the critical section nesting depth. */
#if ( configNUMBER_OF_CORES == 1 )
   adrp    X0, ullCriticalNesting
   add     X0, X0, :lo12:ullCriticalNesting   /* X0 = &ullCriticalNesting */
#else
   adrp    X0, ullCriticalNestings
   add     X0, X0, :lo12:ullCriticalNestings  /* X0 = &ullCriticalNestings */
   /* Calculate per-core index using MPIDR_EL1 for SMP support. */
   MRS X1, MPIDR_EL1    /* Read the Multiprocessor Affinity Register. */
   AND X1, X1, # 0xff   /* Extract Aff0 (core ID). */
   LSL X1, X1, # 3      /* Multiply core ID by pointer size (8 bytes). */
   ADD X0, X0, X1       /* Add offset to base address. */
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 48: 代码片段 48

```asm
LDR X3, [ X0 ]
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 49: 代码片段 49

```asm
/* Save the FPU context indicator. */
adrp    X0, ullPortTaskHasFPUContext
add     X0, X0, :lo12:ullPortTaskHasFPUContext   /* X0 = &ullPortTaskHasFPUContext */
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 50: 预处理配置

```asm
#if ( configNUMBER_OF_CORES > 1 )
   ADD X0, X0, X1 /* Add to the base of the FPU array. */
#endif
LDR X2, [ X0 ]
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 51: 代码片段 51

```asm
/* Save the FPU context, if any (32 128-bit registers). */
CBZ X2, 4f /* FPU context not present, skip saving FPU registers. */
savefloatregisters
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 52: 代码片段 52

```asm
4 :
/* Store the critical nesting count and FPU context indicator. */
STP X2, X3, [ SP, # - 0x10 ] !
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 53: 预处理配置

```asm
#if ( configNUMBER_OF_CORES == 1 )
   adrp    X0, pxCurrentTCB
   add     X0, X0, :lo12:pxCurrentTCB   /* X0 = &pxCurrentTCB */
#else
   adrp    X0, pxCurrentTCBs
   add     X0, X0, :lo12:pxCurrentTCBs  /* X0 = &pxCurrentTCBs */
   MRS X1, MPIDR_EL1    /* Read Multiprocessor Affinity Register .*/
   AND X1, X1, # 0xff   /* Extract core ID. */
   LSL X1, X1, # 3      /* Multiply core ID by pointer size. */
   ADD X0, X0, X1       /* Offset for current core's TCB pointer. */
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 54: 代码片段 54

```asm
LDR X1, [ X0 ]
MOV X0, SP
STR X0, [ X1 ]      /* Save pxTopOfStack on the TCB. */
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 55: 代码片段 55

```asm
/* Switch to use the EL1 stack pointer. */
MSR SPSEL, # 1
   .endm
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 56: 说明性注释

```asm
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。

## 片段 57: 代码片段 57

```asm
   .macro portRESTORE_CONTEXT
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 58: 预处理配置

```asm
#if ( configENABLE_MPU == 1 )
   /* Switch to use the EL1 stack pointer. */
   MSR SPSEL, # 1
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 59: 代码片段 59

```asm
   savefuncontextgpregs
   BL xPortIsTaskPrivileged
   CBNZ X0, 3f              /* If task is privileged, skip restoring MPU context. */
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 60: 代码片段 60

```asm
   /* Switch to use the EL0 stack pointer. */
   MSR SPSEL, # 0
   #if ( configNUMBER_OF_CORES == 1 )
      adrp    X0, pxCurrentTCB
      add     X0, X0, :lo12:pxCurrentTCB   /* X0 = &pxCurrentTCB */
   #else
      adrp    X0, pxCurrentTCBs
      add     X0, X0, :lo12:pxCurrentTCBs  /* X0 = &pxCurrentTCBs */
      /* Get the core ID to index the TCB correctly. */
      MRS X2, MPIDR_EL1  /* Read the Multiprocessor Affinity Register */
      AND X2, X2, # 0xff /* Extract Aff0 which contains the core ID */
      LSL X2, X2, # 3    /* Scale the core ID to the size of a pointer (64-bit system) */
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 61: 代码片段 61

```asm
      ADD X0, X0, X2     /* Add the offset for the current core's TCB pointer */
   #endif
   LDR X0, [ X0 ]
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 62: 代码片段 62

```asm
   DMB SY                 /* Complete outstanding transfers before disabling MPU. */
   MRS X1, SCTLR_EL1      /* X1 = SCTLR_EL1 */
   BIC X1, X1, # (1 << 0) /* Clears bit 0 of X1 */
   MSR SCTLR_EL1, X1      /* Disable MPU. */
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 63: 代码片段 63

```asm
   ADD X0, X0, #16         /* X0 = X0 + 16. X0 now points to MAIR_EL1 in TCB. */
   LDR X1, [ X0 ], # 0x8   /* X1 = *X0 i.e. X1 = MAIR_EL1, X0 = X0 + 8. */
   MSR MAIR_EL1, X1        /* Program MAIR_EL1. */
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 64: 代码片段 64

```asm
   portLOAD_MPU_REGIONS_ADDRESSES /* Load MPU region addresses from TCB. */
   MRS X1, SCTLR_EL1              /* X1 = SCTLR_EL1 */
   ORR X1, X1, # (1 << 0)         /* Sets bit 0 of X1 */
   MSR SCTLR_EL1, X1              /* Enable MPU. */
   DSB SY                         /* Force memory writes before continuing. */
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 65: 代码片段 65

```asm
3 :
   MSR SPSEL, # 1
   restorefuncontextgpregs
#endif /* #if ( configENABLE_MPU == 1 ) */
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 66: 代码片段 66

```asm
   /* Switch to use the EL0 stack pointer. */
   MSR SPSEL, # 0
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 67: 预处理配置

```asm
   #if ( configNUMBER_OF_CORES == 1 )
      adrp    X0, pxCurrentTCB
      add     X0, X0, :lo12:pxCurrentTCB   /* X0 = &pxCurrentTCB */
   #else
      adrp    X0, pxCurrentTCBs
      add     X0, X0, :lo12:pxCurrentTCBs  /* X0 = &pxCurrentTCBs */
      /* Get the core ID to index the TCB correctly. */
      MRS X2, MPIDR_EL1  /* Read the Multiprocessor Affinity Register */
      AND X2, X2, # 0xff /* Extract Aff0 which contains the core ID */
      LSL X2, X2, # 3    /* Scale the core ID to the size of a pointer (64-bit system) */
      ADD X0, X0, X2     /* Add the offset for the current core's TCB pointer */
   #endif
   LDR X1, [ X0 ]
   LDR X0, [ X1 ]               /* X0 = Location of saved context in TCB. */
   MOV SP, X0
   LDP X2, X3, [ SP ], # 0x10   /* Retrieve critical nesting and FPU indicator */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 68: 预处理配置

```asm
   #if ( configNUMBER_OF_CORES == 1 )
      adrp    X0, ullCriticalNesting
      add     X0, X0, :lo12:ullCriticalNesting   /* X0 = &ullCriticalNesting */
   #else
      adrp    X0, ullCriticalNestings
      add     X0, X0, :lo12:ullCriticalNestings  /* X0 = &ullCriticalNestings */
      /* Calculate offset for current core's ullCriticalNesting */
      MRS X1, MPIDR_EL1  /* Read Multiprocessor Affinity Register */
      AND X1, X1, # 0xff /* Extract Aff0, which contains the core ID */
      LSL X1, X1, # 3    /* Scale core ID to the size of a pointer (assuming 64-bit system) */
      ADD X0, X0, X1     /* Add offset for the current core's ullCriticalNesting */
   #endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 69: 代码片段 69

```asm
   MOV X1, # 255            /* Default mask */
   CBZ X3, 4f
   MOV X1, # portMAX_API_PRIORITY_MASK
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 70: 代码片段 70

```asm
4:
   MSR ICC_PMR_EL1, X1      /* Set interrupt mask */
   DSB SY
   ISB SY
   STR X3, [ X0 ]           /* Restore critical nesting */
   /* Restore the FPU context indicator. */
   adrp    X0, ullPortTaskHasFPUContext
   add     X0, X0, :lo12:ullPortTaskHasFPUContext   /* X0 = &ullPortTaskHasFPUContext */
   #if ( configNUMBER_OF_CORES > 1 )
      MRS X1, MPIDR_EL1  /* Read Multiprocessor Affinity Register */
      AND X1, X1, # 0xff /* Extract Aff0, which contains the core ID */
      LSL X1, X1, # 3    /* Scale core ID to the size of a pointer (assuming 64-bit system) */
      ADD X0, X0, X1     /* Add to the base of the FPU array */
   #endif
   STR X2, [ X0 ]
   /* Restore the FPU context, if any. */
   CBZ X2, 5f
   restorefloatregisters
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 71: 代码片段 71

```asm
5:
   LDP X2, X3, [ SP ], # 0x10  /* Restore SPSR and ELR */
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 72: 代码片段 72

```asm
   MSR SPSR_EL1, X3
   MSR ELR_EL1, X2
   restoreallgpregisters
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 73: 预处理配置

```asm
#if ( configENABLE_MPU == 1 )
   /* Save pxTopOfStack ( ullContext ) on the task's TCB and set SP_EL0 to ullTaskUnprivilegedSP. */
   MSR SPSEL, # 1
   STP   X8, X9, [ SP, # - 0x10 ] !
   STR   X10, [ SP, # - 0x10 ] !
   #if ( configNUMBER_OF_CORES == 1 )
      adrp    X8, pxCurrentTCB
      add     X8, X8, :lo12:pxCurrentTCB   /* X8 = &pxCurrentTCB */
   #else
      adrp    X8, pxCurrentTCBs
      add     X8, X8, :lo12:pxCurrentTCBs  /* X8 = &pxCurrentTCBs */
      /* Get the core ID to index the TCB correctly. */
      MRS X10, MPIDR_EL1   /* Read the Multiprocessor Affinity Register */
      AND X10, X10, # 0xff /* Extract Aff0 which contains the core ID */
      LSL X10, X10, # 3    /* Scale the core ID to the size of a pointer (64-bit system) */
      ADD X8, X8, X10      /* Add the offset for the current core's TCB pointer */
   #endif
   LDR X9, [ X8 ]
   MRS X8, SP_EL0
   STR X8, [ X9 ]         /* Store pxTopOfStack on task's TCB */
   ADD X9, X9, #8         /* X9 = X9 + 8. X1 now points to ullTaskUnprivilegedSP in TCB. */
   LDR X9, [ X9 ]
   MSR SP_EL0, X9        /* Use ullTaskUnprivilegedSP as SP_EL0. */
   LDR X10, [ SP ], # 0x10
   LDP X8, X9, [ SP ], # 0x10
#endif /* #if ( configENABLE_MPU == 1 ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 74: 代码片段 74

```asm
   /* Switch to use the EL1 stack pointer. */
   MSR SPSEL, # 1
   .endm
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 75: 说明性注释

```asm
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。

## 片段 76: 汇编标签 FreeRTOS_SWI_Handler

```asm
/******************************************************************************
 * FreeRTOS_SWI_Handler handler is used to perform a context switch.
 *****************************************************************************/
   .align 8
   .type FreeRTOS_SWI_Handler, % function
FreeRTOS_SWI_Handler:
/* Save X0-X5 temporarily as they are used in the handler. */
STP X0, X1, [SP, #-0x10]!
STP X2, X3, [SP, #-0x10]!
STP X4, X5, [SP, #-0x10]!
```

**解说：** 这一段是汇编标签 `FreeRTOS_SWI_Handler` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 77: 代码片段 77

```asm
MRS X4, ELR_EL1  /* Save exception return address. */
MRS X5, SPSR_EL1 /* Save program status register address. */
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 78: 代码片段 78

```asm
/* Decide action based on SVC immediate without corrupting any task context. */
MRS X0, ESR_EL1
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 79: 代码片段 79

```asm
/* Extract exception class. */
LSR X1, X0, # 26
CMP X1, # 0x15             /* 0x15 = SVC instruction. */
B.NE FreeRTOS_Abort
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 80: 代码片段 80

```asm
/* Extract SVC immediate from ISS[15:0]. */
AND X2, X0, # 0xFFFF
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 81: 代码片段 81

```asm
/* portSVC_YIELD: yield from a running task. */
CMP X2, # portSVC_YIELD
B.EQ FreeRTOS_Yield
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 82: 代码片段 82

```asm
/* portSVC_START_FIRST_TASK: start first task on this core without saving any prior context. */
CMP X2, # portSVC_START_FIRST_TASK
B.EQ Start_First_Task
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 83: 代码片段 83

```asm
1:
/* portSVC_DISABLE_INTERRUPTS: disable IRQs (DAIF.I) in SPSR_EL1 without touching task context. */
CMP X2, # portSVC_DISABLE_INTERRUPTS
B.NE 2f
ORR X5, X5, # (1 << portPSTATE_I_BIT) /* Set I bit in SPSR_EL1 */
MSR ELR_EL1, X4
MSR SPSR_EL1, X5
LDP X4, X5, [SP], #0x10
LDP X2, X3, [SP], #0x10
LDP X0, X1, [SP], #0x10
DSB SY
ISB SY
ERET
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 84: 代码片段 84

```asm
2:
/* portSVC_ENABLE_INTERRUPTS: enable IRQs (DAIF.I clear) in SPSR_EL1 without touching task context. */
CMP X2, # portSVC_ENABLE_INTERRUPTS
B.NE 3f
BIC X5, X5, # (1 << portPSTATE_I_BIT) /* Clear I bit in SPSR_EL1 */
MSR ELR_EL1, X4
MSR SPSR_EL1, X5
LDP X4, X5, [SP], #0x10
LDP X2, X3, [SP], #0x10
LDP X0, X1, [SP], #0x10
ERET
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 85: 代码片段 85

```asm
3:
/* portSVC_GET_CORE_ID: return core ID in X0 (Aff0 of MPIDR_EL1). */
CMP X2, # portSVC_GET_CORE_ID
B.NE 4f
MRS X0, MPIDR_EL1
AND X0, X0, # 0xff
MSR SPSR_EL1, X5
/* Restore X5-X1 while discarding old X0. */
LDP X4, X5, [SP], #0x10
LDP X2, X3, [ SP ], # 0x10
LDP XZR, X1, [ SP ], # 0x10
ERET
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 86: 代码片段 86

```asm
4:
/* portSVC_MASK_ALL_INTERRUPTS: set ICC_PMR_EL1 to max API mask and return previous-mask-equal flag in X0. */
CMP X2, # portSVC_MASK_ALL_INTERRUPTS
B.NE 5f
/* Read current PMR and compare. */
MRS X0, ICC_PMR_EL1
CMP X0, # portMAX_API_PRIORITY_MASK
B.EQ 41f
/* Disable IRQs while updating PMR. */
MSR DAIFSET, # 2
DSB SY
ISB SY
/* Write new PMR value. */
MOV X1, # portMAX_API_PRIORITY_MASK
MSR ICC_PMR_EL1, X1
DSB SY
ISB SY
/* Re-enable IRQs. */
MSR DAIFCLR, # 2
DSB SY
ISB SY
MSR ELR_EL1, X4
MSR SPSR_EL1, X5
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 87: 代码片段 87

```asm
41:
/* Restore X5-X1 while discarding old X0. */
LDP X4, X5, [ SP ], # 0x10
LDP X2, X3, [ SP ], # 0x10
LDP XZR, X1, [ SP ], # 0x10
ERET
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 88: 代码片段 88

```asm
5:
/* portSVC_UNMASK_ALL_INTERRUPTS: set ICC_PMR_EL1 to portUNMASK_VALUE to unmask all interrupts. */
CMP X2, # portSVC_UNMASK_ALL_INTERRUPTS
B.NE 6f
/* Disable IRQs while updating PMR. */
MSR DAIFSET, # 2
DSB SY
ISB SY
MOV X0, #portUNMASK_VALUE             /* Unmask all interrupts. */
MSR ICC_PMR_EL1, X0
DSB SY
ISB SY
/* Re-enable IRQs. */
MSR DAIFCLR, # 2
DSB SY
ISB SY
MSR ELR_EL1, X4
MSR SPSR_EL1, X5
LDP X4, X5, [SP], #0x10
LDP X2, X3, [SP], #0x10
LDP X0, X1, [SP], #0x10
ERET
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 89: 代码片段 89

```asm
6:
/* portSVC_UNMASK_INTERRUPTS: set ICC_PMR_EL1 to uxNewMaskValue stored in X0. */
CMP X2, # portSVC_UNMASK_INTERRUPTS
B.NE 7f
/* Disable IRQs while updating PMR. */
MSR DAIFSET, # 2
DSB SY
ISB SY
LDR X0, [ SP, # 0x20 ]                    /* Original X0 */
MSR ICC_PMR_EL1, X0
DSB SY
ISB SY
/* Re-enable IRQs. */
MSR DAIFCLR, # 2
DSB SY
ISB SY
MSR ELR_EL1, X4
MSR SPSR_EL1, X5
LDP X4, X5, [SP], #0x10
LDP X2, X3, [SP], #0x10
LDP X0, X1, [SP], #0x10
ERET
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 90: 代码片段 90

```asm
7:
#if ( configENABLE_MPU == 1 )
   /* portSVC_CHECK_PRIVILEGE: Check if the task is a privileged task */
   CMP X2, # portSVC_CHECK_PRIVILEGE
   B.NE 8f
   savefuncontextgpregs
   BL xPortIsTaskPrivileged
   restorefuncontextgpregexceptx0 /* xPortIsTaskPrivileged() return value is stored in X0. */
   MSR ELR_EL1, X4
   MSR SPSR_EL1, X5
   /* Restore X5-X1 while discarding old X0. */
   LDP X4, X5, [ SP ], # 0x10
   LDP X2, X3, [ SP ], # 0x10
   LDP XZR, X1, [ SP ], # 0x10
   ERET
#endif /* #if ( configENABLE_MPU == 1 ) */
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 91: 代码片段 91

```asm
8:
/* portSVC_SAVE_TASK_CONTEXT: Save task's context */
CMP X2, # portSVC_SAVE_TASK_CONTEXT
B.NE 9f
MSR ELR_EL1, X4
MSR SPSR_EL1, X5
/* Restore X5-X0. */
LDP X4, X5, [ SP ], # 0x10
LDP X2, X3, [ SP ], # 0x10
LDP X0, X1, [ SP ], # 0x10
portSAVE_CONTEXT
ERET
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 92: 代码片段 92

```asm
9:
/* portSVC_RESTORE_CONTEXT: Restore task's context */
CMP X2, # portSVC_RESTORE_CONTEXT
B.NE 10f
MSR ELR_EL1, X4
MSR SPSR_EL1, X5
/* Restore X5-X0. */
LDP X4, X5, [ SP ], # 0x10
LDP X2, X3, [ SP ], # 0x10
LDP X0, X1, [ SP ], # 0x10
portRESTORE_CONTEXT
ERET
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 93: 代码片段 93

```asm
10:
/* portSVC_DELETE_CURRENT_TASK: Delete current task */
CMP X2, # portSVC_DELETE_CURRENT_TASK
B.NE 11f
/* Restore X5-X0. */
LDP X4, X5, [ SP ], #0x10
LDP X2, X3, [ SP ], # 0x10
LDP X0, X1, [ SP ], # 0x10
#if ( configNUMBER_OF_CORES == 1 )
   adrp    X0, pxCurrentTCB
   add     X0, X0, :lo12:pxCurrentTCB   /* X0 = &pxCurrentTCB */
#else
   adrp    X0, pxCurrentTCBs
   add     X0, X0, :lo12:pxCurrentTCBs  /* X0 = &pxCurrentTCBs */
   /* Get the core ID to index the TCB correctly. */
   MRS X1, MPIDR_EL1  /* Read the Multiprocessor Affinity Register */
   AND X1, X1, # 0xff /* Extract Aff0 which contains the core ID */
   LSL X1, X1, # 3    /* Scale the core ID to the size of a pointer (64-bit system) */
   ADD X0, X0, X1     /* Add the offset for the current core's TCB pointer */
#endif
LDR X0, [ X0 ] /* X0 = pxCurrentTCB */
B vTaskDelete
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 94: 代码片段 94

```asm
11:
/* portSVC_INTERRUPT_CORE: Interrupt core */
CMP X2, # portSVC_INTERRUPT_CORE
B.NE 12f
LDR X0, [ SP, # 0x20 ]                    /* Original X0 */
MSR ICC_SGI1R_EL1, X0                     /* X0 contains the value to write to ICC_SGI1R_EL1 */
MSR ELR_EL1, X4
MSR SPSR_EL1, X5
/* Restore X5-X0. */
LDP X4, X5, [SP], #0x10
LDP X2, X3, [ SP ], # 0x10
LDP X0, X1, [ SP ], # 0x10
ERET
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 95: 代码片段 95

```asm
12:
#if ( configENABLE_MPU == 1 )
   /* ---------- SystemCallEnter? ---------------------------------*/
   LDR     X3, =NUM_SYSTEM_CALLS
   CMP     X2, X3
   BLO     121f                          /* imm 0 … NUM_SYSCALLS-1 */
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 96: 代码片段 96

```asm
   /* ---------- SystemCallExit? ----------------------------------*/
   LDR     X3, =portSVC_SYSTEM_CALL_EXIT
   CMP     X2, X3
   BEQ     122f
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 97: 代码片段 97

```asm
/* ---------- SystemCallEnter -------------------------------------*/
121:
   /* If calling task is privileged, directly tail-call the implementation at EL1. */
   savefuncontextgpregs
   BL xPortIsTaskPrivileged
   restorefuncontextgpregexceptx0         /* X0 holds pdTRUE if privileged */
   CBNZ X0, priv_path
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 98: 预处理配置

```asm
   /* Unprivileged tasks path */
   #if ( configNUMBER_OF_CORES == 1 )
      adrp    X0, pxCurrentTCB
      add     X0, X0, :lo12:pxCurrentTCB   /* X0 = &pxCurrentTCB */
   #else
      adrp    X0, pxCurrentTCBs
      add     X0, X0, :lo12:pxCurrentTCBs  /* X0 = &pxCurrentTCBs */
      /* Get the core ID to index the TCB correctly. */
      MRS X1, MPIDR_EL1  /* Read the Multiprocessor Affinity Register */
      AND X1, X1, # 0xff /* Extract Aff0 which contains the core ID */
      LSL X1, X1, # 3    /* Scale the core ID to the size of a pointer (64-bit system) */
      ADD X0, X0, X1     /* Add the offset for the current core's TCB pointer */
   #endif
   LDR X0, [ X0 ]
   LDR X0, [ X0 ]         /* X0 = Location of saved context in TCB. */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 99: 代码片段 99

```asm
   /* Save inputs (X0-X3) and LR (X30)
    * onto the current task's context to be used by the system call implementation.
    */
   STR X30, [ X0, # ( portOFFSET_TO_LR * 8 ) ]
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 100: 代码片段 100

```asm
   /* Read original X0, X1, X2, and X3 from the EL1 stack without modifying SP, and store.
    * [SP+0x20] -> X0, [SP+0x28] -> X1, [SP+0x10] -> X2, [SP+0x18] -> X3. */
   LDR X1, [ SP, # 0x20 ]                    /* Original X0 */
   STR X1, [ X0, # ( portOFFSET_TO_X0 * 8 ) ]
   LDR X1, [ SP, # 0x28 ]                    /* Original X1 */
   STR X1, [ X0, # ( portOFFSET_TO_X1 * 8 ) ]
   LDR X1, [ SP, # 0x10 ]                    /* Original X2 */
   STR X1, [ X0, # ( portOFFSET_TO_X2 * 8 ) ]
   LDR X1, [ SP, # 0x18 ]                    /* Original X3 */
   STR X1, [ X0, # ( portOFFSET_TO_X3 * 8 ) ]
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 101: 代码片段 101

```asm
   /* Restore X2-X5 to their original values, discard X1 and X0 as they contain system call number
    * and location of task's saved context in TCB.
    */
   MOV X1, X2                                /* Pass system call */
   LDP X4, X5, [ SP ], #0x10
   LDP X2, X3, [ SP ], #0x10
   ADD SP, SP, #0x10                         /* Discard X0 and X1 */
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 102: 代码片段 102

```asm
   savesyscallcontextgpregs
   BL  vSystemCallEnter   /* returns after programming ELR/SPSR/SP_EL0 and args */
   /* Set LR for the syscall implementation to point to vRequestSystemCallExit. */
   adrp    X30, vRequestSystemCallExit
   add     X30, X30, :lo12:vRequestSystemCallExit
   restoresyscallcontextgpregs
   ERET
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 103: 汇编标签 priv_path

```asm
priv_path:
   /* Load implementation address: uxSystemCallImplementations[X2] (64-bit entries). */
   adrp    X3, uxSystemCallImplementations
   add     X3, X3, :lo12:uxSystemCallImplementations
   LSL     X2, X2, #3           /* Multiply index by size of pointer (8 bytes). */
   ADD     X3, X3, X2           /* X3 = &uxSystemCallImplementations[X2] */
   LDR     X3, [ X3 ]           /* X3 = uxSystemCallImplementations[X2] */
   /* Return from exception directly to implementation; preserve original LR and registers. */
   MSR     ELR_EL1, X3
   MSR     SPSR_EL1, X5
   /* Restore X5-X0. */
   LDP     X4, X5, [ SP ], #0x10
   LDP     X2, X3, [ SP ], #0x10
   LDP     X0, X1, [ SP ], #0x10
   ERET
```

**解说：** 这一段是汇编标签 `priv_path` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 104: 代码片段 104

```asm
   /* ---------- SystemCallExit -----------------------------------*/
122:
   LDR     X0, [ SP, # 0x20 ]    /* Restore X0 without changing SP as it contains system call return value */
   savefuncontextgpregs
   BL      vSystemCallExit
   restorefuncontextgpregexceptx0
   /* Restore X5-X1 while discarding old X0. */
   LDP     X4, X5, [ SP ], #0x10
   LDP     X2, X3, [ SP ], #0x10
   LDP     XZR, X1, [ SP ], #0x10
   ERET
#endif /* #if ( configENABLE_MPU == 1 ) */
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 105: 汇编标签 FreeRTOS_Abort

```asm
/* ---------- Unexpected EC – just hang in place ---------------------------*/
FreeRTOS_Abort:
B       FreeRTOS_Abort
```

**解说：** 这一段是汇编标签 `FreeRTOS_Abort` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 106: 汇编标签 FreeRTOS_Yield

```asm
FreeRTOS_Yield:
MSR SPSR_EL1, X5
```

**解说：** 这一段是汇编标签 `FreeRTOS_Yield` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 107: 预处理配置

```asm
/* Check if the task is in a critical section by inspecting ullCriticalNesting. */
#if ( configNUMBER_OF_CORES > 1 )
   adrp X0, ullCriticalNestings
   add  X0, X0, :lo12:ullCriticalNestings      /* X0 = &ullCriticalNestings */
   MRS  X1, MPIDR_EL1                          /* Read the Multiprocessor Affinity Register. */
   AND  X1, X1, # 0xff                         /* Extract Aff0 (core ID). */
   LSL  X1, X1, # 3                            /* Multiply core ID by pointer size (8 bytes). */
   ADD  X0, X0, X1                             /* Add offset to base address. */
   LDR  X1, [ X0 ]                             /* Load ullCriticalNesting for this core. */
   CBNZ X1, Skip_Context_Switch                /* Skip context switch if in a critical section. */
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 108: 代码片段 108

```asm
/* Restore X5-X0 to their original values before saving full context. */
LDP X4, X5, [SP], #0x10
LDP X2, X3, [SP], #0x10
LDP X0, X1, [SP], #0x10
portSAVE_CONTEXT
savefuncontextgpregs
#if ( configNUMBER_OF_CORES > 1 )
   MRS x0, mpidr_el1
   AND x0, x0, 255
#endif
BL vTaskSwitchContext
restorefuncontextgpregs
portRESTORE_CONTEXT
ERET
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 109: 汇编标签 Skip_Context_Switch

```asm
Skip_Context_Switch:
/* Restore X5-X0 to their original values. */
LDP X4, X5, [SP], #0x10
LDP X2, X3, [SP], #0x10
LDP X0, X1, [SP], #0x10
ERET
```

**解说：** 这一段是汇编标签 `Skip_Context_Switch` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 110: 汇编标签 Start_First_Task

```asm
Start_First_Task:
   /* Restore X5-X0 to their original values. */
   LDP X4, X5, [SP], #0x10
   LDP X2, X3, [SP], #0x10
   LDP X0, X1, [SP], #0x10
   portRESTORE_CONTEXT
   ERET
```

**解说：** 这一段是汇编标签 `Start_First_Task` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 111: 汇编标签 vPortSaveTaskContext

```asm
/******************************************************************************
 * vPortSaveTaskContext is used to save the task's context into its stack.
 *****************************************************************************/
   .align 8
   .type vPortSaveTaskContext, % function
vPortSaveTaskContext:
portSAVE_CONTEXT
RET
```

**解说：** 这一段是汇编标签 `vPortSaveTaskContext` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 112: 汇编标签 vPortRestoreTaskContext

```asm
/******************************************************************************
 * vPortRestoreTaskContext is used to start the scheduler.
 *****************************************************************************/
   .align 8
   .type vPortRestoreTaskContext, % function
vPortRestoreTaskContext:
.set freertos_vector_base, _freertos_vector_table
/* Install the FreeRTOS interrupt handlers. */
LDR X1, = freertos_vector_base
MSR VBAR_EL1, X1
DSB SY
ISB SY
/* Start the first task. */
portRESTORE_CONTEXT
ERET
```

**解说：** 这一段是汇编标签 `vPortRestoreTaskContext` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 113: 汇编标签 FreeRTOS_IRQ_Handler

```asm
/******************************************************************************
 * FreeRTOS_IRQ_Handler handles IRQ entry and exit.
 *
 * This handler is supposed to be used only for IRQs and never for FIQs. Per ARM
 * GIC documentation [1], Group 0 interrupts are always signaled as FIQs. Since
 * this handler is only for IRQs, We can safely assume Group 1 while accessing
 * Interrupt Acknowledge and End Of Interrupt registers and therefore, use
 * ICC_IAR1_EL1 and ICC_EOIR1_EL1.
 *
 * [1] https://developer.arm.com/documentation/198123/0300/Arm-CoreLink-GIC-fundamentals
 *****************************************************************************/
   .align 8
   .type FreeRTOS_IRQ_Handler, % function
FreeRTOS_IRQ_Handler:
/* Save volatile registers. */
saveallgpregisters
savefloatregisters
```

**解说：** 这一段是汇编标签 `FreeRTOS_IRQ_Handler` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 114: 代码片段 114

```asm
/* Save the SPSR and ELR. */
MRS X3, SPSR_EL1
MRS X2, ELR_EL1
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 115: 代码片段 115

```asm
STP X2, X3, [ SP, # - 0x10 ] !
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 116: 预处理配置

```asm
/* Increment the interrupt nesting counter. */
#if ( configNUMBER_OF_CORES == 1 )
   adrp    X5, ullPortInterruptNesting
   add     X5, X5, :lo12:ullPortInterruptNesting   /* X5 = &ullPortInterruptNesting */
#else
   adrp    X5, ullPortInterruptNestings
   add     X5, X5, :lo12:ullPortInterruptNestings  /* X5 = &ullPortInterruptNestings */
   MRS X2, MPIDR_EL1  /* Read Multiprocessor Affinity Register. */
   AND X2, X2, # 0xff /* Extract Aff0, which contains the core ID. */
   LSL X2, X2, # 3    /* Scale core ID to the size of a pointer (assuming 64-bit system). */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 117: 代码片段 117

```asm
   /* Calculate offset for the current core's ullPortYieldRequired and load its address. */
   ADD X5, X5, X2     /* Add offset for the current core's ullPortYieldRequired. */
#endif
LDR X1, [ X5 ]     /* Old nesting count in X1. */
ADD X6, X1, # 1
STR X6, [ X5 ]     /* Address of nesting count variable in X5. */
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 118: 代码片段 118

```asm
/* Maintain the interrupt nesting information across the function call. */
STP X1, X5, [ SP, # - 0x10 ] !
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 119: 代码片段 119

```asm
/* Read interrupt ID from the interrupt acknowledge register and store it
 * in X0 for future parameter and interrupt clearing use. */
MRS X0, ICC_IAR1_EL1
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 120: 代码片段 120

```asm
/* Maintain the interrupt ID value across the function call. */
STP X0, X1, [ SP, # - 0x10 ] !
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 121: 代码片段 121

```asm
savefuncontextgpregs
/* Call the C handler. */
BL vApplicationIRQHandler
restorefuncontextgpregs
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 122: 代码片段 122

```asm
/* Disable interrupts. */
MSR DAIFSET, # 2
DSB SY
ISB SY
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 123: 代码片段 123

```asm
/* Restore the interrupt ID value. */
LDP X0, X1, [ SP ], # 0x10
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 124: 代码片段 124

```asm
/* End IRQ processing by writing interrupt ID value to the EOI register. */
MSR ICC_EOIR1_EL1, X0
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 125: 代码片段 125

```asm
/* Restore the critical nesting count. */
LDP X1, X5, [ SP ], # 0x10
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 126: 代码片段 126

```asm
STR X1, [ X5 ]
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 127: 代码片段 127

```asm
/* Has interrupt nesting unwound? */
CMP X1, # 0
B.NE Exit_IRQ_No_Context_Switch
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 128: 代码片段 128

```asm
/* Is a context switch required? */
adrp    X0, ullPortYieldRequired
add     X0, X0, :lo12:ullPortYieldRequired  /* X0 = &ullPortYieldRequired */
#if ( configNUMBER_OF_CORES > 1 )
   MRS X2, MPIDR_EL1  /* Read Multiprocessor Affinity Register. */
   AND X2, X2, # 0xff /* Extract Aff0, which contains the core ID. */
   LSL X2, X2, # 3    /* Scale core ID to the size of a pointer (assuming 64-bit system). */
/* Calculate offset for the current core's ullPortYieldRequired and load its address. */
   ADD X0, X0, X2     /* Add offset for the current core's ullPortYieldRequired. */
#endif
LDR X1, [ X0 ]
CMP X1, # 0
B.EQ Exit_IRQ_No_Context_Switch
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 129: 预处理配置

```asm
/* Check if the task is in a critical section by inspecting ullCriticalNesting. */
#if ( configNUMBER_OF_CORES > 1 )
   adrp X0, ullCriticalNestings
   add  X0, X0, :lo12:ullCriticalNestings      /* X0 = &ullCriticalNestings */
   MRS  X1, MPIDR_EL1                          /* Read the Multiprocessor Affinity Register. */
   AND  X1, X1, # 0xff                         /* Extract Aff0 (core ID). */
   LSL  X1, X1, # 3                            /* Multiply core ID by pointer size (8 bytes). */
   ADD  X0, X0, X1                             /* Add offset to base address. */
   LDR  X1, [ X0 ]                             /* Load ullCriticalNesting for this core. */
   CBNZ X1, Exit_IRQ_No_Context_Switch         /* Skip context switch if in a critical section. */
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 130: 代码片段 130

```asm
/* Reset ullPortYieldRequired to 0. */
MOV X2, # 0
STR X2, [ X0 ]
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 131: 代码片段 131

```asm
/* Restore volatile registers. */
LDP X4, X5, [ SP ], # 0x10 /* SPSR and ELR. */
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 132: 代码片段 132

```asm
MSR SPSR_EL1, X5
MSR ELR_EL1, X4
DSB SY
ISB SY
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 133: 代码片段 133

```asm
restorefloatregisters
restoreallgpregisters
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 134: 代码片段 134

```asm
/* Save the context of the current task and select a new task to run. */
portSAVE_CONTEXT
#if configNUMBER_OF_CORES > 1
   MRS x0, mpidr_el1
   AND x0, x0, 255
#endif
savefuncontextgpregs
BL vTaskSwitchContext
restorefuncontextgpregs
portRESTORE_CONTEXT
ERET
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 135: 汇编标签 Exit_IRQ_No_Context_Switch

```asm
Exit_IRQ_No_Context_Switch:
/* Restore volatile registers. */
LDP X4, X5, [ SP ], # 0x10 /* SPSR and ELR. */
```

**解说：** 这一段是汇编标签 `Exit_IRQ_No_Context_Switch` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 136: 代码片段 136

```asm
MSR SPSR_EL1, X5
MSR ELR_EL1, X4
DSB SY
ISB SY
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 137: 代码片段 137

```asm
restorefloatregisters
restoreallgpregisters
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 138: 代码片段 138

```asm
ERET
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 139: 说明性注释

```asm
/******************************************************************************
 * If the application provides an implementation of vApplicationIRQHandler(),
 * then it will get called directly without saving the FPU registers on
 * interrupt entry, and this weak implementation of
 * vApplicationIRQHandler() will not get called.
 *
 * If the application provides its own implementation of
 * vApplicationFPUSafeIRQHandler() then this implementation of
 * vApplicationIRQHandler() will be called, save the FPU registers, and then
 * call vApplicationFPUSafeIRQHandler().
 *
 * Therefore, if the application writer wants FPU registers to be saved on
 * interrupt entry their IRQ handler must be called
 * vApplicationFPUSafeIRQHandler(), and if the application writer does not want
 * FPU registers to be saved on interrupt entry their IRQ handler must be
 * called vApplicationIRQHandler().
 *****************************************************************************/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：If the application provides an implementation of vApplicationIRQHandler(), then it will get called directly without saving the FPU registers on interrupt entry, and this weak implementation of vApplicationIRQHandler() will not get called. I。

## 片段 140: 汇编标签 vApplicationIRQHandler

```asm
   .align 8
   .weak vApplicationIRQHandler
   .type vApplicationIRQHandler, % function
vApplicationIRQHandler:
```

**解说：** 这一段是汇编标签 `vApplicationIRQHandler` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 141: 代码片段 141

```asm
/* Save FPU registers (32 128-bits + 2 64-bits configuration and status registers). */
savefloatregisters
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 142: 代码片段 142

```asm
savefuncontextgpregs
/* Call the C handler. */
BL vApplicationFPUSafeIRQHandler
restorefuncontextgpregs
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 143: 代码片段 143

```asm
/* Restore FPU registers. */
restorefloatregisters
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 144: 代码片段 144

```asm
RET
   .end
```

**解说：** 这一段是 `portASM.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。
