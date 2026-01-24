
<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python Version" />
  <img src="https://img.shields.io/badge/Clash-Supported-darkviolet" alt="Clash Supported" />
  <img src="https://img.shields.io/badge/Shadowrocket-Supported-mediumpurple" alt="Shadowrocket Supported" />
</div>

# 🚀 auto-rules-fusion

> 一个简单、支持自定义的 **广告屏蔽 + 规则融合** 工具

✨ **多源拉取 + 本地自定义 → 去重融合 → 一键生成 Clash / Shadowrocket 配置！**

---

## 🧩 功能一览

✅ 自动从远程拉取多种规则源（广告、直连、代理等）

✅ 支持用户自定义/覆盖规则（放在 `custom/` 目录）

✅ 自动去重、分类（`reject` / `direct` / `proxy`）

✅ 输出适用于 Clash 和 Shadowrocket 的配置文件

### 📁 目录结构

```text
auto-rule-fusion/
├── dist/               # 生成的配置文件存放目录
├── remote_config/      # 从网络拉取的配置文件，可直接用
├── src/                # 源代码目录
│   ├── custom/         # 用户自定义规则目录
│   ├── lib/            # 程序运行后分类生成的中间文件和资源
│   └── utils/          # 工具模块
└── requirements.txt    # Python依赖
```

---

## ⚡ 快速上手

1. 如果你想使用推荐的其他作者的配置文件，进入 `remote_config/` 文件夹，选择你想用的客户端平台并下载配置文件：
   - `sr/` → Shadowrocket 配置文件
   - `clash/` → Clash 配置文件

   如果你有喜欢的配置文件，可以到`src/lib/remote_config.txt`中添加 URL，程序运行时会自动拉取更新。
2. 运行 `src/main.py`，生成经过解析、融合的配置文件，输出在 `dist/` 目录下

> 💡 **Clash 配置文件还在完善中，建议优先使用 Shadowrocket 系列。**

---

## 👨‍💻 开发者 / 想自己更新规则的用户指南

### 环境准备

需要 Python 3.10+，然后执行：

```bash
pip install -r requirements.txt
```

### 生成流程

只需一步，程序会自动更新拉取远程规则，合并本地规则，生成最终配置文件：

```bash
python src/main.py
```

生成的配置文件会出现在 `dist/` 目录下。

---

### ✏️ 自定义规则（强烈推荐）

想加/删/改规则，直接编辑下列文件：

- `src/custom/manual_reject.txt`  → 🚫 强制屏蔽（广告、跟踪器等）
- `src/custom/manual_direct.txt`  → 🌐 强制直连（国内网站、CDN等）
- `src/custom/manual_proxy.txt`   → 🚀 强制走代理（需要翻墙的域名）

**格式：一行一个域名，支持如下写法：**

```text
domain.com
www.example.com
google.com
```

> 修改后重新运行上面 py 文件即可生效！

---

### 💡 小提示

- 生成的中间文件都在 `src/lib/`，一般只用来 debug，不建议直接修改
- 当前主力输出是 Shadowrocket，其他客户端格式还在逐步补充
- 有问题或想加新模板，欢迎 issue 或 PR

🎉 **祝使用愉快！**

---

### 🗂️ 详细文件树

```text
auto-rule-fusion/
├── dist/               # 生成的配置文件存放目录
├── remote_config/      # 从网络拉取的配置文件
│   ├── clash/              # Clash 配置文件
│   └── sr/                 # Shadowrocket 配置文件
├── src/                # 源代码目录
│   ├── custom/             # 用户自定义目录
│   │   ├── general.conf        # 自定义通用模块
│   │   ├── manual_direct.txt   # 自定义直连规则
│   │   ├── manual_proxy.txt    # 自定义代理规则
│   │   ├── manual_reject.txt   # 自定义拒绝规则
│   │   └── remote_config.txt   # 远程配置文件地址列表
│   ├── lib/                # 程序运行后分类生成的中间文件和资源
│   │   ├── direct.txt          # 生成的直连规则
│   │   ├── proxy.txt           # 生成的代理规则
│   │   ├── reject.txt          # 生成的拒绝规则
│   │   ├── cl_template.yaml    # Clash 配置文件模板
│   │   └── sr_template.conf    # Shadowrocket 配置文件模板
│   └── utils/              # 工具模块
│       ├── storage/            # 文件读写相关
│       │   ├── cache_manager.py    # 缓存管理
│       │   └── text_manager.py     # 文档管理
│       ├── tool/               # 工具函数
│       │   ├── check.py            # 检查函数
│       │   ├── download.py         # 下载函数
│       │   └── scan_file.py        # 扫描文件函数
│       ├── builder.py          # 最终配置文件生成
│       ├── config_proc.py      # 配置文件解析
│       ├── get_config.py       # 网络配置文件获取
│       └── lib_manager.py      # lib 目录管理
├── README.md           # 项目说明文档
└── requirements.txt    # Python依赖
```

---