---
name: computer-use
description: |
  控制 Mac 电脑：截图查看屏幕、移动鼠标、点击、输入文字、打开应用。
  当用户说"帮我打开 XX"、"点击 XX"、"搜索 XX"、"操作我的电脑"、"帮我在屏幕上做 XX"、
  "截个屏看看"、"自动化这个操作"时触发。即使用户没说"computer use"，只要是需要操控
  屏幕/鼠标/键盘的任务都应触发此 skill。
---

# Computer Use（macOS 原生方案）

通过 `screencapture`、`cliclick`、`osascript` 三个工具实现完整的桌面控制能力。

## 前置依赖

### 必须安装

```bash
brew install cliclick
```

`screencapture` 和 `osascript` 是 macOS 内置工具，无需安装。

### 必须授权（系统设置 → 隐私与安全性）

| 权限 | 用途 | 授权对象 |
|------|------|---------|
| 屏幕录制 | `screencapture` 截图 | Terminal / iTerm2 |
| 辅助功能 | 鼠标点击、键盘输入 | Terminal / iTerm2 |

> 如果截图报错 `could not create image from display`，是屏幕录制权限未开；
> 如果点击/键盘没反应，是辅助功能权限未开。

---

## 核心工具速查

### 截图
```bash
screencapture -x /tmp/screen_$(date +%s).png
```
截图后用 Read 工具读取图片，可直接看到屏幕内容。`-x` 静默截图（不播放快门音）。

### 鼠标操作
```bash
cliclick p                # 获取当前鼠标坐标（返回 x,y）
cliclick m:960,540        # 移动到坐标（不点击）
cliclick c:960,540        # 左键单击
cliclick dc:960,540       # 左键双击
cliclick rc:960,540       # 右键单击
```

### 按键
```bash
cliclick kp:return        # 回车
cliclick kp:esc           # Escape（注意：是 esc 不是 escape）
cliclick kp:tab           # Tab
cliclick kp:space         # 空格
cliclick kp:delete        # 删除
cliclick kp:arrow-up      # 方向键
cliclick kp:page-down     # Page Down
```

### 键盘输入和组合键（重要：必须指定进程名）

**输入文字到指定应用** — 必须用 `tell process` 而不是 `tell application "System Events"` 直接发，否则输入会打到当前焦点应用（可能是 Terminal 自己）：

```bash
osascript -e '
tell application "System Events"
    tell process "Safari"
        keystroke "要输入的内容"
    end tell
end tell'
```

**常用组合键：**
```bash
# Cmd+L 聚焦地址栏
osascript -e 'tell application "System Events" to tell process "Safari" to keystroke "l" using command down'

# Cmd+A 全选
osascript -e 'tell application "System Events" to tell process "Safari" to keystroke "a" using command down'

# Cmd+C / Cmd+V
osascript -e 'tell application "System Events" to tell process "Safari" to keystroke "c" using command down'
osascript -e 'tell application "System Events" to tell process "Safari" to keystroke "v" using command down'

# 回车（key code 方式）
osascript -e 'tell application "System Events" to tell process "Safari" to key code 36'
```

---

## 激活应用并操作（关键模式）

单独用 `tell application "X" to activate` 在其他 App 抢占焦点时经常失效。
**正确做法**：activate + 设置窗口位置 + 通过 `tell process` 发送操作，三步合一：

```bash
osascript << 'EOF'
tell application "Safari"
    activate
    set bounds of front window to {200, 100, 1400, 900}
end tell
delay 0.8
tell application "System Events"
    tell process "Safari"
        set frontmost to true
        keystroke "l" using command down
        delay 0.3
        keystroke "a" using command down
        keystroke "搜索词"
        key code 36
    end tell
end tell
EOF
```

`set bounds` 会把窗口移到前面并调整大小，避免被其他窗口（包括 Claude Code 自己的窗口）遮挡。

---

## 感知-行动循环

```
1. screencapture → Read 读图，理解当前屏幕状态
2. 根据截图中元素位置，执行 cliclick 或 osascript 操作
3. sleep 0.5~1.5（等界面渲染完成）
4. 再次截图确认结果
5. 重复直到任务完成
```

**坐标定位：** macOS Retina 屏下截图分辨率是逻辑分辨率的 2 倍，但 `cliclick` 使用**逻辑坐标**，两者一致，不需要换算。

---

## 常见工作流

### 打开 Safari 搜索
```bash
osascript << 'EOF'
tell application "Safari"
    activate
    set bounds of front window to {200, 100, 1400, 900}
end tell
delay 0.8
tell application "System Events"
    tell process "Safari"
        set frontmost to true
        keystroke "l" using command down
        delay 0.3
        keystroke "a" using command down
        keystroke "搜索词"
        key code 36
    end tell
end tell
EOF
sleep 2
screencapture -x /tmp/result.png
```

### 点击屏幕上某个元素
```bash
# 先截图找坐标
screencapture -x /tmp/s.png
# 分析图片后点击
cliclick c:x,y
sleep 0.3
screencapture -x /tmp/after.png  # 确认结果
```

### 在输入框中输入内容
```bash
cliclick c:x,y   # 点击输入框获取焦点
sleep 0.2
osascript -e 'tell application "System Events" to tell process "AppName" to keystroke "输入内容"'
```

### 查看当前运行的应用
```bash
osascript -e 'tell application "System Events" to get name of every process whose visible is true'
```

---

## 注意事项

- 每次操作后 `sleep 0.3~1.5` 再截图，给界面渲染留时间
- 涉及发送消息、删除文件等不可逆操作，先截图给用户确认再执行
- 进程名（`tell process "Safari"`）用英文名，不是中文应用名
- 如果不知道进程名，先用上面的「查看当前运行的应用」命令查
