# arc_support.s 代码解说

源文件：`portable/ThirdParty/GCC/ARC_v1/arc_support.s`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 文件头和许可证

```asm
/*
 * FreeRTOS Kernel <DEVELOPMENT BRANCH>
 * Copyright (C) 2020 Synopsys, Inc. or its affiliates.  All Rights Reserved.
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
/**
 * \file
 * \ingroup OS_FREERTOS
 * \brief  freertos support for arc processor
 *  like task dispatcher, interrupt handler
 */
/** @cond OS_FREERTOS_ASM_ARC_SUPPORT */
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：\file \ingroup OS_FREERTOS \brief freertos support for arc processor like task dispatcher, interrupt handler / /** @cond OS_FREERTOS_ASM_ARC_SUPPORT。

## 片段 3: 宏 __ASSEMBLY__

```asm
/*
 * core-dependent part in assemble language (for arc)
 */
#define __ASSEMBLY__
#include "arc/arc.h"
#include "arc/arc_asm_common.h"
```

**解说：** 这一段定义宏 `__ASSEMBLY__`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 4: 汇编标签 dispatch

```asm
/*
 *  task dispatcher
 *
 */
    .text
    .align 4
    .global dispatch
dispatch:
/*
 *  the pre-conditions of this routine are task context, CPU is
 *  locked, dispatch is enabled.
 */
    SAVE_NONSCRATCH_REGS        /* save callee save registers */
    mov r1, dispatch_r
    PUSH    r1          /* save return address */
    ld  r0, [pxCurrentTCB]
    bl  dispatcher
```

**解说：** 这一段是汇编标签 `dispatch` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 5: 汇编标签 dispatch_r

```asm
/* return routine when task dispatch happened in task context */
dispatch_r:
    RESTORE_NONSCRATCH_REGS     /* recover registers */
    j   [blink]
```

**解说：** 这一段是汇编标签 `dispatch_r` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 6: 汇编标签 start_dispatch

```asm
/*
 *  start dispatch
 */
    .global start_dispatch
    .align 4
start_dispatch:
/*
 *  this routine is called in the non-task context during the startup of the kernel
 *  , and all the interrupts are locked.
 *
 *  when the dispatcher is called, the cpu is locked, no nest exception (CPU exception/interrupt).
 *  In target_initialize, all interrupt priority mask should be cleared, cpu should be
 *  locked, the interrupts outside the kernel such as fiq can be
 *  enabled.
 */
    clri
    mov r0, 0
    st  r0, [exc_nest_count]
    b   dispatcher_0
/*
 *  dispatcher
 */
dispatcher:
    ld  r1, [ulCriticalNesting]
    PUSH    r1          /* save critical nesting */
    st  sp, [r0]        /* save stack pointer of current task, r0->pxCurrentTCB */
    jl  vTaskSwitchContext  /* change the value of pxCurrentTCB */
/*
 *  before dispatcher is called, task context | cpu locked | dispatch enabled
 *  should be satisfied. In this routine, the processor will jump
 *  into the entry of next to run task
 *
 *  i.e. kernel mode, IRQ disabled, dispatch enabled
 */
dispatcher_0:
    ld  r1, [pxCurrentTCB]
    ld  sp, [r1]    /* recover task stack */
#if ARC_FEATURE_STACK_CHECK
    lr r0, [AUX_STATUS32]
    bclr r0, r0, AUX_STATUS_BIT_SC
    flag r0
    jl  vPortSetStackCheck
    lr r0, [AUX_STATUS32]
    bset r0, r0, AUX_STATUS_BIT_SC
    flag r0
#endif
    POP r0      /* get critical nesting */
    st  r0, [ulCriticalNesting]
    POP r0      /* get return address  */
    j   [r0]
```

**解说：** 这一段是汇编标签 `start_dispatch` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 7: 汇编标签 start_r

```asm
/*
 *  task startup routine
 *
 */
    .text
    .global start_r
    .align 4
start_r:
    seti    /* unlock cpu */
    mov blink, vPortEndTask /* set return address */
    POP r1          /* get task function body */
    POP r0          /* get task parameters */
    j   [r1]
```

**解说：** 这一段是汇编标签 `start_r` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 8: 汇编标签 exc_entry_cpu

```asm
/****** exceptions and interrupts handing ******/
/****** entry for exception handling ******/
    .global exc_entry_cpu
    .align 4
exc_entry_cpu:
```

**解说：** 这一段是汇编标签 `exc_entry_cpu` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 9: 代码片段 9

```asm
    EXCEPTION_PROLOGUE
```

**解说：** 这一段是 `arc_support.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 10: 代码片段 10

```asm

    mov blink,  sp
    mov r3, sp      /* as exception handler's para(p_excinfo) */
```

**解说：** 这一段是 `arc_support.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 11: 汇编标签 exc_handler_1

```asm
    ld  r1, [exc_nest_count]
    add r1, r1, 1
    st  r1, [exc_nest_count]
    brne    r1, 0, exc_handler_1
/* change to exception stack if interrupt happened in task context */
    mov sp, _e_stack
exc_handler_1:
    PUSH    blink
```

**解说：** 这一段是汇编标签 `exc_handler_1` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 12: 预处理配置

```asm
/* find the exception cause */
#if ARC_FEATURE_CORE_700
    lr  r0, [AUX_ECR]
    lsr r0, r0, 16
    bmsk    r0, r0, 7
#endif
    mov r1, exc_int_handler_table
    ld.as   r2, [r1, r0]
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 13: 代码片段 13

```asm
    mov r0, r3
    jl  [r2]        /* !!!!jump to exception handler where interrupts are not allowed! */
```

**解说：** 这一段是 `arc_support.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 14: 汇编标签 ret_exc

```asm
/* interrupts are not allowed */
ret_exc:
    POP sp
    mov r1, exc_nest_count
    ld  r0, [r1]
    sub r0, r0, 1
    st  r0, [r1]
    brne    r0, 0, ret_exc_1  /* nested exception case */
    lr  r1, [AUX_IRQ_LV12]
    brne    r1, 0, ret_exc_1  /* nested or pending interrupt case */
```

**解说：** 这一段是汇编标签 `ret_exc` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 15: 汇编标签 ret_exc_1

```asm
    ld  r0, [context_switch_reqflg]
    brne    r0, 0, ret_exc_2
ret_exc_1:  /* return from non-task context, interrupts or exceptions are nested */
```

**解说：** 这一段是汇编标签 `ret_exc_1` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 16: 代码片段 16

```asm
    EXCEPTION_EPILOGUE
#if ARC_FEATURE_CORE_600
    rtie ilink2
#else
    rtie
#endif
```

**解说：** 这一段是 `arc_support.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 17: 汇编标签 ret_exc_2

```asm
/* there is a dispatch request */
ret_exc_2:
    /* clear dispatch request */
    mov r0, 0
    st  r0, [context_switch_reqflg]
```

**解说：** 这一段是汇编标签 `ret_exc_2` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 18: 代码片段 18

```asm
    ld  r0, [pxCurrentTCB]
    breq    r0, 0, ret_exc_1
```

**解说：** 这一段是 `arc_support.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 19: 代码片段 19

```asm
    SAVE_CALLEE_REGS    /* save callee save registers */
```

**解说：** 这一段是 `arc_support.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 20: 代码片段 20

```asm
    lr  r0, [AUX_STATUS32]
    bclr    r0, r0, AUX_STATUS_BIT_AE   /* clear exception bit */
    flag    r0
```

**解说：** 这一段是 `arc_support.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 21: 代码片段 21

```asm
    mov r1, ret_exc_r   /* save return address */
    PUSH    r1
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 22: 代码片段 22

```asm
    bl  dispatcher  /* r0->pxCurrentTCB */
```

**解说：** 这一段是 `arc_support.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 23: 汇编标签 ret_exc_r

```asm
ret_exc_r:
    /* recover exception status */
    lr  r0, [AUX_STATUS32]
    bset    r0, r0, AUX_STATUS_BIT_AE
    flag    r0
```

**解说：** 这一段是汇编标签 `ret_exc_r` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 24: 代码片段 24

```asm
    RESTORE_CALLEE_REGS /* recover registers */
    EXCEPTION_EPILOGUE
#if ARC_FEATURE_CORE_600
    rtie ilink2
#else
    rtie
#endif
```

**解说：** 这一段是 `arc_support.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 25: 汇编标签 exc_entry_int

```asm
/****** entry for normal interrupt exception handling ******/
    .global exc_entry_int   /* entry for interrupt handling */
    .align 4
exc_entry_int:
```

**解说：** 这一段是汇编标签 `exc_entry_int` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 26: 代码片段 26

```asm
    INTERRUPT_PROLOGUE
```

**解说：** 这一段是 `arc_support.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 27: 代码片段 27

```asm
    mov blink, sp
```

**解说：** 这一段是 `arc_support.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 28: 代码片段 28

```asm
    /* disable interrupt */
    push r0
    lr  r0, [AUX_STATUS32]
    push r0
    bclr r0, r0, AUX_STATUS_BIT_E1
    bclr r0, r0, AUX_STATUS_BIT_E2
    flag r0
    ld  r3, [exc_nest_count]
    add r2, r3, 1
    st  r2, [exc_nest_count]
    /* enable interrupt */
    pop r0
    flag r0
    pop r0
```

**解说：** 这一段是 `arc_support.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 29: 汇编标签 irq_handler_1

```asm
    brne    r3, 0, irq_handler_1
/* change to exception stack if interrupt happened in task context */
    mov sp, _e_stack
#if ARC_FEATURE_STACK_CHECK
    lr r0, [AUX_STATUS32]
    bclr r0, r0, AUX_STATUS_BIT_SC
    flag r0
#endif
irq_handler_1:
    PUSH    blink
```

**解说：** 这一段是汇编标签 `irq_handler_1` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 30: 汇编标签 irq_hint_handled

```asm
/* critical area */
#if ARC_FEATURE_CORE_700
    lr  r0, [AUX_IRQ_CAUSE1]
#endif
    mov r1, exc_int_handler_table
    ld.as   r2, [r1, r0]    /* r2 = exc_int_handler_table + irqno *4 */
/* handle software triggered interrupt */
    lr  r3, [AUX_IRQ_HINT]
    cmp r3, r0
    bne.d irq_hint_handled
    xor r3, r3, r3
    sr  r3, [AUX_IRQ_HINT]
irq_hint_handled:
```

**解说：** 这一段是汇编标签 `irq_hint_handled` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 31: 汇编标签 ret_int

```asm
    jl  [r2]        /* jump to interrupt handler */
/* no interrupts are allowed from here */
ret_int:
    clri    /* disable interrupt */
```

**解说：** 这一段是汇编标签 `ret_int` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 32: 代码片段 32

```asm
    POP sp
    mov r1, exc_nest_count
    ld  r0, [r1]
    sub r0, r0, 1
    st  r0, [r1]
/* if there are multi-bits set in IRQ_LV12, it's still in nest interrupt */
    lr  r1, [AUX_IRQ_LV12]
```

**解说：** 这一段是 `arc_support.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 33: 汇编标签 ret_int_1

```asm
    ld  r0, [context_switch_reqflg]
    brne    r0, 0, ret_int_2
ret_int_1:  /* return from non-task context */
    INTERRUPT_EPILOGUE
#if ARC_FEATURE_CORE_600
/* TODO: series 600 IRQ6 and IRQ7 uses ilink2 */
    rtie ilink1
#else
    rtie
#endif
/* there is a dispatch request */
ret_int_2:
    /* clear dispatch request */
    mov r0, 0
    st  r0, [context_switch_reqflg]
```

**解说：** 这一段是汇编标签 `ret_int_1` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 34: 代码片段 34

```asm
    ld  r0, [pxCurrentTCB]
    breq    r0, 0, ret_int_1
```

**解说：** 这一段是 `arc_support.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 35: 代码片段 35

```asm
/* r1 has old AUX_IRQ_LV12 */
    PUSH    r1
/* clear related bits in IRQ_ACT manually to simulate a irq return  */
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 36: 代码片段 36

```asm
    SAVE_CALLEE_REGS    /* save callee save registers */
    mov r1, ret_int_r   /* save return address */
    PUSH    r1
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 37: 代码片段 37

```asm
    bl  dispatcher  /* r0->pxCurrentTCB */
```

**解说：** 这一段是 `arc_support.s` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 38: 汇编标签 ret_int_r

```asm
ret_int_r:
    RESTORE_CALLEE_REGS /* recover registers */
    POPAX   AUX_IRQ_LV12
    INTERRUPT_EPILOGUE
#if ARC_FEATURE_CORE_600
    rtie ilink1
#else
    rtie
#endif
```

**解说：** 这一段是汇编标签 `ret_int_r` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 39: 说明性注释

```asm
/** @endcond */
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：@endcond。
