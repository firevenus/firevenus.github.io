---
title: 想用AI写完文章之后直接发到微信，该怎么做？
description: 14个微信公众号MCP Server全景对比与选型建议
date: 2026-08-01
author: Enki Yan
tags: [MCP, 微信公众号, AI, 工具选型]
---

> 本文复盘了一次完整的微信公众号 MCP Server 选型过程：从 GitHub/Gitee 搜到 14 个相关项目，逐一拆解功能矩阵，到最终基于实测体验选出 5 个活跃项目，推荐两个组合方案。如果你也想用 AI 写完文章后一句话发到公众号草稿箱，这篇能帮你少走弯路。

> 以下是目前 AI 能找到的几个用 AI 把文章直接发布到微信公众号草稿箱的 MCP，如有遗漏，欢迎大家补充。如果有任何对于功能改进上的建议，也随时欢迎大家提出。

---

## 一、为什么需要 MCP？为什么只能发到草稿箱？

微信公众号后台的编辑器已支持导入 Markdown 文件，但仅限于基础的格式转换，没有主题美化、素材管理、草稿 CRUD 等能力。而通过 API 发草稿需要处理 access_token、multipart 上传、内联 CSS 等一堆细节。对于用 AI 助手辅助写作的人来说，"写完 Markdown → 一句话发到草稿箱、带主题排版、自动上传封面"才是最自然的流程。

MCP（Model Context Protocol）让 AI 助手直接调用工具完成任务。于是问题变成：**哪个 MCP Server 能用？**

答案是：没有一个能打的——但拼起来可以。

**那为什么只能发到草稿箱，不能直接发布？**

两方面原因：

**第一，微信公众号 API 本身的限制。** 微信公众号的 `freepublish`（发布到公开）接口有权限门槛——未认证的订阅号调用会直接返回 48001 错误（api unauthorized），根本发不出去。即使公众号已完成认证，部分接口也仅对服务号开放。所以对于大多数个人运营者来说，通过 API "直接发布"在技术层面就走不通，只能调 `draft/add` 接口把文章先存进草稿箱。

**第二，AI 写完的文章需要人工再审核一遍。** AI 辅助写作虽然效率高，但难免出现事实偏差、措辞不当、排版错位、封面图不匹配等问题。把文章发到草稿箱而不是直接发布，相当于留了一道人工把关的工序——在公众号后台预览确认无误后，手动点击"群发"即可。这不是能力不够，而是工作流设计上最合理的一步：**AI 负责把活干到 90%，人负责最后那 10% 的把关。**

---

## 二、14 个项目全景扫描

在 GitHub 和 Gitee 上搜索"微信公众号 MCP""WeChat Official Account MCP""markdown to wechat"等关键词，共发现 **14 个相关项目**，按功能定位分为三类：

### A 类：排版 + 发草稿（有主题美化）

| # | 项目名 | Repo | 语言 | 最近更新 |
|---|---|---|---|---|
| 1 | **文颜 MCP** | github.com/caol64/wenyan-mcp | TypeScript | 2026-04 |
| 2 | **markdown2wechat** | github.com/maricoxu/markdown2wechat-mcp | TypeScript (Fork) | 2025-11 |
| 3 | **夏颜 MCP** | github.com/herofox2024/xiayan-mcp | Python | 2025-12 |
| 4 | **floodsung/wenyan-mcp** | github.com/floodsung/wenyan-mcp | TypeScript (Fork) | 2026-02 |
| 5 | **md2wechat-mcp-server** | github.com/geekjourneyx/md2wechat-mcp-server | Go | 2025-06 |

### B 类：API 全功能管理（草稿 CRUD + 发布 + 素材）

| # | 项目名 | Repo | 语言 | 最近更新 |
|---|---|---|---|---|
| 6 | **wechat-official-account-mcp** | github.com/xwang152-jack/wechat-official-account-mcp | TypeScript | 2026-05 |
| 7 | **oukanghua/wechat_official_account_mcp** | github.com/oukanghua/wechat_official_account_mcp | Python | 2026-05 |
| 8 | **kakaxi3019/wechat_oa_api_mcp** | github.com/kakaxi3019/wechat_oa_api_mcp | Python | 2025-11 |
| 9 | **tc6-01/weixin-mcp** | github.com/tc6-01/weixin-mcp | Go | 2025-06 |
| 10 | **wechat-publisher-mcp** | github.com/BobGod/wechat-publisher-mcp | JavaScript | 2025-07 |
| 11 | **GongZhongHao_MCP** | github.com/yikaikkk/GongZhongHao_MCP | Go | 2025-10 |

### C 类：多平台同步 / Agent Skill / CLI

| # | 项目名 | Repo | 类型 | 最近更新 |
|---|---|---|---|---|
| 12 | **Wechatsync** | github.com/wechatsync/Wechatsync | 浏览器扩展 + CLI + MCP | 2026-05 |
| 13 | **md2wechat-skill** | github.com/geekjourneyx/md2wechat-skill | CLI + Agent Skill | 2026-07 |
| 14 | **md2wechat-lite** | github.com/geekjourneyx/md2wechat-lite | CLI | 2026-02 |

> **特别说明**：⑬ md2wechat-skill 虽列在 C 类，但实际能力远超 CLI 工具定位——它同时具备排版（48 专业主题 + 60 项排版语法）、发草稿、AI 配图、多账号管理、小绿书等能力，是 14 个项目中功能覆盖面最广的。之所以单列，是因为它不是传统 MCP Server（stdio/http 协议），而是面向 AI Agent 的 CLI 工具（JSON 契约），集成方式不同。详见第四章专项分析。

Gitee 上有文颜 MCP 的两个镜像（lfslfs/WXgzh-mcp 和 li_jian-Lee/WXgzh-mcp），均为 fork，不单独评测。

---

## 三、功能矩阵：谁有什么

把 11 个核心 MCP Server 和 md2wechat-skill 放进一张功能矩阵，横向对比：

| 功能维度 | ①文颜 | ②md2wechat | ③夏颜 | ⑤md2wechat-go | ⑥woa-mcp | ⑦oukanghua | ⑧kakaxi | ⑩publisher | ⑬md2wechat-skill |
|---|---|---|---|---|---|---|---|---|---|
| **主题排版** | 7套+自定义 | 7套(同文颜) | 8套+自定义 | 4套 | ❌ | ❌ | ❌ | 基础HTML | **48套+60项语法** |
| **Mermaid图表** | ✅ | ✅+手绘风格 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 未明确 |
| **代码高亮** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | 未明确 |
| **发草稿** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅(直接发布) | ✅ |
| **草稿查询** | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| **草稿删除** | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **草稿更新** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| **正式发布** | ❌ | ❌ | ❌ | ❌ | ✅ submit | ✅ | ✅ | ✅ | ❌ |
| **素材上传** | ✅ 图片 | ✅+COS | ✅ 临时/永久 | ❌ | ✅ 临时/永久 | ✅ 临时/永久 | ❌ | ✅ 封面 | ✅ 图片 |
| **素材管理** | ❌ | ❌ | ✅ CRUD | ❌ | ✅ CRUD | ✅ CRUD | ✅ 删除 | ❌ | ❌ |
| **封面图自动生成** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ 智能配色 | ✅ **AI配图** |
| **小绿书(图片消息)** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **多公众号** | ✅ Server模式 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **远程Server(绕IP白名单)** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ 固定出口IP |
| **Agent原生设计** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ **6+Agent平台** |
| **批量发布** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Brand Profile** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **预览/检查** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ 预览 | ✅ **inspect** |
| **Docker** | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | 静态二进制 |
| **开源协议** | Apache-2.0 | Apache-2.0 | Apache-2.0 | MIT | MIT | 未标注 | 未标注 | 未标注 | **BUSL-1.1** |

> 注：④floodsung、⑨tc6-01、⑪GZH_MCP 因功能基础或不成熟，从矩阵中移除以节省篇幅。⑬md2wechat-skill 的免费模式仅含 3 个基础主题，48 个专业主题需 API/专业模式。

**一句话总结这张表：⑬md2wechat-skill 排版能力最强（48 主题 + AI 配图 + Agent 原生），但许可证非开源、免费版主题少、无草稿管理。文颜 + woa-mcp 组合则是开源生态下覆盖面最广的方案。**

---

## 四、关键项目逐一拆解

### 排版之王：文颜 MCP（①）

1.3k star，社区最活跃，功能最全的排版 MCP。7+ 主题 + 自定义 CSS、Mermaid 转图、小绿书、远程 Server 模式（绕 IP 白名单）、多公众号管理、Docker 部署。

**短板致命**：只能 Create 草稿，不能查、改、删；不能正式发布；没有素材 CRUD。也就是说，发完草稿之后的所有管理操作都得去公众号后台手动做。

### Mermaid 增强：markdown2wechat（②）

在文颜基础上 fork，增加了 Mermaid→图片自动转换（含手绘风格）和腾讯云 COS 图床。思路好，但依赖重（puppeteer/Chrome/sharp），Windows 安装容易踩坑。同样没有草稿 CRUD 和发布。

### Python 生态：夏颜 MCP（③）

Python 实现，10 个 MCP 工具，有主题预览、自定义主题 CRUD、素材 CRUD。8 套主题。社区小，无 Mermaid，无正式发布。如果你更习惯 Python 生态，这是 A 类里唯一有素材管理的。

### API 管理之王：wechat-official-account-mcp（⑥）

TypeScript，MIT 协议。草稿 Create/Read/Delete、正式发布（submit）、素材 CRUD、SQLite 本地存储、AES 加密敏感字段、日志脱敏。功能完整度在 B 类里最高。

**短板同样致命**：完全没有排版/主题系统，发的是原始 HTML，文章在公众号里显示就是一坨没有样式的文字。

### 全家桶：oukanghua/wechat_official_account_mcp（⑦）

FastMCP 2.0，功能最多：草稿 CRUD + 发布 + 状态查询 + AI 聊天 + 静态网页生成 + S3 存储 + Docker。但功能多而杂，Python 依赖重，同样没有排版。

### 封面自动生成：wechat-publisher-mcp（⑩）

唯一有封面图自动生成（智能配色 PNG）和预览模式（发预览给指定 OpenID）的项目。还能查发布后数据（阅读/点赞/评论/分享）。但无草稿管理、无素材管理、无主题排版。

### 精简安全：kakaxi/wechat_oa_api_mcp（⑧）

5 个工具精简，内置限流和 Token 缓存。安全性考虑多。但无排版、无素材上传，功能最少。

### 不推荐的：⑪GongZhongHao_MCP

作者自述"功能未完全测试"，3 次提交，不成熟。

### 全能选手：md2wechat-skill（⑬）

Go 实现，274 次提交，2026 年 7 月仍在活跃更新。是 14 个项目中功能覆盖面最广的：48 个专业主题 + 60 项排版语法（`:::module` 系列）、AI 配图（封面 + 信息图，支持多 provider）、发草稿、多账号管理、小绿书、批量发布、Brand Profile（长期风格记忆）、inspect 发布前检查。

最大亮点是**Agent 原生设计**——不是通用工具改成 Agent 能用，而是从头为 Agent 调用优化的 CLI：JSON 单行紧凑输出、固定命令边界、6+ Agent 平台兼容（Claude Code、Codex、WorkBuddy、Kimi Work 等），还有专门的 WORKBUDDY.md 集成文档。

**短板需要正视**：
1. **许可证 BUSL-1.1**（Source Available，非开源）——个人/学习/非营利免费，商业使用需授权。与文颜(Apache-2.0)、woa-mcp(MIT) 的完全开源不同。
2. **免费模式主题少**——免费 AI 模式仅 3 个基础主题，且不直接返回 HTML（需外部 LLM 处理）；48 个专业主题需 API/专业模式。
3. **无草稿管理**——和文颜一样只能 Create，不能查/改/删草稿。
4. **无正式发布**——只发草稿，不能 submit 到公开。
5. Mermaid 和代码高亮未在 README 中明确说明。

---

## 五、实测开发过程：从踩坑到封装 Skill

在对比过程中，我实际安装了 3 个 MCP Server 并测试：

### 5.1 安装与配置

通过 `~/.workbuddy/.mcp.json` 配置了三个 Server：

```json
{
  "mcpServers": {
    "wenyan-mcp": { "command": "npx", "args": ["-y", "wenyan-mcp"] },
    "wechat-official-account-mcp": { "command": "npx", "args": ["-y", "@anthropic/wechat-official-account-mcp"] },
    "markdown2wechat": { "command": "node", "args": ["./markdown2wechat-mcp/dist/index.js"] }
  }
}
```

### 5.2 实测发现的坑

| 坑 | 项目 | 原因 | 解决 |
|---|---|---|---|
| IP 白名单 40164 | 所有项目 | 服务器出口 IP 不在白名单 | `curl ifconfig.me` 查出口 IP，加入白名单 |
| 未认证订阅号 48001 | woa-mcp | `freepublish`（发布到公开）需要认证 | 改用 `draft/add`，只发草稿 |
| marked v15 兼容 | 自己写的脚本 | `marked.parse()` 返回 `[object Object]` | 检测输出，abort 并提示 |
| 微信不支持 `<style>` | 所有项目 | 只接受内联样式 | 用正则后处理，给每个标签加 `style=""` |
| 文章正文图片 | 自己写的脚本 | 本地图片路径微信无法访问 | 需先调 `uploadimg` API 上传获取微信 URL |
| Node.js inline 脚本语法 | 自己写的脚本 | `data += chunk` 缺分号导致解析错误 | 改为 `(chunk) => { data += chunk; }` |

### 5.3 从脚本到 Skill 的封装

踩完坑后，我把完整流程封装成了一个可复用的 Skill（`wechat-draft-publisher`），核心是一个参数化 Node.js 脚本 `publish_draft.js`，流程：

```
读取 Markdown → marked 转 HTML → 正则后处理加内联样式 → 
（可选）生成占位封面 PNG → 获取 access_token → 
上传封面素材获取 media_id → 创建草稿 → 完成
```

脚本支持以下参数，全部命令行传入，不再硬编码：

| 参数 | 说明 |
|---|---|
| `--article` | Markdown 文件路径 |
| `--title` | 文章标题 |
| `--author` | 作者名 |
| `--digest` | 摘要（不传自动截取前 120 字） |
| `--cover` | 封面图路径（不传生成纯色占位图） |
| `--appid` / `--secret` | 凭证（或从环境变量/mcp.json 读取） |
| `--dry-run` | 只转 HTML 不调 API |
| `--output` | HTML 输出到文件 |

**关键设计决策：**

1. **零外部依赖渲染封面**：占位封面用纯 Node.js Buffer 手写 PNG 编码（zlib + CRC32），不依赖 sharp/canvas，避免安装问题。
2. **内联 CSS 用正则后处理**：不引入复杂排版引擎，`marked.parse()` 输出标准 HTML 后，用正则给每个标签注入 `style` 属性。样式参考文颜默认主题调色。
3. **dry-run 模式**：先看 HTML 效果再决定是否调 API，避免浪费 API 调用配额。
4. **凭证读取优先级**：命令行参数 > 环境变量 > `~/.workbuddy/.mcp.json`。这样在 AI 助手对话里可以自动从配置文件读取，不用每次手动输入。

### 5.4 Skill 验证

用 `--dry-run` 模式跑了一篇真实文章（3000 字深度分析），输出 HTML 检查无误：标题/正文/引用/表格/代码块/列表全部正确添加内联样式，无 `[object Object]`，无乱码。

---

## 六、现有 MCP 的核心短板汇总

把 14 个项目的不足归为五类，这也是新 MCP 需要弥补的：

### 短板 1：排版与 API 割裂

最大的问题。A 类（文颜系）排版强但 API 弱，B 类（woa-mcp 系）API 强但排版为零。用户要么装两个 Server 拼着用，要么忍受没排版的文章。

### 短板 2：草稿管理不完整

大部分项目只支持 Create（发草稿），不支持 Read/Update/Delete。发完之后想改标题、删旧稿、查列表——得去公众号后台手动操作。只有 woa-mcp（⑥）和 oukanghua（⑦）支持 C/R/D，但都不支持 Update。

### 短板 3：正文图片上传缺失

文章正文中的本地图片需要先通过 `uploadimg` API 上传获取微信 URL，再替换 Markdown 中的图片路径。**14 个项目中，没有一个自动处理这个流程。** 文颜和 markdown2wechat 支持上传图片，但需要手动调用；大部分 B 类项目完全不支持。

### 短板 4：Token 管理粗糙

access_token 有效期 2 小时，大部分项目每次调用都重新获取，没有缓存。频繁调用容易触发微信限频（45009）。只有 kakaxi（⑧）做了 Token 缓存 + 限流。

### 短板 5：Windows 兼容性

markdown2wechat 依赖 puppeteer/Chrome/sharp，在 Windows 上安装容易踩坑（Chrome 路径、sharp 原生模块编译）。文颜 MCP 纯 TypeScript 没这个问题，但也 fork 出了 floodsung 版修复 FormData 兼容问题——说明跨平台稳定性还需要关注。

---

## 七、5 个活跃项目与实用推荐

### 近期仍在维护的 5 个项目

14 个项目中，最近 3 个月（2026 年 4 月以后）仍在更新的只有 **5 个**：

| 项目 | Repo 地址 | 最近更新 | 核心能力 | 协议 |
|---|---|---|---|---|
| **文颜 MCP** | github.com/caol64/wenyan-mcp | 2026-04 | 7+ 主题、Mermaid、代码高亮、发草稿、小绿书、远程 Server | Apache-2.0 |
| **woa-mcp** | github.com/xwang152-jack/wechat-official-account-mcp | 2026-05 | 草稿 C/R/D、正式发布、素材 CRUD、AES 加密 | MIT |
| **oukanghua** | github.com/oukanghua/wechat_official_account_mcp | 2026-05 | 草稿 CRUD、发布、素材 CRUD、状态查询、Docker | 未标注 |
| **Wechatsync** | github.com/wechatsync/Wechatsync | 2026-05 | 多平台一键同步（微信+知乎+掘金+简书等） | 开源 |
| **md2wechat-skill** | github.com/geekjourneyx/md2wechat-skill | 2026-07 | **48 主题、60 项排版语法、AI 配图、Agent 原生、多账号、批量发布** | BUSL-1.1 |

其余 9 个项目更新停滞在 2026 年 2 月或更早，部分已超半年未更新，不建议作为主力工具。

### 已知短板

| 短板 | 影响 | 变通方案 |
|---|---|---|
| 排版与 API 割裂 | 排版派不管 API，API 派不排版 | 文颜 + woa-mcp 双装，或 md2wechat-skill + woa-mcp |
| 草稿不支持 Update | 无法修改已有草稿内容 | 删旧稿重新发 |
| 正文图片不自动上传 | 本地图片需手动处理 | 先上传图床，替换 Markdown 中的 URL |
| md2wechat-skill 免费版主题少 | 免费模式仅 3 主题，48 主题需 API 模式 | 用文颜替代，或升级 API 模式 |
| md2wechat-skill 不可商用 | BUSL-1.1 协议，商业使用需授权 | 商业场景用文颜(Apache-2.0) + woa-mcp(MIT) |

### 推荐方案

**方案一：文颜 MCP + woa-mcp（双装，开源首选，覆盖 95% 场景）**

文颜负责排版 + 发草稿，woa-mcp 负责草稿查询/删除、正式发布、素材管理。两个都是 TypeScript，`npx` 直接装，5 分钟搞定。完全开源，商业使用无限制。

- 文颜 MCP：github.com/caol64/wenyan-mcp
- woa-mcp：github.com/xwang152-jack/wechat-official-account-mcp

```json
{
  "mcpServers": {
    "wenyan-mcp": { "command": "npx", "args": ["-y", "wenyan-mcp"] },
    "wechat-official-account-mcp": { "command": "npx", "args": ["-y", "@anthropic/wechat-official-account-mcp"] }
  }
}
```

**方案二：md2wechat-skill（单装，Agent 原生，排版最强）**

如果你用 WorkBuddy、Claude Code 等 AI Agent 辅助写作，且是个人/非营利使用，md2wechat-skill 是体验最好的单一工具：48 主题 + AI 配图 + Brand Profile + Agent 原生 JSON 契约。npm 一行安装，`inspect → preview → convert` 三步流程清晰。

- Repo：github.com/geekjourneyx/md2wechat-skill

```bash
npm install -g @geekjourneyx/md2wechat
```

需要草稿管理/正式发布时，加装 woa-mcp 即可。注意 BUSL-1.1 协议：个人免费，商业使用需授权。

**不推荐安装的**：GongZhongHao_MCP（功能未完全测试）、md2wechat-mcp-server（不发布只转换）、tc6-01/weixin-mcp（1 次提交）、kakaxi（8 个月未更新）、publisher-mcp（1 年未更新）。

---

## 八、总结

14 个项目里，真正值得装的只有 5 个活跃项目。选两个组合使用，就能覆盖绝大多数场景：

- **开源免费、商业无忧**：文颜 MCP + woa-mcp（排版 + API 全功能）
- **Agent 原生、排版最强**：md2wechat-skill + woa-mcp（48 主题 + AI 配图 + 草稿管理）

没必要造新轮子。真正的硬缺口只有正文图片自动上传和草稿 Update 两个，属于边缘需求。选两个活跃项目组合使用，就是目前最好用的方案。

---

*本文基于 2026 年 7 月的实际调研和开发体验撰写。项目更新频繁，建议在选型前到各 repo 确认最新状态。*
