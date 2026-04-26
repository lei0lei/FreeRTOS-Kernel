# copy_files.py 代码解说

源文件：`portable/ARMv8M/copy_files.py`

> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。

## 片段 1: 脚本片段

```python
#/*
# * FreeRTOS Kernel <DEVELOPMENT BRANCH>
# * Copyright (C) 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# *
# * SPDX-License-Identifier: MIT
# *
# * Permission is hereby granted, free of charge, to any person obtaining a copy of
# * this software and associated documentation files (the "Software"), to deal in
# * the Software without restriction, including without limitation the rights to
# * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# * the Software, and to permit persons to whom the Software is furnished to do so,
# * subject to the following conditions:
# *
# * The above copyright notice and this permission notice shall be included in all
# * copies or substantial portions of the Software.
# *
# * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# *
# * https://www.FreeRTOS.org
# * https://github.com/FreeRTOS
# *
# */
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 2: 脚本片段

```python
import os
import shutil
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 3: 脚本片段

```python
_THIS_FILE_DIRECTORY_ = os.path.dirname(os.path.realpath(__file__))
_FREERTOS_PORTABLE_DIRECTORY_ = os.path.dirname(_THIS_FILE_DIRECTORY_)
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 4: 脚本片段

```python
_COMPILERS_ = ['GCC', 'IAR']
_ARCH_NS_ = ['ARM_CM85', 'ARM_CM85_NTZ', 'ARM_CM55', 'ARM_CM55_NTZ', 'ARM_CM52', 'ARM_CM52_NTZ', 'ARM_CM35P', 'ARM_CM35P_NTZ', 'ARM_CM33', 'ARM_CM33_NTZ', 'ARM_CM23', 'ARM_CM23_NTZ', 'ARM_STAR_MC3', 'ARM_STAR_MC3_NTZ']
_ARCH_S_ = ['ARM_CM85', 'ARM_CM55', 'ARM_CM52', 'ARM_CM35P', 'ARM_CM33', 'ARM_CM23', 'ARM_STAR_MC3']
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 5: 脚本片段

```python
# Files to be compiled in the Secure Project
_SECURE_COMMON_FILE_PATHS_ = [
    os.path.join('secure', 'context'),
    os.path.join('secure', 'heap'),
    os.path.join('secure', 'init'),
    os.path.join('secure', 'macros')
]
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 6: 脚本片段

```python
_SECURE_PORTABLE_FILE_PATHS_ = {
    'GCC':{
        'ARM_CM23'     :[os.path.join('secure', 'context', 'portable', 'GCC', 'ARM_CM23')],
        'ARM_CM33'     :[os.path.join('secure', 'context', 'portable', 'GCC', 'ARM_CM33')],
        'ARM_CM35P'    :[os.path.join('secure', 'context', 'portable', 'GCC', 'ARM_CM33')],
        'ARM_CM52'     :[os.path.join('secure', 'context', 'portable', 'GCC', 'ARM_CM33')],
        'ARM_CM55'     :[os.path.join('secure', 'context', 'portable', 'GCC', 'ARM_CM33')],
        'ARM_CM85'     :[os.path.join('secure', 'context', 'portable', 'GCC', 'ARM_CM33')],
        'ARM_STAR_MC3' :[os.path.join('secure', 'context', 'portable', 'GCC', 'ARM_CM33')]
    },
    'IAR':{
        'ARM_CM23'     :[os.path.join('secure', 'context', 'portable', 'IAR', 'ARM_CM23')],
        'ARM_CM33'     :[os.path.join('secure', 'context', 'portable', 'IAR', 'ARM_CM33')],
        'ARM_CM35P'    :[os.path.join('secure', 'context', 'portable', 'IAR', 'ARM_CM33')],
        'ARM_CM52'     :[os.path.join('secure', 'context', 'portable', 'IAR', 'ARM_CM33')],
        'ARM_CM55'     :[os.path.join('secure', 'context', 'portable', 'IAR', 'ARM_CM33')],
        'ARM_CM85'     :[os.path.join('secure', 'context', 'portable', 'IAR', 'ARM_CM33')],
        'ARM_STAR_MC3' :[os.path.join('secure', 'context', 'portable', 'IAR', 'ARM_CM33')]
    }
}
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 7: 脚本片段

```python
# Files to be compiled in the Non-Secure Project
_NONSECURE_COMMON_FILE_PATHS_ = [
    'non_secure'
]
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 8: 脚本片段

```python
_NONSECURE_PORTABLE_FILE_PATHS_ = {
    'GCC':{
        'ARM_CM23'         : [os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM23')],
        'ARM_CM23_NTZ'     : [os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM23_NTZ')],
        'ARM_CM33'         : [os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM33')],
        'ARM_CM33_NTZ'     : [os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM33_NTZ')],
        'ARM_CM35P'        : [os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM33', 'portasm.c'),
                              os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM33', 'mpu_wrappers_v2_asm.c'),
                              os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM35P', 'portmacro.h')],
        'ARM_CM35P_NTZ'    : [os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM33_NTZ', 'portasm.c'),
                              os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM33_NTZ', 'mpu_wrappers_v2_asm.c'),
                              os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM35P', 'portmacro.h')],
        'ARM_CM52'         : [os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM33', 'portasm.c'),
                              os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM33', 'mpu_wrappers_v2_asm.c'),
                              os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM52', 'portmacro.h')],
        'ARM_CM52_NTZ'     : [os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM33_NTZ', 'portasm.c'),
                              os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM33_NTZ', 'mpu_wrappers_v2_asm.c'),
                              os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM52', 'portmacro.h')],
        'ARM_CM55'         : [os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM33', 'portasm.c'),
                              os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM33', 'mpu_wrappers_v2_asm.c'),
                              os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM55', 'portmacro.h')],
        'ARM_CM55_NTZ'     : [os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM33_NTZ', 'portasm.c'),
                              os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM33_NTZ', 'mpu_wrappers_v2_asm.c'),
                              os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM55', 'portmacro.h')],
        'ARM_CM85'         : [os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM33', 'portasm.c'),
                              os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM33', 'mpu_wrappers_v2_asm.c'),
                              os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM85', 'portmacro.h')],
        'ARM_CM85_NTZ'     : [os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM33_NTZ', 'portasm.c'),
                              os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM33_NTZ', 'mpu_wrappers_v2_asm.c'),
                              os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM85', 'portmacro.h')],
        'ARM_STAR_MC3'     : [os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM33', 'portasm.c'),
                              os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM33', 'mpu_wrappers_v2_asm.c'),
                              os.path.join('non_secure', 'portable', 'GCC', 'ARM_STAR_MC3', 'portmacro.h')],
        'ARM_STAR_MC3_NTZ' : [os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM33_NTZ', 'portasm.c'),
                              os.path.join('non_secure', 'portable', 'GCC', 'ARM_CM33_NTZ', 'mpu_wrappers_v2_asm.c'),
                              os.path.join('non_secure', 'portable', 'GCC', 'ARM_STAR_MC3', 'portmacro.h')]
    },
    'IAR':{
        'ARM_CM23'         : [os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM23')],
        'ARM_CM23_NTZ'     : [os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM23_NTZ')],
        'ARM_CM33'         : [os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM33')],
        'ARM_CM33_NTZ'     : [os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM33_NTZ')],
        'ARM_CM35P'        : [os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM33', 'portasm.s'),
                              os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM33', 'mpu_wrappers_v2_asm.S'),
                              os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM35P', 'portmacro.h')],
        'ARM_CM35P_NTZ'    : [os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM33_NTZ', 'portasm.s'),
                              os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM33_NTZ', 'mpu_wrappers_v2_asm.S'),
                              os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM35P', 'portmacro.h')],
        'ARM_CM52'         : [os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM33', 'portasm.s'),
                              os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM33', 'mpu_wrappers_v2_asm.S'),
                              os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM52', 'portmacro.h')],
        'ARM_CM52_NTZ'     : [os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM33_NTZ', 'portasm.s'),
                              os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM33_NTZ', 'mpu_wrappers_v2_asm.S'),
                              os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM52', 'portmacro.h')],
        'ARM_CM55'         : [os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM33', 'portasm.s'),
                              os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM33', 'mpu_wrappers_v2_asm.S'),
                              os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM55', 'portmacro.h')],
        'ARM_CM55_NTZ'     : [os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM33_NTZ', 'portasm.s'),
                              os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM33_NTZ', 'mpu_wrappers_v2_asm.S'),
                              os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM55', 'portmacro.h')],
        'ARM_CM85'         : [os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM33', 'portasm.s'),
                              os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM33', 'mpu_wrappers_v2_asm.S'),
                              os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM85', 'portmacro.h')],
        'ARM_CM85_NTZ'     : [os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM33_NTZ', 'portasm.s'),
                              os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM33_NTZ', 'mpu_wrappers_v2_asm.S'),
                              os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM85', 'portmacro.h')],
        'ARM_STAR_MC3'     : [os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM33', 'portasm.s'),
                              os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM33', 'mpu_wrappers_v2_asm.S'),
                              os.path.join('non_secure', 'portable', 'IAR', 'ARM_STAR_MC3', 'portmacro.h')],
        'ARM_STAR_MC3_NTZ' : [os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM33_NTZ', 'portasm.s'),
                              os.path.join('non_secure', 'portable', 'IAR', 'ARM_CM33_NTZ', 'mpu_wrappers_v2_asm.S'),
                              os.path.join('non_secure', 'portable', 'IAR', 'ARM_STAR_MC3', 'portmacro.h')]
    },
}
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 9: 脚本片段 else

```python

def copy_files_in_dir(src_abs_path, dst_abs_path):
    if os.path.isfile(src_abs_path):
        print('Src: {}'.format(src_abs_path))
        print('Dst: {}\n'.format(dst_abs_path))
        shutil.copy2(src_abs_path, dst_abs_path)
    else:
        for src_file in os.listdir(src_abs_path):
            src_file_abs_path = os.path.join(src_abs_path, src_file)
            if os.path.isfile(src_file_abs_path) and src_file != 'ReadMe.txt':
                if not os.path.exists(dst_abs_path):
                    os.makedirs(dst_abs_path)
                print('Src: {}'.format(src_file_abs_path))
                print('Dst: {}\n'.format(dst_abs_path))
                shutil.copy2(src_file_abs_path, dst_abs_path)
```

**解说：** 这一段是脚本逻辑的一部分，围绕 `else` 或相邻命令完成自动化处理。

## 片段 10: 脚本片段

```python

def copy_common_files_for_compiler_and_arch(compiler, arch, src_paths, dst_path):
    for src_path in src_paths:
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 11: 脚本片段

```python
        src_abs_path = os.path.join(_THIS_FILE_DIRECTORY_, src_path)
        dst_abs_path = os.path.join(_FREERTOS_PORTABLE_DIRECTORY_, compiler, arch, dst_path)
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 12: 脚本片段

```python
        copy_files_in_dir(src_abs_path, dst_abs_path)
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 13: 脚本片段

```python

def copy_portable_files_for_compiler_and_arch(compiler, arch, src_paths, dst_path):
    for src_path in src_paths[compiler][arch]:
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 14: 脚本片段

```python
        src_abs_path = os.path.join(_THIS_FILE_DIRECTORY_, src_path)
        dst_abs_path = os.path.join(_FREERTOS_PORTABLE_DIRECTORY_, compiler, arch, dst_path)
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 15: 脚本片段

```python
        copy_files_in_dir(src_abs_path, dst_abs_path)
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 16: 脚本片段

```python

def copy_files():
    # Copy Secure Files
    for compiler in _COMPILERS_:
        for arch in _ARCH_S_:
            copy_common_files_for_compiler_and_arch(compiler, arch, _SECURE_COMMON_FILE_PATHS_, 'secure')
            copy_portable_files_for_compiler_and_arch(compiler, arch, _SECURE_PORTABLE_FILE_PATHS_, 'secure')
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 17: 脚本片段

```python
    # Copy Non-Secure Files
    for compiler in _COMPILERS_:
        for arch in _ARCH_NS_:
            copy_common_files_for_compiler_and_arch(compiler, arch, _NONSECURE_COMMON_FILE_PATHS_, 'non_secure')
            copy_portable_files_for_compiler_and_arch(compiler, arch, _NONSECURE_PORTABLE_FILE_PATHS_, 'non_secure')
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 18: 脚本片段

```python

def main():
    copy_files()
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。

## 片段 19: 脚本片段

```python

if __name__ == '__main__':
    main()
```

**解说：** 这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。
