# portasm.S 代码解说

源文件：`portable/GCC/PPC405_Xilinx/portasm.S`

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
#include "FreeRTOSConfig.h"
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 代码片段 3

```asm
    .extern pxCurrentTCB
    .extern vTaskSwitchContext
    .extern xTaskIncrementTick
    .extern vPortISRHandler
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 4: 代码片段 4

```asm
    .global vPortStartFirstTask
    .global vPortYield
    .global vPortTickISR
    .global vPortISRWrapper
    .global vPortSaveFPURegisters
    .global vPortRestoreFPURegisters
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 5: 代码片段 5

```asm
.set    BChainField, 0
.set    NextLRField, BChainField + 4
.set    MSRField,    NextLRField + 4
.set    PCField,     MSRField    + 4
.set    LRField,     PCField     + 4
.set    CTRField,    LRField     + 4
.set    XERField,    CTRField    + 4
.set    CRField,     XERField    + 4
.set    USPRG0Field, CRField     + 4
.set    r0Field,     USPRG0Field + 4
.set    r2Field,     r0Field     + 4
.set    r3r31Field,  r2Field     + 4
.set    IFrameSize,  r3r31Field  + ( ( 31 - 3 ) + 1 ) * 4
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 6: 代码片段 6

```asm

.macro portSAVE_STACK_POINTER_AND_LR
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 7: 代码片段 7

```asm
    /* Get the address of the TCB. */
    xor     R0, R0, R0
    addis   R2, R0, pxCurrentTCB@ha
    lwz     R2, pxCurrentTCB@l( R2 )
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 8: 代码片段 8

```asm
    /* Store the stack pointer into the TCB */
    stw     SP, 0( R2 )
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 9: 代码片段 9

```asm
    /* Save the link register */
    stwu    R1, -24( R1 )
    mflr    R0
    stw     R31, 20( R1 )
    stw     R0, 28( R1 )
    mr      R31, r1
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 10: 代码片段 10

```asm
.endm
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 11: 代码片段 11

```asm
.macro portRESTORE_STACK_POINTER_AND_LR
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 12: 代码片段 12

```asm
    /* Restore the link register */
    lwz     R11, 0( R1 )
    lwz     R0, 4( R11 )
    mtlr    R0
    lwz     R31, -4( R11 )
    mr      R1, R11
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 13: 代码片段 13

```asm
    /* Get the address of the TCB. */
    xor     R0, R0, R0
    addis   SP, R0, pxCurrentTCB@ha
    lwz     SP, pxCurrentTCB@l( R1 )
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 14: 代码片段 14

```asm
    /* Get the task stack pointer from the TCB. */
    lwz     SP, 0( SP )
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 15: 代码片段 15

```asm
.endm
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 16: 汇编标签 vPortStartFirstTask

```asm

vPortStartFirstTask:
```

**解说：** 这一段是汇编标签 `vPortStartFirstTask` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 17: 代码片段 17

```asm
    /* Get the address of the TCB. */
    xor     R0, R0, R0
    addis   SP, R0, pxCurrentTCB@ha
    lwz     SP, pxCurrentTCB@l( SP )
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 18: 代码片段 18

```asm
    /* Get the task stack pointer from the TCB. */
    lwz     SP, 0( SP )
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 19: 代码片段 19

```asm
    /* Restore MSR register to SRR1. */
    lwz     R0, MSRField(R1)
    mtsrr1  R0
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 20: 代码片段 20

```asm
    /* Restore current PC location to SRR0. */
    lwz     R0, PCField(R1)
    mtsrr0  R0
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 21: 代码片段 21

```asm
    /* Save  USPRG0 register */
    lwz     R0, USPRG0Field(R1)
    mtspr   0x100,R0
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 22: 代码片段 22

```asm
    /* Restore Condition register */
    lwz     R0, CRField(R1)
    mtcr    R0
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 23: 代码片段 23

```asm
    /* Restore Fixed Point Exception register */
    lwz     R0, XERField(R1)
    mtxer   R0
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 24: 代码片段 24

```asm
    /* Restore Counter register */
    lwz     R0, CTRField(R1)
    mtctr   R0
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 25: 代码片段 25

```asm
    /* Restore Link register */
    lwz     R0, LRField(R1)
    mtlr    R0
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 26: 代码片段 26

```asm
    /* Restore remaining GPR registers. */
    lmw R3,r3r31Field(R1)
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 27: 代码片段 27

```asm
    /* Restore r0 and r2. */
    lwz     R0, r0Field(R1)
    lwz     R2, r2Field(R1)
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 28: 代码片段 28

```asm
    /* Remove frame from stack */
    addi    R1,R1,IFrameSize
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 29: 代码片段 29

```asm
    /* Return into the first task */
    rfi
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 31: 汇编标签 vPortYield

```asm
vPortYield:
```

**解说：** 这一段是汇编标签 `vPortYield` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 32: 代码片段 32

```asm
    portSAVE_STACK_POINTER_AND_LR
    bl vTaskSwitchContext
    portRESTORE_STACK_POINTER_AND_LR
    blr
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 33: 汇编标签 vPortTickISR

```asm
vPortTickISR:
```

**解说：** 这一段是汇编标签 `vPortTickISR` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 34: 代码片段 34

```asm
    portSAVE_STACK_POINTER_AND_LR
    bl xTaskIncrementTick
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 35: 预处理配置

```asm
    #if configUSE_PREEMPTION == 1
        bl vTaskSwitchContext
    #endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 36: 代码片段 36

```asm
    /* Clear the interrupt */
    lis     R0, 2048
    mttsr   R0
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 37: 代码片段 37

```asm
    portRESTORE_STACK_POINTER_AND_LR
    blr
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 38: 汇编标签 vPortISRWrapper

```asm
vPortISRWrapper:
```

**解说：** 这一段是汇编标签 `vPortISRWrapper` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 39: 代码片段 39

```asm
    portSAVE_STACK_POINTER_AND_LR
    bl vPortISRHandler
    portRESTORE_STACK_POINTER_AND_LR
    blr
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 40: 预处理配置

```asm
#if configUSE_FPU == 1
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 41: 汇编标签 vPortSaveFPURegisters

```asm
vPortSaveFPURegisters:
```

**解说：** 这一段是汇编标签 `vPortSaveFPURegisters` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 42: 代码片段 42

```asm
    /* Enable APU and mark FPU as present. */
    mfmsr   r0
    xor     r30, r30, r30
    oris    r30, r30, 512
    ori     r30, r30, 8192
    or      r0, r0, r30
    mtmsr   r0
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 43: 预处理配置

```asm
#ifdef USE_DP_FPU
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 44: 代码片段 44

```asm
    /* Buffer address is in r3.  Save each flop register into an offset from
    this buffer address. */
    stfd    f0, 0(r3)
    stfd    f1, 8(r3)
    stfd    f2, 16(r3)
    stfd    f3, 24(r3)
    stfd    f4, 32(r3)
    stfd    f5, 40(r3)
    stfd    f6, 48(r3)
    stfd    f7, 56(r3)
    stfd    f8, 64(r3)
    stfd    f9, 72(r3)
    stfd    f10, 80(r3)
    stfd    f11, 88(r3)
    stfd    f12, 96(r3)
    stfd    f13, 104(r3)
    stfd    f14, 112(r3)
    stfd    f15, 120(r3)
    stfd    f16, 128(r3)
    stfd    f17, 136(r3)
    stfd    f18, 144(r3)
    stfd    f19, 152(r3)
    stfd    f20, 160(r3)
    stfd    f21, 168(r3)
    stfd    f22, 176(r3)
    stfd    f23, 184(r3)
    stfd    f24, 192(r3)
    stfd    f25, 200(r3)
    stfd    f26, 208(r3)
    stfd    f27, 216(r3)
    stfd    f28, 224(r3)
    stfd    f29, 232(r3)
    stfd    f30, 240(r3)
    stfd    f31, 248(r3)
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 45: 代码片段 45

```asm
    /* Also save the FPSCR. */
    mffs    f31
    stfs    f31, 256(r3)
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 46: 预处理配置

```asm
#else
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 47: 代码片段 47

```asm
    /* Buffer address is in r3.  Save each flop register into an offset from
    this buffer address. */
    stfs    f0, 0(r3)
    stfs    f1, 4(r3)
    stfs    f2, 8(r3)
    stfs    f3, 12(r3)
    stfs    f4, 16(r3)
    stfs    f5, 20(r3)
    stfs    f6, 24(r3)
    stfs    f7, 28(r3)
    stfs    f8, 32(r3)
    stfs    f9, 36(r3)
    stfs    f10, 40(r3)
    stfs    f11, 44(r3)
    stfs    f12, 48(r3)
    stfs    f13, 52(r3)
    stfs    f14, 56(r3)
    stfs    f15, 60(r3)
    stfs    f16, 64(r3)
    stfs    f17, 68(r3)
    stfs    f18, 72(r3)
    stfs    f19, 76(r3)
    stfs    f20, 80(r3)
    stfs    f21, 84(r3)
    stfs    f22, 88(r3)
    stfs    f23, 92(r3)
    stfs    f24, 96(r3)
    stfs    f25, 100(r3)
    stfs    f26, 104(r3)
    stfs    f27, 108(r3)
    stfs    f28, 112(r3)
    stfs    f29, 116(r3)
    stfs    f30, 120(r3)
    stfs    f31, 124(r3)
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 48: 代码片段 48

```asm
    /* Also save the FPSCR. */
    mffs    f31
    stfs    f31, 128(r3)
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 49: 预处理配置

```asm
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 50: 代码片段 50

```asm
    blr
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 51: 预处理配置

```asm
#endif /* configUSE_FPU. */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 52: 预处理配置

```asm

#if configUSE_FPU == 1
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 53: 汇编标签 vPortRestoreFPURegisters

```asm
vPortRestoreFPURegisters:
```

**解说：** 这一段是汇编标签 `vPortRestoreFPURegisters` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 54: 代码片段 54

```asm
    /* Enable APU and mark FPU as present. */
    mfmsr   r0
    xor     r30, r30, r30
    oris    r30, r30, 512
    ori     r30, r30, 8192
    or      r0, r0, r30
    mtmsr   r0
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 55: 预处理配置

```asm
#ifdef USE_DP_FPU
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 56: 说明性注释

```asm
    /* Buffer address is in r3.  Restore each flop register from an offset
    into this buffer.
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：Buffer address is in r3. Restore each flop register from an offset into this buffer.。

## 片段 57: 代码片段 57

```asm
    First the FPSCR. */
    lfs     f31, 256(r3)
    mtfsf   f31, 7
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 58: 代码片段 58

```asm
    lfd     f0, 0(r3)
    lfd     f1, 8(r3)
    lfd     f2, 16(r3)
    lfd     f3, 24(r3)
    lfd     f4, 32(r3)
    lfd     f5, 40(r3)
    lfd     f6, 48(r3)
    lfd     f7, 56(r3)
    lfd     f8, 64(r3)
    lfd     f9, 72(r3)
    lfd     f10, 80(r3)
    lfd     f11, 88(r3)
    lfd     f12, 96(r3)
    lfd     f13, 104(r3)
    lfd     f14, 112(r3)
    lfd     f15, 120(r3)
    lfd     f16, 128(r3)
    lfd     f17, 136(r3)
    lfd     f18, 144(r3)
    lfd     f19, 152(r3)
    lfd     f20, 160(r3)
    lfd     f21, 168(r3)
    lfd     f22, 176(r3)
    lfd     f23, 184(r3)
    lfd     f24, 192(r3)
    lfd     f25, 200(r3)
    lfd     f26, 208(r3)
    lfd     f27, 216(r3)
    lfd     f28, 224(r3)
    lfd     f29, 232(r3)
    lfd     f30, 240(r3)
    lfd     f31, 248(r3)
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 59: 预处理配置

```asm
#else
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 60: 说明性注释

```asm
    /* Buffer address is in r3.  Restore each flop register from an offset
    into this buffer.
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：Buffer address is in r3. Restore each flop register from an offset into this buffer.。

## 片段 61: 代码片段 61

```asm
    First the FPSCR. */
    lfs     f31, 128(r3)
    mtfsf   f31, 7
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 62: 代码片段 62

```asm
    lfs     f0, 0(r3)
    lfs     f1, 4(r3)
    lfs     f2, 8(r3)
    lfs     f3, 12(r3)
    lfs     f4, 16(r3)
    lfs     f5, 20(r3)
    lfs     f6, 24(r3)
    lfs     f7, 28(r3)
    lfs     f8, 32(r3)
    lfs     f9, 36(r3)
    lfs     f10, 40(r3)
    lfs     f11, 44(r3)
    lfs     f12, 48(r3)
    lfs     f13, 52(r3)
    lfs     f14, 56(r3)
    lfs     f15, 60(r3)
    lfs     f16, 64(r3)
    lfs     f17, 68(r3)
    lfs     f18, 72(r3)
    lfs     f19, 76(r3)
    lfs     f20, 80(r3)
    lfs     f21, 84(r3)
    lfs     f22, 88(r3)
    lfs     f23, 92(r3)
    lfs     f24, 96(r3)
    lfs     f25, 100(r3)
    lfs     f26, 104(r3)
    lfs     f27, 108(r3)
    lfs     f28, 112(r3)
    lfs     f29, 116(r3)
    lfs     f30, 120(r3)
    lfs     f31, 124(r3)
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 63: 预处理配置

```asm
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 64: 代码片段 64

```asm
    blr
```

**解说：** 这一段是 `portasm.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 65: 预处理配置

```asm
#endif /* configUSE_FPU. */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。
