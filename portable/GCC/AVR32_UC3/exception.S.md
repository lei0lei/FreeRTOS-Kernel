# exception.S 代码解说

源文件：`portable/GCC/AVR32_UC3/exception.S`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 文件头和许可证

```asm
/*
 * FreeRTOS Kernel <DEVELOPMENT BRANCH>
 * Copyright (C) 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * SPDX-License-Identifier: MIT AND BSD-3-Clause
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
/*This file is prepared for Doxygen automatic documentation generation.*/
/*! \file *********************************************************************
 *
 * \brief Exception and interrupt vectors.
 *
 * This file maps all events supported by an AVR32UC.
 *
 * - Compiler:           GNU GCC for AVR32
 * - Supported devices:  All AVR32UC devices with an INTC module can be used.
 * - AppNote:
 *
 * \author               Atmel Corporation (Now Microchip):
 *                                        https://www.microchip.com \n
 *                       Support and FAQ: https://www.microchip.com/support/
 *
 ******************************************************************************/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：This file is prepared for Doxygen automatic documentation generation.*/ /*! \file ********************************************************************* \brief Exception and interrupt vectors. This file maps all events supported by an AVR32U。

## 片段 3: 说明性注释

```asm
/*
 * Copyright (c) 2007, Atmel Corporation All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * 3. The name of ATMEL may not be used to endorse or promote products derived
 * from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY ATMEL ``AS IS'' AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE EXPRESSLY AND
 * SPECIFICALLY DISCLAIMED. IN NO EVENT SHALL ATMEL BE LIABLE FOR ANY DIRECT,
 * INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 * THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：Copyright (c) 2007, Atmel Corporation All rights reserved. Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met: 1. Redistributions of source code must。

## 片段 4: 预处理配置

```asm

#include <avr32/io.h>
#include "intc.h"
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 5: 说明性注释

```asm

//! @{
//! \verbatim
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：! @{ ! \verbatim。

## 片段 6: 代码片段 6

```asm

  .section  .exception, "ax", @progbits
```

**解说：** 这一段是 `exception.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 7: 说明性注释

```asm

// Start of Exception Vector Table.
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：Start of Exception Vector Table.。

## 片段 8: 代码片段 8

```asm
  // EVBA must be aligned with a power of two strictly greater than the EVBA-
  // relative offset of the last vector.
  .balign 0x200
```

**解说：** 这一段是 `exception.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 9: 汇编标签 _evba

```asm
  // Export symbol.
  .global _evba
  .type _evba, @function
_evba:
```

**解说：** 这一段是汇编标签 `_evba` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 10: 汇编标签 _handle_Unrecoverable_Exception

```asm
        .org  0x000
        // Unrecoverable Exception.
_handle_Unrecoverable_Exception:
        rjmp $
```

**解说：** 这一段是汇编标签 `_handle_Unrecoverable_Exception` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 11: 汇编标签 _handle_TLB_Multiple_Hit

```asm
        .org  0x004
        // TLB Multiple Hit: UNUSED IN AVR32UC.
_handle_TLB_Multiple_Hit:
        rjmp $
```

**解说：** 这一段是汇编标签 `_handle_TLB_Multiple_Hit` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 12: 汇编标签 _handle_Bus_Error_Data_Fetch

```asm
        .org  0x008
        // Bus Error Data Fetch.
_handle_Bus_Error_Data_Fetch:
        rjmp $
```

**解说：** 这一段是汇编标签 `_handle_Bus_Error_Data_Fetch` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 13: 汇编标签 _handle_Bus_Error_Instruction_Fetch

```asm
        .org  0x00C
         // Bus Error Instruction Fetch.
_handle_Bus_Error_Instruction_Fetch:
        rjmp $
```

**解说：** 这一段是汇编标签 `_handle_Bus_Error_Instruction_Fetch` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 14: 汇编标签 _handle_NMI

```asm
        .org  0x010
        // NMI.
_handle_NMI:
        rjmp $
```

**解说：** 这一段是汇编标签 `_handle_NMI` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 15: 汇编标签 _handle_Instruction_Address

```asm
        .org  0x014
        // Instruction Address.
_handle_Instruction_Address:
        rjmp $
```

**解说：** 这一段是汇编标签 `_handle_Instruction_Address` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 16: 汇编标签 _handle_ITLB_Protection

```asm
        .org  0x018
        // ITLB Protection.
_handle_ITLB_Protection:
        rjmp $
```

**解说：** 这一段是汇编标签 `_handle_ITLB_Protection` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 17: 汇编标签 _handle_Breakpoint

```asm
        .org  0x01C
        // Breakpoint.
_handle_Breakpoint:
        rjmp $
```

**解说：** 这一段是汇编标签 `_handle_Breakpoint` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 18: 汇编标签 _handle_Illegal_Opcode

```asm
        .org  0x020
        // Illegal Opcode.
_handle_Illegal_Opcode:
        rjmp $
```

**解说：** 这一段是汇编标签 `_handle_Illegal_Opcode` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 19: 汇编标签 _handle_Unimplemented_Instruction

```asm
        .org  0x024
        // Unimplemented Instruction.
_handle_Unimplemented_Instruction:
        rjmp $
```

**解说：** 这一段是汇编标签 `_handle_Unimplemented_Instruction` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 20: 汇编标签 _handle_Privilege_Violation

```asm
        .org  0x028
        // Privilege Violation.
_handle_Privilege_Violation:
        rjmp $
```

**解说：** 这一段是汇编标签 `_handle_Privilege_Violation` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 21: 汇编标签 _handle_Floating_Point

```asm
        .org  0x02C
        // Floating-Point: UNUSED IN AVR32UC.
_handle_Floating_Point:
        rjmp $
```

**解说：** 这一段是汇编标签 `_handle_Floating_Point` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 22: 汇编标签 _handle_Coprocessor_Absent

```asm
        .org  0x030
        // Coprocessor Absent: UNUSED IN AVR32UC.
_handle_Coprocessor_Absent:
        rjmp $
```

**解说：** 这一段是汇编标签 `_handle_Coprocessor_Absent` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 23: 汇编标签 _handle_Data_Address_Read

```asm
        .org  0x034
        // Data Address (Read).
_handle_Data_Address_Read:
        rjmp $
```

**解说：** 这一段是汇编标签 `_handle_Data_Address_Read` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 24: 汇编标签 _handle_Data_Address_Write

```asm
        .org  0x038
        // Data Address (Write).
_handle_Data_Address_Write:
        rjmp $
```

**解说：** 这一段是汇编标签 `_handle_Data_Address_Write` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 25: 汇编标签 _handle_DTLB_Protection_Read

```asm
        .org  0x03C
        // DTLB Protection (Read).
_handle_DTLB_Protection_Read:
        rjmp $
```

**解说：** 这一段是汇编标签 `_handle_DTLB_Protection_Read` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 26: 汇编标签 _handle_DTLB_Protection_Write

```asm
        .org  0x040
        // DTLB Protection (Write).
_handle_DTLB_Protection_Write:
        rjmp $
```

**解说：** 这一段是汇编标签 `_handle_DTLB_Protection_Write` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 27: 汇编标签 _handle_DTLB_Modified

```asm
        .org  0x044
        // DTLB Modified: UNUSED IN AVR32UC.
_handle_DTLB_Modified:
        rjmp $
```

**解说：** 这一段是汇编标签 `_handle_DTLB_Modified` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 28: 汇编标签 _handle_ITLB_Miss

```asm
        .org  0x050
        // ITLB Miss: UNUSED IN AVR32UC.
_handle_ITLB_Miss:
        rjmp $
```

**解说：** 这一段是汇编标签 `_handle_ITLB_Miss` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 29: 汇编标签 _handle_DTLB_Miss_Read

```asm
        .org  0x060
        // DTLB Miss (Read): UNUSED IN AVR32UC.
_handle_DTLB_Miss_Read:
        rjmp $
```

**解说：** 这一段是汇编标签 `_handle_DTLB_Miss_Read` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 30: 汇编标签 _handle_DTLB_Miss_Write

```asm
        .org  0x070
        // DTLB Miss (Write): UNUSED IN AVR32UC.
_handle_DTLB_Miss_Write:
        rjmp $
```

**解说：** 这一段是汇编标签 `_handle_DTLB_Miss_Write` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 31: 汇编标签 _handle_Supervisor_Call

```asm
        .org  0x100
        // Supervisor Call.
_handle_Supervisor_Call:
        lda.w   pc, SCALLYield
```

**解说：** 这一段是汇编标签 `_handle_Supervisor_Call` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 32: 说明性注释

```asm

// Interrupt support.
// The interrupt controller must provide the offset address relative to EVBA.
// Important note:
//   All interrupts call a C function named _get_interrupt_handler.
//   This function will read group and interrupt line number to then return in
//   R12 a pointer to a user-provided interrupt handler.
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：Interrupt support. The interrupt controller must provide the offset address relative to EVBA. Important note: All interrupts call a C function named _get_interrupt_handler. This function will read group and interrupt line number to then ret。

## 片段 33: 代码片段 33

```asm
  .balign 4
```

**解说：** 这一段是 `exception.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 34: 汇编标签 _int0

```asm
_int0:
  // R8-R12, LR, PC and SR are automatically pushed onto the system stack by the
  // CPU upon interrupt entry.
#if 1 // B1832: interrupt stack changed to exception stack if exception is detected.
  mfsr    r12, AVR32_SR
  bfextu  r12, r12, AVR32_SR_M0_OFFSET, AVR32_SR_M0_SIZE + AVR32_SR_M1_SIZE + AVR32_SR_M2_SIZE
  cp.w    r12, 0b110
  brlo    _int0_normal
  lddsp   r12, sp[0 * 4]
  stdsp   sp[6 * 4], r12
  lddsp   r12, sp[1 * 4]
  stdsp   sp[7 * 4], r12
  lddsp   r12, sp[3 * 4]
  sub     sp, -6 * 4
  rete
_int0_normal:
#endif
  mov     r12, 0  // Pass the int_lev parameter to the _get_interrupt_handler function.
  call    _get_interrupt_handler
  cp.w    r12, 0  // Get the pointer to the interrupt handler returned by the function.
  movne   pc, r12 // If this was not a spurious interrupt (R12 != NULL), jump to the handler.
  rete            // If this was a spurious interrupt (R12 == NULL), return from event handler.
```

**解说：** 这一段是汇编标签 `_int0` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 35: 汇编标签 _int1

```asm
_int1:
  // R8-R12, LR, PC and SR are automatically pushed onto the system stack by the
  // CPU upon interrupt entry.
#if 1 // B1832: interrupt stack changed to exception stack if exception is detected.
  mfsr    r12, AVR32_SR
  bfextu  r12, r12, AVR32_SR_M0_OFFSET, AVR32_SR_M0_SIZE + AVR32_SR_M1_SIZE + AVR32_SR_M2_SIZE
  cp.w    r12, 0b110
  brlo    _int1_normal
  lddsp   r12, sp[0 * 4]
  stdsp   sp[6 * 4], r12
  lddsp   r12, sp[1 * 4]
  stdsp   sp[7 * 4], r12
  lddsp   r12, sp[3 * 4]
  sub     sp, -6 * 4
  rete
_int1_normal:
#endif
  mov     r12, 1  // Pass the int_lev parameter to the _get_interrupt_handler function.
  call    _get_interrupt_handler
  cp.w    r12, 0  // Get the pointer to the interrupt handler returned by the function.
  movne   pc, r12 // If this was not a spurious interrupt (R12 != NULL), jump to the handler.
  rete            // If this was a spurious interrupt (R12 == NULL), return from event handler.
```

**解说：** 这一段是汇编标签 `_int1` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 36: 汇编标签 _int2

```asm
_int2:
  // R8-R12, LR, PC and SR are automatically pushed onto the system stack by the
  // CPU upon interrupt entry.
#if 1 // B1832: interrupt stack changed to exception stack if exception is detected.
  mfsr    r12, AVR32_SR
  bfextu  r12, r12, AVR32_SR_M0_OFFSET, AVR32_SR_M0_SIZE + AVR32_SR_M1_SIZE + AVR32_SR_M2_SIZE
  cp.w    r12, 0b110
  brlo    _int2_normal
  lddsp   r12, sp[0 * 4]
  stdsp   sp[6 * 4], r12
  lddsp   r12, sp[1 * 4]
  stdsp   sp[7 * 4], r12
  lddsp   r12, sp[3 * 4]
  sub     sp, -6 * 4
  rete
_int2_normal:
#endif
  mov     r12, 2  // Pass the int_lev parameter to the _get_interrupt_handler function.
  call    _get_interrupt_handler
  cp.w    r12, 0  // Get the pointer to the interrupt handler returned by the function.
  movne   pc, r12 // If this was not a spurious interrupt (R12 != NULL), jump to the handler.
  rete            // If this was a spurious interrupt (R12 == NULL), return from event handler.
```

**解说：** 这一段是汇编标签 `_int2` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 37: 汇编标签 _int3

```asm
_int3:
  // R8-R12, LR, PC and SR are automatically pushed onto the system stack by the
  // CPU upon interrupt entry.
#if 1 // B1832: interrupt stack changed to exception stack if exception is detected.
  mfsr    r12, AVR32_SR
  bfextu  r12, r12, AVR32_SR_M0_OFFSET, AVR32_SR_M0_SIZE + AVR32_SR_M1_SIZE + AVR32_SR_M2_SIZE
  cp.w    r12, 0b110
  brlo    _int3_normal
  lddsp   r12, sp[0 * 4]
  stdsp   sp[6 * 4], r12
  lddsp   r12, sp[1 * 4]
  stdsp   sp[7 * 4], r12
  lddsp   r12, sp[3 * 4]
  sub     sp, -6 * 4
  rete
_int3_normal:
#endif
  mov     r12, 3  // Pass the int_lev parameter to the _get_interrupt_handler function.
  call    _get_interrupt_handler
  cp.w    r12, 0  // Get the pointer to the interrupt handler returned by the function.
  movne   pc, r12 // If this was not a spurious interrupt (R12 != NULL), jump to the handler.
  rete            // If this was a spurious interrupt (R12 == NULL), return from event handler.
```

**解说：** 这一段是汇编标签 `_int3` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 38: 说明性注释

```asm

// Constant data area.
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：Constant data area.。

## 片段 39: 代码片段 39

```asm
  .balign 4
```

**解说：** 这一段是 `exception.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 40: 汇编标签 ipr_val

```asm
  // Values to store in the interrupt priority registers for the various interrupt priority levels.
  // The interrupt priority registers contain the interrupt priority level and
  // the EVBA-relative interrupt vector offset.
  .global ipr_val
  .type ipr_val, @object
ipr_val:
  .word (INT0 << AVR32_INTC_IPR0_INTLEV_OFFSET) | (_int0 - _evba),\
        (INT1 << AVR32_INTC_IPR0_INTLEV_OFFSET) | (_int1 - _evba),\
        (INT2 << AVR32_INTC_IPR0_INTLEV_OFFSET) | (_int2 - _evba),\
        (INT3 << AVR32_INTC_IPR0_INTLEV_OFFSET) | (_int3 - _evba)
```

**解说：** 这一段是汇编标签 `ipr_val` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 41: 说明性注释

```asm

//! \endverbatim
//! @}
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：! \endverbatim ! @}。
