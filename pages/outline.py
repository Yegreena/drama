import streamlit as st
import json
import os
from openai import OpenAI
import time

# Page configuration
st.set_page_config(
    page_title="短剧生成器 - 创意对话与大纲生成",
    layout="wide",
    
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .chat-container {
        height: 65vh;
        overflow-y: auto;
        border-radius: 10px;
        padding: 15px;
        background-color: #ffffff;
        margin-bottom: 10px;
        border: 1px solid #e0e0e0;
    }
    .outline-container {
        height: 85vh;
        overflow-y: auto;
        border-radius: 10px;
        padding: 20px;
        background-color: #f9f9f9;
        border: 1px solid #e6e6e6;
    }
    .stTextArea textarea {
        height: 100px;
    }
    .generate-btn {
        width: 100%;
        margin-top: 10px;
        background-color: #4CAF50;
        color: white;
    }
    .chat-btn {
        width: 100%;
        margin-top: 10px;
    }
    .next-btn {
        width: 100%;
        margin-top: 10px;
        background-color: #2196F3;
        color: white;
    }
    .header {
        text-align: center;
        margin-bottom: 20px;
    }
    .editable-field {
        margin-bottom: 15px;
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 5px;
    }
    .chat-message {
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 15px;
        max-width: 80%;
    }
    .user-message {
        background-color: #e1f5fe;
        margin-left: auto;
        margin-right: 10px;
    }
    .assistant-message {
        background-color: #f1f1f1;
        margin-right: auto;
        margin-left: 10px;
    }
    .inspiration-card {
        padding: 10px;
        background-color: #fff8e1;
        border-radius: 5px;
        margin-bottom: 10px;
        border-left: 4px solid #ffc107;
    }
    .system-message {
        background-color: #fff8e1;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 15px;
        border-left: 4px solid #ffc107;
        font-style: italic;
        font-size: 0.9em;
    }
    .outline-title {
        font-size: 1.5em;
        font-weight: bold;
        margin-bottom: 15px;
        padding-bottom: 5px;
        border-bottom: 2px solid #2196F3;
    }
    .outline-section {
        margin-bottom: 20px;
        padding: 15px;
        background-color: white;
        border-radius: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .section-title {
        font-weight: bold;
        margin-bottom: 10px;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    
if 'outline_data' not in st.session_state:
    st.session_state.outline_data = {
        "题材": "",
        "风格": "",
        "标题": "",
        "故事梗概": "",
        "人物设定": "",
        "故事结构": "",
        "情感基调": "",
        "潜在亮点": ""
    }

# Flag to clear input after submission
if 'clear_input' not in st.session_state:
    st.session_state.clear_input = False
    
# Flag to track if outline has been generated
if 'outline_generated' not in st.session_state:
    st.session_state.outline_generated = False

# Function to generate response using OpenAI API
def generate_chat_response(user_input):
    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your_api_key_here"))
        
        # System prompt for the AI screenwriter
        system_prompt = """你是一个经验丰富的**短剧编剧专家**，擅长将模糊的灵感发展为具有吸引力的完整故事。你的特长是：
        * 把普通情境转化为引人入胜的三分钟短剧；
        * 构建人物动机，设计戏剧冲突；
        * 精准控制节奏和转折，确保短小而不失高潮；
        * 可根据用户输入的**文本描述**判断故事风格与基调，协助用户迭代大纲。

        请以以下风格展开你的回应：
        1. **角色分析清晰**（帮用户明确人物设定与动机）
        2. **故事结构专业**（使用三幕式结构或冲突推进结构）
        3. **节奏控制得当**（适合短剧快节奏、强反转）
        4. **风格可调**（支持情感、悬疑、喜剧、科幻等多种类型）
        5. **鼓励协作**（主动提问，帮助用户完善模糊想法）

        注意：不要一次性提出太多问题，每次聚焦在1-2个最关键的问题上，引导用户逐步深入。
        回复要简洁有力，不要太长，聚焦在关键要素上。
        你的目标是帮助用户开发出一个能打动人心的短视频故事。"""
        
        # Prepare messages for API call
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add chat history
        for message in st.session_state.chat_history:
            messages.append({"role": message["role"], "content": message["content"]})
        
        # Add current user input
        messages.append({"role": "user", "content": user_input})
        
        # Call the API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.8,
            max_tokens=1000,
            # stream=True
        )
        
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"生成回复失败: {str(e)}")
        return "抱歉，我在处理您的请求时遇到了问题。请再试一次或者重新表述您的想法。"

# Function to generate outline using OpenAI API
def generate_outline():
    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your_api_key_here"))
        
        # Create system prompt for outline generation
        system_prompt = """你是一位专业的短剧大纲创作专家。
        请根据之前的对话内容，生成一个完整、专业的短剧大纲。
        你的输出必须包含以下八个部分，每个部分的内容要详细且富有创意：
        1. 【题材】：明确的剧作类型与背景
        2. 【风格】：创作风格与表达方式
        3. 【标题】：引人注目且反映内容的标题
        4. 【故事梗概】：200字左右的整体故事脉络
        5. 【人物设定】：主要角色的背景与动机
        6. 【故事结构】：三幕式或其他结构的明确分段
        7. 【情感基调】：作品的情感色彩与氛围描述
        8. 【潜在亮点】：值得关注的特色卖点
        
        以JSON格式输出，不要包含任何其他说明文字。确保每个部分都有实质性内容。"""
        
        # Prepare messages for API call
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add chat history for context
        for message in st.session_state.chat_history:
            messages.append({"role": message["role"], "content": message["content"]})
        
        # Call the API
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        # Extract and parse JSON content
        result = json.loads(response.choices[0].message.content)
        
        # Ensure expected structure with default values
        required_fields = ["题材", "风格", "标题", "故事梗概", "人物设定", "故事结构", "情感基调", "潜在亮点"]
        for field in required_fields:
            if field not in result:
                result[field] = ""
                
        return result
    except Exception as e:
        st.error(f"生成大纲失败: {str(e)}")
        return st.session_state.outline_data

# Function to navigate to script generation page
def go_to_script_generation():
    st.session_state.page = "script_generation"
    st.rerun()

# Add a welcome message to chat history if it's empty
if not st.session_state.chat_history:
    welcome_message = {
        "role": "assistant", 
        "content": """👋 你好！我是你的短剧创意顾问。我能帮你把简单的灵感发展成吸引人的短剧故事。

无论你有一个模糊的想法、一个场景、一种情感，或者甚至只是一种氛围，我都可以帮你构建一个完整的故事大纲。

请告诉我你的初步想法，比如：
- 一个情境（"办公室同事之间的暗恋"）
- 一种情感（"青春期的叛逆与和解"）
- 一个场景（"电梯里偶遇前任"）
- 一个角色（"事业有成但情感空虚的女性"）

我会引导你一步步完善故事，最后点击"生成故事大纲"按钮，我会为你创作一个完整的专业短剧大纲。"""
    }
    st.session_state.chat_history.append(welcome_message)

# Main application layout
st.markdown("<h1 class='header'>短剧生成器 - 创意对话</h1>", unsafe_allow_html=True)

# Create two columns for layout


# Left column - Chat     interface

st.markdown("<h3>创意对话</h3>", unsafe_allow_html=True)
    
container = st.container()

# User input section
st.markdown("<p style='font-size:14px; font-weight:bold;'>输入你的想法：</p>", unsafe_allow_html=True)

# Text input with proper clearing mechanism
if st.session_state.clear_input:
    st.session_state.clear_input = False
    user_input = st.text_area("", value="", height=100, key="user_input", 
                            placeholder="请输入你的创意或想法，例如：'想拍一个关于社交媒体时代友情的短剧'")
else:
    user_input = st.text_area("", height=100, key="user_input", 
                            placeholder="请输入你的创意或想法，例如：'想拍一个关于社交媒体时代友情的短剧'")

# Chat button
if st.button("发送消息", key="chat_button", type="primary", use_container_width=True):
    if user_input:
        # Add user message to chat history
        user_message = {"role": "user", "content": user_input}
        st.session_state.chat_history.append(user_message)
        
        # Generate response
        with st.spinner("思考中..."):
            response = generate_chat_response(user_input)

            # Add assistant response to chat history
            assistant_message = {"role": "assistant", "content": response}
            st.session_state.chat_history.append(assistant_message)
        
        # Clear input
        st.session_state.clear_input = True
        st.rerun()
    else:
        st.warning("请输入内容后再发送")

# Generate outline button
if st.button("生成故事大纲", key="generate_outline_button", type="secondary", use_container_width=True):
    if len(st.session_state.chat_history) > 1:  # Ensure there's some conversation
        with st.spinner("正在生成专业短剧大纲..."):
            outline_result = generate_outline()
            st.session_state.outline_data = outline_result
            st.session_state.outline_generated = True
            
            # Add system message about outline generation
            system_message = {"role": "system", "content": "已根据我们的对话生成了完整的短剧大纲，请查看右侧面板。"}
            st.session_state.chat_history.append(system_message)
        
        st.rerun()
    else:
        st.warning("请先进行一些创意讨论，再生成大纲")

with container:
    html_messages = ['<div class="chat-container">']

    # ✅ 把所有消息拼接成 html 字符串
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            html_messages.append(f'<div class="chat-message user-message">{message["content"]}</div>')
        elif message["role"] == "assistant":
            html_messages.append(f'<div class="chat-message assistant-message">{message["content"]}</div>')
        elif message["role"] == "system":
            html_messages.append(f'<div class="system-message">{message["content"]}</div>')

    html_messages.append('</div>')  # ✅ 结束 container

    # ✅ 一次性写入
    st.markdown("\n".join(html_messages), unsafe_allow_html=True)

# Right column - Outline display

st.markdown("## 短剧大纲")

st.text_input("标题", value=st.session_state.outline_data["标题"], key="title")

col1, col2 = st.columns(2)
with col1:
    st.text_input("题材", value=st.session_state.outline_data["题材"], key="genre")
with col2:
    st.text_input("风格", value=st.session_state.outline_data["风格"], key="style")

st.text_area("故事梗概", value=st.session_state.outline_data["故事梗概"], height=150, key="synopsis")

st.text_area("人物设定", value=st.session_state.outline_data["人物设定"], height=150, key="characters")

st.text_area("故事结构", value=st.session_state.outline_data["故事结构"], height=150, key="structure")

st.text_area("情感基调", value=st.session_state.outline_data["情感基调"], height=80, key="tone")

st.text_area("潜在亮点", value=st.session_state.outline_data["潜在亮点"], height=80, key="highlights")

if st.button("下一步生成脚本", key="next_button", type="primary", use_container_width=True):
    st.success("即将跳转到脚本生成页面...")
    time.sleep(1)
    go_to_script_generation()
