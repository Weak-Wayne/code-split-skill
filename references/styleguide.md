# 代码模块化拆分风格指南

## 1. 目录结构规范

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

## 2. 文件命名规范

### 2.1 通用文件
- 使用小写字母 + 连字符：`user-service.ts`
- 避免下划线：`user_service.ts` ❌

### 2.2 组件文件
- 使用大驼峰命名：`UserProfile.tsx`
- 目录名使用小写：`components/user-profile/`

### 2.3 工具函数
- 使用小驼峰命名：`formatDate.ts`

### 2.4 类型定义
- 使用小写：`types/user.ts`
- 接口使用大驼峰：`interface User {}`

## 3. 导出规范

### 3.1 模块导出
```typescript
// src/auth/index.ts
export { login } from './login';
export { register } from './register';
export * from './types';
```

### 3.2 根目录导出
```typescript
// src/index.ts
export * from './auth';
export * from './api';
export * from './components';
```

## 4. 代码风格

### 4.1 导入顺序
1. 外部依赖
2. 内部模块
3. 同目录文件
4. 样式文件

```typescript
// ✅ 正确
import React from 'react';
import { login } from '@/auth';
import { formatDate } from './utils';
import './styles.css';
```

### 4.2 函数命名
- 函数名使用小驼峰：`getUserInfo()`
- 组件名使用大驼峰：`const UserCard = () => {}`

### 4.3 类型命名
- 接口使用 `I` 前缀：`interface IUser {}`
- 类型使用 `T` 前缀：`type TStatus = 'active' | 'inactive'`
- 枚举使用全大写：`enum HTTP_STATUS {}`

## 5. 模块职责边界

### 5.1 auth/
- ✅ 用户登录、注册、退出
- ✅ Token管理、权限验证
- ❌ 数据请求（属于api/）
- ❌ UI展示（属于components/）

### 5.2 api/
- ✅ 接口封装、请求拦截
- ✅ Mock数据
- ❌ 业务逻辑（属于hooks/）
- ❌ 状态管理（属于stores/）

### 5.3 components/
- ✅ UI展示组件
- ✅ 纯展示逻辑
- ❌ 业务逻辑（属于hooks/）
- ❌ API调用（属于api/）

### 5.4 hooks/
- ✅ 业务逻辑封装
- ✅ 状态管理逻辑
- ❌ UI渲染（属于components/）
- ❌ 直接DOM操作

### 5.5 utils/
- ✅ 通用工具函数
- ✅ 纯函数、无副作用
- ❌ 业务逻辑（属于hooks/）
- ❌ 状态管理

## 6. 最佳实践

### 6.1 单一职责
每个文件只做一件事：
```typescript
// ✅ 正确：单一职责
// src/utils/format.ts
export const formatDate = (date: Date) => {};

// ❌ 错误：多个职责混合
// src/utils/helpers.ts
export const formatDate = () => {};
export const validateEmail = () => {};
export const fetchData = () => {};
```

### 6.2 避免循环依赖
```typescript
// ❌ 错误：循环依赖
// a.ts
import { b } from './b';
export const a = () => b();

// b.ts
import { a } from './a';
export const b = () => a();
```

### 6.3 使用路径别名
```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}
```

## 7. 质量检查清单

- [ ] 每个文件不超过200行
- [ ] 每个函数不超过50行
- [ ] 无未使用的导入
- [ ] 类型定义完整
- [ ] 无循环依赖
- [ ] 导出规范
- [ ] 命名符合规范