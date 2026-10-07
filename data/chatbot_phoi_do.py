import streamlit as st
import base64
import os
import json 

st.set_page_config(page_title="Chatbot phối đồ", layout="wide", initial_sidebar_state="collapsed")

# Khởi tạo trạng thái chung
if 'theme' not in st.session_state:
    st.session_state.theme = 'light' 
if 'current_step_index' not in st.session_state:
    st.session_state.current_step_index = 0
if 'selected_items' not in st.session_state:
    st.session_state.selected_items = {'Áo': None, 'Quần': None, 'Nón': None, 'Túi xách': None, 'Phụ kiện': None}

steps = ['Áo', 'Quần', 'Nón', 'Túi xách', 'Phụ kiện']
current_step = steps[st.session_state.current_step_index]

def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        target_path = bin_file
    elif os.path.exists(os.path.join(os.path.dirname(__file__), '..', bin_file)):
        target_path = os.path.join(os.path.dirname(__file__), '..', bin_file)
    else:
        return ""
    with open(target_path, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_base64 = get_base64_of_bin_file('trongdong.jpg')
font_base64 = get_base64_of_bin_file('fontChu.otf') 

# -----------------------------
# 1. TẠO CSS ĐỘNG DỰA TRÊN THEME VÀ SỬA LỖI NÚT BẤM
# -----------------------------
if st.session_state.theme == 'light':
    theme_css = f"""
    [data-testid="stAppViewContainer"] {{
        background-color: #F3EEE0 !important;
        background-image: none !important;
        overflow-x: hidden !important;
    }}
    .scrollable-pattern {{
        position: absolute;
        top: -3rem; 
        left: 50%;
        transform: translateX(-50%);
        width: 100vw;
        height: 142px; 
        background-image: url('data:image/jpeg;base64,{img_base64}');
        background-size: 300px;
        background-repeat: repeat;
        filter: invert(1); 
        opacity: 0.05; 
        z-index: 0;
        pointer-events: none;
    }}
    
    /* Trả lại độ mỏng mặc định cho chữ thường */
    .stMarkdown, p, span, div, h1, h2, h3, h4, h5, h6, label {{ color: #123C46 !important; font-weight: normal; }}
    .elodie-title {{ color: #D85A3F !important; }}
    
    /* Giao diện nút bấm Theme sáng */
    [data-testid="stButton"] button {{ background-color: transparent !important; border: 2px solid #D85A3F !important; }}
    [data-testid="stButton"] button p {{ color: #D85A3F !important; font-weight: bold !important; }}
    
    [data-testid="stButton"] button:hover, [data-testid="stButton"] button:focus, [data-testid="stButton"] button:active {{ 
        background-color: #D85A3F !important; 
    }}
    [data-testid="stButton"] button:hover p, [data-testid="stButton"] button:focus p, [data-testid="stButton"] button:active p {{ 
        color: #FFFFFF !important; 
    }}
    
    div[data-testid="stButton"] > button[kind="primary"] {{ background-color: #D85A3F !important; border-color: #D85A3F !important; }}
    div[data-testid="stButton"] > button[kind="primary"] p {{ color: #FFFFFF !important; }}
    
    [data-testid="stTextInput"] input {{ background-color: #FFFFFF !important; color: #123C46 !important; border: 2px solid #559E9E !important; font-weight: normal !important; }}
    [data-testid="stTextInput"] input::placeholder {{ color: #8BA8A8 !important; }}
    
    .mockup-area {{ border: 3px solid #D85A3F; background-color: rgba(255, 255, 255, 0.55); }}
    .white-box {{ background-color: #FFFFFF; color: #123C46 !important; border: 1px solid #559E9E; }}
    .color-circle {{ border: 2px solid #123C46; }}
    .chatbot-area {{ background-color: rgba(222, 231, 231, 0.85); }}
    
    .product-card {{ border: 2px solid #559E9E; background-color: #FFFFFF; }}
    .product-card.selected {{ border: 3px solid #123C46; background-color: #DEE7E7; }}
    .product-card.selected::after {{ color: #123C46; }}
    .product-name {{ color: #123C46 !important; }}
    """
else:
    theme_css = f"""
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(120, 20, 20, 0.85), rgba(120, 20, 20, 0.9)) !important;
        background-image: linear-gradient(rgba(120, 20, 20, 0.85), rgba(120, 20, 20, 0.9)) !important; 
        overflow-x: hidden !important;
    }}
    .scrollable-pattern {{
        position: absolute;
        top: -3rem; 
        left: 50%;
        transform: translateX(-50%);
        width: 100vw;
        height: 142px; 
        background-image: url('data:image/jpeg;base64,{img_base64}');
        background-size: 300px;
        background-repeat: repeat;
        opacity: 0.15; 
        z-index: 0;
        pointer-events: none;
    }}
    
    /* Trả lại độ mỏng mặc định cho chữ thường */
    .stMarkdown, p, span, div, h1, h2, h3, h4, h5, h6, label {{ color: #F1E3C8 !important; font-weight: normal; }}
    .elodie-title {{ color: #E53935 !important; }} 
    
    /* Giao diện nút bấm Theme tối */
    [data-testid="stButton"] button {{ background-color: transparent !important; border: 2px solid #F1E3C8 !important; }}
    [data-testid="stButton"] button p {{ color: #F1E3C8 !important; font-weight: bold !important; }}
    
    [data-testid="stButton"] button:hover, [data-testid="stButton"] button:focus, [data-testid="stButton"] button:active {{ 
        background-color: #F1E3C8 !important; 
        border-color: #F1E3C8 !important; 
    }}
    [data-testid="stButton"] button:hover p, [data-testid="stButton"] button:focus p, [data-testid="stButton"] button:active p {{ 
        color: #781414 !important; 
    }}
    
    div[data-testid="stButton"] > button[kind="primary"] {{ background-color: #E53935 !important; border-color: #E53935 !important; }}
    div[data-testid="stButton"] > button[kind="primary"] p {{ color: #FFFFFF !important; }}
    
    [data-testid="stTextInput"] input {{ background-color: rgba(0,0,0,0.2) !important; color: #F1E3C8 !important; border: 1.5px solid #E53935 !important; font-weight: normal !important; }}
    [data-testid="stTextInput"] input::placeholder {{ color: #888 !important; }}
    
    .mockup-area {{ border: 3px solid #E53935; background-color: rgba(0, 0, 0, 0.2); }}
    .white-box {{ background-color: #4a0c0c; color: #F1E3C8 !important; border: 1px solid #E53935; }}
    .color-circle {{ border: 2px solid #F1E3C8; }}
    .chatbot-area {{ border-left: 2px solid rgba(241, 227, 200, 0.3); background-color: transparent; }}
    
    .product-card {{ border: 2px solid rgba(241, 227, 200, 0.2); background-color: rgba(74, 12, 12, 0.8); }}
    .product-card.selected {{ border: 3px solid #4CAF50; background-color: rgba(76, 175, 80, 0.1); }}
    .product-card.selected::after {{ color: #4CAF50; }}
    .product-name {{ color: #F1E3C8 !important; }}
    """

custom_css = f"""
<style>
    /* Xóa bỏ khoảng trắng và thanh cuộn ngang cấp cao nhất */
    html, body {{
        overflow-x: hidden !important;
    }}
    
    @font-face {{
        font-family: 'Elodie';
        src: url(data:font/otf;charset=utf-8;base64,{font_base64}) format('opentype');
    }}
    
    header[data-testid="stHeader"] {{ display: none !important; }}
    
    .block-container {{ position: relative; z-index: 1; padding-top: 2rem !important; }}
    
    /* Font Elodie trả về nguyên bản mềm mại */
    .elodie-title {{ 
        font-family: 'Elodie', sans-serif !important; 
        letter-spacing: 1.5px !important; 
        font-size: 32px !important; 
        margin-bottom: 10px; 
        font-weight: normal !important; 
        position: relative; 
        z-index: 2;
    }}
    
    /* Cấu hình kích thước nút nhỏ gọn và hiệu ứng nảy */
    [data-testid="stButton"] button {{ 
        border-radius: 8px; 
        transition: all 0.3s ease; 
        padding: 6px 16px !important; 
        position: relative; 
        z-index: 2;
    }}
    [data-testid="stButton"] button p {{
        font-size: 15px !important; 
        margin: 0 !important;
    }}
    [data-testid="stButton"] button:hover {{ transform: translateY(-2px); }}
    
    [data-testid="stTextInput"] input {{ border-radius: 8px; position: relative; z-index: 2; }}
    
    .mockup-area {{ border-radius: 20px; height: 450px; display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 20px; position: relative; z-index: 2; }}
    .white-box {{ padding: 10px 25px; border-radius: 10px; margin: 5px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); font-weight: bold; font-size: 16px; }}
    .color-circle {{ width: 35px; height: 35px; border-radius: 50%; margin-bottom: 15px; cursor: pointer; display: block; position: relative; z-index: 2; }}
    .chatbot-area {{ border-radius: 15px; height: 450px; padding: 20px; display: flex; flex-direction: column; position: relative; z-index: 2; }}
    
    .product-card {{ border-radius: 10px; padding: 10px; text-align: center; position: relative; height: 180px; transition: all 0.2s; z-index: 2; }}
    .product-card.selected::after {{ content: '✔'; position: absolute; bottom: 5px; left: 10px; font-size: 20px; font-weight: bold; }}
    .product-card img {{ width: 100%; height: 100px; object-fit: cover; border-radius: 5px; }}
    .product-name {{ margin-top: 10px; font-size: 14px; font-family: sans-serif; font-weight: bold !important; }}
    
    {theme_css}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
st.markdown('<div class="scrollable-pattern"></div>', unsafe_allow_html=True)

# -----------------------------
# 2. THANH ĐIỀU HƯỚNG CÓ NÚT THEME
# -----------------------------
top_left, top_mid, top_right, top_theme = st.columns([1.5, 6.5, 1, 1])
with top_left:
    if st.button("Trang chủ", use_container_width=True):
        st.switch_page("app.py")
with top_right:
    st.button("Xuất", type="primary", use_container_width=True)
with top_theme:
    theme_label = "Sáng" if st.session_state.theme == 'dark' else "Tối"
    if st.button(theme_label, use_container_width=True):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()

# Đổi màu đường kẻ ngang thanh điều hướng
st.markdown("<hr style='border: 1px solid rgba(241, 227, 200, 0.15); margin: 10px 0 20px 0; position: relative; z-index: 2;'>", unsafe_allow_html=True)

# -----------------------------
# 3. NỬA TRÊN: MÀU - MOCKUP - CHATBOT NGANG HÀNG
# -----------------------------
col_color, col_mockup, col_chat = st.columns([0.8, 6.2, 3])

with col_color:
    st.markdown('<div class="elodie-title" style="font-size: 24px !important; white-space: nowrap;">Màu</div>', unsafe_allow_html=True)
    colors = ['#E75A3A', '#7BC8C6', '#FCEBA7', '#0F4C5C', '#FFFFFF', '#000000']
    for c in colors:
        st.markdown(f'<div class="color-circle" style="background-color: {c};"></div>', unsafe_allow_html=True)

with col_mockup:
    mockup_html = '<div class="mockup-area">'
    mockup_html += '<div class="elodie-title" style="position:absolute; top:10px;">Preview Mockup</div>'
    
    has_item = False
    for k, v in st.session_state.selected_items.items():
        if v:
            mockup_html += f'<div class="white-box">✨ {k}: {v["name"]}</div>'
            has_item = True
            
    if not has_item:
        mockup_html += '<p>Chưa có trang phục nào được chọn</p>'
        
    mockup_html += '</div>'
    st.markdown(mockup_html, unsafe_allow_html=True)

with col_chat:
    st.markdown('<div class="chatbot-area">', unsafe_allow_html=True)
    st.markdown('<div class="elodie-title">Chatbot Tư Vấn</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:14px; margin-bottom:20px;">Khu vực tích hợp AI Chatbot. Hệ thống sẽ phân tích các trang phục bạn chọn và đưa ra gợi ý.</p>', unsafe_allow_html=True)
    st.text_input("Ví dụ: Áo Tấc đỏ nên phối với quần màu gì?", label_visibility="collapsed")
    st.button("Gửi")
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# 4. NỬA DƯỚI: KHU VỰC CHỌN SẢN PHẨM
# -----------------------------
# Đổi màu đường kẻ ngang khu vực sản phẩm
st.markdown("<hr style='border: 1px solid rgba(241, 227, 200, 0.15); margin: 10px 0 20px 0;'>", unsafe_allow_html=True)

nav_col1, nav_col2, nav_col3 = st.columns([1.5, 7, 1.5])
with nav_col1:
    if st.button("❮ Về trước", disabled=(st.session_state.current_step_index == 0), use_container_width=True):
        st.session_state.current_step_index -= 1
        st.rerun()
        
with nav_col2:
    tab_cols = st.columns(len(steps))
    for i, step in enumerate(steps):
        with tab_cols[i]:
            btn_type = "primary" if i == st.session_state.current_step_index else "secondary"
            if st.button(step, type=btn_type, use_container_width=True, key=f"tab_{i}"):
                st.session_state.current_step_index = i
                st.rerun()
                
with nav_col3:
    if st.button("Tiếp ❯", disabled=(st.session_state.current_step_index == len(steps)-1), use_container_width=True):
        st.session_state.current_step_index += 1
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f'<div class="elodie-title">Chọn {current_step}</div>', unsafe_allow_html=True)

mock_data = {
    'Áo': [{'id': 'a1', 'name': 'Áo Tấc Đỏ'}, {'id': 'a2', 'name': 'Áo Giao Lĩnh'}, {'id': 'a3', 'name': 'Áo Nhật Bình'}],
    'Quần': [{'id': 'q1', 'name': 'Quần Lụa Trắng'}, {'id': 'q2', 'name': 'Quần Đen Ống Rộng'}, {'id': 'q3', 'name': 'Váy Đụp'}],
    'Nón': [{'id': 'n1', 'name': 'Nón Quai Thao'}, {'id': 'n2', 'name': 'Khăn Đóng'}, {'id': 'n3', 'name': 'Nón Lá'}],
    'Túi xách': [{'id': 't1', 'name': 'Túi Gấm'}, {'id': 't2', 'name': 'Tay Nải'}],
    'Phụ kiện': [{'id': 'p1', 'name': 'Quạt Giấy'}, {'id': 'p2', 'name': 'Ngọc Bội'}]
}

current_items = mock_data.get(current_step, [])
item_cols = st.columns(max(len(current_items), 4)) 

for i, item in enumerate(current_items):
    with item_cols[i]:
        is_selected = False
        if st.session_state.selected_items[current_step] and st.session_state.selected_items[current_step]['id'] == item['id']:
            is_selected = True
        
        card_class = "product-card selected" if is_selected else "product-card"
        
        st.markdown(f"""
        <div class="{card_class}">
            <img src="https://via.placeholder.com/150x100/FFFFFF/123C46?text={item['name']}" alt="{item['name']}">
            <div class="product-name">{item['name']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        btn_label = "Hủy chọn" if is_selected else "Chọn"
        if st.button(btn_label, key=f"btn_{item['id']}", use_container_width=True):
            if is_selected:
                st.session_state.selected_items[current_step] = None 
            else:
                st.session_state.selected_items[current_step] = item 
            st.rerun()