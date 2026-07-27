# skill-samectx

TRAE/Cursor 上下文同步技能 - 智能分析对话并生成 samectx 命令

[English](#english-version)

## 简介

这是一个 TRAE/Cursor SKILL，用于智能分析对话内容，提取关键信息，并生成 `samectx` npm 工具命令，帮助用户保存对话上下文到本地项目目录，支持多用户协作和跨设备同步。

## 核心功能

- 🤖 **智能分析**：自动识别对话中的关键任务、关键点和关键决策
- 📝 **命令生成**：根据分析结果生成带参数的 `samectx sync` 命令
- 🌍 **双语支持**：同时支持中文和英文对话
- 🚀 **用户友好**：提供清晰的提示和命令示例
- 🔄 **跨设备同步**：支持通过 Git 实现跨设备同步

## 与 npm-samectx 的关系

- **npm-samectx**：核心功能实现，提供实际的上下文保存和管理功能
- **skill-samectx**：智能助手，分析对话并生成相应的 npm 命令

## 工作原理

1. **触发**：当对话中包含相关关键词或内容时，技能自动激活
2. **分析**：分析对话内容，提取关键任务、关键点和关键决策
3. **生成**：生成带参数的 `samectx sync` 命令
4. **提示**：向用户显示分析结果和执行命令
5. **执行**：用户复制并执行命令，保存上下文到本地

## 安装

### 1. 安装依赖

```bash
# 全局安装 samectx npm 包
npm install -g samectx
```

### 2. 安装技能

将此 SKILL 目录添加到 TRAE 或 Cursor 的 skills 目录：

```bash
# 克隆仓库
git clone https://github.com/ethanhuangcst/skill-samectx.git

# 添加到 TRAE skills 目录
cp -r skill-samectx ~/.trae/skills/

# 或添加到 Cursor skills 目录
cp -r skill-samectx ~/.cursor/skills/
```

## 使用

### 触发场景

SKILL 会在以下场景自动触发：

- 用户提到「保存上下文」、「同步笔记」、「记录对话」等关键词
- 对话中包含明确的任务、决策或技术讨论
- 用户直接请求保存当前对话

### 示例

**场景 1：基本同步**

用户：「我需要保存这次对话的内容」

技能会生成：
```bash
samectx sync
```

**场景 2：带参数同步**

用户：「我们需要实现用户登录功能，使用 JWT 进行认证，选择 bcrypt 加密密码」

技能会生成：
```bash
samectx sync --tasks "实现用户登录功能" --keypoints "使用JWT进行认证" --decisions "选择bcrypt加密密码"
```

## 技能文件结构

- **skill.md**：技能主文件，包含完整的技能逻辑和功能
- **skills/**：包含各子技能文件
  - **config.md**：配置管理提示
  - **init.md**：初始化提示
  - **install.md**：安装引导
  - **sync.md**：同步提示

## 技术依赖

- **npm 包**：`samectx` (全局安装)
- **Node.js**：>= 14.0.0
- **Git**：用于跨设备同步

## 注意事项

- 笔记将保存在项目目录的 `samectx-notes/{username}/` 文件夹中
- 建议将笔记目录提交到 Git 仓库以支持跨设备同步
- 请勿在笔记中包含敏感信息（密码、密钥等）

## 故障排除

- **用户名识别错误**：运行 `samectx config --username <name>` 设置用户名
- **笔记位置错误**：检查当前工作目录或使用 `-d` 参数指定目录
- **Git 冲突**：手动解决冲突，保留各自的笔记文件

## 相关链接

- **npm 包**：https://github.com/ethanhuangcst/npm-samectx
- **npm 发布**：https://www.npmjs.com/package/samectx

## 许可证

MIT

## 作者

ethanhuangcst

## 版本

- **技能版本**：1.0.0
- **最后更新**：2026-03-23

---

## <a name="english-version"></a>English Version

[中文](#skill-samectx)

# skill-samectx

TRAE/Cursor Context Sync Skill - Intelligent conversation analysis and samectx command generation

## Introduction

This is a TRAE/Cursor SKILL that intelligently analyzes conversation content, extracts key information, and generates `samectx` npm tool commands to help users save conversation context to local project directories, supporting multi-user collaboration and cross-device synchronization.

## Core Features

- 🤖 **Intelligent Analysis**：Automatically identifies key tasks, key points, and key decisions in conversations
- 📝 **Command Generation**：Generates parameterized `samectx sync` commands based on analysis results
- 🌍 **Bilingual Support**：Supports both Chinese and English conversations
- 🚀 **User-Friendly**：Provides clear prompts and command examples
- 🔄 **Cross-Device Sync**：Supports cross-device synchronization via Git

## Relationship with npm-samectx

- **npm-samectx**：Core functionality implementation, providing actual context saving and management features
- **skill-samectx**：Intelligent assistant that analyzes conversations and generates corresponding npm commands

## Working Principle

1. **Trigger**：The skill automatically activates when conversations contain relevant keywords or content
2. **Analysis**：Analyzes conversation content to extract key tasks, key points, and key decisions
3. **Generation**：Generates parameterized `samectx sync` commands
4. **Prompt**：Displays analysis results and execution commands to the user
5. **Execution**：User copies and executes the command to save context locally

## Installation

### 1. Install Dependencies

```bash
# Install samectx npm package globally
npm install -g samectx
```

### 2. Install the Skill

Add this SKILL directory to TRAE or Cursor's skills directory：

```bash
# Clone the repository
git clone https://github.com/ethanhuangcst/skill-samectx.git

# Add to TRAE skills directory
cp -r skill-samectx ~/.trae/skills/

# Or add to Cursor skills directory
cp -r skill-samectx ~/.cursor/skills/
```

## Usage

### Trigger Scenarios

The SKILL automatically triggers in the following scenarios：

- User mentions keywords like "save context", "sync notes", "record conversation", etc.
- Conversation contains clear tasks, decisions, or technical discussions
- User directly requests to save the current conversation

### Examples

**Scenario 1: Basic Sync**

User: "I need to save the content of this conversation"

The skill will generate：
```bash
samectx sync
```

**Scenario 2: Sync with Parameters**

User: "We need to implement user login functionality, use JWT for authentication, and choose bcrypt for password encryption"

The skill will generate：
```bash
samectx sync --tasks "Implement user login functionality" --keypoints "Use JWT for authentication" --decisions "Choose bcrypt for password encryption"
```

## Skill File Structure

- **skill.md**：Main skill file containing complete skill logic and functionality
- **skills/**：Contains sub-skill files
  - **config.md**：Configuration management prompts
  - **init.md**：Initialization prompts
  - **install.md**：Installation guidance
  - **sync.md**：Synchronization prompts

## Technical Dependencies

- **npm package**：`samectx` (globally installed)
- **Node.js**：>= 14.0.0
- **Git**：for cross-device synchronization

## Notes

- Notes will be saved in the `samectx-notes/{username}/` folder in the project directory
- It is recommended to commit the notes directory to the Git repository to support cross-device synchronization
- Do not include sensitive information (passwords, keys, etc.) in notes

## Troubleshooting

- **Username recognition error**：Run `samectx config --username <name>` to set the username
- **Note location error**：Check the current working directory or use the `-d` parameter to specify a directory
- **Git conflict**：Manually resolve conflicts and keep each user's notes files

## Related Links

- **npm package**：https://github.com/ethanhuangcst/npm-samectx
- **npm publication**：https://www.npmjs.com/package/samectx

## License

MIT

## Author

ethanhuangcst

## Version

- **Skill version**：1.0.0
- **Last updated**：2026-03-23