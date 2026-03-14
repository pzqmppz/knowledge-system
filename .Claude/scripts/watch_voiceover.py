#!/usr/bin/env python3
"""
口播稿自动监听脚本
监听指定目录，新文件写入完成后提示执行 voiceover-xray 拆解
"""

import os
import sys
import time
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ============ 配置 ============

# 监听目录
WATCH_DIR = Path(r"E:\n8n_work\output\播客口播稿")

# 输出目录（仅用于日志显示）
OUTPUT_DIR = Path(__file__).parent.parent.parent / "拆解报告" / "口播稿"

# 支持的文件扩展名
SUPPORTED_EXTENSIONS = {".md", ".txt", ".docx"}

# 文件稳定等待时间（秒），确保文件写入完成
STABLE_WAIT = 2

# 日志配置
LOG_FILE = Path(__file__).parent / "watch_voiceover.log"

# 已处理文件记录
PROCESSED_FILE = Path(__file__).parent / "watch_voiceover_processed.json"

# 记录保留天数（超过此天数的记录会被清理）
RECORD_RETENTION_DAYS = 30

# ============ 日志设置 ============

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


# ============ 持久化管理器 ============

class ProcessedManager:
    """已处理文件持久化管理器"""

    def __init__(self, record_file: Path):
        self.record_file = record_file
        self.records = {}  # {file_path: {"timestamp": str, "processed_at": str}}
        self.load()

    def load(self):
        """从文件加载已处理记录"""
        if self.record_file.exists():
            try:
                with open(self.record_file, "r", encoding="utf-8") as f:
                    self.records = json.load(f)
                logger.info(f"已加载 {len(self.records)} 条历史记录")
            except Exception as e:
                logger.warning(f"加载记录文件失败: {e}，将创建新记录")
                self.records = {}
        else:
            logger.info("记录文件不存在，将创建新记录")
            self.records = {}

    def save(self):
        """保存已处理记录到文件"""
        try:
            with open(self.record_file, "w", encoding="utf-8") as f:
                json.dump(self.records, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存记录文件失败: {e}")

    def is_processed(self, file_path: Path) -> bool:
        """检查文件是否已处理"""
        path_str = str(file_path)
        if path_str in self.records:
            logger.debug(f"文件已处理，跳过: {file_path.name}")
            return True
        return False

    def mark_processed(self, file_path: Path):
        """标记文件为已处理"""
        path_str = str(file_path)
        self.records[path_str] = {
            "timestamp": time.time(),
            "processed_at": datetime.now().isoformat(),
            "file_name": file_path.name
        }
        self.save()

    def cleanup_old_records(self, days: int = RECORD_RETENTION_DAYS):
        """清理超过指定天数的旧记录"""
        cutoff_time = time.time() - (days * 24 * 3600)
        old_count = len(self.records)

        to_remove = [
            path for path, record in self.records.items()
            if record.get("timestamp", 0) < cutoff_time
        ]

        for path in to_remove:
            del self.records[path]

        removed_count = len(to_remove)
        if removed_count > 0:
            self.save()
            logger.info(f"清理了 {removed_count} 条超过 {days} 天的旧记录")

    def clear_all(self):
        """清空所有记录"""
        self.records = {}
        self.save()
        logger.info("已清空所有处理记录")

    def list_processed(self) -> list:
        """列出所有已处理的文件"""
        return [
            {
                "path": path,
                "name": record.get("file_name", Path(path).name),
                "processed_at": record.get("processed_at", "unknown")
            }
            for path, record in self.records.items()
        ]


# ============ 文件处理器 ============

class VoiceoverHandler(FileSystemEventHandler):
    """口播稿文件事件处理器"""

    def __init__(self, processed_manager: ProcessedManager):
        super().__init__()
        self.processed_manager = processed_manager
        # 记录文件创建时间，用于判断文件是否稳定
        self.file_timers = {}

    def on_created(self, event):
        """文件创建事件"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # 检查文件扩展名
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            logger.debug(f"跳过不支持的文件类型: {file_path.name}")
            return

        # 检查是否已处理
        if self.processed_manager.is_processed(file_path):
            logger.info(f"文件已在历史记录中，跳过: {file_path.name}")
            return

        # 检查是否正在监听
        if str(file_path) in self.file_timers:
            return

        logger.info(f"检测到新文件: {file_path.name}")

        # 设置定时器，等待文件稳定
        self.file_timers[str(file_path)] = time.time()

    def on_modified(self, event):
        """文件修改事件"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # 只关注正在监听的文件
        if str(file_path) in self.file_timers:
            # 更新修改时间
            self.file_timers[str(file_path)] = time.time()
            logger.debug(f"文件写入中，更新时间: {file_path.name}")

    def check_stable_files(self):
        """检查是否有文件已稳定（停止写入）"""
        current_time = time.time()
        stable_files = []

        for file_path_str, last_modified in list(self.file_timers.items()):
            # 检查文件是否稳定（超过设定时间没有变化）
            if current_time - last_modified >= STABLE_WAIT:
                file_path = Path(file_path_str)

                # 确保文件存在且不为空
                if file_path.exists() and file_path.stat().st_size > 0:
                    stable_files.append(file_path)
                    del self.file_timers[file_path_str]

        return stable_files

    def process_file(self, file_path: Path):
        """处理文件：提示执行 voiceover-xray 命令"""
        if self.processed_manager.is_processed(file_path):
            return

        logger.info(f"文件已稳定，准备处理: {file_path.name}")
        logger.info("=" * 60)
        logger.info(f"请在 Claude Code 中执行以下命令:")
        logger.info(f"  /voiceover-xray \"{file_path}\"")
        logger.info("=" * 60)

        # 标记为已处理
        self.processed_manager.mark_processed(file_path)
        logger.info(f"已标记为已处理: {file_path.name}")


# ============ 主程序 ============

def main():
    """主函数"""
    print("=" * 60)
    print("口播稿自动监听脚本")
    print("=" * 60)
    print(f"监听目录: {WATCH_DIR}")
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"支持格式: {', '.join(SUPPORTED_EXTENSIONS)}")
    print(f"日志文件: {LOG_FILE}")
    print(f"记录文件: {PROCESSED_FILE}")
    print("=" * 60)
    print("监听中... (按 Ctrl+C 停止)")
    print()

    # 检查目录是否存在
    if not WATCH_DIR.exists():
        logger.error(f"监听目录不存在: {WATCH_DIR}")
        logger.info("请先创建目录或检查路径配置")
        sys.exit(1)

    # 创建持久化管理器
    processed_manager = ProcessedManager(PROCESSED_FILE)

    # 清理旧记录
    processed_manager.cleanup_old_records()

    # 创建事件处理器
    event_handler = VoiceoverHandler(processed_manager)

    # 创建观察者
    observer = Observer()
    observer.schedule(event_handler, str(WATCH_DIR), recursive=False)

    # 启动监听
    observer.start()

    try:
        while True:
            time.sleep(1)

            # 检查是否有稳定的文件需要处理
            stable_files = event_handler.check_stable_files()

            for file_path in stable_files:
                event_handler.process_file(file_path)

    except KeyboardInterrupt:
        logger.info("收到停止信号，正在关闭...")
        observer.stop()
    except Exception as e:
        logger.error(f"发生错误: {e}", exc_info=True)
        observer.stop()

    observer.join()
    logger.info("监听已停止")


# ============ 命令行工具 ============

def cmd_list():
    """列出所有已处理的文件"""
    manager = ProcessedManager(PROCESSED_FILE)

    print("\n" + "=" * 60)
    print("已处理文件列表")
    print("=" * 60)

    processed_list = manager.list_processed()

    if not processed_list:
        print("暂无已处理文件")
    else:
        for i, item in enumerate(processed_list, 1):
            print(f"\n{i}. {item['name']}")
            print(f"   处理时间: {item['processed_at']}")
            print(f"   文件路径: {item['path']}")

    print(f"\n总计: {len(processed_list)} 个文件")
    print("=" * 60)


def cmd_clear():
    """清空所有处理记录"""
    manager = ProcessedManager(PROCESSED_FILE)
    manager.clear_all()


def cmd_cleanup(days: int = None):
    """清理指定天数前的记录"""
    if days is None:
        days = RECORD_RETENTION_DAYS

    manager = ProcessedManager(PROCESSED_FILE)
    manager.cleanup_old_records(days)


if __name__ == "__main__":
    # 支持命令行参数
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "list":
            cmd_list()
        elif command == "clear":
            cmd_clear()
        elif command == "cleanup":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else None
            cmd_cleanup(days)
        else:
            print(f"未知命令: {command}")
            print("\n可用命令:")
            print("  python watch_voiceover.py        # 启动监听")
            print("  python watch_voiceover.py list   # 列出已处理文件")
            print("  python watch_voiceover.py clear  # 清空所有记录")
            print("  python watch_voiceover.py cleanup [days]  # 清理旧记录")
    else:
        main()
