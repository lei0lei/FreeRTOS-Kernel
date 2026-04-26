# 项目整体代码结构

FreeRTOS-Kernel 这个仓库只包含 FreeRTOS 内核源码、公共头文件、移植层和少量示例配置。完整的 Demo 工程通常在 `FreeRTOS/FreeRTOS` 主仓里，本仓更像是可被应用项目或 Demo 引入的内核组件。

## 顶层核心文件

`tasks.c` 是调度器核心。它管理任务控制块、任务状态列表、就绪列表、延时列表、挂起列表、删除清理、tick 推进、抢占判断以及 SMP 下的多核调度辅助逻辑。大多数内核对象最终都要通过它阻塞或唤醒任务。

`queue.c` 实现队列，同时也支撑二值信号量、计数信号量、互斥量和递归互斥量。它使用同一个 `Queue_t` 结构，根据队列项大小、互斥量持有者字段和不同 API 路径表达不同同步原语。

`list.c` 提供内核通用双向环形链表。调度器的就绪列表、延时列表、事件等待列表、定时器列表都建立在 `List_t` 和 `ListItem_t` 上。

`timers.c` 实现软件定时器。它创建一个 Timer 服务任务，并通过定时器命令队列接收启动、停止、重置、修改周期和挂起函数调用等请求。

`event_groups.c` 实现事件组。事件组用一个位图保存事件状态，用等待列表记录正在等待某些位满足条件的任务。

`stream_buffer.c` 实现 Stream Buffer 和 Message Buffer。它们用于字节流或消息流传递，主要依赖任务通知唤醒等待的一方。

`croutine.c` 实现可选协程功能。协程是早期面向极低资源设备的轻量机制，现代项目通常更常使用任务。

## 头文件目录

`include/FreeRTOS.h` 是内核公共入口头文件，通常必须先于 `task.h`、`queue.h` 等子系统头文件包含。它汇总基础类型、配置检查、移植层入口和内核级默认配置。

`include/task.h`、`include/queue.h`、`include/timers.h`、`include/event_groups.h`、`include/stream_buffer.h` 等文件定义应用可见 API、类型句柄和配置条件。

`include/list.h` 定义链表结构和大量宏。FreeRTOS 为了降低运行时开销，很多链表操作通过宏完成。

`include/portable.h` 定义内核与移植层之间的接口契约，例如启动调度器、内存分配、栈初始化和 tickless idle 相关入口。

## 移植层目录

`portable/` 按编译器、芯片架构或第三方平台组织。典型 port 目录会包含 `port.c`、`portmacro.h`，有些架构还包含汇编文件，例如 `portASM.S` 或 `portasm.s`。

移植层负责把内核的抽象动作映射到具体硬件，包括上下文切换、临界区、中断优先级约束、tick 中断、栈初始化、yield 指令和特定处理器寄存器保存恢复。

`portable/MemMang/` 存放动态内存实现，包含 `heap_1.c` 到 `heap_5.c`。应用通常只选择其中一个参与编译。

## 示例与构建辅助

`examples/template_configuration/FreeRTOSConfig.h` 是配置模板，帮助新项目理解必须提供哪些配置宏。

`CMakeLists.txt` 和各级子目录里的 `CMakeLists.txt` 支持用 CMake 选择 port、heap 和内核源文件。

`README.md`、`MISRA.md`、`History.txt`、`LICENSE.md` 等文件提供使用说明、规范说明、版本历史和许可证信息。

## 一句话地图

可以把这个仓库理解成五层。

1. `list.c` 提供链表基础设施。
2. `tasks.c` 使用链表实现调度和任务状态管理。
3. `queue.c`、`event_groups.c`、`timers.c`、`stream_buffer.c` 在调度器之上实现同步、通信和时间事件。
4. `portable/` 把调度器需要的硬件动作接到具体 CPU 和编译器。
5. `portable/MemMang/` 为动态创建任务、队列、定时器等对象提供堆内存。
