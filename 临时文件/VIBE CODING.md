Vibe Coding 完整开发流程（从 0 到发布）
## 📖 **流程总览**

```
🟢 准备阶段 (30分钟)
    ↓
🟡 迭代开发阶段 (循环执行，直到功能完成)
    ↓
🔴 交付阶段 (30分钟)
    ↓
🟣 复盘阶段 (10分钟)

```

---

## 🟢 **阶段 1：准备阶段 (Preparation)**

**目标：** 将"演示代码"转化为"工程代码"，建立开发基线

### 【Step 0】技能预加载 ⭐ **NEW**

```markdown
【对话 1】
你："我要开发一个 [功能描述]，请先加载相关技能文档"

Claude:
正在加载技能文档...
✅ 已读取：frontend-design/SKILL.md
✅ 已读取：tdd-workflow/SKILL.md
✅ 已读取：security-review/SKILL.md
✅ 已读取：coding-standards/SKILL.md

准备就绪，请描述你的需求。

```

**💡 小 Tip：**

```markdown
# 如何知道要加载哪些技能？
根据你的任务类型选择：

- 前端开发 → frontend-design, frontend-patterns
- 后端 API → backend-patterns, security-review
- 文档处理 → docx, pdf, pptx
- 全栈功能 → tdd-workflow, coding-standards

快捷命令：
"加载前端开发相关的所有 skills"

```

---

### 【Step 1】需求共创

```markdown
【对话 2】
你："我要做一个 [具体功能]，帮我生成 PRD"

Claude:
# Product Requirements Document

## 功能概述
[功能描述]

## 用户故事
- 作为 [角色]，我想 [操作]，以便 [目标]
- ...

## 核心功能点
1. [功能点 1]
2. [功能点 2]

## 技术要求
- 前端：Next.js 15 + TypeScript
- 状态管理：React Context
- API：Next.js API Routes
- 数据库：Supabase

## 成功标准
- [ ] 用户可以 [操作 1]
- [ ] 系统能够 [响应 1]

是否确认此 PRD？如需修改请告知。

```

**💡 小 Tip：**

```markdown
# PRD 确认清单
在说"确认"前，检查：
✅ 功能边界清晰（不做什么也要写明）
✅ 技术栈已确定
✅ 成功标准可测试
✅ 没有模糊的词（如"优化"、"提升"）

如果 PRD 太抽象：
"请细化第 3 点，给出具体的输入输出示例"

```

---

### 【Step 2】UI 生成（可选）

```markdown
【对话 3】
你："将 PRD 投喂给 v0，生成前端 UI"

# 在 v0.dev 中：
1. 粘贴 PRD
2. 生成 UI 代码
3. 下载到本地项目

```

**💡 小 Tip：**

```markdown
# 如果不用 v0，直接让 Claude 生成：
"基于 PRD，生成 React 组件骨架（只要结构，不要实现逻辑）"

# 如果用了 v0：
"v0 生成的代码在 src/v0-output/，请分析但不要直接使用"

```

---

### 【Step 3】工程初始化

```markdown
【对话 4】
你："初始化项目工程结构"

Claude:
# 执行初始化命令
$ git init
$ npm create next-app@latest . --typescript --tailwind --app
$ git add .
$ git commit -m "chore: initial commit"

✅ 项目已初始化
✅ Git 仓库已创建
✅ 依赖已安装

下一步：运行 /update-codemaps 生成架构文档

```

---

### 【Step 4】架构重构 ⭐ **关键**

```markdown
【对话 5】
你："作为 Architect agent，将 v0 生成的代码重构为工程化结构，
遵循 frontend-patterns skill 的规范"

Claude (architect agent):
正在分析 v0 代码...

检测到问题：
❌ 所有代码在一个 500 行的文件中
❌ 组件、逻辑、样式混在一起
❌ 无类型定义

重构方案：
src/
├── app/
│   └── page.tsx (50 行) - 页面入口
├── components/
│   ├── ui/
│   │   ├── Button.tsx (30 行)
│   │   └── Input.tsx (30 行)
│   └── features/
│       └── SearchBar.tsx (80 行)
├── hooks/
│   └── useDebounce.ts (20 行)
├── lib/
│   └── api.ts (40 行)
└── types/
    └── index.ts (20 行)

总计：~270 行（原 500 行拆分后）

是否执行重构？
```

**💡 小 Tip - 如何控制拆分粒度：**

```markdown
# 如果拆分太细（文件太多）：
"文件太多了，把 ui/ 下的组件合并到 components/ui.tsx"

# 如果拆分太粗（单文件太大）：
"SearchBar.tsx SLOC 有 200 行，请拆分为：
- SearchBar.tsx (主组件，50 行)
- SearchInput.tsx (输入框，30 行)
- SearchResults.tsx (结果列表，80 行)
- useSearch.ts (搜索逻辑，40 行)"

# 黄金标准：
单文件SLOC 30-80 行（最多不超过 150 行）

你："列出 SLOC>200 行的文件"
    ↓
Claude: 分析报告 (包含文件作用、拆分优先级)
    ↓
你："拆分 [具体文件名]"
    ↓
Claude: 拆分方案 (Phase 1-N，每个 Phase 预估行数)
    ↓
你：选择执行方式
    ├─ 方式 A："一次性执行全部"
    │     ↓
    │  Claude: 批量创建文件，更新引用
    │
    └─ 方式 B："先执行 Phase 1"（推荐）
          ↓
       Claude: 创建第一个文件，更新主文件
          ↓
       你："测试一下" (人工验证)
          ↓
       你："继续 Phase 2"
          ↓
       重复直到完成
       
# 扫描大文件
扫描项目中所有代码文件，列出：
1. SLOC超过 200 的文件（按行数降序）
2. 每个文件的作用说明
3. 拆分优先级建议（高/中/低）
4. 预估拆分后的文件数量

格式：
| 文件名 | 行数 | 作用 | 优先级 | 拆分方案 |

# 针对性拆分
对文件 [文件路径] 生成拆分方案：
1. 分析当前结构（列出主要功能块）
2. 提出拆分方案（每个新文件的职责和预估行数）
3. 给出拆分前后对比
4. 提供渐进式拆分的 Phase 划分（每 Phase 一个小改动）

等我确认后再执行拆分。

# 批量重构
生成整个项目的大文件重构计划：
1. 统计所有 SLOC >200 行的文件
2. 按目录分类
3. 建议重构顺序（Week 1/2/3）
4. 评估风险（核心页面 vs 工具函数）
5. 提供自动化检测方案（ESLint 规则）

不要立即执行，先给我计划。
```

---

### 【Step 5】制定计划 ⭐ **关键**

```markdown
【对话 6】
**你："/plan 基于当前架构，制定开发计划，每个任务控制在 50-80 行代码"**

Claude (planner agent):
# Implementation Plan: 搜索功能

## Phase 1: 基础架构 (40 行)
**文件：** types/index.ts, lib/api.ts
**任务：**
1. 定义 SearchQuery 和 SearchResult 类型
2. 创建 API 客户端骨架

**验证点：** TypeScript 编译通过

---

## Phase 2: UI 组件 (70 行)
**文件：** components/SearchBar.tsx, components/SearchInput.tsx
**任务：**
1. 实现 SearchInput 受控组件
2. 实现 SearchBar 组合组件
3. 添加 loading 状态显示

**验证点：** 组件可以渲染，状态更新正常

---

## Phase 3: 搜索逻辑 (60 行)
**文件：** hooks/useSearch.ts, lib/api.ts
**任务：**
1. 实现 useSearch hook
2. 集成 useDebounce (防抖)
3. 实现 API 调用逻辑

**验证点：** 搜索请求发送成功

---

## Phase 4: 结果展示 (50 行)
**文件：** components/SearchResults.tsx
**任务：**
1. 实现结果列表组件
2. 添加空状态处理
3. 添加错误状态处理

**验证点：** 结果正确展示

---

## Phase 5: 测试覆盖 (80 行)
**文件：** __tests__/SearchBar.test.tsx, __tests__/useSearch.test.ts
**任务：**
1. 单元测试：useSearch hook
2. 组件测试：SearchBar
3. 集成测试：完整搜索流程

**验证点：** 测试覆盖率 > 80%

---

总计：5 个 Phase，300 行代码
预计时间：2-3 小时

请确认此计划，然后我们开始 Phase 1。

```

**💡 小 Tip - 如何调整 Phase 大小：**

```markdown
# 如果 Phase 太大（超过 100 行）：
"Phase 2 有 150 行，太大了。请拆分为：
- Phase 2a: SearchInput 组件 (40 行)
- Phase 2b: SearchBar 组件 (50 行)
- Phase 2c: Loading 状态 (30 行)"

# 如果 Phase 太小（不到 30 行）：
"Phase 1 和 Phase 2 都很小，合并为一个 Phase"

# 最佳 Phase 大小：
单个 Phase 30-80 行代码（对应 1 轮微循环）

```

---

## 🟡 **阶段 2：迭代开发阶段 (Iterative Development)**

**目标：** 针对每个 Phase，执行 TDD 微循环

### 🌟微循环🌟针对单个 Phase

```markdown
┌─────────────────────────────────────────────┐
│ 一次微循环                                   │
├─────────────────────────────────────────────┤
│ 对话 1: "
/tdd phase 1.1 [功能描述]，禁止将逻辑与类型混在一个文件，SLOC（不计注释）严格限制在 80 行，超标则自动拆分。
│                                             │
│         (自动完成 Red + Green)              │
├─────────────────────────────────────────────┤
│ 对话 2: "
/code-review
│                                            │
│         → 如果有 CRITICAL：立即修复         │
│         → 如果是建议：记录，继续            │
├─────────────────────────────────────────────┤
│ 对话 3: "
/verify quick
│                                             │
│         → 如果失败：/build-fix              │
│         → 如果通过：人工测试                │
├─────────────────────────────────────────────┤
│ 对话 4: (人工验收)                          │
│         "测试通过" 或 "有问题，修复XX"      │
├─────────────────────────────────────────────┤
│ 对话 5: "
/checkpoint create 'feat: ...'
│                                             │
│         (锁定胜局)                          │
└─────────────────────────────────────────────┘

总计：4-5 轮对话 最后执行commit后进入下一个循环
```

```jsx
git add .
git commit -m "feat:phase 1.1 [功能描述]"
```

---

### **Step 1：编写测试 (Red)**

```markdown
【对话 7】
你："/tdd 执行 Phase 1：基础架构"

Claude (tdd-guide agent):
已读取 tdd-workflow skill。

## Phase 1: 基础架构 - 测试先行

### 1.1 定义类型 (types/index.ts)
```typescript
export interface SearchQuery {
  keyword: string
  filters?: {
    category?: string
    dateRange?: [Date, Date]
  }
}

export interface SearchResult {
  id: string
  title: string
  snippet: string
  relevance: number
}

### 1.2 编写测试 (lib/api.test.ts)
```typescript
import { searchAPI } from './api'

describe('searchAPI', () => {
  it('should return empty array for empty query', async () => {
    const results = await searchAPI({ keyword: '' })
    expect(results).toEqual([])
  })

  it('should call API with correct params', async () => {
    const mockFetch = jest.fn()
    global.fetch = mockFetch
    
    await searchAPI({ keyword: 'test' })
    
    expect(mockFetch).toHaveBeenCalledWith(
      '/api/search?q=test',
      expect.any(Object)
    )
  })
})
```

### 1.3 运行测试（应该失败）
```bash
$ npm test

FAIL lib/api.test.ts
  ✕ should return empty array for empty query
    Error: searchAPI is not defined

测试失败 ✅ (符合预期 - RED 阶段)
```

准备好进入 GREEN 阶段了吗？
```

💡 小 Tip：

```markdown
# 如果 Claude 跳过了测试，直接写实现：
"停！请先写测试，确保测试失败后再写实现"

# 如果测试写得太简单：
"测试不够全面，请添加：
- 边界情况：空字符串、特殊字符
- 错误场景：网络失败、API 返回 500
- 性能测试：1000 条结果的情况"

# 如果测试写得太复杂：
"测试太复杂了，先写基本的 happy path 测试"
```

---

### **Step 2：编写实现 (Green)**

```markdown
【对话 8】
你："继续，写最小实现让测试通过"

Claude (tdd-guide agent):
## Phase 1: 基础架构 - 最小实现

### 实现 API 客户端 (lib/api.ts)
```typescript
import { SearchQuery, SearchResult } from '@/types'

export async function searchAPI(
  query: SearchQuery
): Promise<SearchResult[]> {
  // 处理空查询
  if (!query.keyword.trim()) {
    return []
  }

  try {
    const response = await fetch(`/api/search?q=${query.keyword}`)

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }

    const data = await response.json()
    return data.results || []
  } catch (error) {
    console.error('Search failed:', error)
    return []
  }
}

### 运行测试
```bash
$ npm test

PASS lib/api.test.ts
  ✓ should return empty array for empty query (15ms)
  ✓ should call API with correct params (8ms)

测试通过 ✅ (GREEN 阶段完成)
```

代码已实现，准备进入 Code Review。

```

**💡 小 Tip - 控制实现规模：**

```markdown

# 如果实现超出计划范围：
"你实现了 150 行，但 Phase 1 计划只有 40 行。
请只实现类型定义和 API 骨架，其他功能放到后续 Phase"

# 如果实现不完整：
"测试通过了，但缺少错误处理。请添加：
- 网络超时处理
- API 返回格式验证"

# 黄金标准：
实现代码 = 测试代码 × 1.5 倍行数（合理范围）

```

---

### **Step 3：代码审查 (Review)**

```markdown
【对话 9】
你："/code-review"

Claude (code-reviewer agent):
# Code Review Report

**文件：** lib/api.ts, types/index.ts
**新增代码：** 42 行

## ✅ 通过检查

### 代码质量
- ✅ 函数命名清晰 (searchAPI)
- ✅ 类型定义完整
- ✅ 错误处理得当
- ✅ 无 console.log

### 安全性
- ✅ 无硬编码密钥
- ✅ 输入已验证（空字符串检查）
- ✅ API 调用使用 try-catch

### 最佳实践
- ✅ 使用 TypeScript 泛型
- ✅ 遵循项目 API Response 格式

## ⚠️ 建议改进（非阻塞）

### 1. 添加请求超时
**位置：** lib/api.ts:15
**建议：**
```typescript
const controller = new AbortController()
const timeout = setTimeout(() => controller.abort(), 5000)

const response = await fetch(url, {
  signal: controller.signal
})
clearTimeout(timeout)

### 2. 类型更严格
**位置：** types/index.ts:8
**建议：**
```typescript
// 当前
relevance: number

// 建议改为
relevance: number // 0-1 范围
```

## 总结
🟢 **APPROVED** - 可以继续下一步

建议在后续 Phase 中添加超时处理。
```

💡 小 Tip：

```markdown

# 如果发现 CRITICAL 问题：
立即修复，不要进入下一步！

# 如果建议太多：
"只标注 CRITICAL 和 HIGH 级别问题，MEDIUM 的放到技术债清单"

# 如果没发现任何问题：
可能是 code-reviewer 没认真看，换个问法：
"请特别检查：安全漏洞、类型安全、边界条件处理"

```

---

### **Step 4：机器校验 (Verify)**

```markdown
【对话 10】
你："/verify quick"

Claude:
# Verification Report

## Build Check
```bash
$ npm run build

✓ Compiled successfully
Time: 2.3s
```
✅ PASS

## Type Check
```bash
$ npx tsc --noEmit

No errors found
```
✅ PASS

## Lint Check
```bash
$ npm run lint

All files passed
```
✅ PASS

## Test Suite
```bash
$ npm test

PASS lib/api.test.ts
  ✓ should return empty array (12ms)
  ✓ should call API correctly (8ms)

Tests: 2 passed, 2 total
Time: 1.2s
```
✅ PASS

## 总结
✅ **READY** - Phase 1 可以 checkpoint

新增文件：
- types/index.ts (20 行)
- lib/api.ts (42 行)
- lib/api.test.ts (28 行)
```

**💡 小 Tip - 处理构建错误：**

```markdown
# 如果 verify 失败：
你："/build-fix"

Claude (build-error-resolver agent):
检测到 3 个类型错误...

Error 1: Type 'string | undefined' not assignable to 'string'
File: lib/api.ts:12
Fix: 添加类型守卫

应用修复...
✅ 已修复

重新运行 verify...
✅ 全部通过

# 如果反复失败（3 次以上）：
"回滚到上一个 checkpoint，重新实现这个 Phase"
```

---

### **Step 5：视觉验收 (Visual Check)**

```markdown
【对话 11】(人工操作，不需要 Claude)

# 在浏览器中测试
1. 打开 http://localhost:3000
2. 输入搜索关键词
3. 检查：
   ✅ 输入框正常显示
   ✅ 输入文字时有响应
   ✅ 网络请求正确发送（F12 查看）

如果发现问题：
你："搜索框位置偏左，调整一下"
Claude: (修改 CSS)
你："好了，继续"
```

**💡 小 Tip：**

```markdown
# 视觉验收清单：
- UI 渲染正常（无白屏、错位）
- 交互响应（点击、输入有反馈）
- 加载状态显示（loading spinner）
- 错误提示友好（不是 console.error）

# 如果功能还没完成：
"Phase 1 只是架构，先跳过视觉验收，继续下一个 Phase"

# 如果是后端 API：
用 Postman/curl 测试，不需要浏览器
```

---

### **Step 6：创建检查点 (Checkpoint)**

```markdown
【对话 12】
你："/checkpoint create 'feat: phase 1 - basic architecture'"

Claude:
# 正在创建检查点

## 检查点前置校验
✅ 所有测试通过
✅ 构建成功  
✅ 无 TypeScript 错误

## Git 提交
```bash
$ git add .
$ git commit -m "feat: phase 1 - basic architecture

- Add SearchQuery and SearchResult types
- Implement searchAPI client
- Add unit tests for API client
- Coverage: 90%"

[main abc1234] feat: phase 1 - basic architecture
 3 files changed, 90 insertions(+)
```

## 检查点已创建
📍 检查点： phase-1-complete
🔖 提交： abc1234
📊 统计： +90 lines, 2 tests, 90% coverage

✅ 可以安全进入第2阶段
```

**💡 小 Tip：**

```markdown
# Checkpoint 命名规范：
feat: phase-1-xxx    (新功能)
fix: phase-2-xxx     (修复 bug)
refactor: phase-3-xxx (重构)
test: phase-4-xxx    (补充测试)

# 什么时候创建 checkpoint：
✅ 完成一个 Phase
✅ 通过所有验证
✅ 功能可独立运行

# 什么时候不创建：
❌ 代码写了一半
❌ 测试还没通过
❌ 还有明显 bug
```

---

### 【循环执行】重复微循环

```markdown
【对话 13】
你："Phase 1 完成，开始 Phase 2"

Claude:
已加载 Phase 2 计划：UI 组件 (70 行)

准备开始 TDD 流程：
1. 编写 SearchInput.test.tsx
2. 实现 SearchInput.tsx
3. Code Review
4. Verify
5. Visual Check
6. Checkpoint

开始编写测试...

(重复上面的 Step 1-6)
```

**💡 小 Tip - 加速循环：**

```markdown
# 如果对流程很熟悉，可以批量执行：
"执行 Phase 2 的完整微循环（TDD → Review → Verify → Checkpoint）"

# 如果遇到问题，恢复单步：
"停，让我先看看代码"
"继续下一步"

# 黄金节奏：
新手：每步确认（6-7 轮对话 / Phase）
熟练：批量执行（2-3 轮对话 / Phase）

```

---

## 🔴 **阶段 3：交付阶段 (Delivery)**

**目标：** 确保代码符合生产标准

### 【Step 1】全量安检

```markdown
【对话 N】(所有 Phase 完成后)
你："/verify full"

Claude:
# 全面校验报告

## 构建检查 ✅
```bash
$ npm run build
✓ Production build successful
Bundle size: 234 KB (gzip: 89 KB)
```

## 类型检查 ✅
```bash
$ npx tsc --noEmit
No errors in 24 files
```

## 代码规范检查 (Lint) ✅
```bash
$ npm run lint
All files passed
```

## 测试套件 ✅
```bash
$ npm test -- --coverage

Test Suites: 5 passed, 5 total
Tests:       18 passed, 18 total
Coverage:    87.3% (target: 80%)

File                | % Stmts | % Branch | % Funcs | % Lines
--------------------|---------|----------|---------|--------
lib/api.ts          |   100   |   100    |   100   |   100
hooks/useSearch.ts  |   92.3  |   83.3   |   100   |   92.3
components/SearchBar|   85.7  |   75     |   100   |   85.7
```

## 安全扫描 ✅
```bash
$ npm audit
Found 0 vulnerabilities

✅ No hardcoded secrets detected
✅ No console.log in production code
✅ All user inputs validated
```

## 性能检查 ⚠️
```bash
Lighthouse Score:
Performance: 92/100
Accessibility: 100/100
Best Practices: 95/100
SEO: 100/100
```

## 总结
🟢 **生产环境已就绪 (READY FOR PRODUCTION)**

微小优化建议：
- 考虑对 SearchResults 组件进行懒加载 （可减少 15KB 的首屏加载体积）

是否批准部署？(是/否)
```

💡 小 Tip

```markdown
# 如果发现 CRITICAL 问题：
你："/build-fix"（自动修复）

# 如果错误太多（>10 个）：
你："先修复 CRITICAL 和 HIGH 级别问题，列出清单"

# 如果测试覆盖率不足：
你："/test-coverage - 为覆盖率 <80% 的文件生成测试"
```

---

### 【Step 2】文档同步🌟

```markdown
【对话 N+1】
你："作为 doc-updater agent，更新项目文档"

Claude (doc-updater agent):
# Updating Documentation

## 1. 更新 README.md
```markdown
# 项目名称

## 新增功能 ✨
- 🔍 智能搜索功能
  - 支持关键词搜索
  - 防抖优化（500ms）
  - 结果实时展示

## 使用方法
\`\`\`typescript
import { SearchBar } from '@/components/SearchBar'

<SearchBar onSearch={handleSearch} />
\`\`\`
```

## 2. 更新 Codemaps
```markdown
docs/CODEMAPS/frontend.md

新增模块：
src/
├── components/
│   ├── SearchBar.tsx      # 搜索主组件
│   ├── SearchInput.tsx    # 输入框
│   └── SearchResults.tsx  # 结果列表
├── hooks/
│   └── useSearch.ts       # 搜索逻辑
└── lib/
    └── api.ts             # API 客户端

数据流：
用户输入 → useDebounce → useSearch → API → SearchResults
```

## 3. 更新 .env.example
```bash
# 新增环境变量
NEXT_PUBLIC_API_URL=http://localhost:3000/api
SEARCH_TIMEOUT=5000
```

✅ 文档已同步
```

💡 小 Tip：

```markdown
# 文档同步清单：
✅ README.md（功能清单、使用示例）
✅ CODEMAPS（架构图更新）
✅ .env.example（新增变量）
✅ CHANGELOG.md（版本记录）

# 如果文档太长：
"只更新变更部分，保持其他章节不变"
```

---

### 【Step 3】多 Agent 审查

```markdown
【对话 N+2】
你："/orchestrate feature 'complete search functionality'"

Claude:
# 智能代理编排：搜索功能

## 第 1 阶段：规划审查
代理: planner
✅ 架构符合 PRD
✅ 所有计划阶段已完成
✅ 无缺失功能

## 第 2 阶段：代码审查
代理: code-reviewer
✅ 代码质量：极佳
✅ 未检测到重复代码
✅ 遵循命名规范
⚠️ 次要：为公开 API 添加 JSDoc

## 第 3 阶段：安全审查
代理: security-reviewer
✅ 无硬编码密钥
✅ 已实现输入验证
✅ XSS 防护到位
✅ 已考虑速率限制

## 第 4 阶段：测试覆盖率
代理: tdd-guide
✅ 单元测试：90% 覆盖率
✅ 集成测试：85% 覆盖率
⚠️ E2E 测试：考虑添加 Playwright 测试

## 最终建议
🟢 立即发布

可选改进（非阻塞）：
1. 添加 JSDoc 注释
2. 为完整的搜索流程添加 E2E 测试

是否批准合并到主分支？(是/否)
```

**💡 小 Tip：**

```markdown
# 如果某个 agent 发现问题：
立即修复，然后重新运行 /orchestrate

# 如果想跳过某些检查：
"/orchestrate feature '...' --skip-e2e"

# 如果想自定义 agent 顺序：
"/orchestrate custom 'planner,code-reviewer,security-reviewer' 'task description'"

```

---

### 【Step 4】最终验收 (UAT)

```markdown
【对话 N+3】(人工操作)

# User Acceptance Testing

## 测试场景 1：基本搜索
1. 打开应用
2. 输入 "Next.js"
3. 验证：
   ✅ 结果在 500ms 后出现（防抖）
   ✅ 显示 5 条相关结果
   ✅ 结果按相关度排序

## 测试场景 2：空搜索
1. 输入框留空，点击搜索
2. 验证：
   ✅ 显示友好提示："请输入搜索关键词"
   ✅ 不发送 API 请求

## 测试场景 3：错误处理
1. 关闭后端 API
2. 输入搜索关键词
3. 验证：
   ✅ 显示错误提示："搜索失败，请稍后重试"
   ✅ UI 不崩溃

如果全部通过 → 继续
如果有问题 → 记录 bug，回到开发阶段

```

**💡 小 Tip：**

```markdown
# UAT 清单模板：
✅ 核心功能可用（Happy Path）
✅ 边界情况处理（Empty, Null）
✅ 错误场景优雅降级（Network Fail）
✅ 性能符合预期（Loading < 3s）
✅ 移动端适配（如需要）

# 如果测试失败：
记录问题 → 创建 bug 修复 Phase → 重新走微循环

```

---

### 【Step 5】提交代码

```markdown
【对话 N+4】
你："所有测试通过，提交代码"

Claude:
# Git 工作流

## 1. 最终检查
```bash
$ git status

On branch feature/search
Changes to be committed:
  new file:   src/components/SearchBar.tsx
  new file:   src/hooks/useSearch.ts
  ...
  (24 files changed, 432 insertions)
```

## 2. 提交 (Commit)
```bash
$ git add .
$ git commit -m "feat: implement search functionality

Features:
- Semantic search with debounce (500ms)
- Real-time results display
- Error handling and empty states
- Mobile responsive design

Tests:
- Unit tests: 90% coverage
- Integration tests: 85% coverage
- UAT: All scenarios passed

Closes #123"
```

## 3. 推送 (Push)
```bash
$ git push origin feature/search

remote: Create pull request for 'feature/search'
remote: https://github.com/user/repo/pull/456
```

## 4. 创建 Pull Request (PR)
# PR 标题：feat: 实现搜索功能

## 概述
新增带实时结果的智能搜索功能。

## 改动点
- 📁 累计修改 24 个文件 (+432 行)
- ✅ 新增 18 个测试用例
- 📊 测试覆盖率：87.3%

## 测试详情
- [x] 单元测试通过
- [x] 集成测试通过
- [x] 手动用户验收测试 (UAT) 已完成
- [x] 安全审查通过

## 截图
(附上搜索功能截图)

## 部署说明
- 需添加环境变量 `SEARCH_TIMEOUT` (默认值: 5000)
- 无需数据库迁移
```

✅ PR 已创建: https://github.com/user/repo/pull/456
```

💡 小 Tip：

```markdown
# Commit Message 规范：
type(scope): subject

body

footer

# Type 类型：
feat     - 新功能
fix      - Bug 修复
refactor - 重构
test     - 测试
docs     - 文档
chore    - 构建/工具

# 如果想自动生成 PR 描述：
"基于 git diff，生成 PR description"
```

---

## 🟣 **阶段 4：复盘阶段 (Retrospective)**

**目标：** 沉淀经验，持续改进

### 【Step 1】手动提取经验

```markdown
【对话 N+5】
你："/learn - 提取本次开发中的关键经验"

Claude (continuous-learning skill):
# 学习提取

## 发现的问题模式
1. **防抖实现错误**
   - 问题：useDebounce 在 strict mode 下触发两次
   - 根因：useEffect cleanup 未正确处理
   - 解决方案：
```typescript
   useEffect(() => {
     const handler = setTimeout(() => {
       setDebouncedValue(value)
     }, delay)
     
     return () => clearTimeout(handler) // 关键！
   }, [value, delay])
```

2. **TypeScript 类型推断失败**
   - 问题：fetch 返回类型为 any
   - 解决方案：显式声明泛型
```typescript
   const response = await fetch<SearchResult[]>(url)
```

## 值得保存的模式
是否将以下内容保存为技能？
1. "防抖 Hook 正确实现"（推荐）
2. "API 调用类型安全模式"（推荐）

保存到：~/.claude/skills/learned/ ? (yes/no)
```

💡 小 Tip：

```markdown
# 什么值得提取为技能？
✅ 解决了花费 >30 分钟的问题
✅ 发现了框架/库的非官方文档坑
✅ 创建了可复用的代码模式
✅ 总结了特定场景的最佳实践

# 什么不值得提取？
❌ 一次性的业务逻辑
❌ 简单的语法错误
❌ 文档已有的内容
❌ 项目特定的配置
```

---

### 【Step 2】自动评估（会话结束时）

```markdown
# 无需手动操作
# 当你关闭 Claude 会话时，Stop hook 自动触发

[Hook] Session has 45 messages - evaluate for extractable patterns
[Hook] Found 2 potential learnings:
  1. Next.js 15 App Router 特定问题
  2. Supabase RLS 配置模式

[Hook] Saved to ~/.claude/skills/learned/session-2025-02-04.md

```

**💡 小 Tip：**

```markdown
# 查看自动提取的技能：
你："列出最近学到的技能"

Claude:
~/.claude/skills/learned/
├── session-2025-02-04.md (今天)
├── session-2025-02-01.md
└── session-2025-01-28.md

# 如果自动提取太多垃圾：
编辑 skills/continuous-learning/config.json
调整 min_session_length 和 extraction_threshold

```

---

### 【Step 3】更新项目 Skill（可选）

```markdown
【对话 N+6】
你："基于本次开发，更新项目 skill 文档"

Claude:
# 更新：~/.claude/skills/learned/your-project-patterns.md

## 新增模式

### 搜索功能实现
```typescript
// ✅ 标准模式：useSearch hook
export function useSearch(endpoint: string) {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)

  const debouncedQuery = useDebounce(query, 500)

  useEffect(() => {
    if (!debouncedQuery) {
      setResults([])
      return
    }

    setLoading(true)
    searchAPI({ keyword: debouncedQuery })
      .then(setResults)
      .finally(() => setLoading(false))
  }, [debouncedQuery])

  return { query, setQuery, results, loading }
}

### API 调用规范更新

所有搜索类 API 必须：

1. 支持防抖（500ms）
2. 处理空查询（返回空数组）
3. 超时设置（5s）
4. 错误降级（显示友好提示）

✅ 已更新项目 skill

```

## 📊 完整流程时间估算

| 阶段 | 步骤 | 时间 | 对话轮数 |
| --- | --- | --- | --- |
| **🟢 准备** | 0. 技能预加载 | 2 分钟 | 1 |
|  | 1. 需求共创 | 10 分钟 | 2-3 |
|  | 2. UI 生成 | 10 分钟 | 1 (v0) |
|  | 3. 工程初始化 | 5 分钟 | 1 |
|  | 4. 架构重构 | 15 分钟 | 2-3 |
|  | 5. 制定计划 | 10 分钟 | 1-2 |
|  | **小计** | **~50 分钟** | **8-11** |
| **🟡 开发** | 微循环 × N 轮 | 每轮 15-20 分钟 | 每轮 6-7 |
|  | (假设 5 个 Phase) | **~90 分钟** | **30-35** |
| **🔴 交付** | 1. 全量安检 | 5 分钟 | 1 |
|  | 2. 文档同步 | 10 分钟 | 1-2 |
|  | 3. 多 Agent 审查 | 10 分钟 | 1 |
|  | 4. UAT | 15 分钟 | 人工 |
|  | 5. 提交代码 | 5 分钟 | 1 |
|  | **小计** | **~45 分钟** | **4-5** |
| **🟣 复盘** | 1. 手动提取 | 5 分钟 | 1 |
|  | 2. 自动评估 | 0 分钟 | 自动 |
|  | 3. 更新 Skill | 5 分钟 | 1 |
|  | **小计** | **~10 分钟** | **2** |
| **总计** |  | **~3 小时** | **44-53 轮对话** |

## 🎯 **关键 Tips 总结**

### ⭐ **控制代码生成规模**

```markdown
# 问题：Claude 一次生成 500 行
解决方案 1：用 /plan 强制拆分
"执行 /plan，每个 Phase 控制在 50-80 行"

解决方案 2：用 TodoWrite 实时跟踪
"用 TodoWrite 展示进度，我会控制节奏"

解决方案 3：用 Hook 自动提醒
(配置 PreToolUse hook，>100 行时暂停)

```

---

### ⭐ **Phase 拆分粒度**

```markdown
# 太大（>150 行）：
"Phase 2 太大，拆分为 2a, 2b, 2c"

# 太小（<30 行）：
"Phase 1 和 2 都很小，合并为一个 Phase"

# 黄金标准：
单个 Phase = 30-80 行新代码
对应 1 轮完整微循环（TDD → Review → Verify → Checkpoint）

```

---

### ⭐ **处理意外情况**

```markdown
# Claude 跳过测试，直接写实现：
"停！请先写测试"

# 测试太简单：
"测试不够全面，添加边界情况和错误场景"

# 实现超出计划：
"Phase 1 计划 40 行，你写了 150 行。只实现计划内容"

# 构建失败：
"/build-fix"（自动修复）

# 反复失败：
"回滚到上一个 checkpoint"

```

---

### ⭐ **加速开发节奏**

```markdown
# 新手模式（每步确认）：
你："写测试"
Claude: (生成测试)
你："写实现"
Claude: (生成实现)
你："/code-review"
...

# 熟练模式（批量执行）：
你："执行 Phase 2 的完整微循环"
Claude: (自动执行 TDD → Review → Verify → Checkpoint)

# 专家模式（自动化）：
你："/orchestrate feature 'implement search' --auto-checkpoint"
Claude: (完全自动化执行所有 Phase)
step 2 /verify quick
step 3 /checkpoint create
repeat（重复）
```

---

### ⭐ **质量保证清单**

```markdown
每个 Phase 结束前，确认：
✅ 测试先写，且失败了（Red）
✅ 实现后，测试通过了（Green）
✅ Code Review 无 CRITICAL 问题
✅ /verify quick 全部通过
✅ 视觉/功能验收 OK
✅ Checkpoint 已创建

全部功能完成前，确认：
✅ /verify full 通过
✅ 文档已同步
✅ 多 Agent 审查通过
✅ UAT 全场景测试通过
✅ PR 已创建

```

---

## 🚀 **立即可用的快捷 Prompt**

### 【启动新项目】

```markdown
我要开发 [功能名称]，使用 vibe coding SOP。请：
1. 加载相关技能：frontend-design, tdd-workflow, security-review
2. 帮我生成 PRD
3. 制定开发计划（每 Phase 50-80 行代码）
4. 等我确认后，开始 Phase 1

不要一次性生成所有代码！

```

### 【接手现有项目】

```markdown
我有一个开发了一半的项目，请：
1. 执行 /update-codemaps（生成架构文档）
2. 分析代码规范，生成项目 skill
3. 执行 /plan（生成待办清单）
4. 总结当前状态，告诉我下一步做什么

完成后等我指令。

```

### 【执行单个 Phase】

```markdown
执行 Phase [N]：[Phase 名称]

遵循 TDD 流程：
1. 先写测试（确保失败）
2. 写最小实现（让测试通过）
3. 运行 /code-review
4. 运行 /verify quick
5. 等我视觉验收
6. 创建 checkpoint

每步完成后暂停，等我确认。

```

### 【批量执行（熟练后）】

```markdown
执行 Phase [N] 的完整微循环：
TDD → Code Review → Verify → Checkpoint

中间不要暂停，除非遇到错误。

```

### 【全自动模式（专家）】

```markdown
/orchestrate feature "[功能描述]" 

要求：
- 自动拆分 Phase（每个 50-80 行）
- 每个 Phase 自动执行微循环
- 全部完成后运行 /verify full
- 生成 PR description

遇到 CRITICAL 问题时暂停，其他自动处理。

```

---

希望这个完整流程对你有帮助！🎉

**核心原则总结：**

1. ✅ **技能先行** - 开始前先加载 skills
2. ✅ **规划优先** - 用 /plan 拆分任务
3. ✅ **测试驱动** - 先写测试，再写代码
4. ✅ **小步迭代** - 每 50 行一个循环
5. ✅ **持续验证** - 每步都要 verify
6. ✅ **经验沉淀** - 用 /learn 保存模式

祝你 vibe coding 愉快！🚀

接手项目流程

```jsx
┌─────────────────────────────────────────────────────┐
│ 第 1 步：生成代码地图 (15 分钟)                      │
├─────────────────────────────────────────────────────┤
│ 命令："/update-codemaps"                             │
│ 输出：docs/CODEMAPS/*.md                             │
│ 作用：让 Claude 理解项目架构                         │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│ 第 2 步：提取代码模式 (10 分钟)                      │
├─────────────────────────────────────────────────────┤
│ 命令："分析代码模式，生成 skill"                     │
│ 输出：~/.claude/skills/learned/your-project.md      │
│ 作用：让 Claude 学习你的代码风格                     │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│ 第 3 步：生成开发计划 (5 分钟)                       │
├─────────────────────────────────────────────────────┤
│ 命令："/plan 基于现状生成 roadmap"                   │
│ 输出：开发任务清单（按优先级排序）                   │
│ 作用：明确接下来要做什么                             │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│ 🎯 开始执行 vibe coding SOP                          │
└─────────────────────────────────────────────────────┘
```