# QuickAdd 每日摘抄 - 导入指南

## 一、安装 QuickAdd 插件

1. 打开 Obsidian 设置 (`Ctrl + ,`)
2. 点击 **社区插件** → **浏览**
3. 搜索 `QuickAdd` → 安装并启用

---

## 二、导入配置文件

### 方法 A：手动复制（推荐）

1. 打开项目目录下的 `.obsidian/plugins/quickadd/data.json` 文件
2. 用记事本或代码编辑器打开
3. 复制下面的内容，**替换整个文件内容**：

```json
{
  "choices": [
    {
      "id": "daily-excerpt-20260313",
      "name": "每日摘抄",
      "type": "Capture",
      "command": false,
      "captureToActiveFile": false,
      "createInSamePaneAsActiveFile": false,
      "captureTo": "摘抄笔记/{{DATE:YYYY-MM}}/{{DATE:YYYY-MM-DD}}-摘抄.md",
      "captureFormat": "\n\n## {{TIME}} 摘抄\n\n**来源**：[[{{active_filepath}}]]\n\n> {{selection}}\n\n**我的思考**：\n\n\n---",
      "insertAfter": {
        "insertAfterWhere": {
          "path": "摘抄笔记/{{DATE:YYYY-MM}}/{{DATE:YYYY-MM-DD}}-摘抄.md",
          "newline": true
        },
        "createIfNotFound": true,
        "appendToEndOf": "file"
      },
      "prepend": false,
      "task": false,
      "openFileInNewTab": {
        "enabled": false,
        "focus": true
      }
    }
  ],
  "macros": []
}
```

4. 保存文件，重启 Obsidian

---

### 方法 B：通过 Obsidian 导入

1. 在 Obsidian 中打开 `QuickAdd-每日摘抄.json` 文件
2. 全选复制内容
3. 打开 `设置` → `QuickAdd` → `Manage Choices`
4. 点击 `Import/Export` → `Import`
5. 粘贴内容并确认

---

## 三、设置快捷键

1. 打开 `设置` → `快捷键`
2. 搜索 `QuickAdd: Run Choice`
3. 找到 `每日摘抄`，设置快捷键（如 `Ctrl + Shift + Q`）

---

## 四、使用方法

1. 选中要摘抄的文字
2. 按 `Ctrl + Shift + Q`
3. 自动追加到当天摘抄文件

---

*配置文件位置：`摘抄笔记/QuickAdd-每日摘抄.json`*
