# 代码模块化拆分技能 (Code Split Skill)

一个帮助AI模型进行代码模块化拆分的IDE技能包，避免将所有业务逻辑写在单个文件中。

---

## ✨ 功能特点

- 📦 **智能模块分类**：自动识别并分类不同功能模块
- 📋 **强制分析文档**：编写代码前必须输出模块功能分析
- ⚡ **GitHub一键安装**：通过仓库地址直接安装
- 📝 **规范约束**：遵循统一的代码拆分标准
- 🔍 **精确触发**：只有明确请求时才触发，避免误触发
- 🛠 **辅助工具**：提供项目结构生成器、验证器和代码拆分分析器

---

## 🚀 安装方式

### 方式一：GitHub仓库安装（推荐）

```bash
# 克隆仓库到本地
git clone https://github.com/your-username/code-split-skill.git
```

然后根据所使用的IDE，将技能包安装到对应的技能目录：
- **Trae IDE**: 将仓库复制到 `~/.trae/skills/code-split-skill`
- **其他IDE**: 请参考对应IDE的技能安装文档

### 方式二：IDE内置安装

在支持技能市场的IDE中：
1. 打开技能市场
2. 搜索 **"代码模块化拆分"**
3. 点击 **安装**

### 方式三：手动安装

```bash
# 克隆仓库
git clone https://github.com/your-username/code-split-skill.git

# 进入目录
cd code-split-skill

# 运行安装脚本（如果需要）
bash install.sh
```

---

## 📁 项目结构

```
code-split-skill/
├── skill.json              # 技能配置文件（IDE识别必需）
├── prompt.md               # 技能规则说明（核心逻辑）
├── install.sh              # 一键安装脚本
├── README.md               # 使用说明文档
├── references/             # 参考资源库
│   ├── styleguide.md       # 代码风格指南
│   └── templates.md        # 代码模板库
└── scripts/                # 辅助脚本工具
    ├── generate-structure.py   # 项目结构生成器
    └── validate-structure.py   # 结构验证器
```

---

## 🎯 核心功能

### 触发条件（精确匹配）

技能只会在以下**明确场景**下触发：

#### 🔹 明确触发关键词（优先匹配）
- **"使用代码模块化拆分"**
- **"用code-split-skill"**
- **"请模块化编写"**
- **"按模块拆分"**

#### 🔹 场景触发（结合上下文）
当用户输入以下内容**且涉及代码编写**时触发：
- `"帮我创建一个项目"` + 具体需求
- `"实现一个登录功能"` + 技术栈
- `"重构这个文件"` + 文件内容
- `"拆分这段代码"` + 代码片段

#### 🔹 反向排除（避免误触发）
以下情况**不会**触发：
- 纯问题咨询："什么是模块化？"
- 简单查询："如何安装依赖？"
- 非代码任务："帮我写个文档"
- 闲聊对话："你好"

### 适用场景

| 场景 | 说明 | 示例 |
|------|------|------|
| **新项目创建** | 从0到1规范建立项目结构 | "帮我创建一个React项目" |
| **功能开发** | 新增功能时按模块编写 | "实现用户注册功能" |
| **代码重构** | 拆分臃肿文件为多个模块 | "拆分这个5000行的文件" |
| **规范统一** | 团队协作时统一代码风格 | "按规范编写API层" |

### ⚠️ 重构风险说明

**重要提醒**：在对已有项目进行重构时，请务必注意以下风险：

| 风险类型 | 说明 | 建议 |
|----------|------|------|
| **代码破坏** | 手动拆分代码可能引入错误 | 重构前备份项目 |
| **依赖关系** | 模块间的依赖可能被破坏 | 使用分析器检测依赖 |
| **测试失败** | 重构后测试可能不通过 | 重构后运行测试套件 |
| **团队协作** | 多人协作时可能产生冲突 | 在独立分支进行重构 |

**安全保障措施**：
- ✅ 所有分析工具均为**只读模式**，不会修改任何文件
- ✅ 拆分建议仅为参考，需要用户手动执行
- ✅ 提供结构验证器，重构后可验证是否符合规范

---

## 📚 使用指南

### 方式一：明确调用（最推荐）

```
使用代码模块化拆分，帮我创建一个用户登录系统
```

### 方式二：场景触发

```
帮我创建一个React电商项目，包含用户登录、商品列表、购物车功能
```

### 方式三：代码重构

```
请帮我拆分这段代码到不同模块：

// app.js (原文件内容)
const express = require('express');
const app = express();

// 登录逻辑
app.post('/login', (req, res) => { ... });

// 商品逻辑
app.get('/products', (req, res) => { ... });
```

---

## � 辅助工具

### 1. 项目结构生成器

自动生成标准的模块化项目结构：

```bash
# 使用方式
python3 scripts/generate-structure.py [目标目录]

# 示例：在当前目录生成
python3 scripts/generate-structure.py

# 示例：指定目录生成
python3 scripts/generate-structure.py ./my-project

# 指定要创建的模块
python3 scripts/generate-structure.py --modules auth api components utils
```

生成的结构：
```
src/
├── auth/          # 认证模块
├── api/           # API模块
├── components/    # UI组件
├── utils/         # 工具函数
├── hooks/         # 自定义Hooks
├── config/        # 配置文件
├── types/         # 类型定义
├── stores/        # 状态管理
├── layouts/       # 布局组件
├── pages/         # 页面组件
└── index.ts       # 统一导出
```

### 2. 结构验证器

验证现有项目结构是否符合模块化规范：

```bash
# 使用方式
python3 scripts/validate-structure.py [项目目录]

# 示例：验证当前目录
python3 scripts/validate-structure.py

# 示例：验证指定目录
python3 scripts/validate-structure.py ./my-project
```

输出示例：
```
============================================
📋 代码模块化结构验证报告
============================================

🔹 auth/
   ✅ 存在index.ts
   ✅ 目录非空
   ✅ 文件数量≤10 (3)

🔹 api/
   ✅ 存在index.ts
   ✅ 目录非空
   ✅ 文件数量≤10 (5)

============================================
📊 总分: 100.0% (6/6)
🎉 项目结构符合模块化规范！
```

### 3. 代码拆分分析器

分析已有项目中的大型文件，提供模块化拆分建议（**只读模式，不会修改任何文件**）：

```bash
# 使用方式
python3 scripts/analyze-and-split.py [项目目录]

# 示例：分析当前目录
python3 scripts/analyze-and-split.py

# 示例：分析指定目录并导出拆分计划
python3 scripts/analyze-and-split.py ./my-project --output-plan split-plan.md
```

输出示例：
```
🔍 代码模块化拆分分析器（只读模式）
============================================================
安全保障：
  • 不会修改、删除或创建任何文件
  • 仅分析代码结构，提供拆分建议
  • 所有修改需要用户手动执行
============================================================

📊 代码拆分分析报告（只读模式）
======================================================================

📈 项目摘要
----------------------------------------
  • 代码文件总数: 15
  • 大型文件数量: 3
  • 检测到的模块: auth, api, utils

📁 文件分析详情
----------------------------------------

  🔴 大型文件（>200行）- 需要关注

    📄 src/app.ts
       行数: 520
       函数: 12个
       💡 拆分建议:
         - 将不同职责的代码拆分到不同模块
         - 建议将相关代码移至 src/auth/ 目录
         - 建议将相关代码移至 src/api/ 目录

🎯 综合拆分建议
----------------------------------------
  1. 发现3个大文件，建议拆分
  2. 检测到3个模块类型: auth, api, utils

📋 推荐的模块目录结构
----------------------------------------
  src/
    ├── auth/          # ✅ 已检测到
    ├── api/           # ✅ 已检测到
    ├── components/    # 可选
    ├── utils/         # ✅ 已检测到
    └── index.ts       # 统一导出
```

---

## �📝 输出格式

### 第一步：模块功能分析

技能触发后，首先输出分析文档：

```markdown
## 模块功能分析

### 1. 认证模块 (auth/)
- 职责：处理用户登录、注册、Token验证
- 文件：`src/auth/login.ts`, `src/auth/register.ts`, `src/auth/token.ts`

### 2. API模块 (api/)
- 职责：后端接口封装和调用
- 文件：`src/api/user-api.ts`, `src/api/product-api.ts`

### 3. UI组件 (components/)
- 职责：页面展示组件
- 文件：`src/components/LoginForm.tsx`, `src/components/ProductList.tsx`

### 4. 工具函数 (utils/)
- 职责：通用工具方法
- 文件：`src/utils/validation.ts`, `src/utils/format.ts`

### 5. 类型定义 (types/)
- 职责：TypeScript类型声明
- 文件：`src/types/index.ts`

### 文件结构预览
```
src/
├── auth/
│   ├── login.ts
│   ├── register.ts
│   └── token.ts
├── api/
│   ├── user-api.ts
│   └── product-api.ts
├── components/
│   ├── LoginForm.tsx
│   └── ProductList.tsx
├── utils/
│   ├── validation.ts
│   └── format.ts
├── types/
│   └── index.ts
└── index.ts
```
```

### 第二步：代码实现

分析文档后，按模块输出代码：

```typescript
// src/auth/login.ts
export const login = async (username: string, password: string): Promise<LoginResponse> => {
  // 登录逻辑实现
};
```

---

## 📦 模块分类标准

| 模块 | 目录 | 职责说明 | 示例文件 |
|------|------|----------|----------|
| **认证** | `auth/` | 用户登录、注册、Token管理、权限验证 | login.ts, register.ts |
| **API** | `api/` | 后端接口调用、请求封装、响应处理 | user-api.ts |
| **组件** | `components/` | UI组件、页面组件、可复用组件 | Header.tsx, Button.tsx |
| **工具** | `utils/` | 通用工具函数、格式化、验证 | format.ts, validation.ts |
| **Hooks** | `hooks/` | 自定义React Hooks | useAuth.ts, useFetch.ts |
| **配置** | `config/` | 环境变量、全局配置、常量 | constants.ts |
| **类型** | `types/` | TypeScript类型定义、接口声明 | index.ts |
| **状态** | `stores/` | 状态管理（如Zustand、Pinia） | userStore.ts |
| **布局** | `layouts/` | 页面布局组件 | MainLayout.tsx |
| **页面** | `pages/` | 页面级组件 | HomePage.tsx |

---

## 📖 代码风格指南

### 命名规范
- **组件文件**：大驼峰 `UserProfile.tsx`
- **工具函数**：小驼峰或连字符 `formatDate.ts`, `string-utils.ts`
- **类型定义**：小写文件名，接口大驼峰 `user.ts` → `interface User {}`

### 导入顺序
1. 外部依赖
2. 内部模块（使用路径别名 `@/`）
3. 同目录文件
4. 样式文件

### 导出规范
- 每个模块目录必须有 `index.ts`
- 通过根目录 `src/index.ts` 统一导出
- 优先使用命名导出

---

## 🔧 配置说明

在 `skill.json` 中可配置：

```json
{
  "config": {
    "defaultModuleTypes": ["auth", "api", "components", "utils", "hooks", "config", "types"],
    "enableAutoSplit": true,
    "requireAnalysisDoc": true,
    "maxFileLines": 200,
    "maxFunctionLines": 50
  }
}
```

| 配置项 | 类型 | 说明 |
|--------|------|------|
| `defaultModuleTypes` | array | 默认模块类型列表 |
| `enableAutoSplit` | boolean | 是否启用自动拆分 |
| `requireAnalysisDoc` | boolean | 是否强制输出分析文档 |
| `maxFileLines` | number | 单个文件最大行数限制 |
| `maxFunctionLines` | number | 单个函数最大行数限制 |

---

## 📊 使用流程图

```
用户输入 → 触发检测 → 模块分析 → 代码编写 → 统一导出
    ↓
  是否包含触发关键词？
    ↓ (是)
  输出模块功能分析文档
    ↓
  按模块拆分编写代码
    ↓
  通过index.ts统一导出
```

---

## 📜 许可证

MIT License

---

## 🤝 贡献

欢迎提交Issue和PR！

---

## 📧 联系方式

如有问题，请在GitHub仓库提交Issue。