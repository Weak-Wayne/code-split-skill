#!/usr/bin/env python3
"""
代码模块化拆分 - 代码拆分分析器
分析已有项目中的大型文件，提供模块化拆分建议

⚠️ 安全保障：
- 本工具为纯只读模式，不会修改任何文件
- 仅分析代码结构，提供拆分建议
- 所有操作需要用户确认后手动执行
"""

import os
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional

MODULE_TYPES = {
    'auth': ['login', 'register', 'logout', 'token', 'verify', 'auth', 'password'],
    'api': ['api', 'http', 'fetch', 'client', 'service', 'request'],
    'components': ['component', 'ui', 'view', 'card', 'button', 'form', 'modal'],
    'utils': ['util', 'helper', 'format', 'validate', 'tools', 'common'],
    'hooks': ['use', 'hook', 'state'],
    'config': ['config', 'constant', 'env', 'setting'],
    'types': ['type', 'interface', 'schema'],
    'stores': ['store', 'state', 'manager'],
}

def analyze_file(file_path: Path) -> Dict[str, any]:
    """
    分析单个文件，识别可能的模块归属
    """
    try:
        content = file_path.read_text()
        lines = content.split('\n')
        line_count = len(lines)
        
        # 识别关键词
        keywords = []
        for module, terms in MODULE_TYPES.items():
            for term in terms:
                if term.lower() in content.lower():
                    keywords.append((module, term))
        
        # 识别函数和类
        functions = []
        classes = []
        for i, line in enumerate(lines, 1):
            if 'function ' in line or 'const ' in line and '=' in line and '=>' in line:
                parts = line.split()
                for part in parts:
                    if part and part[0].isalpha():
                        if 'function' in line:
                            func_name = parts[parts.index('function') + 1].split('(')[0]
                        else:
                            func_name = parts[parts.index('const') + 1].split('=')[0]
                        functions.append((func_name, i))
                        break
            elif 'class ' in line:
                class_name = line.split()[1].split('{')[0]
                classes.append((class_name, i))
        
        return {
            'path': str(file_path),
            'line_count': line_count,
            'keywords': keywords,
            'functions': functions,
            'classes': classes,
            'size_status': 'large' if line_count > 200 else 'medium' if line_count > 100 else 'small'
        }
    except Exception as e:
        return {
            'path': str(file_path),
            'error': str(e)
        }

def suggest_split(file_info: Dict[str, any]) -> List[Dict[str, str]]:
    """
    根据文件分析结果提供拆分建议
    """
    suggestions = []
    
    if file_info.get('size_status') == 'large':
        suggestions.append({
            'action': 'split',
            'reason': f"文件过大（{file_info['line_count']}行），建议拆分",
            'suggestion': '将不同职责的代码拆分到不同模块'
        })
    
    # 根据关键词建议模块归属
    if file_info.get('keywords'):
        modules = set(k[0] for k in file_info['keywords'])
        for module in modules:
            suggestions.append({
                'action': 'move',
                'reason': f"检测到{module}相关代码",
                'suggestion': f"建议将相关代码移至 src/{module}/ 目录"
            })
    
    # 根据函数/类数量建议拆分
    func_count = len(file_info.get('functions', []))
    class_count = len(file_info.get('classes', []))
    if func_count > 5:
        suggestions.append({
            'action': 'split',
            'reason': f"包含{func_count}个函数，建议拆分",
            'suggestion': '每个文件建议不超过5个核心函数'
        })
    
    return suggestions

def analyze_project(path: str) -> Dict[str, any]:
    """
    分析整个项目
    """
    base = Path(path).resolve()
    src_dir = base / 'src'
    
    if not src_dir.exists():
        print(f"❌ 错误：src目录不存在: {src_dir}")
        return {}
    
    print(f"🔍 正在分析项目: {base}")
    print("📌 模式：只读分析（不会修改任何文件）\n")
    
    results = {
        'files': [],
        'summary': {
            'total_files': 0,
            'large_files': 0,
            'modules_detected': [],
            'suggestions': []
        }
    }
    
    # 遍历所有TypeScript/JavaScript文件
    for ext in ('*.ts', '*.tsx', '*.js', '*.jsx'):
        for file_path in src_dir.rglob(ext):
            if 'node_modules' in str(file_path):
                continue
            
            file_info = analyze_file(file_path)
            file_info['suggestions'] = suggest_split(file_info)
            results['files'].append(file_info)
            
            # 统计
            results['summary']['total_files'] += 1
            if file_info.get('size_status') == 'large':
                results['summary']['large_files'] += 1
            
            # 检测到的模块
            for module, _ in file_info.get('keywords', []):
                if module not in results['summary']['modules_detected']:
                    results['summary']['modules_detected'].append(module)
    
    # 生成综合建议
    if results['summary']['large_files'] > 0:
        results['summary']['suggestions'].append(
            f"发现{results['summary']['large_files']}个大文件，建议拆分"
        )
    
    detected_modules = results['summary']['modules_detected']
    if detected_modules:
        results['summary']['suggestions'].append(
            f"检测到{len(detected_modules)}个模块类型: {', '.join(detected_modules)}"
        )
    
    return results

def print_analysis_report(results: Dict[str, any]):
    """
    打印分析报告
    """
    print("=" * 70)
    print("📊 代码拆分分析报告（只读模式）")
    print("=" * 70)
    print("⚠️ 本工具为纯只读模式，不会修改任何文件")
    print("=" * 70)
    
    # 摘要
    summary = results['summary']
    print(f"\n📈 项目摘要")
    print("-" * 40)
    print(f"  • 代码文件总数: {summary['total_files']}")
    print(f"  • 大型文件数量: {summary['large_files']}")
    print(f"  • 检测到的模块: {', '.join(summary['modules_detected']) if summary['modules_detected'] else '无'}")
    
    # 文件分析详情
    print("\n📁 文件分析详情")
    print("-" * 40)
    
    large_files = [f for f in results['files'] if f.get('size_status') == 'large']
    medium_files = [f for f in results['files'] if f.get('size_status') == 'medium']
    
    if large_files:
        print("\n  🔴 大型文件（>200行）- 需要关注")
        for file_info in large_files:
            print(f"\n    📄 {file_info['path']}")
            print(f"       行数: {file_info['line_count']}")
            if file_info.get('functions'):
                print(f"       函数: {len(file_info['functions'])}个")
            if file_info.get('classes'):
                print(f"       类: {len(file_info['classes'])}个")
            
            if file_info.get('suggestions'):
                print("       💡 拆分建议:")
                for suggestion in file_info['suggestions']:
                    print(f"         - {suggestion['suggestion']}")
    
    if medium_files:
        print("\n  🟡 中等文件（100-200行）- 建议优化")
        for file_info in medium_files:
            print(f"    📄 {file_info['path']} - {file_info['line_count']}行")
    
    # 综合建议
    print("\n🎯 综合拆分建议")
    print("-" * 40)
    
    if summary['suggestions']:
        for i, suggestion in enumerate(summary['suggestions'], 1):
            print(f"  {i}. {suggestion}")
    else:
        print("  ✅ 项目结构良好，暂无需拆分")
    
    print("\n📋 推荐的模块目录结构")
    print("-" * 40)
    print("  src/")
    for module in MODULE_TYPES.keys():
        if module in summary['modules_detected']:
            print(f"    ├── {module}/          # ✅ 已检测到")
        else:
            print(f"    ├── {module}/          # 可选")
    print("    └── index.ts           # 统一导出")
    
    print("\n📝 拆分步骤建议")
    print("-" * 40)
    print("  1. 先创建标准模块目录结构")
    print("  2. 分析大型文件的功能职责")
    print("  3. 将代码按职责迁移到对应模块")
    print("  4. 更新index.ts导出")
    print("  5. 验证项目结构")
    
    print("\n🔧 工具命令")
    print("-" * 40)
    print("  # 创建模块目录结构")
    print("  python3 scripts/generate-structure.py .")
    print("")
    print("  # 验证拆分后的结构")
    print("  python3 scripts/validate-structure.py .")

def generate_split_plan(results: Dict[str, any]) -> str:
    """
    生成详细的拆分计划
    """
    plan = []
    plan.append("# 代码拆分计划")
    plan.append("")
    plan.append("## 1. 项目现状分析")
    plan.append(f"- 代码文件总数: {results['summary']['total_files']}")
    plan.append(f"- 大型文件数量: {results['summary']['large_files']}")
    plan.append(f"- 检测到的模块: {', '.join(results['summary']['modules_detected'])}")
    plan.append("")
    plan.append("## 2. 拆分目标")
    plan.append("- 每个文件不超过200行")
    plan.append("- 单一职责原则")
    plan.append("- 按模块分类组织")
    plan.append("")
    plan.append("## 3. 详细拆分方案")
    
    large_files = [f for f in results['files'] if f.get('size_status') == 'large']
    for file_info in large_files:
        plan.append("")
        plan.append(f"### {file_info['path']}")
        plan.append(f"- 现状: {file_info['line_count']}行")
        plan.append(f"- 函数: {len(file_info.get('functions', []))}个")
        plan.append(f"- 类: {len(file_info.get('classes', []))}个")
        plan.append("- 建议:")
        for suggestion in file_info.get('suggestions', []):
            plan.append(f"  - {suggestion['suggestion']}")
    
    plan.append("")
    plan.append("## 4. 预期结果")
    plan.append("```")
    plan.append("src/")
    for module in MODULE_TYPES.keys():
        plan.append(f"├── {module}/")
        plan.append(f"│   └── index.ts")
    plan.append("└── index.ts")
    plan.append("```")
    
    return '\n'.join(plan)

def main():
    parser = argparse.ArgumentParser(
        description='代码模块化拆分 - 代码拆分分析器（只读模式）',
        epilog='分析已有项目，提供模块化拆分建议'
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='./',
        help='项目目录路径（默认当前目录）'
    )
    parser.add_argument(
        '--output-plan',
        type=str,
        help='将拆分计划导出到指定文件'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='静默模式，仅输出关键结果'
    )
    
    args = parser.parse_args()
    
    # 安全提醒
    if not args.quiet:
        print("🔍 代码模块化拆分分析器（只读模式）")
        print("=" * 60)
        print("安全保障：")
        print("  • 不会修改、删除或创建任何文件")
        print("  • 仅分析代码结构，提供拆分建议")
        print("  • 所有修改需要用户手动执行")
        print("=" * 60)
    
    # 执行分析
    results = analyze_project(args.path)
    
    # 输出报告
    if results and not args.quiet:
        print_analysis_report(results)
    
    # 导出拆分计划
    if args.output_plan and results:
        plan = generate_split_plan(results)
        Path(args.output_plan).write_text(plan)
        print(f"\n📄 拆分计划已导出到: {args.output_plan}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ 用户中断操作")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 发生错误：{str(e)}")
        sys.exit(1)