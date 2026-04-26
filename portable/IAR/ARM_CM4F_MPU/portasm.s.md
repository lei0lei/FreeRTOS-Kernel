# portasm.s 代码解说

源文件：`portable/IAR/ARM_CM4F_MPU/portasm.s`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 文件头和许可证

```asm
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

## 片段 2: 预处理配置

```asm
/* Including FreeRTOSConfig.h here will cause build errors if the header file
contains code not understood by the assembler - for example the 'extern' keyword.
To avoid errors place any such code inside a #ifdef __ICCARM__/#endif block so
the code is included in C files but excluded by the preprocessor in assembly
files (__ICCARM__ is defined by the IAR C compiler but not by the IAR assembler. */
#include <FreeRTOSConfig.h>
#include <mpu_syscall_numbers.h>
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 代码片段 3

```asm
    RSEG    CODE:CODE(2)
    thumb
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 代码片段 4

```asm
    EXTERN pxCurrentTCB
    EXTERN vTaskSwitchContext
    EXTERN vPortSVCHandler_C
    EXTERN vSystemCallEnter
    EXTERN vSystemCallExit
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 5: 代码片段 5

```asm
    PUBLIC xPortPendSVHandler
    PUBLIC vPortSVCHandler
    PUBLIC vPortStartFirstTask
    PUBLIC vPortEnableVFP
    PUBLIC vPortRestoreContextOfFirstTask
    PUBLIC xIsPrivileged
    PUBLIC vResetPrivilege
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 6: 说明性注释

```asm
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。

## 片段 7: 预处理配置 configUSE_MPU_WRAPPERS_V1

```asm
#ifndef configUSE_MPU_WRAPPERS_V1
    #define configUSE_MPU_WRAPPERS_V1 0
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 8: 预处理配置 configENABLE_ERRATA_837070_WORKAROUND

```asm
/* Errata 837070 workaround must be enabled on Cortex-M7 r0p0
 * and r0p1 cores. */
#ifndef configENABLE_ERRATA_837070_WORKAROUND
    #define configENABLE_ERRATA_837070_WORKAROUND 0
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 9: 宏 portSVC_START_SCHEDULER

```asm
/* These must be in sync with portmacro.h. */
#define portSVC_START_SCHEDULER        100
#define portSVC_SYSTEM_CALL_EXIT       103
/*-----------------------------------------------------------*/
```

**解说：** 这一段定义宏 `portSVC_START_SCHEDULER`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 10: 汇编标签 xPortPendSVHandler

```asm
xPortPendSVHandler:
```

**解说：** 这一段是汇编标签 `xPortPendSVHandler` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 11: 代码片段 11

```asm
    ldr r3, =pxCurrentTCB
    ldr r2, [r3]                           /* r2 = pxCurrentTCB. */
    ldr r1, [r2]                           /* r1 = Location where the context should be saved. */
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 12: 代码片段 12

```asm
    /*------------ Save Context. ----------- */
    mrs r3, control
    mrs r0, psp
    isb
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 13: 代码片段 13

```asm
    add r0, r0, #0x20                      /* Move r0 to location where s0 is saved. */
    tst lr, #0x10
    ittt eq
    vstmiaeq r1!, {s16-s31}                /* Store s16-s31. */
    vldmiaeq r0, {s0-s16}                  /* Copy hardware saved FP context into s0-s16. */
    vstmiaeq r1!, {s0-s16}                 /* Store hardware saved FP context. */
    sub r0, r0, #0x20                      /* Set r0 back to the location of hardware saved context. */
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 14: 代码片段 14

```asm
    stmia r1!, {r3-r11, lr}                /* Store CONTROL register, r4-r11 and LR. */
    ldmia r0, {r4-r11}                     /* Copy hardware saved context into r4-r11. */
    stmia r1!, {r0, r4-r11}                /* Store original PSP (after hardware has saved context) and the hardware saved context. */
    str r1, [r2]                           /* Save the location from where the context should be restored as the first member of TCB. */
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 15: 代码片段 15

```asm
    /*---------- Select next task. --------- */
    mov r0, #configMAX_SYSCALL_INTERRUPT_PRIORITY
#if ( configENABLE_ERRATA_837070_WORKAROUND == 1 )
    cpsid i                                /* ARM Cortex-M7 r0p1 Errata 837070 workaround. */
#endif
    msr basepri, r0
    dsb
    isb
#if ( configENABLE_ERRATA_837070_WORKAROUND == 1 )
    cpsie i                                /* ARM Cortex-M7 r0p1 Errata 837070 workaround. */
#endif
    bl vTaskSwitchContext
    mov r0, #0
    msr basepri, r0
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 16: 代码片段 16

```asm
    /*------------ Program MPU. ------------ */
    ldr r3, =pxCurrentTCB
    ldr r2, [r3]                           /* r2 = pxCurrentTCB. */
    add r2, r2, #4                         /* r2 = Second item in the TCB which is xMPUSettings. */
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 17: 代码片段 17

```asm
    dmb                                    /* Complete outstanding transfers before disabling MPU. */
    ldr r0, =0xe000ed94                    /* MPU_CTRL register. */
    ldr r3, [r0]                           /* Read the value of MPU_CTRL. */
    bic r3, #1                             /* r3 = r3 & ~1 i.e. Clear the bit 0 in r3. */
    str r3, [r0]                           /* Disable MPU. */
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 18: 代码片段 18

```asm
    ldr r0, =0xe000ed9c                    /* Region Base Address register. */
    ldmia r2!, {r4-r11}                    /* Read 4 sets of MPU registers [MPU Region # 0 - 3]. */
    stmia r0, {r4-r11}                     /* Write 4 sets of MPU registers [MPU Region # 0 - 3]. */
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 19: 预处理配置

```asm
#ifdef configTOTAL_MPU_REGIONS
    #if ( configTOTAL_MPU_REGIONS == 16 )
        ldmia r2!, {r4-r11}                 /* Read 4 sets of MPU registers [MPU Region # 4 - 7]. */
        stmia r0, {r4-r11}                  /* Write 4 sets of MPU registers. [MPU Region # 4 - 7]. */
        ldmia r2!, {r4-r11}                 /* Read 4 sets of MPU registers [MPU Region # 8 - 11]. */
        stmia r0, {r4-r11}                  /* Write 4 sets of MPU registers. [MPU Region # 8 - 11]. */
    #endif /* configTOTAL_MPU_REGIONS == 16. */
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 20: 代码片段 20

```asm
    ldr r0, =0xe000ed94                    /* MPU_CTRL register. */
    ldr r3, [r0]                           /* Read the value of MPU_CTRL. */
    orr r3, #1                             /* r3 = r3 | 1 i.e. Set the bit 0 in r3. */
    str r3, [r0]                           /* Enable MPU. */
    dsb                                    /* Force memory writes before continuing. */
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 21: 代码片段 21

```asm
    /*---------- Restore Context. ---------- */
    ldr r3, =pxCurrentTCB
    ldr r2, [r3]                           /* r2 = pxCurrentTCB. */
    ldr r1, [r2]                           /* r1 = Location of saved context in TCB. */
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 22: 代码片段 22

```asm
    ldmdb r1!, {r0, r4-r11}                /* r0 contains PSP after the hardware had saved context. r4-r11 contain hardware saved context. */
    msr psp, r0
    stmia r0!, {r4-r11}                    /* Copy the hardware saved context on the task stack. */
    ldmdb r1!, {r3-r11, lr}                /* r3 contains CONTROL register. r4-r11 and LR restored. */
    msr control, r3
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 23: 代码片段 23

```asm
    tst lr, #0x10
    ittt eq
    vldmdbeq r1!, {s0-s16}                 /* s0-s16 contain hardware saved FP context. */
    vstmiaeq r0!, {s0-s16}                 /* Copy hardware saved FP context on the task stack. */
    vldmdbeq r1!, {s16-s31}                /* Restore s16-s31. */
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 24: 代码片段 24

```asm
    str r1, [r2]                           /* Save the location where the context should be saved next as the first member of TCB. */
    bx lr
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 25: 说明性注释

```asm
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。

## 片段 26: 预处理配置

```asm
#if ( configUSE_MPU_WRAPPERS_V1 == 0 )
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 27: 汇编标签 vPortSVCHandler

```asm
vPortSVCHandler:
    tst lr, #4
    ite eq
    mrseq r0, msp
    mrsne r0, psp
```

**解说：** 这一段是汇编标签 `vPortSVCHandler` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 28: 代码片段 28

```asm
    ldr r1, [r0, #24]
    ldrb r2, [r1, #-2]
    cmp r2, #NUM_SYSTEM_CALLS
    blt syscall_enter
    cmp r2, #portSVC_SYSTEM_CALL_EXIT
    beq syscall_exit
    b vPortSVCHandler_C
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 29: 汇编标签 syscall_enter

```asm
    syscall_enter:
        mov r1, lr
        b vSystemCallEnter
```

**解说：** 这一段是汇编标签 `syscall_enter` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 30: 汇编标签 syscall_exit

```asm
    syscall_exit:
        mov r1, lr
        b vSystemCallExit
```

**解说：** 这一段是汇编标签 `syscall_exit` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 31: 预处理配置

```asm
#else /* #if ( configUSE_MPU_WRAPPERS_V1 == 0 ) */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 32: 汇编标签 vPortSVCHandler

```asm
vPortSVCHandler:
    #ifndef USE_PROCESS_STACK
        tst lr, #4
        ite eq
        mrseq r0, msp
        mrsne r0, psp
    #else
        mrs r0, psp
    #endif
        b vPortSVCHandler_C
```

**解说：** 这一段是汇编标签 `vPortSVCHandler` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 33: 预处理配置

```asm
#endif /* #if ( configUSE_MPU_WRAPPERS_V1 == 0 ) */
/*-----------------------------------------------------------*/
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 34: 汇编标签 vPortStartFirstTask

```asm
vPortStartFirstTask:
    /* Use the NVIC offset register to locate the stack. */
    ldr r0, =0xE000ED08
    ldr r0, [r0]
    ldr r0, [r0]
    /* Set the msp back to the start of the stack. */
    msr msp, r0
    /* Clear the bit that indicates the FPU is in use in case the FPU was used
    before the scheduler was started - which would otherwise result in the
    unnecessary leaving of space in the SVC stack for lazy saving of FPU
    registers. */
    mov r0, #0
    msr control, r0
    /* Call SVC to start the first task. */
    cpsie i
    cpsie f
    dsb
    isb
    svc #portSVC_START_SCHEDULER
```

**解说：** 这一段是汇编标签 `vPortStartFirstTask` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 35: 说明性注释

```asm
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。

## 片段 36: 汇编标签 vPortRestoreContextOfFirstTask

```asm
vPortRestoreContextOfFirstTask:
    ldr r0, =0xE000ED08                    /* Use the NVIC offset register to locate the stack. */
    ldr r0, [r0]
    ldr r0, [r0]
    msr msp, r0                            /* Set the msp back to the start of the stack. */
```

**解说：** 这一段是汇编标签 `vPortRestoreContextOfFirstTask` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 37: 代码片段 37

```asm
    /*------------ Program MPU. ------------ */
    ldr r3, =pxCurrentTCB
    ldr r2, [r3]                           /* r2 = pxCurrentTCB. */
    add r2, r2, #4                         /* r2 = Second item in the TCB which is xMPUSettings. */
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 38: 代码片段 38

```asm
    dmb                                    /* Complete outstanding transfers before disabling MPU. */
    ldr r0, =0xe000ed94                    /* MPU_CTRL register. */
    ldr r3, [r0]                           /* Read the value of MPU_CTRL. */
    bic r3, #1                             /* r3 = r3 & ~1 i.e. Clear the bit 0 in r3. */
    str r3, [r0]                           /* Disable MPU. */
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 39: 代码片段 39

```asm
    ldr r0, =0xe000ed9c                    /* Region Base Address register. */
    ldmia r2!, {r4-r11}                    /* Read 4 sets of MPU registers [MPU Region # 0 - 3]. */
    stmia r0, {r4-r11}                     /* Write 4 sets of MPU registers [MPU Region # 0 - 3]. */
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 40: 预处理配置

```asm
#ifdef configTOTAL_MPU_REGIONS
    #if ( configTOTAL_MPU_REGIONS == 16 )
        ldmia r2!, {r4-r11}                /* Read 4 sets of MPU registers [MPU Region # 4 - 7]. */
        stmia r0, {r4-r11}                 /* Write 4 sets of MPU registers. [MPU Region # 4 - 7]. */
        ldmia r2!, {r4-r11}                /* Read 4 sets of MPU registers [MPU Region # 8 - 11]. */
        stmia r0, {r4-r11}                 /* Write 4 sets of MPU registers. [MPU Region # 8 - 11]. */
    #endif /* configTOTAL_MPU_REGIONS == 16. */
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 41: 代码片段 41

```asm
    ldr r0, =0xe000ed94                    /* MPU_CTRL register. */
    ldr r3, [r0]                           /* Read the value of MPU_CTRL. */
    orr r3, #1                             /* r3 = r3 | 1 i.e. Set the bit 0 in r3. */
    str r3, [r0]                           /* Enable MPU. */
    dsb                                    /* Force memory writes before continuing. */
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 42: 代码片段 42

```asm
    /*---------- Restore Context. ---------- */
    ldr r3, =pxCurrentTCB
    ldr r2, [r3]                           /* r2 = pxCurrentTCB. */
    ldr r1, [r2]                           /* r1 = Location of saved context in TCB. */
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 43: 代码片段 43

```asm
    ldmdb r1!, {r0, r4-r11}                /* r0 contains PSP after the hardware had saved context. r4-r11 contain hardware saved context. */
    msr psp, r0
    stmia r0, {r4-r11}                     /* Copy the hardware saved context on the task stack. */
    ldmdb r1!, {r3-r11, lr}                /* r3 contains CONTROL register. r4-r11 and LR restored. */
    msr control, r3
    str r1, [r2]                           /* Save the location where the context should be saved next as the first member of TCB. */
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 44: 代码片段 44

```asm
    mov r0, #0
    msr basepri, r0
    bx lr
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 45: 说明性注释

```asm
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。

## 片段 46: 汇编标签 vPortEnableVFP

```asm
vPortEnableVFP:
    /* The FPU enable bits are in the CPACR. */
    ldr.w r0, =0xE000ED88
    ldr r1, [r0]
```

**解说：** 这一段是汇编标签 `vPortEnableVFP` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 47: 代码片段 47

```asm
    /* Enable CP10 and CP11 coprocessors, then save back. */
    orr r1, r1, #( 0xf << 20 )
    str r1, [r0]
    bx  r14
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 48: 说明性注释

```asm
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。

## 片段 49: 汇编标签 xIsPrivileged

```asm
xIsPrivileged:
    mrs r0, control     /* r0 = CONTROL. */
    tst r0, #1          /* Perform r0 & 1 (bitwise AND) and update the conditions flag. */
    ite ne
    movne r0, #0        /* CONTROL[0]!=0. Return false to indicate that the processor is not privileged. */
    moveq r0, #1        /* CONTROL[0]==0. Return true to indicate that the processor is privileged. */
    bx lr               /* Return. */
/*-----------------------------------------------------------*/
```

**解说：** 这一段是汇编标签 `xIsPrivileged` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 50: 汇编标签 vResetPrivilege

```asm
vResetPrivilege:
    mrs r0, control     /* r0 = CONTROL. */
    orr r0, r0, #1      /* r0 = r0 | 1. */
    msr control, r0     /* CONTROL = r0. */
    bx lr               /* Return to the caller. */
/*-----------------------------------------------------------*/
```

**解说：** 这一段是汇编标签 `vResetPrivilege` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 51: 代码片段 51

```asm
    END
```

**解说：** 这一段是 `portasm.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。
