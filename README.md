# 🎬 短剧生成器 · Streamlit Web 应用

本项目是一个基于 [Streamlit](https://streamlit.io) 和 [OpenAI API](https://platform.openai.com/) 的短剧创作辅助工具。  
支持用户通过文字或图片对话生成短剧大纲，并一键生成分镜脚本，适合剧本创作者、导演、编剧爱好者快速进行灵感整理与初步脚本开发。

---

## 📦 项目结构

```
drama_project/
├── home.py         # 主入口文件
├── pages/                   # 子页面模块（如分镜生成）
├── requirements.txt         # 依赖包清单
└── README.md
```

---

## 🚀 如何运行

### 1. 安装依赖

建议在虚拟环境中运行：

```bash
pip install -r requirements.txt
```

### 2. 设置 API 密钥

将你的 OpenAI API Key 写入 `.env` 文件：

```ini
# .env 文件内容示例
OPENAI_API_KEY=your_api_key_here
```

或者直接在代码中通过环境变量传入。

### 3. 启动应用

```bash
streamlit run streamlit_app.py
```

---

## 🛠️ 功能说明

- 📋 **创意对话生成题材与风格**  
  多轮对话帮助明确短剧方向与类型。

- ✍️ **结构化大纲编辑器**  
  包括标题、题材、风格、人物设定、故事结构、情感基调、潜在亮点等模块。

- 🎞️ **分镜脚本自动生成**  
  自动生成 10-15 镜头剧本，包括镜头描述、持续时间、景别，支持上传参考图。

- 💡 **灵感加速器**  
  降低剧本创作门槛，提升初稿效率。
