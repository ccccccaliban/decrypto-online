import streamlit as st
import random
import json
import os
import time

# ==========================================
# 1. 基础配置与字体设置
# ==========================================
st.set_page_config(page_title="解码战 Online", page_icon="📡", layout="wide")

# 注入自定义字体 CSS (保持你的字体设置)
st.markdown("""
    <style>
    @import url("https://fontsapi.zeoseven.com/881/main/result.css");
    
    html, body, [class*="css"] {
        font-family: "Jigmo", sans-serif;
        font-weight: normal;
    }
    h1, h2, h3 {
        font-family: "Jigmo", sans-serif !important;
    }
    .stButton button {
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

DATA_FILE = "online_rooms.json"
WORD_FILE = "word_sets.txt"  # <--- 指定你的词库文件名

# ==========================================
# 2. 词库读取逻辑 (新增)
# ==========================================
@st.cache_data # 使用缓存，避免每次刷新都重新读文件
def load_word_pool():
    """
    尝试从 txt 文件读取词库。
    忽略 [难度] 标签，将所有符合格式的词组混入一个大池子。
    """
    pool = []
    
    # 1. 尝试读取文件
    if os.path.exists(WORD_FILE):
        try:
            with open(WORD_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    # 跳过空行和 [标签]
                    if not line or (line.startswith("[") and line.endswith("]")):
                        continue
                    
                    # 处理中文逗号
                    line = line.replace("，", ",")
                    words = line.split(",")
                    
                    # 只有当这一行确实有词时才加入
                    if len(words) >= 4: 
                        # 取前4个词重新组合，确保干净
                        clean_line = ",".join([w.strip() for w in words[:4]])
                        pool.append(clean_line)
        except Exception as e
