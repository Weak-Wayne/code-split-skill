<div align="center">

# code-split-skill
**A Code SKILL for writing modular code — analyze first, split second.**

[![License: MIT](https://img.shields.io/badge/License-MIT-FB923C.svg?style=flat-square)](./LICENSE)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)


---

</div>

## ✨ What it does

Feed the SKILL a **project requirement**, **existing code**, or **file structure** — any combination works. It produces a comprehensive **Module Analysis Document** **first**. Only then does it generate the modular code structure.

The result: Clean separation of concerns, maintainable codebase, consistent across projects, portable across AI tools.

## 🎯 Two Working Modes

### 🚀 New Project Mode
Start from scratch with a well-organized modular structure:
- Automatically creates standard module directories
- Generates proper exports and configuration files
- Follows industry best practices

### 🔧 Refactoring Mode  
Analyze and improve existing projects:
- Scans for large files (>200 lines)
- Identifies module patterns and dependencies
- Provides safe, read-only splitting recommendations
- **Never modifies your code** — only offers suggestions

## 🧭 How it works

**Phase A · Understand**  
Extracts requirements from your input — whether creating new or refactoring existing code.

**Phase B · Analyze**  
Produces a full module analysis:
- Module classification
- File structure proposal
- Function/Class mapping
- Dependency graph

**Phase C · Generate**  
Creates modular code structure following the spec, or provides refactoring recommendations.

## 📦 Repository Layout

```
code-split-skill/
├── skill.json                    # skill configuration (IDE recognition)
├── prompt.md                     # core instructions for the AI
├── README.md                     # this landing page
├── index.md                      # detailed documentation
├── install.sh                    # installation script
├── references/                   # style guides, code templates
│   ├── styleguide.md             # naming conventions & best practices
│   └── templates.md              # code templates for various modules
└── scripts/                      # helper tools
    ├── generate-structure.py     # project structure generator
    ├── validate-structure.py     # structure validation tool
    └── analyze-and-split.py      # code analysis & split tool
```

## 🚀 Quick Start

### Install
```bash
git clone https://github.com/Weak-Wayne/code-split-skill 
```

### Run Tools
```bash
# Generate project structure
python3 scripts/generate-structure.py ./my-project

# Analyze existing project
python3 scripts/analyze-and-split.py ./existing-project

# Validate structure
python3 scripts/validate-structure.py ./my-project
```

## 🔒 Safety First

All analysis tools operate in **read-only mode**:

| Feature | Status |
|---------|--------|
| Never modifies files | ✅ |
| Never deletes code | ✅ |
| Only provides recommendations | ✅ |
| Full backup recommended before refactoring | ⚠️ |

## 📋 Module Classification

| Module | Purpose | Example Files |
|--------|---------|---------------|
| `auth/` | Authentication & authorization | login.ts, register.ts |
| `api/` | API calls & client | user-api.ts |
| `components/` | UI components | Header.tsx, Button.tsx |
| `utils/` | Utility functions | format.ts, validation.ts |
| `hooks/` | Custom hooks | useAuth.ts, useFetch.ts |
| `config/` | Configuration | constants.ts |
| `types/` | TypeScript types | index.ts |

## 📖 Documentation

For detailed usage instructions, configuration options, and API reference, please see the [full documentation](./index.md).

## 📄 License

[MIT](./LICENSE) — use it, fork it, ship it.

---

<div align="center">

**Built with ❤️ by [@Weak-Wayne](https://github.com/Weak-Wayne)**

[Documentation](./index.md) · [Report Issues](https://github.com/Weak-Wayne/code-split-skill/issues) · [Install](#-quick-start)

</div>
