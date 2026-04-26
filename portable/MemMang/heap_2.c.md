# heap_2.c 代码解说

源文件：`portable/MemMang/heap_2.c`

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

## 片段 2: 预处理配置 MPU_WRAPPERS_INCLUDED_FROM_API_FILE

```c
/*
 * A sample implementation of pvPortMalloc() and vPortFree() that permits
 * allocated blocks to be freed, but does not combine adjacent free blocks
 * into a single larger block (and so will fragment memory).  See heap_4.c for
 * an equivalent that does combine adjacent blocks into single larger blocks.
 *
 * See heap_1.c, heap_3.c and heap_4.c for alternative implementations, and the
 * memory management pages of https://www.FreeRTOS.org for more information.
 */
#include <stdlib.h>
#include <string.h>

/* Defining MPU_WRAPPERS_INCLUDED_FROM_API_FILE prevents task.h from redefining
 * all the API functions to use the MPU wrappers.  That should only be done when
 * task.h is included from an application file. */
#define MPU_WRAPPERS_INCLUDED_FROM_API_FILE

#include "FreeRTOS.h"
#include "task.h"

#undef MPU_WRAPPERS_INCLUDED_FROM_API_FILE

#if ( configSUPPORT_DYNAMIC_ALLOCATION == 0 )
    #error This file must not be used if configSUPPORT_DYNAMIC_ALLOCATION is 0
#endif
```

**解说：** 这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。

## 片段 3: 预处理配置 configHEAP_CLEAR_MEMORY_ON_FREE

```c
#ifndef configHEAP_CLEAR_MEMORY_ON_FREE
    #define configHEAP_CLEAR_MEMORY_ON_FREE    0
#endif
```

**解说：** 这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。

## 片段 4: 宏 configADJUSTED_HEAP_SIZE

```c
/* A few bytes might be lost to byte aligning the heap start address. */
#define configADJUSTED_HEAP_SIZE    ( configTOTAL_HEAP_SIZE - portBYTE_ALIGNMENT )

/* Assumes 8bit bytes! */
#define heapBITS_PER_BYTE           ( ( size_t ) 8 )

/* Max value that fits in a size_t type. */
#define heapSIZE_MAX                ( ~( ( size_t ) 0 ) )

/* Check if multiplying a and b will result in overflow. */
#define heapMULTIPLY_WILL_OVERFLOW( a, b )    ( ( ( a ) > 0 ) && ( ( b ) > ( heapSIZE_MAX / ( a ) ) ) )

/* Check if adding a and b will result in overflow. */
#define heapADD_WILL_OVERFLOW( a, b )         ( ( a ) > ( heapSIZE_MAX - ( b ) ) )

/* MSB of the xBlockSize member of an BlockLink_t structure is used to track
 * the allocation status of a block.  When MSB of the xBlockSize member of
 * an BlockLink_t structure is set then the block belongs to the application.
 * When the bit is free the block is still part of the free heap space. */
#define heapBLOCK_ALLOCATED_BITMASK    ( ( ( size_t ) 1 ) << ( ( sizeof( size_t ) * heapBITS_PER_BYTE ) - 1 ) )
#define heapBLOCK_SIZE_IS_VALID( xBlockSize )    ( ( ( xBlockSize ) & heapBLOCK_ALLOCATED_BITMASK ) == 0 )
#define heapBLOCK_IS_ALLOCATED( pxBlock )        ( ( ( pxBlock->xBlockSize ) & heapBLOCK_ALLOCATED_BITMASK ) != 0 )
#define heapALLOCATE_BLOCK( pxBlock )            ( ( pxBlock->xBlockSize ) |= heapBLOCK_ALLOCATED_BITMASK )
#define heapFREE_BLOCK( pxBlock )                ( ( pxBlock->xBlockSize ) &= ~heapBLOCK_ALLOCATED_BITMASK )

/*-----------------------------------------------------------*/

/* Allocate the memory for the heap. */
#if ( configAPPLICATION_ALLOCATED_HEAP == 1 )

/* The application writer has already defined the array used for the RTOS
 * heap - probably so it can be placed in a special segment or address. */
    extern uint8_t ucHeap[ configTOTAL_HEAP_SIZE ];
```

**解说：** 这一段定义宏 `configADJUSTED_HEAP_SIZE`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 5: 预处理配置

```c
#else
    PRIVILEGED_DATA static uint8_t ucHeap[ configTOTAL_HEAP_SIZE ];
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 6: 预处理配置

```c
#endif /* configAPPLICATION_ALLOCATED_HEAP */
```

**解说：** 这一段在编译前生效，用来定义编译条件、常量或包含关系。

## 片段 7: 类型定义 A_BLOCK_LINK

```c
/* Define the linked list structure.  This is used to link free blocks in order
 * of their size. */
typedef struct A_BLOCK_LINK
{
    struct A_BLOCK_LINK * pxNextFreeBlock; /*<< The next free block in the list. */
    size_t xBlockSize;                     /*<< The size of the free block. */
} BlockLink_t;
```

**解说：** 这一段定义类型 `A_BLOCK_LINK`，把相关字段或取值组织成一个明确的数据结构，方便内核代码传递和维护状态。

## 片段 8: 代码片段 8

```c
static const size_t xHeapStructSize = ( ( sizeof( BlockLink_t ) + ( size_t ) ( portBYTE_ALIGNMENT - 1 ) ) & ~( ( size_t ) portBYTE_ALIGNMENT_MASK ) );
```

**解说：** 这一段是 `heap_2.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 9: 宏 heapMINIMUM_BLOCK_SIZE

```c
#define heapMINIMUM_BLOCK_SIZE    ( ( size_t ) ( xHeapStructSize * 2 ) )

/* Create a couple of list links to mark the start and end of the list. */
PRIVILEGED_DATA static BlockLink_t xStart, xEnd;
```

**解说：** 这一段定义宏 `heapMINIMUM_BLOCK_SIZE`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 10: 代码片段 10

```c
/* Keeps track of the number of free bytes remaining, but says nothing about
 * fragmentation. */
PRIVILEGED_DATA static size_t xFreeBytesRemaining = configADJUSTED_HEAP_SIZE;
/* Indicates whether the heap has been initialised or not. */
PRIVILEGED_DATA static BaseType_t xHeapHasBeenInitialised = pdFALSE;
/*-----------------------------------------------------------*/
/*
 * Initialises the heap structures before their first use.
 */
static void prvHeapInit( void ) PRIVILEGED_FUNCTION;
```

**解说：** 这一段是 `heap_2.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 11: 宏 prvInsertBlockIntoFreeList

```c
/*-----------------------------------------------------------*/
/* STATIC FUNCTIONS ARE DEFINED AS MACROS TO MINIMIZE THE FUNCTION CALL DEPTH. */
/*
 * Insert a block into the list of free blocks - which is ordered by size of
 * the block.  Small blocks at the start of the list and large blocks at the end
 * of the list.
 */
#define prvInsertBlockIntoFreeList( pxBlockToInsert )                                                                               \
    {                                                                                                                               \
        BlockLink_t * pxIterator;                                                                                                   \
        size_t xBlockSize;                                                                                                          \
                                                                                                                                    \
        xBlockSize = pxBlockToInsert->xBlockSize;                                                                                   \
                                                                                                                                    \
        /* Iterate through the list until a block is found that has a larger size */                                                \
        /* than the block we are inserting. */                                                                                      \
        for( pxIterator = &xStart; pxIterator->pxNextFreeBlock->xBlockSize < xBlockSize; pxIterator = pxIterator->pxNextFreeBlock ) \
        {                                                                                                                           \
            /* There is nothing to do here - just iterate to the correct position. */                                               \
        }                                                                                                                           \
                                                                                                                                    \
        /* Update the list to include the block being inserted in the correct */                                                    \
        /* position. */                                                                                                             \
        pxBlockToInsert->pxNextFreeBlock = pxIterator->pxNextFreeBlock;                                                             \
        pxIterator->pxNextFreeBlock = pxBlockToInsert;                                                                              \
    }
```

**解说：** 这一段定义宏 `prvInsertBlockIntoFreeList`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。

## 片段 12: 函数 pvPortMalloc

```c
/*-----------------------------------------------------------*/
void * pvPortMalloc( size_t xWantedSize )
{
    BlockLink_t * pxBlock;
    BlockLink_t * pxPreviousBlock;
    BlockLink_t * pxNewBlockLink;
    void * pvReturn = NULL;
    size_t xAdditionalRequiredSize;
    size_t xAllocatedBlockSize = 0;

    if( xWantedSize > 0 )
    {
        /* The wanted size must be increased so it can contain a BlockLink_t
         * structure in addition to the requested amount of bytes. */
        if( heapADD_WILL_OVERFLOW( xWantedSize, xHeapStructSize ) == 0 )
        {
            xWantedSize += xHeapStructSize;

            /* Ensure that blocks are always aligned to the required number
             * of bytes. */
            if( ( xWantedSize & portBYTE_ALIGNMENT_MASK ) != 0x00 )
            {
                /* Byte alignment required. */
                xAdditionalRequiredSize = portBYTE_ALIGNMENT - ( xWantedSize & portBYTE_ALIGNMENT_MASK );

                if( heapADD_WILL_OVERFLOW( xWantedSize, xAdditionalRequiredSize ) == 0 )
                {
                    xWantedSize += xAdditionalRequiredSize;
                }
                else
                {
                    xWantedSize = 0;
                }
            }
            else
            {
                mtCOVERAGE_TEST_MARKER();
            }
        }
        else
        {
            xWantedSize = 0;
        }
    }
    else
    {
        mtCOVERAGE_TEST_MARKER();
    }

    vTaskSuspendAll();
    {
        /* If this is the first call to malloc then the heap will require
         * initialisation to setup the list of free blocks. */
        if( xHeapHasBeenInitialised == pdFALSE )
        {
            prvHeapInit();
            xHeapHasBeenInitialised = pdTRUE;
        }

        /* Check the block size we are trying to allocate is not so large that the
         * top bit is set.  The top bit of the block size member of the BlockLink_t
         * structure is used to determine who owns the block - the application or
         * the kernel, so it must be free. */
        if( heapBLOCK_SIZE_IS_VALID( xWantedSize ) != 0 )
        {
            if( ( xWantedSize > 0 ) && ( xWantedSize <= xFreeBytesRemaining ) )
            {
                /* Blocks are stored in byte order - traverse the list from the start
                 * (smallest) block until one of adequate size is found. */
                pxPreviousBlock = &xStart;
                pxBlock = xStart.pxNextFreeBlock;

                while( ( pxBlock->xBlockSize < xWantedSize ) && ( pxBlock->pxNextFreeBlock != NULL ) )
                {
                    pxPreviousBlock = pxBlock;
                    pxBlock = pxBlock->pxNextFreeBlock;
                }

                /* If we found the end marker then a block of adequate size was not found. */
                if( pxBlock != &xEnd )
                {
                    /* Return the memory space - jumping over the BlockLink_t structure
                     * at its start. */
                    pvReturn = ( void * ) ( ( ( uint8_t * ) pxPreviousBlock->pxNextFreeBlock ) + xHeapStructSize );

                    /* This block is being returned for use so must be taken out of the
                     * list of free blocks. */
                    pxPreviousBlock->pxNextFreeBlock = pxBlock->pxNextFreeBlock;

                    /* If the block is larger than required it can be split into two. */
                    if( ( pxBlock->xBlockSize - xWantedSize ) > heapMINIMUM_BLOCK_SIZE )
                    {
                        /* This block is to be split into two.  Create a new block
                         * following the number of bytes requested. The void cast is
                         * used to prevent byte alignment warnings from the compiler. */
                        pxNewBlockLink = ( void * ) ( ( ( uint8_t * ) pxBlock ) + xWantedSize );

                        /* Calculate the sizes of two blocks split from the single
                         * block. */
                        pxNewBlockLink->xBlockSize = pxBlock->xBlockSize - xWantedSize;
                        pxBlock->xBlockSize = xWantedSize;

                        /* Insert the new block into the list of free blocks.
                         * The list of free blocks is sorted by their size, we have to
                         * iterate to find the right place to insert new block. */
                        prvInsertBlockIntoFreeList( ( pxNewBlockLink ) );
                    }

                    xFreeBytesRemaining -= pxBlock->xBlockSize;

                    xAllocatedBlockSize = pxBlock->xBlockSize;

                    /* The block is being returned - it is allocated and owned
                     * by the application and has no "next" block. */
                    heapALLOCATE_BLOCK( pxBlock );
                    pxBlock->pxNextFreeBlock = NULL;
                }
            }
        }

        traceMALLOC( pvReturn, xAllocatedBlockSize );

        /* Prevent compiler warnings when trace macros are not used. */
        ( void ) xAllocatedBlockSize;
    }
    ( void ) xTaskResumeAll();

    #if ( configUSE_MALLOC_FAILED_HOOK == 1 )
    {
        if( pvReturn == NULL )
        {
            vApplicationMallocFailedHook();
        }
    }
    #endif

    return pvReturn;
}
```

**解说：** 这一段实现函数 `pvPortMalloc`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 13: 函数 vPortFree

```c
/*-----------------------------------------------------------*/
void vPortFree( void * pv )
{
    uint8_t * puc = ( uint8_t * ) pv;
    BlockLink_t * pxLink;

    if( pv != NULL )
    {
        /* The memory being freed will have an BlockLink_t structure immediately
         * before it. */
        puc -= xHeapStructSize;

        /* This unexpected casting is to keep some compilers from issuing
         * byte alignment warnings. */
        pxLink = ( void * ) puc;

        configASSERT( heapBLOCK_IS_ALLOCATED( pxLink ) != 0 );
        configASSERT( pxLink->pxNextFreeBlock == NULL );

        if( heapBLOCK_IS_ALLOCATED( pxLink ) != 0 )
        {
            if( pxLink->pxNextFreeBlock == NULL )
            {
                /* The block is being returned to the heap - it is no longer
                 * allocated. */
                heapFREE_BLOCK( pxLink );
                #if ( configHEAP_CLEAR_MEMORY_ON_FREE == 1 )
                {
                    ( void ) memset( puc + xHeapStructSize, 0, pxLink->xBlockSize - xHeapStructSize );
                }
                #endif

                vTaskSuspendAll();
                {
                    /* Add this block to the list of free blocks. */
                    prvInsertBlockIntoFreeList( ( ( BlockLink_t * ) pxLink ) );
                    xFreeBytesRemaining += pxLink->xBlockSize;
                    traceFREE( pv, pxLink->xBlockSize );
                }
                ( void ) xTaskResumeAll();
            }
        }
    }
}
```

**解说：** 这一段实现函数 `vPortFree`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 14: 函数 xPortGetFreeHeapSize

```c
/*-----------------------------------------------------------*/
size_t xPortGetFreeHeapSize( void )
{
    return xFreeBytesRemaining;
}
```

**解说：** 这一段实现函数 `xPortGetFreeHeapSize`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 15: 函数 vPortInitialiseBlocks

```c
/*-----------------------------------------------------------*/
void vPortInitialiseBlocks( void )
{
    /* This just exists to keep the linker quiet. */
}
```

**解说：** 这一段实现函数 `vPortInitialiseBlocks`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 16: 函数 pvPortCalloc

```c
/*-----------------------------------------------------------*/
void * pvPortCalloc( size_t xNum,
                     size_t xSize )
{
    void * pv = NULL;

    if( heapMULTIPLY_WILL_OVERFLOW( xNum, xSize ) == 0 )
    {
        pv = pvPortMalloc( xNum * xSize );

        if( pv != NULL )
        {
            ( void ) memset( pv, 0, xNum * xSize );
        }
    }

    return pv;
}
```

**解说：** 这一段实现函数 `pvPortCalloc`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 17: 代码片段 19

```c
/*-----------------------------------------------------------*/
static void prvHeapInit( void ) /* PRIVILEGED_FUNCTION */
{
    BlockLink_t * pxFirstFreeBlock;
    uint8_t * pucAlignedHeap;

    /* Ensure the heap starts on a correctly aligned boundary. */
    pucAlignedHeap = ( uint8_t * ) ( ( ( portPOINTER_SIZE_TYPE ) & ucHeap[ portBYTE_ALIGNMENT - 1 ] ) & ( ~( ( portPOINTER_SIZE_TYPE ) portBYTE_ALIGNMENT_MASK ) ) );

    /* xStart is used to hold a pointer to the first item in the list of free
     * blocks.  The void cast is used to prevent compiler warnings. */
    xStart.pxNextFreeBlock = ( void * ) pucAlignedHeap;
    xStart.xBlockSize = ( size_t ) 0;

    /* xEnd is used to mark the end of the list of free blocks. */
    xEnd.xBlockSize = configADJUSTED_HEAP_SIZE;
    xEnd.pxNextFreeBlock = NULL;

    /* To start with there is a single free block that is sized to take up the
     * entire heap space. */
    pxFirstFreeBlock = ( BlockLink_t * ) pucAlignedHeap;
    pxFirstFreeBlock->xBlockSize = configADJUSTED_HEAP_SIZE;
    pxFirstFreeBlock->pxNextFreeBlock = &xEnd;
}
```

**解说：** 这一段是 `heap_2.c` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。

## 片段 18: 函数 vPortHeapResetState

```c
/*-----------------------------------------------------------*/
/*
 * Reset the state in this file. This state is normally initialized at start up.
 * This function must be called by the application before restarting the
 * scheduler.
 */
void vPortHeapResetState( void )
{
    xFreeBytesRemaining = configADJUSTED_HEAP_SIZE;

    xHeapHasBeenInitialised = pdFALSE;
}
```

**解说：** 这一段实现函数 `vPortHeapResetState`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。

## 片段 19: 说明性注释

```c
/*-----------------------------------------------------------*/
```

**解说：** 这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：-----------------------------------------------------------。
