# porthardware.h 代码解说

源文件：`portable/IAR/AVR_Mega0/porthardware.h`

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

## 片段 2: 预处理配置 PORTHARDWARE_H

```c
#ifndef PORTHARDWARE_H
#define PORTHARDWARE_H

#ifndef __IAR_SYSTEMS_ASM__
    #include <ioavr.h>
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 预处理配置 TICK_INT_vect

```c
#include "FreeRTOSConfig.h"

/*-----------------------------------------------------------*/

#if ( configUSE_TIMER_INSTANCE == 0 )

    #define TICK_INT_vect    TCB0_INT_vect
    #define INT_FLAGS        TCB0_INTFLAGS
    #define INT_MASK         TCB_CAPT_bm

    #define TICK_init()                                      \
    {                                                        \
        TCB0.CCMP = configCPU_CLOCK_HZ / configTICK_RATE_HZ; \
        TCB0.INTCTRL = TCB_CAPT_bm;                          \
        TCB0.CTRLA = TCB_ENABLE_bm;                          \
    }
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 4: 预处理配置 TICK_INT_vect

```c
#elif ( configUSE_TIMER_INSTANCE == 1 )

    #define TICK_INT_vect    TCB1_INT_vect
    #define INT_FLAGS        TCB1_INTFLAGS
    #define INT_MASK         TCB_CAPT_bm

    #define TICK_init()                                      \
    {                                                        \
        TCB1.CCMP = configCPU_CLOCK_HZ / configTICK_RATE_HZ; \
        TCB1.INTCTRL = TCB_CAPT_bm;                          \
        TCB1.CTRLA = TCB_ENABLE_bm;                          \
    }
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 5: 预处理配置 TICK_INT_vect

```c
#elif ( configUSE_TIMER_INSTANCE == 2 )

    #define TICK_INT_vect    TCB2_INT_vect
    #define INT_FLAGS        TCB2_INTFLAGS
    #define INT_MASK         TCB_CAPT_bm

    #define TICK_init()                                      \
    {                                                        \
        TCB2.CCMP = configCPU_CLOCK_HZ / configTICK_RATE_HZ; \
        TCB2.INTCTRL = TCB_CAPT_bm;                          \
        TCB2.CTRLA = TCB_ENABLE_bm;                          \
    }
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 6: 预处理配置 TICK_INT_vect

```c
#elif ( configUSE_TIMER_INSTANCE == 3 )

    #define TICK_INT_vect    TCB3_INT_vect
    #define INT_FLAGS        TCB3_INTFLAGS
    #define INT_MASK         TCB_CAPT_bm

    #define TICK_init()                                      \
    {                                                        \
        TCB3.CCMP = configCPU_CLOCK_HZ / configTICK_RATE_HZ; \
        TCB3.INTCTRL = TCB_CAPT_bm;                          \
        TCB3.CTRLA = TCB_ENABLE_bm;                          \
    }
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 7: 预处理配置 TICK_INT_vect

```c
#elif ( configUSE_TIMER_INSTANCE == 4 )

    #define TICK_INT_vect    RTC_CNT_vect
    #define INT_FLAGS        RTC_INTFLAGS
    #define INT_MASK         RTC_OVF_bm

/* Hertz to period for RTC setup */
    #define RTC_PERIOD_HZ( x )    ( 32768 * ( ( 1.0 / x ) ) )
    #define TICK_init()                                        \
    {                                                          \
        while( RTC.STATUS > 0 ) {; }                           \
        RTC.CTRLA = RTC_PRESCALER_DIV1_gc | 1 << RTC_RTCEN_bp; \
        RTC.PER = RTC_PERIOD_HZ( configTICK_RATE_HZ );         \
        RTC.INTCTRL |= 1 << RTC_OVF_bp;                        \
    }
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 8: 预处理配置

```c
#else /* if ( configUSE_TIMER_INSTANCE == 0 ) */
    #undef TICK_INT_vect
    #undef INT_FLAGS
    #undef INT_MASK
    #undef TICK_init()
    #error Invalid timer setting.
#endif /* if ( configUSE_TIMER_INSTANCE == 0 ) */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 9: 预处理配置

```c
/*-----------------------------------------------------------*/
#endif /* PORTHARDWARE_H */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。
