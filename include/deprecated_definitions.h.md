# deprecated_definitions.h 代码解说

源文件：`include/deprecated_definitions.h`

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

## 片段 2: 预处理配置 DEPRECATED_DEFINITIONS_H

```c
#ifndef DEPRECATED_DEFINITIONS_H
#define DEPRECATED_DEFINITIONS_H


/* Each FreeRTOS port has a unique portmacro.h header file.  Originally a
 * pre-processor definition was used to ensure the pre-processor found the correct
 * portmacro.h file for the port being used.  That scheme was deprecated in favour
 * of setting the compiler's include path such that it found the correct
 * portmacro.h file - removing the need for the constant and allowing the
 * portmacro.h file to be located anywhere in relation to the port being used.  The
 * definitions below remain in the code for backward compatibility only.  New
 * projects should not use them. */

#ifdef OPEN_WATCOM_INDUSTRIAL_PC_PORT
    #include "..\..\Source\portable\owatcom\16bitdos\pc\portmacro.h"
    typedef void ( __interrupt __far * pxISR )();
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 4: 预处理配置

```c
#ifdef OPEN_WATCOM_FLASH_LITE_186_PORT
    #include "..\..\Source\portable\owatcom\16bitdos\flsh186\portmacro.h"
    typedef void ( __interrupt __far * pxISR )();
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 5: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 6: 预处理配置

```c
#ifdef GCC_MEGA_AVR
    #include "../portable/GCC/ATMega323/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 7: 预处理配置

```c
#ifdef IAR_MEGA_AVR
    #include "../portable/IAR/ATMega323/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 8: 预处理配置

```c
#ifdef MPLAB_PIC24_PORT
    #include "../../Source/portable/MPLAB/PIC24_dsPIC/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 9: 预处理配置

```c
#ifdef MPLAB_DSPIC_PORT
    #include "../../Source/portable/MPLAB/PIC24_dsPIC/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 10: 预处理配置

```c
#ifdef MPLAB_PIC18F_PORT
    #include "../../Source/portable/MPLAB/PIC18F/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 11: 预处理配置

```c
#ifdef MPLAB_PIC32MX_PORT
    #include "../../Source/portable/MPLAB/PIC32MX/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 12: 预处理配置

```c
#ifdef _FEDPICC
    #include "libFreeRTOS/Include/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 13: 预处理配置

```c
#ifdef SDCC_CYGNAL
    #include "../../Source/portable/SDCC/Cygnal/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 14: 预处理配置

```c
#ifdef GCC_ARM7
    #include "../../Source/portable/GCC/ARM7_LPC2000/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 15: 预处理配置

```c
#ifdef GCC_ARM7_ECLIPSE
    #include "portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 16: 预处理配置

```c
#ifdef ROWLEY_LPC23xx
    #include "../../Source/portable/GCC/ARM7_LPC23xx/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 17: 预处理配置

```c
#ifdef IAR_MSP430
    #include "..\..\Source\portable\IAR\MSP430\portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 18: 预处理配置

```c
#ifdef GCC_MSP430
    #include "../../Source/portable/GCC/MSP430F449/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 19: 预处理配置

```c
#ifdef ROWLEY_MSP430
    #include "../../Source/portable/Rowley/MSP430F449/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 20: 预处理配置

```c
#ifdef ARM7_LPC21xx_KEIL_RVDS
    #include "..\..\Source\portable\RVDS\ARM7_LPC21xx\portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 21: 预处理配置

```c
#ifdef SAM7_GCC
    #include "../../Source/portable/GCC/ARM7_AT91SAM7S/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 22: 预处理配置

```c
#ifdef SAM7_IAR
    #include "..\..\Source\portable\IAR\AtmelSAM7S64\portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 23: 预处理配置

```c
#ifdef SAM9XE_IAR
    #include "..\..\Source\portable\IAR\AtmelSAM9XE\portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 24: 预处理配置

```c
#ifdef LPC2000_IAR
    #include "..\..\Source\portable\IAR\LPC2000\portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 25: 预处理配置

```c
#ifdef STR71X_IAR
    #include "..\..\Source\portable\IAR\STR71x\portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 26: 预处理配置

```c
#ifdef STR75X_IAR
    #include "..\..\Source\portable\IAR\STR75x\portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 27: 预处理配置

```c
#ifdef STR75X_GCC
    #include "..\..\Source\portable\GCC\STR75x\portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 28: 预处理配置

```c
#ifdef STR91X_IAR
    #include "..\..\Source\portable\IAR\STR91x\portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 29: 预处理配置

```c
#ifdef GCC_H8S
    #include "../../Source/portable/GCC/H8S2329/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 30: 预处理配置

```c
#ifdef GCC_AT91FR40008
    #include "../../Source/portable/GCC/ARM7_AT91FR40008/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 31: 预处理配置

```c
#ifdef RVDS_ARMCM3_LM3S102
    #include "../../Source/portable/RVDS/ARM_CM3/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 32: 预处理配置

```c
#ifdef GCC_ARMCM3_LM3S102
    #include "../../Source/portable/GCC/ARM_CM3/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 33: 预处理配置

```c
#ifdef GCC_ARMCM3
    #include "../../Source/portable/GCC/ARM_CM3/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 34: 预处理配置

```c
#ifdef IAR_ARM_CM3
    #include "../../Source/portable/IAR/ARM_CM3/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 35: 预处理配置

```c
#ifdef IAR_ARMCM3_LM
    #include "../../Source/portable/IAR/ARM_CM3/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 36: 预处理配置

```c
#ifdef HCS12_CODE_WARRIOR
    #include "../../Source/portable/CodeWarrior/HCS12/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 37: 预处理配置

```c
#ifdef MICROBLAZE_GCC
    #include "../../Source/portable/GCC/MicroBlaze/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 38: 预处理配置

```c
#ifdef TERN_EE
    #include "..\..\Source\portable\Paradigm\Tern_EE\small\portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 39: 预处理配置

```c
#ifdef GCC_HCS12
    #include "../../Source/portable/GCC/HCS12/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 40: 预处理配置

```c
#ifdef GCC_MCF5235
    #include "../../Source/portable/GCC/MCF5235/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 41: 预处理配置

```c
#ifdef COLDFIRE_V2_GCC
    #include "../../../Source/portable/GCC/ColdFire_V2/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 42: 预处理配置

```c
#ifdef COLDFIRE_V2_CODEWARRIOR
    #include "../../Source/portable/CodeWarrior/ColdFire_V2/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 43: 预处理配置

```c
#ifdef GCC_PPC405
    #include "../../Source/portable/GCC/PPC405_Xilinx/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 44: 预处理配置

```c
#ifdef GCC_PPC440
    #include "../../Source/portable/GCC/PPC440_Xilinx/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 45: 预处理配置

```c
#ifdef _16FX_SOFTUNE
    #include "..\..\Source\portable\Softune\MB96340\portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 46: 预处理配置

```c
#ifdef BCC_INDUSTRIAL_PC_PORT

/* A short file name has to be used in place of the normal
 * FreeRTOSConfig.h when using the Borland compiler. */
    #include "frconfig.h"
    #include "..\portable\BCC\16BitDOS\PC\prtmacro.h"
    typedef void ( __interrupt __far * pxISR )();
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 47: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 48: 预处理配置

```c
#ifdef BCC_FLASH_LITE_186_PORT

/* A short file name has to be used in place of the normal
 * FreeRTOSConfig.h when using the Borland compiler. */
    #include "frconfig.h"
    #include "..\portable\BCC\16BitDOS\flsh186\prtmacro.h"
    typedef void ( __interrupt __far * pxISR )();
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 49: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 50: 预处理配置

```c
#ifdef __GNUC__
    #ifdef __AVR32_AVR32A__
        #include "portmacro.h"
    #endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 51: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 52: 预处理配置

```c
#ifdef __ICCAVR32__
    #ifdef __CORE__
        #if __CORE__ == __AVR32A__
            #include "portmacro.h"
        #endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 53: 预处理配置

```c
    #endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 54: 预处理配置

```c
#endif
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 55: 预处理配置

```c
#ifdef __91467D
    #include "portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 56: 预处理配置

```c
#ifdef __96340
    #include "portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 57: 预处理配置

```c
#ifdef __IAR_V850ES_Fx3__
    #include "../../Source/portable/IAR/V850ES/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 58: 预处理配置

```c
#ifdef __IAR_V850ES_Jx3__
    #include "../../Source/portable/IAR/V850ES/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 59: 预处理配置

```c
#ifdef __IAR_V850ES_Jx3_L__
    #include "../../Source/portable/IAR/V850ES/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 60: 预处理配置

```c
#ifdef __IAR_V850ES_Jx2__
    #include "../../Source/portable/IAR/V850ES/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 61: 预处理配置

```c
#ifdef __IAR_V850ES_Hx2__
    #include "../../Source/portable/IAR/V850ES/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 62: 预处理配置

```c
#ifdef __IAR_78K0R_Kx3__
    #include "../../Source/portable/IAR/78K0R/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 63: 预处理配置

```c
#ifdef __IAR_78K0R_Kx3L__
    #include "../../Source/portable/IAR/78K0R/portmacro.h"
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 64: 预处理配置

```c
#endif /* DEPRECATED_DEFINITIONS_H */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。
