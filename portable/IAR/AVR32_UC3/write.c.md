# write.c 代码解说

源文件：`portable/IAR/AVR32_UC3/write.c`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 文件头和许可证

```c
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

## 片段 2: 预处理配置

```c
/*This file is prepared for Doxygen automatic documentation generation.*/
/*! \file *********************************************************************
*
* \brief System-specific implementation of the \ref __write function used by
*         the standard library.
*
* - Compiler:           IAR EWAVR32
* - Supported devices:  All AVR32 devices with a USART module can be used.
* - AppNote:
*
* \author               Atmel Corporation (Now Microchip):
*                                        https://www.microchip.com \n
*                       Support and FAQ: https://www.microchip.com/support
*
******************************************************************************/
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
#include <yfuns.h>
#include <avr32/io.h>
#include "usart.h"


_STD_BEGIN


#pragma module_name = "?__write"


/*! Pointer to the base of the USART module instance to use for stdio. */
__no_init volatile avr32_usart_t * volatile stdio_usart_base;
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 函数 __write

```c
/*! \brief Writes a number of bytes, at most \a size, from the memory area
 *         pointed to by \a buffer.
 *
 * If \a buffer is zero then \ref __write performs flushing of internal buffers,
 * if any. In this case, \a handle can be \c -1 to indicate that all handles
 * should be flushed.
 *
 * \param handle File handle to write to.
 * \param buffer Pointer to buffer to read bytes to write from.
 * \param size Number of bytes to write.
 *
 * \return The number of bytes written, or \c _LLIO_ERROR on failure.
 */
size_t __write( int handle,
                const uint8_t * buffer,
                size_t size )
{
    size_t nChars = 0;

    if( buffer == 0 )
    {
        /* This means that we should flush internal buffers. */
        return 0;
    }

    /* This implementation only writes to stdout and stderr. */
    /* For all other file handles, it returns failure. */
    if( ( handle != _LLIO_STDOUT ) && ( handle != _LLIO_STDERR ) )
    {
        return _LLIO_ERROR;
    }

    for( ; size != 0; --size )
    {
        if( usart_putchar( stdio_usart_base, *buffer++ ) < 0 )
        {
            return _LLIO_ERROR;
        }

        ++nChars;
    }

    return nChars;
}
```

**解说：** 这一段实现函数 `__write`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 4: 代码片段 4

```c
_STD_END
```

**解说：** 这一段是 `write.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。
