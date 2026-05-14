# 代码模板库

## 1. 认证模块模板

### 1.1 login.ts
```typescript
import { APIResponse } from '@/types';

export interface LoginParams {
  username: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  user: {
    id: string;
    username: string;
  };
}

export const login = async (params: LoginParams): Promise<APIResponse<LoginResponse>> => {
  try {
    // 登录逻辑
    return { success: true, data: { token: '', user: { id: '', username: '' } } };
  } catch (error) {
    return { success: false, error: (error as Error).message };
  }
};
```

### 1.2 auth/index.ts
```typescript
export { login } from './login';
export { register } from './register';
export { logout } from './logout';
export { verifyToken } from './verify';
export * from './types';
```

## 2. API模块模板

### 2.1 user-api.ts
```typescript
import { APIResponse, User } from '@/types';

export const getUserById = async (id: string): Promise<APIResponse<User>> => {
  try {
    const response = await fetch(`/api/users/${id}`);
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: (error as Error).message };
  }
};
```

## 3. 组件模块模板

### 3.1 基础组件
```typescript
import React from 'react';

interface Props {
  title: string;
  subtitle?: string;
}

const ComponentName: React.FC<Props> = ({ title, subtitle }) => {
  return (
    <div className="component-name">
      <h2>{title}</h2>
      {subtitle && <p>{subtitle}</p>}
    </div>
  );
};

export default ComponentName;
```

### 3.2 容器组件
```typescript
import React, { useState, useEffect } from 'react';
import { fetchData } from '@/api';
import { DataItem } from '@/types';

const DataList: React.FC = () => {
  const [data, setData] = useState<DataItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      const result = await fetchData();
      if (result.success) {
        setData(result.data);
      }
      setLoading(false);
    };
    loadData();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <ul>
      {data.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
};

export default DataList;
```

## 4. Hooks模板

### 4.1 useAuth.ts
```typescript
import { useState, useCallback } from 'react';
import { login, logout, verifyToken } from '@/auth';
import { LoginParams, User } from '@/types';

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const handleLogin = useCallback(async (params: LoginParams) => {
    const result = await login(params);
    if (result.success && result.data) {
      setUser(result.data.user);
      localStorage.setItem('token', result.data.token);
    }
    return result;
  }, []);

  const handleLogout = useCallback(() => {
    logout();
    setUser(null);
    localStorage.removeItem('token');
  }, []);

  const checkAuth = useCallback(async () => {
    const token = localStorage.getItem('token');
    if (token) {
      const result = await verifyToken(token);
      if (result.success && result.data) {
        setUser(result.data);
      }
    }
    setLoading(false);
  }, []);

  return {
    user,
    loading,
    login: handleLogin,
    logout: handleLogout,
    checkAuth,
  };
};
```

### 4.2 useFetch.ts
```typescript
import { useState, useEffect } from 'react';
import { APIResponse } from '@/types';

type FetchFunction<T> = () => Promise<APIResponse<T>>;

export const useFetch = <T>(fetchFn: FetchFunction<T>) => {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const result = await fetchFn();
        if (result.success) {
          setData(result.data || null);
          setError(null);
        } else {
          setError(result.error || 'Unknown error');
        }
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [fetchFn]);

  const refetch = () => {
    fetchData();
  };

  return { data, loading, error, refetch };
};
```

## 5. 工具函数模板

### 5.1 validation.ts
```typescript
export const validateEmail = (email: string): boolean => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
};

export const validatePassword = (password: string): { valid: boolean; message: string } => {
  if (password.length < 8) {
    return { valid: false, message: '密码至少需要8个字符' };
  }
  if (!/(?=.*[a-zA-Z])/.test(password)) {
    return { valid: false, message: '密码需要包含字母' };
  }
  if (!/(?=.*\d)/.test(password)) {
    return { valid: false, message: '密码需要包含数字' };
  }
  return { valid: true, message: '' };
};
```

### 5.2 format.ts
```typescript
export const formatDate = (date: Date, format: string = 'YYYY-MM-DD'): string => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');

  return format
    .replace('YYYY', String(year))
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds);
};

export const formatCurrency = (amount: number, currency: string = 'CNY'): string => {
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency,
  }).format(amount);
};
```

## 6. 配置文件模板

### 6.1 constants.ts
```typescript
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000';

export const STORAGE_KEYS = {
  TOKEN: 'auth_token',
  USER: 'user_info',
  THEME: 'app_theme',
};

export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  INTERNAL_ERROR: 500,
};
```

## 7. 类型定义模板

### 7.1 index.ts
```typescript
export interface APIResponse<T = unknown> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface User {
  id: string;
  username: string;
  email: string;
  avatar?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface Pagination<T> {
  data: T[];
  page: number;
  pageSize: number;
  total: number;
  totalPages: number;
}

export type Status = 'active' | 'inactive' | 'pending';

export interface ErrorResponse {
  code: number;
  message: string;
  details?: string[];
}
```