# FreeRTOS-Kernel 总览解说

这个目录放的是项目级总结文档，用来从整体上理解 FreeRTOS-Kernel 的代码结构、运行逻辑、核心算法和主要子系统。它们和仓库根目录下自动生成的 `*.c.md`、`*.h.md` 不同：逐文件文档适合看某个源码文件的每段代码，这里的文档适合先建立全局地图。

建议阅读顺序如下。

1. `project-structure.md`

   先看仓库由哪些目录和核心文件组成，哪些文件属于内核公共逻辑，哪些属于移植层、示例配置或构建辅助。

2. `kernel-runtime-logic.md`

   重点解释任务从创建、就绪、运行、阻塞、唤醒到删除的大致生命周期，以及调度器如何根据优先级选择任务。

3. `core-algorithms.md`

   集中说明内核中最重要的数据结构和算法，包括双向链表、就绪列表、延时列表、事件等待列表、定时器列表和优先级选择。

4. `subsystems.md`

   横向解释队列、信号量、互斥量、事件组、软件定时器、Stream Buffer、Message Buffer 和协程之间的关系。

5. `porting-and-memory.md`

   说明 `portable/` 移植层与 `portable/MemMang/heap_*.c` 内存管理实现的职责边界。

这些总结文档面向阅读理解，不是官方 API 文档，也不会替代源码。真正核对细节时，应回到对应源码，例如 `tasks.c.md`、`queue.c.md`、`timers.c.md` 和 `portable/MemMang/heap_4.c.md`。
