# addFreeRTOS.h 代码解说

源文件：`portable/WizC/PIC18/addFreeRTOS.h`

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

## 片段 2: 预处理配置 WIZC_FREERTOS_H

```c
/*
Changes from V3.0.0

Changes from V3.0.1

Changes from V4.0.1
    Uselib pragma added for Croutine.c
*/
/*
 * The installation script will automatically prepend this file to the default FreeRTOS.h.
 */
#ifndef WIZC_FREERTOS_H
#define WIZC_FREERTOS_H

#pragma noheap
#pragma wizcpp expandnl   on
#pragma wizcpp searchpath "$__PATHNAME__/libFreeRTOS/Include/"
#pragma wizcpp uselib     "$__PATHNAME__/libFreeRTOS/Modules/Croutine.c"
#pragma wizcpp uselib     "$__PATHNAME__/libFreeRTOS/Modules/Tasks.c"
#pragma wizcpp uselib     "$__PATHNAME__/libFreeRTOS/Modules/Queue.c"
#pragma wizcpp uselib     "$__PATHNAME__/libFreeRTOS/Modules/List.c"
#pragma wizcpp uselib     "$__PATHNAME__/libFreeRTOS/Modules/Port.c"

#endif  /* WIZC_FREERTOS_H */
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。
