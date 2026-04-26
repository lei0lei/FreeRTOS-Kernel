# xtensa_vector_defaults.S 代码解说

源文件：`portable/ThirdParty/GCC/Xtensa_ESP32/xtensa_vector_defaults.S`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 文件头和许可证

```asm
/*
 * SPDX-FileCopyrightText: 2015-2022 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Apache-2.0
 */
```

**解说：** 这一段是文件头，说明项目归属、许可证和免责条款；它告诉使用者这个文件按 MIT 许可证发布。

## 片段 2: 预处理配置

```asm
#include "xtensa_rtos.h"
#include "esp_idf_version.h"
#if (ESP_IDF_VERSION < ESP_IDF_VERSION_VAL(4, 2, 0))
#include "esp_panic.h"
#else
#include "esp_private/panic_reason.h"
#endif /* ESP_IDF_VERSION < ESP_IDF_VERSION_VAL(4, 2, 0) */
#include "sdkconfig.h"
#include "soc/soc.h"
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 说明性注释

```asm
/*
This file contains the default handlers for the high interrupt levels as well as some specialized exceptions.
The default behaviour is to just exit the interrupt or call the panic handler on the exceptions
*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：This file contains the default handlers for the high interrupt levels as well as some specialized exceptions. The default behaviour is to just exit the interrupt or call the panic handler on the exceptions。

## 片段 4: 预处理配置

```asm

#if XCHAL_HAVE_DEBUG
    .global    xt_debugexception
    .weak xt_debugexception
    .set xt_debugexception, _xt_debugexception
    .section .iram1,"ax"
    .type       _xt_debugexception,@function
    .align      4
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 5: 汇编标签 XT_DEBUGCAUSE_DI

```asm
_xt_debugexception:
#if (CONFIG_ESP32_ECO3_CACHE_LOCK_FIX && CONFIG_BTDM_CTRL_HLI)
#define XT_DEBUGCAUSE_DI        (5)
    getcoreid   a0
#if (CONFIG_BTDM_CTRL_PINNED_TO_CORE == PRO_CPU_NUM)
    beqz    a0, 1f
#else
    bnez    a0, 1f
#endif
```

**解说：** 这一段是汇编标签 `XT_DEBUGCAUSE_DI` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 6: 代码片段 6

```asm
    rsr     a0, DEBUGCAUSE
    extui   a0, a0, XT_DEBUGCAUSE_DI, 1
    bnez    a0, _xt_debug_di_exc
1:
#endif //(CONFIG_ESP32_ECO3_CACHE_LOCK_FIX && CONFIG_BTDM_CTRL_HLI)
```

**解说：** 这一段是 `xtensa_vector_defaults.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 7: 代码片段 7

```asm
    movi    a0,PANIC_RSN_DEBUGEXCEPTION
    wsr     a0,EXCCAUSE
    /* _xt_panic assumes a level 1 exception. As we're
       crashing anyhow, copy EPC & EXCSAVE from DEBUGLEVEL
       to level 1. */
    rsr     a0,(EPC + XCHAL_DEBUGLEVEL)
    wsr     a0,EPC_1
    rsr     a0,(EXCSAVE + XCHAL_DEBUGLEVEL)
    wsr     a0,EXCSAVE_1
    call0   _xt_panic                       /* does not return */
    rfi     XCHAL_DEBUGLEVEL
```

**解说：** 这一段计算并返回结果；调用者会根据返回值继续决定后续流程。

## 片段 8: 汇编标签 _xt_debug_di_exc

```asm
#if (CONFIG_ESP32_ECO3_CACHE_LOCK_FIX && CONFIG_BTDM_CTRL_HLI)
    .align  4
_xt_debug_di_exc:
```

**解说：** 这一段是汇编标签 `_xt_debug_di_exc` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 9: 说明性注释

```asm
    /*
    The delay time can be calculated by the following formula:
      T = ceil(0.25 + max(t1, t2)) us
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：The delay time can be calculated by the following formula: T = ceil(0.25 + max(t1, t2)) us。

## 片段 10: 代码片段 10

```asm
      t1 = 80 / f1, t2 = (1 + 14/N) * 20 / f2
```

**解说：** 这一段是 `xtensa_vector_defaults.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 11: 汇编标签 f1

```asm
      f1: PSRAM access frequency, unit: MHz.
      f2: Flash access frequency, unit: MHz.
```

**解说：** 这一段是汇编标签 `f1` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 12: 代码片段 12

```asm
      When flash is slow/fast read, N = 1.
      When flash is DOUT/DIO read, N = 2.
      When flash is QOUT/QIO read, N = 4.
```

**解说：** 这一段是 `xtensa_vector_defaults.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 13: 代码片段 13

```asm
      And after testing, when CPU frequency is 240 MHz, it will take 1us to loop 27 times.
    */
#if defined(CONFIG_ESPTOOLPY_FLASHMODE_QIO) || defined(CONFIG_ESPTOOLPY_FLASHMODE_QOUT)
```

**解说：** 这一段是 `xtensa_vector_defaults.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 14: 预处理配置

```asm
# if defined(CONFIG_ESPTOOLPY_FLASHFREQ_80M) && defined(CONFIG_SPIRAM_SPEED_80M)
    movi    a0, 54
# elif defined(CONFIG_ESPTOOLPY_FLASHFREQ_80M) && defined(CONFIG_SPIRAM_SPEED_40M)
    movi    a0, 81
# elif defined(CONFIG_ESPTOOLPY_FLASHFREQ_40M) && defined(CONFIG_SPIRAM_SPEED_40M)
    movi    a0, 81
# elif defined(CONFIG_ESPTOOLPY_FLASHFREQ_26M) && defined(CONFIG_SPIRAM_SPEED_40M)
    movi    a0, 108
# else
    movi    a0, 135
# endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 15: 预处理配置

```asm
#elif defined(CONFIG_ESPTOOLPY_FLASHMODE_DIO) || defined(CONFIG_ESPTOOLPY_FLASHMODE_DOUT)
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 16: 预处理配置

```asm
# if defined(CONFIG_ESPTOOLPY_FLASHFREQ_80M) && defined(CONFIG_SPIRAM_SPEED_80M)
    movi    a0, 81
# elif defined(CONFIG_ESPTOOLPY_FLASHFREQ_80M) && defined(CONFIG_SPIRAM_SPEED_40M)
    movi    a0, 81
# elif defined(CONFIG_ESPTOOLPY_FLASHFREQ_40M) && defined(CONFIG_SPIRAM_SPEED_40M)
    movi    a0, 135
# elif defined(CONFIG_ESPTOOLPY_FLASHFREQ_26M) && defined(CONFIG_SPIRAM_SPEED_40M)
    movi    a0, 189
# else
    movi    a0, 243
# endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 17: 预处理配置

```asm
#else
    movi    a0, 243
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 18: 代码片段 18

```asm
1:  addi    a0, a0, -1         /* delay_us(N) */
    .rept   4
    nop
    .endr
    bnez    a0, 1b
```

**解说：** 这一段是 `xtensa_vector_defaults.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 19: 代码片段 19

```asm
    rsr     a0, EXCSAVE+XCHAL_DEBUGLEVEL
    rfi     XCHAL_DEBUGLEVEL
#endif //(CONFIG_ESP32_ECO3_CACHE_LOCK_FIX && CONFIG_BTDM_CTRL_HLI)
#endif /* Debug exception */
```

**解说：** 这一段是 `xtensa_vector_defaults.S` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 20: 汇编标签 _xt_highint2

```asm

#if XCHAL_NUM_INTLEVELS >=2 && XCHAL_EXCM_LEVEL <2 && XCHAL_DEBUGLEVEL !=2
    .global    xt_highint2
    .weak xt_highint2
    .set xt_highint2, _xt_highint2
    .section .iram1,"ax"
    .type       _xt_highint2,@function
    .align      4
_xt_highint2:
```

**解说：** 这一段是汇编标签 `_xt_highint2` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 21: 汇编标签 .L_xt_highint2_exit

```asm
    /* Default handler does nothing; just returns */
    .align  4
.L_xt_highint2_exit:
    rsr     a0, EXCSAVE_2                   /* restore a0 */
    rfi     2
```

**解说：** 这一段是汇编标签 `.L_xt_highint2_exit` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 22: 预处理配置

```asm
#endif  /* Level 2 */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 23: 预处理配置

```asm
#if XCHAL_NUM_INTLEVELS >=3 && XCHAL_EXCM_LEVEL <3 && XCHAL_DEBUGLEVEL !=3
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 24: 汇编标签 _xt_highint3

```asm
    .global    xt_highint3
    .weak xt_highint3
    .set xt_highint3, _xt_highint3
    .section .iram1,"ax"
    .type       _xt_highint3,@function
    .align      4
_xt_highint3:
```

**解说：** 这一段是汇编标签 `_xt_highint3` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 25: 说明性注释

```asm
    /* Default handler does nothing; just returns */
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：Default handler does nothing; just returns。

## 片段 26: 汇编标签 .L_xt_highint3_exit

```asm
    .align  4
.L_xt_highint3_exit:
    rsr     a0, EXCSAVE_3                   /* restore a0 */
    rfi     3
```

**解说：** 这一段是汇编标签 `.L_xt_highint3_exit` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 27: 预处理配置

```asm
#endif  /* Level 3 */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 28: 预处理配置

```asm
#if XCHAL_NUM_INTLEVELS >=4 && XCHAL_EXCM_LEVEL <4 && XCHAL_DEBUGLEVEL !=4
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 29: 汇编标签 _xt_highint4

```asm
    .global    xt_highint4
    .weak xt_highint4
    .set xt_highint4, _xt_highint4
    .section .iram1,"ax"
    .type       _xt_highint4,@function
    .align      4
_xt_highint4:
```

**解说：** 这一段是汇编标签 `_xt_highint4` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 30: 说明性注释

```asm
    /* Default handler does nothing; just returns */
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：Default handler does nothing; just returns。

## 片段 31: 汇编标签 .L_xt_highint4_exit

```asm
    .align  4
.L_xt_highint4_exit:
    rsr     a0, EXCSAVE_4                   /* restore a0 */
    rfi     4
```

**解说：** 这一段是汇编标签 `.L_xt_highint4_exit` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 32: 预处理配置

```asm
#endif  /* Level 4 */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 33: 预处理配置

```asm
#if XCHAL_NUM_INTLEVELS >=5 && XCHAL_EXCM_LEVEL <5 && XCHAL_DEBUGLEVEL !=5
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 34: 汇编标签 _xt_highint5

```asm
    .global    xt_highint5
    .weak xt_highint5
    .set xt_highint5, _xt_highint5
    .section .iram1,"ax"
    .type       _xt_highint5,@function
    .align      4
_xt_highint5:
```

**解说：** 这一段是汇编标签 `_xt_highint5` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 35: 说明性注释

```asm
    /* Default handler does nothing; just returns */
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：Default handler does nothing; just returns。

## 片段 36: 汇编标签 .L_xt_highint5_exit

```asm
    .align  4
.L_xt_highint5_exit:
    rsr     a0, EXCSAVE_5                   /* restore a0 */
    rfi     5
```

**解说：** 这一段是汇编标签 `.L_xt_highint5_exit` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 37: 预处理配置

```asm

#endif  /* Level 5 */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 38: 预处理配置

```asm
#if XCHAL_NUM_INTLEVELS >=6 && XCHAL_EXCM_LEVEL <6 && XCHAL_DEBUGLEVEL !=6
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 39: 汇编标签 _xt_highint6

```asm
    .global    _xt_highint6
    .global    xt_highint6
    .weak xt_highint6
    .set xt_highint6, _xt_highint6
    .section .iram1,"ax"
    .type       _xt_highint6,@function
    .align      4
_xt_highint6:
```

**解说：** 这一段是汇编标签 `_xt_highint6` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 40: 说明性注释

```asm
    /* Default handler does nothing; just returns */
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：Default handler does nothing; just returns。

## 片段 41: 汇编标签 .L_xt_highint6_exit

```asm
    .align  4
.L_xt_highint6_exit:
    rsr     a0, EXCSAVE_6                   /* restore a0 */
    rfi     6
```

**解说：** 这一段是汇编标签 `.L_xt_highint6_exit` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 42: 预处理配置

```asm
#endif  /* Level 6 */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 43: 预处理配置

```asm
#if XCHAL_HAVE_NMI
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 44: 汇编标签 _xt_nmi

```asm
    .global    _xt_nmi
    .global    xt_nmi
    .weak xt_nmi
    .set xt_nmi, _xt_nmi
    .section .iram1,"ax"
    .type       _xt_nmi,@function
    .align      4
_xt_nmi:
```

**解说：** 这一段是汇编标签 `_xt_nmi` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 45: 说明性注释

```asm
    /* Default handler does nothing; just returns */
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：Default handler does nothing; just returns。

## 片段 46: 汇编标签 .L_xt_nmi_exit

```asm
    .align  4
.L_xt_nmi_exit:
    rsr     a0, EXCSAVE + XCHAL_NMILEVEL    /* restore a0 */
    rfi     XCHAL_NMILEVEL
```

**解说：** 这一段是汇编标签 `.L_xt_nmi_exit` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。

## 片段 47: 预处理配置

```asm
#endif  /* NMI */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。
