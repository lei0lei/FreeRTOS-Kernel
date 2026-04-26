#!/usr/bin/env python3
"""Generate side-by-side Markdown explanations for source files.

The generated files are intentionally documentation artifacts.  Each source
file gets a sibling file named "<source file name>.md", for example
"tasks.c.md" or "portmacro.h.md".
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


SOURCE_SUFFIXES = {
    ".c",
    ".h",
    ".s",
    ".S",
    ".py",
    ".sh",
}

SPECIAL_SOURCE_NAMES = {
    "CMakeLists.txt",
}

SKIP_DIRS = {
    ".git",
    ".github",
}

MAX_FALLBACK_BLOCK_LINES = 80


@dataclass
class Segment:
    title: str
    kind: str
    lines: list[str]


def is_source_file(path: Path) -> bool:
    if path.name.endswith(".md"):
        return False
    if path.name in SPECIAL_SOURCE_NAMES:
        return True
    return path.suffix in SOURCE_SUFFIXES


def iter_source_files(root: Path) -> list[Path]:
    files: list[Path] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.parts[-2:] == ("tools", "generate_code_markdown.py"):
            continue
        if is_source_file(path):
            files.append(path)

    return sorted(files)


def language_for(path: Path) -> str:
    if path.suffix in {".c", ".h"}:
        return "c"
    if path.suffix in {".s", ".S"}:
        return "asm"
    if path.suffix == ".py":
        return "python"
    if path.suffix == ".sh":
        return "bash"
    if path.name == "CMakeLists.txt":
        return "cmake"
    return "text"


def strip_comment_markers(text: str) -> str:
    cleaned = re.sub(r"^\s*/\*+", "", text)
    cleaned = re.sub(r"\*/\s*$", "", cleaned)
    cleaned = re.sub(r"^\s*\* ?", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^\s*// ?", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^\s*# ?", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def first_identifier(text: str) -> str | None:
    patterns = [
        r"\b(?:static\s+)?(?:BaseType_t|UBaseType_t|void|int|size_t|TickType_t|TaskHandle_t|QueueHandle_t|uint\w+_t|port\w+_t|[A-Za-z_]\w+\s*\*)\s+([A-Za-z_]\w+)\s*\(",
        r"#\s*define\s+([A-Za-z_]\w+)",
        r"\b(?:typedef\s+)?(?:struct|enum)\s+([A-Za-z_]\w+)",
        r"\btypedef\b.*?\b([A-Za-z_]\w+)\s*;",
        r"^\s*([A-Za-z_.$][\w.$]*):",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
        if match:
            return match.group(1)

    return None


def code_after_leading_comments(lines: list[str]) -> str:
    i = 0

    while i < len(lines):
        stripped = lines[i].strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("/*"):
            i += 1
            while i < len(lines) and "*/" not in lines[i - 1]:
                i += 1
            continue

        if stripped.startswith("//"):
            i += 1
            continue

        break

    return "".join(lines[i:]).strip()


def segment_title(kind: str, index: int, text: str) -> str:
    identifier = first_identifier(text)

    if kind == "license":
        return "文件头和许可证"
    if kind == "comment":
        return "说明性注释"
    if kind == "preprocessor":
        return f"预处理配置 {identifier}" if identifier else "预处理配置"
    if kind == "function":
        return f"函数 {identifier}" if identifier else "函数实现"
    if kind == "type":
        return f"类型定义 {identifier}" if identifier else "类型定义"
    if kind == "macro":
        return f"宏 {identifier}" if identifier else "宏定义"
    if kind == "asm_label":
        return f"汇编标签 {identifier}" if identifier else "汇编入口"
    if kind == "script_block":
        return f"脚本片段 {identifier}" if identifier else "脚本片段"

    return f"代码片段 {index}"


def classify_block(lines: list[str], source_kind: str) -> str:
    text = "".join(lines)
    stripped = text.strip()
    effective = code_after_leading_comments(lines)

    if not stripped:
        return "blank"
    if stripped.startswith("/*") and "SPDX-License-Identifier" in stripped:
        return "license"
    if not effective and (stripped.startswith("/*") or stripped.startswith("//")):
        return "comment"
    if source_kind == "asm" and re.search(r"^\s*[A-Za-z_.$][\w.$]*:", effective or text, re.MULTILINE):
        return "asm_label"
    if source_kind in {"python", "bash", "cmake"}:
        return "script_block"
    if re.match(r"\s*#\s*define\b", effective):
        return "macro"
    if re.match(r"\s*#", effective):
        return "preprocessor"
    if re.search(r"\btypedef\b|\bstruct\b|\benum\b", effective) and effective.endswith(";"):
        return "type"
    if re.search(r"\)\s*(?:PRIVILEGED_FUNCTION\s*)?\{", effective):
        return "function"

    return "code"


def read_statement(lines: list[str], start: int) -> tuple[list[str], int]:
    block: list[str] = []
    brace_depth = 0
    paren_depth = 0
    in_block_comment = False

    i = start
    while i < len(lines):
        line = lines[i]
        block.append(line)

        scan = line
        if in_block_comment:
            if "*/" in scan:
                scan = scan.split("*/", 1)[1]
                in_block_comment = False
            else:
                i += 1
                continue

        while "/*" in scan:
            before, after = scan.split("/*", 1)
            scan = before
            if "*/" in after:
                scan += after.split("*/", 1)[1]
            else:
                in_block_comment = True
                break

        if not in_block_comment:
            scan = scan.split("//", 1)[0]
            brace_depth += scan.count("{") - scan.count("}")
            paren_depth += scan.count("(") - scan.count(")")

        stripped = line.strip()
        if stripped.endswith("\\"):
            i += 1
            continue
        if brace_depth <= 0 and paren_depth <= 0 and (
            stripped.endswith(";") or stripped.endswith("}") or stripped.startswith("#endif")
        ):
            return block, i + 1

        i += 1

    return block, i


def read_comment(lines: list[str], start: int) -> tuple[list[str], int]:
    block = [lines[start]]

    if "*/" in lines[start]:
        return block, start + 1

    i = start + 1
    while i < len(lines):
        block.append(lines[i])
        if "*/" in lines[i]:
            return block, i + 1
        i += 1

    return block, i


def looks_like_function_start(lines: list[str], start: int) -> bool:
    preview = "".join(lines[start : min(len(lines), start + 8)])
    if ";" in preview.split("{", 1)[0]:
        return False
    if re.match(r"\s*(if|for|while|switch|do|else)\b", preview):
        return False
    return bool(re.search(r"\b[A-Za-z_]\w+\s*\([^;]*\)\s*(?:PRIVILEGED_FUNCTION\s*)?\{", preview, re.DOTALL))


def read_function(lines: list[str], start: int) -> tuple[list[str], int]:
    block: list[str] = []
    brace_depth = 0
    saw_open = False
    i = start

    while i < len(lines):
        line = lines[i]
        block.append(line)
        code = line.split("//", 1)[0]
        brace_depth += code.count("{")
        if "{" in code:
            saw_open = True
        brace_depth -= code.count("}")
        i += 1

        if saw_open and brace_depth <= 0:
            break

    return block, i


def split_c_like(lines: list[str]) -> list[Segment]:
    segments: list[Segment] = []
    pending_comments: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("/*"):
            comment, i = read_comment(lines, i)
            if not segments and "SPDX-License-Identifier" in "".join(comment):
                text = "".join(comment)
                segments.append(Segment(segment_title("license", len(segments) + 1, text), "license", comment))
            else:
                pending_comments.extend(comment)
            continue

        if stripped.startswith("//"):
            pending_comments.append(line)
            i += 1
            continue

        if stripped.startswith("#") or stripped.endswith("\\"):
            block, i = read_statement(lines, i)
            block = pending_comments + block
            pending_comments = []
            kind = classify_block(block, "c")
            text = "".join(block)
            segments.append(Segment(segment_title(kind, len(segments) + 1, text), kind, block))
            continue

        if looks_like_function_start(lines, i):
            block, i = read_function(lines, i)
            block = pending_comments + block
            pending_comments = []
            kind = "function"
            text = "".join(block)
            segments.append(Segment(segment_title(kind, len(segments) + 1, text), kind, block))
            continue

        block, i = read_statement(lines, i)
        block = pending_comments + block
        pending_comments = []
        kind = classify_block(block, "c")
        text = "".join(block)
        segments.append(Segment(segment_title(kind, len(segments) + 1, text), kind, block))

    if pending_comments:
        text = "".join(pending_comments)
        segments.append(Segment(segment_title("comment", len(segments) + 1, text), "comment", pending_comments))

    return merge_small_code_segments(segments)


def split_simple(lines: list[str], source_kind: str) -> list[Segment]:
    segments: list[Segment] = []
    block: list[str] = []

    def flush() -> None:
        nonlocal block
        if not block:
            return
        kind = classify_block(block, source_kind)
        text = "".join(block)
        segments.append(Segment(segment_title(kind, len(segments) + 1, text), kind, block))
        block = []

    for line in lines:
        stripped = line.strip()
        if not stripped and block:
            flush()
            continue
        block.append(line)
        if len(block) >= MAX_FALLBACK_BLOCK_LINES:
            flush()

    flush()
    return segments


def merge_small_code_segments(segments: list[Segment]) -> list[Segment]:
    merged: list[Segment] = []
    buffer: list[str] = []

    def flush_buffer() -> None:
        nonlocal buffer
        if buffer:
            text = "".join(buffer)
            merged.append(Segment(segment_title("code", len(merged) + 1, text), "code", buffer))
            buffer = []

    for segment in segments:
        if segment.kind == "code" and len(segment.lines) < 6:
            buffer.extend(segment.lines)
            if len(buffer) >= MAX_FALLBACK_BLOCK_LINES:
                flush_buffer()
            continue

        flush_buffer()
        merged.append(segment)

    flush_buffer()
    return merged


def explain_segment(segment: Segment, path: Path) -> str:
    text = "".join(segment.lines)
    compact = strip_comment_markers(text)
    identifier = first_identifier(text)

    if segment.kind == "license":
        return "这一段是文件头，说明项目归属、许可证和免责条款；它告诉使用者这个文件按 MIT 许可证发布。"

    if segment.kind == "comment":
        if compact:
            return f"这一段是源码作者留下的说明，概括了后续代码的意图或使用条件。原意可理解为：{compact[:240]}。"
        return "这一段是说明性文字，用来给后续代码提供背景。"

    if segment.kind == "preprocessor":
        if "#include" in text:
            return "这一段引入当前文件依赖的头文件，让后续代码可以使用 FreeRTOS、标准库或移植层提供的类型、宏和函数。"
        if "#if" in text or "#ifdef" in text or "#ifndef" in text:
            return "这一段根据编译配置选择启用或禁用某些代码路径，保证同一份源码可以适配不同内核配置、编译器或硬件端口。"
        return "这一段在编译前生效，用来定义编译条件、常量或包含关系。"

    if segment.kind == "macro":
        if identifier:
            return f"这一段定义宏 `{identifier}`。宏在编译前展开，通常用于表达常量、轻量封装、配置开关或平台相关操作。"
        return "这一段定义宏，供后续代码在编译阶段展开使用。"

    if segment.kind == "type":
        if identifier:
            return f"这一段定义类型 `{identifier}`，把相关字段或取值组织成一个明确的数据结构，方便内核代码传递和维护状态。"
        return "这一段定义结构体、枚举或类型别名，用来描述内核内部使用的数据形状。"

    if segment.kind == "function":
        if identifier:
            return f"这一段实现函数 `{identifier}`。它把一组相关步骤封装成可调用的行为，供内核内部或公开 API 在需要时执行。"
        return "这一段实现一个函数，把一组相关步骤封装成独立的执行单元。"

    if segment.kind == "asm_label":
        if identifier:
            return f"这一段是汇编标签 `{identifier}` 附近的代码，通常对应异常入口、上下文切换、启动流程或特定处理器指令序列。"
        return "这一段是汇编代码，用来完成 C 语言难以直接表达的处理器级操作。"

    if segment.kind == "script_block":
        if identifier:
            return f"这一段是脚本逻辑的一部分，围绕 `{identifier}` 或相邻命令完成自动化处理。"
        return "这一段是脚本逻辑，负责执行构建、检查或仓库维护相关的自动化步骤。"

    if "configASSERT" in text:
        return "这一段执行断言检查，用来在调试阶段尽早发现无效参数、非法状态或配置错误。"
    if "taskENTER_CRITICAL" in text or "portENTER_CRITICAL" in text:
        return "这一段进入临界区，暂时保护共享状态，避免任务切换或中断并发修改同一份数据。"
    if "taskEXIT_CRITICAL" in text or "portEXIT_CRITICAL" in text:
        return "这一段退出临界区，恢复正常调度或中断处理，让系统继续并发运行。"
    if "return" in text:
        return "这一段计算并返回结果；调用者会根据返回值继续决定后续流程。"

    name = path.name
    return f"这一段是 `{name}` 中的普通实现代码，负责准备数据、更新状态或串联前后逻辑，使所在模块能够完成自己的职责。"


def render_markdown(path: Path, root: Path, segments: list[Segment]) -> str:
    rel = path.relative_to(root).as_posix()
    lang = language_for(path)
    parts = [
        f"# {path.name} 代码解说",
        "",
        f"源文件：`{rel}`",
        "",
        "> 本文件由 `tools/generate_code_markdown.py` 自动生成。内容是面向阅读的代码解说，不会替代源码注释或官方文档。",
        "",
    ]

    for index, segment in enumerate(segments, start=1):
        code = "".join(segment.lines).rstrip()
        if not code:
            continue

        parts.extend(
            [
                f"## 片段 {index}: {segment.title}",
                "",
                f"```{lang}",
                code,
                "```",
                "",
                f"**解说：** {explain_segment(segment, path)}",
                "",
            ]
        )

    return "\n".join(parts).rstrip() + "\n"


def split_file(path: Path) -> list[Segment]:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines(keepends=True)
    lang = language_for(path)

    if lang == "c":
        return split_c_like(lines)
    if lang == "asm":
        return split_simple(lines, "asm")
    return split_simple(lines, lang)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root.")
    parser.add_argument("--dry-run", action="store_true", help="Only print what would be generated.")
    args = parser.parse_args()

    root = args.root.resolve()
    files = iter_source_files(root)

    for source in files:
        target = source.with_name(source.name + ".md")
        if args.dry_run:
            print(target.relative_to(root).as_posix())
            continue

        segments = split_file(source)
        target.write_text(render_markdown(source, root, segments), encoding="utf-8", newline="\n")

    print(f"Generated {len(files)} markdown files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
