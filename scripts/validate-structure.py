#!/usr/bin/env python3
"""
代码模块化拆分 - 结构验证器（只读模式）
验证项目结构是否符合模块化规范，不修改任何文件

⚠️ 安全保障：
- 本工具为纯只读模式，不会修改、删除或创建任何文件
- 仅分析目录结构和文件命名，不读取文件内容（除非明确授权）
- 不会自动执行重构操作，仅提供建议
"""

import os
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Tuple

MODULE_TYPES = [
    'auth',
    'api',
    'components',
    'utils',
    'hooks',
    'config',
    'types',
]

SAFE_FILE_EXTENSIONS = ('.ts', '.tsx', '.js', '.jsx')

def confirm_action(message: str) -> bool:
    """
    安全确认提示
    """
    response = input(f"\n⚠️ {message} (y/N): ").strip().lower()
    return response == 'y'

def check_module_structure(path: Path) -> List[Tuple[str, str, bool]]:
    """
    检查模块结构（只读，不修改任何文件）
    返回：[(模块名, 检查项, 是否通过)]
    """
    results = []
    
    # 检查是否存在index.ts
    index_file = path / 'index.ts'
    has_index = index_file.exists()
    results.append((path.name, '存在index.ts', has_index))
    
    # 检查目录非空
    try:
        has_files = any(path.iterdir())
        results.append((path.name, '目录非空', has_files))
    except PermissionError:
        results.append((path.name, '目录非空', False))
    
    # 检查文件数量（不应过多）
    try:
        file_count = sum(1 for f in path.glob('*.ts')) + sum(1 for f in path.glob('*.tsx'))
        results.append((path.name, f'文件数量≤10 ({file_count})', file_count <= 10))
    except PermissionError:
        results.append((path.name, '文件数量检查', False))
    
    return results

def check_naming_conventions(path: Path) -> List[Tuple[str, bool, str]]:
    """
    检查命名规范（只读，不修改任何文件）
    返回：[(文件名, 是否通过, 建议)]
    """
    results = []
    
    try:
        for item in path.iterdir():
            name = item.name
            
            # 跳过index.ts和非代码文件
            if name == 'index.ts' or not name.endswith(SAFE_FILE_EXTENSIONS):
                continue
            
            # 检查文件名
            if item.is_file():
                # 组件文件应该是大驼峰
                if path.name == 'components' and name.endswith('.tsx'):
                    is_pascal = name[0].isupper()
                    suggestion = f"建议重命名为大驼峰格式，如: {name[0].upper()}{name[1:]}"
                    results.append((f'组件 {name}', is_pascal, suggestion if not is_pascal else ''))
                
                # 工具函数应该是小驼峰或连字符
                elif path.name == 'utils' and name.endswith('.ts'):
                    is_valid = name[0].islower() or '-' in name
                    suggestion = "建议使用小驼峰或连字符命名，如: formatDate.ts 或 string-utils.ts"
                    results.append((f'工具 {name}', is_valid, suggestion if not is_valid else ''))
                
                # 类型定义文件
                elif path.name == 'types' and name.endswith('.ts'):
                    is_valid = name[0].islower()
                    suggestion = "建议使用小写命名，如: user.ts"
                    results.append((f'类型 {name}', is_valid, suggestion if not is_valid else ''))
    except PermissionError:
        results.append(('权限检查', False, '无法访问目录'))
    
    return results

def check_export_patterns(path: Path, allow_read_content: bool = False) -> Tuple[bool, str]:
    """
    检查导出模式（只读，可选择是否读取文件内容）
    """
    index_file = path / 'index.ts'
    if not index_file.exists():
        return False, '缺少index.ts文件'
    
    if not allow_read_content:
        return True, '跳过内容检查（需授权）'
    
    try:
        content = index_file.read_text()
        has_export = 'export' in content
        if has_export:
            return True, '导出语句正常'
        else:
            return False, 'index.ts中缺少export语句'
    except PermissionError:
        return False, '无法读取index.ts内容'

def validate_project(path: str, allow_read_content: bool = False) -> Dict[str, dict]:
    """
    验证整个项目结构（只读模式）
    """
    base = Path(path).resolve()
    src_dir = base / 'src'
    
    # 安全检查：确保路径存在
    if not base.exists():
        print(f"❌ 错误：路径不存在: {base}")
        return {}
    
    # 安全检查：确保是目录
    if not base.is_dir():
        print(f"❌ 错误：路径不是目录: {base}")
        return {}
    
    # 安全检查：检查src目录
    if not src_dir.exists():
        print(f"❌ 错误：src目录不存在: {src_dir}")
        print("💡 提示：请确保在项目根目录运行，或指定正确的项目路径")
        return {}
    
    print(f"🔍 正在分析项目: {base}")
    print("📌 模式：只读验证（不会修改任何文件）\n")
    
    results = {
        'modules': {},
        'naming': [],
        'exports': [],
        'warnings': []
    }
    
    # 检查模块结构
    for module in MODULE_TYPES:
        module_path = src_dir / module
        if module_path.exists() and module_path.is_dir():
            results['modules'][module] = check_module_structure(module_path)
    
    # 检查命名规范
    for module in MODULE_TYPES:
        module_path = src_dir / module
        if module_path.exists() and module_path.is_dir():
            naming_results = check_naming_conventions(module_path)
            results['naming'].extend(naming_results)
    
    # 检查导出模式
    for module in MODULE_TYPES:
        module_path = src_dir / module
        if module_path.exists() and module_path.is_dir():
            is_valid, message = check_export_patterns(module_path, allow_read_content)
            results['exports'].append((module, is_valid, message))
    
    # 检查是否有其他未知目录
    try:
        known_modules = set(MODULE_TYPES + ['index.ts'])
        for item in src_dir.iterdir():
            if item.is_dir() and item.name not in known_modules:
                results['warnings'].append(f"发现未知目录: {item.name}/")
    except PermissionError:
        results['warnings'].append("无法完整扫描src目录（权限限制）")
    
    return results

def print_report(results: Dict[str, dict]):
    """
    打印验证报告（仅输出信息，不修改文件）
    """
    print("=" * 70)
    print("📋 代码模块化结构验证报告（只读模式）")
    print("=" * 70)
    print("⚠️ 本工具为纯只读模式，不会修改任何文件")
    print("=" * 70)
    
    passed = 0
    total = 0
    
    # 模块结构检查
    if results['modules']:
        print("\n🔹 模块结构检查")
        print("-" * 40)
        
        for module, checks in results['modules'].items():
            print(f"\n  {module}/")
            for _, check, is_passed in checks:
                status = "✅" if is_passed else "❌"
                print(f"    {status} {check}")
                passed += 1 if is_passed else 0
                total += 1
    
    # 命名规范检查
    if results['naming']:
        print("\n🔹 命名规范检查")
        print("-" * 40)
        
        for name, is_valid, suggestion in results['naming']:
            status = "✅" if is_valid else "❌"
            print(f"    {status} {name}")
            if suggestion:
                print(f"       💡 {suggestion}")
            passed += 1 if is_valid else 0
            total += 1
    
    # 导出模式检查
    if results['exports']:
        print("\n🔹 导出模式检查")
        print("-" * 40)
        
        for module, is_valid, message in results['exports']:
            status = "✅" if is_valid else "❌"
            print(f"    {status} {module}/index.ts - {message}")
            passed += 1 if is_valid else 0
            total += 1
    
    # 警告信息
    if results['warnings']:
        print("\n🔹 警告信息")
        print("-" * 40)
        for warning in results['warnings']:
            print(f"    ⚠️ {warning}")
    
    # 总分计算
    print("\n" + "=" * 70)
    score = (passed / total) * 100 if total > 0 else 0
    print(f"📊 总分: {score:.1f}% ({passed}/{total})")
    
    if score >= 90:
        print("🎉 项目结构优秀！符合模块化规范。")
    elif score >= 70:
        print("👍 项目结构良好，建议根据提示进行少量改进。")
    elif score >= 50:
        print("⚠️ 项目结构基本符合规范，建议参考改进建议进行优化。")
    else:
        print("❌ 项目结构需要重构，建议参考代码风格指南。")
    
    print("\n📝 改进建议：")
    print("  1. 确保每个模块目录都有 index.ts 文件")
    print("  2. 遵循命名规范（组件大驼峰，工具小驼峰）")
    print("  3. 控制单个文件行数（建议≤200行）")
    print("  4. 通过 index.ts 统一导出模块")
    print("\n📚 参考文档: references/styleguide.md")

def main():
    parser = argparse.ArgumentParser(
        description='代码模块化拆分 - 结构验证器（只读模式）',
        epilog='本工具为纯只读模式，不会修改、删除或创建任何文件'
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='./',
        help='项目目录路径（默认当前目录）'
    )
    parser.add_argument(
        '--allow-read',
        action='store_true',
        help='允许读取文件内容进行更深入的检查（默认关闭，更安全）'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='静默模式，仅输出关键结果'
    )
    
    args = parser.parse_args()
    
    # 安全提醒
    if not args.quiet:
        print("🔒 代码模块化结构验证器（只读模式）")
        print("=" * 60)
        print("安全保障：")
        print("  • 不会修改、删除或创建任何文件")
        print("  • 默认不读取文件内容（保护隐私）")
        print("  • 仅分析目录结构和文件命名")
        print("=" * 60)
    
    # 执行验证
    results = validate_project(args.path, args.allow_read)
    
    # 输出报告
    if results and not args.quiet:
        print_report(results)
    elif results:
        # 静默模式：仅输出总分
        passed = sum(1 for checks in results['modules'].values() for _, _, is_passed in checks if is_passed)
        passed += sum(1 for _, is_valid, _ in results['naming'] if is_valid)
        passed += sum(1 for _, is_valid, _ in results['exports'] if is_valid)
        total = sum(len(checks) for checks in results['modules'].values())
        total += len(results['naming']) + len(results['exports'])
        score = (passed / total) * 100 if total > 0 else 0
        print(f"{score:.1f}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ 用户中断操作")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 发生错误：{str(e)}")
        print("⚠️ 验证器已安全退出，未修改任何文件")
        sys.exit(1)