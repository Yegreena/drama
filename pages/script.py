import streamlit as st
import pandas as pd
import json
import os
from openai import OpenAI
import base64
from io import BytesIO
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="短剧生成器 - 分镜脚本",
    layout="wide",
    
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .header {
        text-align: center;
        margin-bottom: 20px;
    }
    .outline-container {
        border-radius: 10px;
        padding: 20px;
        background-color: #f9f9f9;
        border: 1px solid #e6e6e6;
        margin-bottom: 20px;
    }
    .script-container {
        border-radius: 10px;
        padding: 20px;
        background-color: #f9f9f9;
        border: 1px solid #e6e6e6;
    }
    .field-label {
        font-weight: bold;
        margin-bottom: 5px;
    }
    .field-content {
        margin-bottom: 15px;
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 5px;
    }
    .generate-btn {
        width: 100%;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .navigation-btn {
        width: 100%;
        margin-top: 10px;
    }
    .stDataFrame {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'outline_data' not in st.session_state:
    # Default values if coming directly to this page
    st.session_state.outline_data = {
        "题材": "都市职场",
        "风格": "轻喜剧",
        "标题": "加班人生",
        "故事梗概": "年轻白领小李在繁忙的都市职场中挣扎，一次意外的电梯故障让他与公司女神共处一室，发生了一系列啼笑皆非的故事。"
    }
    
if 'script_data' not in st.session_state:
    # Initialize with empty dataframe
    st.session_state.script_data = pd.DataFrame({
        "编号": [],
        "画面": [],
        "画面描述": [],
        "持续时间": [],
        "景别": []
    })

# Function to call OpenAI API and generate script
def generate_script(outline_data):
    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your_api_key_here"))
        
        # Prepare prompt based on outline data
        prompt = f"""
        根据以下短剧大纲，生成一个分镜脚本：
        
        标题：{outline_data['标题']}
        题材：{outline_data['题材']}
        风格：{outline_data['风格']}
        故事梗概：{outline_data['故事梗概']}
        
        请生成一个包含10-15个镜头的分镜脚本。对每个镜头，提供以下信息：
        1. 画面描述（详细描述每个镜头中发生了什么）
        2. 持续时间（以秒为单位）
        3. 景别（如：特写、近景、中景、远景、全景等）
        
        以JSON格式输出，每个镜头作为数组中的一个对象，包含"画面描述"、"持续时间"、"景别"三个字段。
        请确保输出是有效的JSON格式，不要包含任何额外的解释文字。
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一位专业的分镜脚本编剧，擅长将故事梗概转化为具体的分镜头脚本。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7  # 可选，增强输出一致性
        )
        
        # Parse response
        # 提取纯文本内容
        response_text = response.choices[0].message.content

        # 去除可能的```json或```包裹
        if response_text.startswith("```json"):
            response_text = response_text.strip("```json").strip("```").strip()
        elif response_text.startswith("```"):
            response_text = response_text.strip("```").strip()

        result = json.loads(response_text)

        # 判断返回的数据结构
        if isinstance(result, dict):
            if "镜头" in result:
                shots = result["镜头"]
            elif "shots" in result:
                shots = result["shots"]
            else:
                shots = []
        elif isinstance(result, list):
            shots = result
        else:
            shots = []

        script_data = []
        for i, shot in enumerate(shots, 1):
            script_data.append({
                "编号": i,
                "画面": None,
                "画面描述": shot.get("画面描述", ""),
                "持续时间": int(shot.get("持续时间", 3)),  # 默认 3 秒，转换为整数
                "景别": shot.get("景别", "")
            })

        return pd.DataFrame(script_data)

    
    except Exception as e:
        st.error(f"生成脚本失败: {str(e)}")
        # Return a basic template on error
        return pd.DataFrame({
            "编号": [1, 2],
            "画面": [None, None],
            "画面描述": ["场景描述示例1", "场景描述示例2"],
            "持续时间": ["3秒", "4秒"],
            "景别": ["中景", "近景"]
        })

# Function to handle image uploads
def handle_image_upload(img_file):
    if img_file is not None:
        try:
            image = Image.open(img_file)
            # Resize image to a thumbnail for display efficiency
            image.thumbnail((200, 200))
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            return buffered.getvalue()
        except Exception as e:
            st.error(f"图片处理错误: {str(e)}")
    return None

# Function to go back to outline generation page
def go_to_outline_page():
    # In a real multi-page app, this would navigate to the first page
    st.session_state.page = "outline_generation"
    st.experimental_rerun()

# Function to update script data after editing
def update_script_data(edited_df):
    st.session_state.script_data = edited_df

# Main application layout
st.markdown("<h1 class='header'>短剧生成器 - 分镜脚本</h1>", unsafe_allow_html=True)

# Top section - Outline display and editing
st.markdown("## 故事大纲")

st.markdown("<div class='field-label'>故事梗概</div>", unsafe_allow_html=True)
st.session_state.outline_data["故事梗概"] = st.text_area(
    label="",
    value=st.session_state.outline_data["故事梗概"],
    height=150,
    key="synopsis_input"
)

# Generate script button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("生成分镜脚本", key="generate_script_btn", use_container_width=True):
        with st.spinner("正在生成分镜脚本..."):
            # Generate new script
            script_df = generate_script(st.session_state.outline_data)
            st.session_state.script_data = script_df
            st.success("分镜脚本生成完成！")

# Bottom section - Script table display and editing
st.markdown("## 分镜脚本")

with st.container():
    # Check if script data exists and has rows
    if not st.session_state.script_data.empty:
        # Create a copy to avoid modifying the original during editing
        edited_df = st.data_editor(
            st.session_state.script_data,
            column_config={
                "编号": st.column_config.NumberColumn(
                    "编号",
                    help="镜头序号",
                    disabled=True,
                    width="small"
                ),
                "画面": st.column_config.ImageColumn(
                    "画面",
                    help="点击上传镜头参考图片",
                    width="medium"
                ),
                "画面描述": st.column_config.TextColumn(
                    "画面描述",
                    help="详细描述镜头中发生的事情",
                    width="large",
                    max_chars=200
                ),
                "持续时间": st.column_config.NumberColumn(
                    "持续时间（秒）",
                    help="镜头持续的时间（单位：秒）",
                    step=1,
                    min_value=1,
                    max_value=60,
                    width="small"
                ),
                "景别": st.column_config.SelectboxColumn(
                    "景别",
                    help="选择镜头景别",
                    width="medium",
                    options=[
                        "特写", "近景", "中景", "远景", "全景",
                        "俯视", "仰视", "平视", "主观镜头", "其他"
                    ]
                )
            },
            hide_index=True,
            num_rows="dynamic",
            key="script_table",
            use_container_width=True
        )

        
        # Update session state with edited data
        if st.button("保存修改", key="save_changes_btn"):
            st.session_state.script_data = edited_df
            st.success("修改已保存！")
    else:
        st.info('点击上方的"生成分镜脚本"按钮来创建分镜表格。')

