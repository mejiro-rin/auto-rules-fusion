
<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python Version" />
  <img src="https://img.shields.io/badge/Clash-Supported-darkviolet" alt="Clash Supported" />
  <img src="https://img.shields.io/badge/Shadowrocket-Supported-mediumpurple" alt="Shadowrocket Supported" />
</div>

# 🚀 auto-rules-fusion

> 一个简单、支持自定义的 **广告屏蔽 + 规则融合** 工具

自动拉取订阅配置，解析分类其中的规则后进行再次构建

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

直接订阅作者的配置文件，已融合规则，每日10点自动更新。
> 🚀 Shadowrocket
````text
https://raw.githubusercontent.com/mejiro-rin/auto-rules-fusion/refs/heads/generated/SR_config.conf
````
> 😼 Clash 配置文件
````text
功能正在开发中....
````

- 如果你想添加整合其他作者的规则，或者添加自定义规则，请根据下文指导拉取到本地后使用


---

## 👨‍💻 开发者 / 个性化使用指南

### 环境准备

需要 Python 3.10+，然后执行：

```bash
pip install -r requirements.txt
```

### 生成流程

只需一步，程序会自动更新拉取远程规则，合并本地规则，生成最终配置文件：

```bash
cd src
python src/main.py
```
- 请在`src/`目录下运行主程序，否则不确定会出现什么路径错误bug（

产出的配置文件会生成在根目录的 `dist/` 目录下。

---

### ✏️ 自定义规则

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
### 🛒 添加其它作者的配置文件参与整合

在文档`src/custom/remote_config.txt`内，根据使用平台分类，添加配置文件下载或订阅链接。


> 修改后，重新运行 main.py 文件即可生效！

---

### 💡 小提示

- 生成的中间文件都在 `src/lib/`，是解析分类后生成配置的规则与模板，一般用于 debug
- 当前主力输出是 Shadowrocket，其他客户端格式还在逐步补充
- 有问题或想加新模板，欢迎 issue 或 PR

🎉 **祝使用愉快！**

---

### 🗂️ 完整文件树

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
│   ├── lib/                # 程序生成的中间文件和资源
│   │   ├── direct.txt          # 生成的直连规则
│   │   ├── proxy.txt           # 生成的代理规则
│   │   ├── reject.txt          # 生成的拒绝规则
│   │   ├── cl_template.yaml    # Clash 配置文件模板
│   │   └── sr_template.conf    # Shadowrocket 配置文件模板
│   └── utils/              # 工具模块
│       ├── storage/            # 文件读写相关
│       │   └── text_manager.py     # 文档管理
│       ├── tool/               # 工具函数
│       │   ├── check.py            # 检查函数
│       │   ├── download.py         # 下载函数
│       │   └── scan_file.py        # 扫描文件函数
│       ├── builder.py          # 最终配置文件生成
│       ├── config_proc.py      # 配置文件解析
│       ├── get_config.py       # 远程仓库文件拉取
│       └── lib_manager.py      # lib 目录管理
├── README.md           # 项目说明文档
└── requirements.txt    # Python依赖
```

---