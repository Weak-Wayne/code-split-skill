#!/usr/bin/env python3
"""
代码模块化拆分 - 项目结构生成器
自动生成标准的模块化项目结构
"""

import os
import argparse
from pathlib import Path

MODULE_TYPES = [
    'auth',
    'api',
    'components',
    'utils',
    'hooks',
    'config',
    'types',
    'stores',
    'layouts',
    'pages',
]

def create_directory_structure(base_path: str, modules: list = None):
    """
    创建模块化目录结构
    """
    if modules is None:
        modules = MODULE_TYPES
    
    base = Path(base_path)
    
    # 创建src目录
    src_dir = base / 'src'
    src_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建各个模块目录
    for module in modules:
        module_dir = src_dir / module
        module_dir.mkdir(exist_ok=True)
        
        # 创建index.ts文件
        index_file = module_dir / 'index.ts'
        if not index_file.exists():
            index_file.write_text(f'// {module} module exports\n')
    
    # 创建根目录index.ts
    root_index = src_dir / 'index.ts'
    if not root_index.exists():
        exports = '\n'.join([f'export * from \'./{module}\';' for module in modules])
        root_index.write_text(exports + '\n')
    
    # 创建package.json模板
    package_json = base / 'package.json'
    if not package_json.exists():
        package_json.write_text("""{
  "name": "modular-project",
  "version": "1.0.0",
  "description": "A modular codebase",
  "main": "src/index.ts",
  "scripts": {
    "dev": "ts-node src/index.ts",
    "build": "tsc",
    "lint": "eslint . --ext .ts,.tsx",
    "format": "prettier --write ."
  },
  "keywords": ["modular", "typescript"],
  "author": "",
  "license": "MIT"
}
""")
    
    # 创建tsconfig.json模板
    tsconfig_json = base / 'tsconfig.json'
    if not tsconfig_json.exists():
        tsconfig_json.write_text("""{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
""")
    
    print(f"✅ 项目结构已创建在: {base_path}")
    print_structure(base_path)

def print_structure(path: str, prefix: str = ''):
    """
    打印目录结构
    """
    base = Path(path)
    entries = sorted(base.iterdir(), key=lambda x: (not x.is_dir(), x.name))
    
    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        connector = '└──' if is_last else '├──'
        
        print(f"{prefix}{connector} {entry.name}")
        
        if entry.is_dir():
            new_prefix = prefix + ('    ' if is_last else '│   ')
            print_structure(str(entry), new_prefix)

def main():
    parser = argparse.ArgumentParser(
        description='代码模块化拆分 - 项目结构生成器'
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='./',
        help='目标目录路径（默认当前目录）'
    )
    parser.add_argument(
        '--modules',
        nargs='+',
        choices=MODULE_TYPES,
        default=MODULE_TYPES,
        help='指定要创建的模块'
    )
    
    args = parser.parse_args()
    
    create_directory_structure(args.path, args.modules)

if __name__ == '__main__':
    main()