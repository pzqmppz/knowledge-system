# 口播稿自动监听脚本

自动监听 `E:\n8n_work\output\播客口播稿\` 目录，检测到新文件后提示执行 voiceover-xray 拆解。

拆解报告输出到 `知识体系/拆解报告/口播稿/` 目录。

## 文件说明

| 文件 | 说明 |
|------|------|
| `watch_voiceover.py` | 监听脚本主程序 |
| `watch_voiceover_start.bat` | Windows 启动器 |
| `watch_voiceover_start.sh` | Linux/Mac 启动器 |
| `watch_voiceover_requirements.txt` | Python 依赖 |
| `watch_voiceover_processed.json` | 已处理文件记录（自动生成） |
| `watch_voiceover.log` | 运行日志（自动生成） |
| `README.md` | 使用说明（本文件） |

## 快速开始

### Windows

双击运行 `watch_voiceover_start.bat`

### Linux/Mac

```bash
cd .Claude/scripts/
chmod +x watch_voiceover_start.sh
./watch_voiceover_start.sh
```

## 工作原理

```
新文件出现 → 等待2秒确认稳定 → 检查历史记录 → 提示执行命令 → 标记为已处理
```

脚本会检测以下文件类型：`.md`, `.txt`, `.docx`

## 防止重复执行

脚本使用 **持久化记录** 来避免重复处理同一个文件：

1. 所有已处理的文件会被记录到 `watch_voiceover_processed.json`
2. 脚本重启后会自动加载历史记录
3. 即使文件被重新写入，只要记录存在就不会重复处理
4. 超过 30 天的旧记录会自动清理

## 命令行工具

```bash
# 启动监听
python watch_voiceover.py

# 列出所有已处理的文件
python watch_voiceover.py list

# 清空所有处理记录（谨慎使用！）
python watch_voiceover.py clear

# 清理指定天数前的记录（默认30天）
python watch_voiceover.py cleanup 30
```

## 配置

编辑 `watch_voiceover.py` 中的配置项：

```python
# 监听目录
WATCH_DIR = Path(r"E:\n8n_work\output\播客口播稿")

# 输出目录（仅用于日志显示）
OUTPUT_DIR = Path(...) / "拆解报告" / "口播稿"

# 支持的文件扩展名
SUPPORTED_EXTENSIONS = {".md", ".txt", ".docx"}

# 文件稳定等待时间（秒）
STABLE_WAIT = 2

# 记录保留天数（超过此天数的记录会被清理）
RECORD_RETENTION_DAYS = 30
```

## 记录文件格式

`watch_voiceover_processed.json` 示例：

```json
{
  "E:\\n8n_work\\output\\播客口播稿\\example.md": {
    "timestamp": 1742012345.123,
    "processed_at": "2026-03-13T12:34:56.789012",
    "file_name": "example.md"
  }
}
```

## 注意事项

1. 脚本只**提示**命令，需要在 Claude Code 中手动执行
2. 已处理的文件会被永久记录（直到清理）
3. 如需重新处理某个文件，使用 `python watch_voiceover.py clear` 清空记录
4. 日志会同时输出到控制台和 `watch_voiceover.log` 文件
5. 按 `Ctrl+C` 停止监听

## 故障排查

### 依赖安装失败

```bash
pip install watchdog
```

### 目录不存在

确保监听目录 `E:\n8n_work\output\播客口播稿\` 存在。

### 文件未被检测

1. 检查文件扩展名是否在支持列表中
2. 检查日志文件 `watch_voiceover.log`
3. 查看历史记录：`python watch_voiceover.py list`

### 需要重新处理文件

```bash
# 方式1：清空所有记录
python watch_voiceover.py clear

# 方式2：手动编辑 JSON 文件删除特定记录
# 编辑 watch_voiceover_processed.json
```

---

*创建时间: 2026-03-13*
*最后更新: 2026-03-13*
