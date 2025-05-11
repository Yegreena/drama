# 🎬 短剧生成器 · Streamlit Web 应用

本项目是一个基于 [Streamlit](https://streamlit.io) 和 OpenAI API 的短剧创作辅助工具。支持用户通过文字/图片对话生成短剧大纲，并一键生成分镜脚本，适合剧本创作者、导演、编剧爱好者快速进行灵感整理与初步脚本开发。

---

## 📦 项目结构

drama_project/
├── home.py # 主入口文件
├── pages/ # 子页面模块（如分镜生成）
├── requirements.txt # 依赖包清单
└── README.md


---

## 🚀 如何运行

1. **安装依赖**

建议创建虚拟环境后运行：

```bash
pip install -r requirements.txt

2. **设置 API 密钥**

将你的 OpenAI API Key 写入 .env 文件（或者直接在代码中设置）：
OPENAI_API_KEY=your_api_key_here

3. **启动 Streamlit 应用**

```bash
streamlit run streamlit_app.py


🛠️ 功能说明
📋 支持通过聊天生成短剧题材、风格、故事大纲

✍️ 支持结构化展示人物设定、故事结构、情感基调

🎞️ 一键生成多镜头分镜脚本，支持上传参考图

💡 适合创作者快速整理创意和可视化演示

