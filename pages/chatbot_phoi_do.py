import streamlit as st
import base64
import os
import json 

st.set_page_config(page_title="Chatbot phối đồ", layout="wide", initial_sidebar_state="collapsed")

# 1. CẬP NHẬT DANH MỤC TRONG TRẠNG THÁI CHUNG
if 'theme' not in st.session_state:
    st.session_state.theme = 'light' 
if 'current_step_index' not in st.session_state:
    st.session_state.current_step_index = 0

if 'selected_items' not in st.session_state:
    st.session_state.selected_items = {'Trang phục': None, 'Áo': None, 'Váy/Quần': None, 'Nón': None, 'Túi xách': None, 'Phụ kiện': None, 'Giày': None}

steps = ['Trang phục', 'Áo', 'Váy/Quần', 'Nón', 'Túi xách', 'Phụ kiện', 'Giày']
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

img_base64 = get_base64_of_bin_file('data/trongdong.jpg')
font_base64 = get_base64_of_bin_file('data/fontChu.otf') 

# -----------------------------
# CSS GIAO DIỆN VÀ THEME
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
        top: -3rem; left: 50%; transform: translateX(-50%);
        width: 100vw; height: 142px; 
        background-image: url('data:image/jpeg;base64,{img_base64}');
        background-size: 300px; background-repeat: repeat;
        filter: invert(1); opacity: 0.05; z-index: 0; pointer-events: none;
    }}
    .stMarkdown, p, span, div, h1, h2, h3, h4, h5, h6, label {{ color: #123C46 !important; font-weight: normal; }}
    .elodie-title {{ color: #D85A3F !important; }}
    [data-testid="stButton"] button {{ background-color: transparent !important; border: 2px solid #D85A3F !important; }}
    [data-testid="stButton"] button p {{ color: #D85A3F !important; font-weight: bold !important; }}
    [data-testid="stButton"] button:hover, [data-testid="stButton"] button:focus, [data-testid="stButton"] button:active {{ background-color: #D85A3F !important; }}
    [data-testid="stButton"] button:hover p, [data-testid="stButton"] button:focus p, [data-testid="stButton"] button:active p {{ color: #FFFFFF !important; }}
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
        top: -3rem; left: 50%; transform: translateX(-50%);
        width: 100vw; height: 142px; 
        background-image: url('data:image/jpeg;base64,{img_base64}');
        background-size: 300px; background-repeat: repeat;
        opacity: 0.15; z-index: 0; pointer-events: none;
    }}
    .stMarkdown, p, span, div, h1, h2, h3, h4, h5, h6, label {{ color: #F1E3C8 !important; font-weight: normal; }}
    .elodie-title {{ color: #E53935 !important; }} 
    [data-testid="stButton"] button {{ background-color: transparent !important; border: 2px solid #F1E3C8 !important; }}
    [data-testid="stButton"] button p {{ color: #F1E3C8 !important; font-weight: bold !important; }}
    [data-testid="stButton"] button:hover, [data-testid="stButton"] button:focus, [data-testid="stButton"] button:active {{ background-color: #F1E3C8 !important; border-color: #F1E3C8 !important; }}
    [data-testid="stButton"] button:hover p, [data-testid="stButton"] button:focus p, [data-testid="stButton"] button:active p {{ color: #781414 !important; }}
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
    html, body {{ overflow-x: hidden !important; }}
    @font-face {{ font-family: 'Elodie'; src: url(data:font/otf;charset=utf-8;base64,{font_base64}) format('opentype'); }}
    header[data-testid="stHeader"] {{ display: none !important; }}
    .block-container {{ position: relative; z-index: 1; padding-top: 2rem !important; }}
    .elodie-title {{ font-family: 'Elodie', sans-serif !important; letter-spacing: 1.5px !important; font-size: 32px !important; margin-bottom: 10px; font-weight: normal !important; position: relative; z-index: 2; }}
    [data-testid="stButton"] button {{ border-radius: 8px; transition: all 0.3s ease; padding: 6px 16px !important; position: relative; z-index: 2; display: flex; align-items: center; justify-content: center; }}
    [data-testid="stButton"] button p {{ font-size: 15px !important; margin: 0 !important; text-align: center; }}
    [data-testid="stButton"] button:hover {{ transform: translateY(-2px); }}
    [data-testid="stTextInput"] input {{ border-radius: 8px; position: relative; z-index: 2; }}
    .mockup-area {{ border-radius: 20px; height: 450px; display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 20px; position: relative; z-index: 2; }}
    .white-box {{ padding: 10px 25px; border-radius: 10px; margin: 5px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); font-weight: bold; font-size: 16px; }}
    .color-circle {{ width: 35px; height: 35px; border-radius: 50%; margin-bottom: 15px; cursor: pointer; display: block; position: relative; z-index: 2; }}
    .chatbot-area {{ border-radius: 15px; height: 450px; padding: 20px; display: flex; flex-direction: column; position: relative; z-index: 2; }}
    .product-card {{ border-radius: 10px; padding: 10px; text-align: center; position: relative; height: 180px; transition: all 0.2s; z-index: 2; margin-bottom: 15px; }}
    .product-card.selected::after {{ content: '✔'; position: absolute; bottom: 5px; left: 10px; font-size: 20px; font-weight: bold; }}
    .product-card img {{ width: 100%; height: 100px; object-fit: cover; border-radius: 5px; }}
    .product-name {{ margin-top: 10px; font-size: 14px; font-family: sans-serif; font-weight: bold !important; line-height: 1.3; }}
    {theme_css}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
st.markdown('<div class="scrollable-pattern"></div>', unsafe_allow_html=True)

# -----------------------------
# THANH ĐIỀU HƯỚNG CÓ NÚT THEME
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

st.markdown("<hr style='border: 1px solid rgba(241, 227, 200, 0.15); margin: 10px 0 20px 0; position: relative; z-index: 2;'>", unsafe_allow_html=True)

# -----------------------------
# NỬA TRÊN: MÀU - MOCKUP - CHATBOT
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
# NỬA DƯỚI: KHU VỰC CHỌN SẢN PHẨM
# -----------------------------
st.markdown("<hr style='border: 1px solid rgba(241, 227, 200, 0.15); margin: 10px 0 20px 0;'>", unsafe_allow_html=True)

# THUẬT TOÁN "CỬA SỔ TRƯỢT" CHO TAB BAR
nav_col1, nav_col2, nav_col3 = st.columns([1.5, 7, 1.5])
with nav_col1:
    if st.button("❮ Trước", disabled=(st.session_state.current_step_index == 0), use_container_width=True):
        st.session_state.current_step_index -= 1
        st.rerun()
        
with nav_col2:
    # Số lượng tab tối đa hiện trên màn hình (để không bị ép chữ)
    VISIBLE_TABS = 4
    
    # Tính toán vị trí bắt đầu hiển thị để tab đang chọn luôn nằm trong vùng nhìn thấy
    start_idx = st.session_state.current_step_index - (VISIBLE_TABS // 2)
    if start_idx < 0:
        start_idx = 0
    if start_idx > len(steps) - VISIBLE_TABS:
        start_idx = max(0, len(steps) - VISIBLE_TABS)
        
    # Cắt danh sách tab vừa đủ để hiển thị
    visible_steps = steps[start_idx : start_idx + VISIBLE_TABS]
    
    tab_cols = st.columns(len(visible_steps))
    for i, step_name in enumerate(visible_steps):
        real_index = start_idx + i
        with tab_cols[i]:
            btn_type = "primary" if real_index == st.session_state.current_step_index else "secondary"
            if st.button(step_name, type=btn_type, use_container_width=True, key=f"tab_{real_index}"):
                st.session_state.current_step_index = real_index
                st.rerun()
                
with nav_col3:
    if st.button("Tiếp ❯", disabled=(st.session_state.current_step_index == len(steps)-1), use_container_width=True):
        st.session_state.current_step_index += 1
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f'<div class="elodie-title">Chọn {current_step}</div>', unsafe_allow_html=True)

def load_json_data():
    try:
        with open('data/trang_phuc.json', 'r', encoding='utf-8') as f:
            trang_phuc = json.load(f)
        with open('data/phu_kien.json', 'r', encoding='utf-8') as f:
            phu_kien = json.load(f)
            
        data = {'Trang phục': [], 'Áo': [], 'Váy/Quần': [], 'Nón': [], 'Túi xách': [], 'Phụ kiện': [], 'Giày': []}
        
        for k, v in trang_phuc.items():
            data['Trang phục'].append({'id': k, 'name': v['ten'], 'file_prefix': v['file_prefix']})
            
        if 'ao_mac_trong' in phu_kien:
            for k, v in phu_kien['ao_mac_trong'].items():
                data['Áo'].append({'id': k, 'name': v['ten'], 'file_prefix': v['file_prefix']})
        if 'ao_khoac' in phu_kien:
            for k, v in phu_kien['ao_khoac'].items():
                data['Áo'].append({'id': k, 'name': v['ten'], 'file_prefix': v['file_prefix']})
                
        if 'quan_vay' in phu_kien:
            for k, v in phu_kien['quan_vay'].items():
                data['Váy/Quần'].append({'id': k, 'name': v['ten'], 'file_prefix': v['file_prefix']})
                
        if 'phu_kien_dau_va_toc' in phu_kien:
            for k, v in phu_kien['phu_kien_dau_va_toc'].items():
                if "mũ" in v['ten'].lower() or "nón" in v['ten'].lower():
                    data['Nón'].append({'id': k, 'name': v['ten'], 'file_prefix': v['file_prefix']})
                else:
                    data['Phụ kiện'].append({'id': k, 'name': v['ten'], 'file_prefix': v['file_prefix']})
                
        if 'tui_xach' in phu_kien:
            for k, v in phu_kien['tui_xach'].items():
                data['Túi xách'].append({'id': k, 'name': v['ten'], 'file_prefix': v['file_prefix']})
                
        if 'giay_dep' in phu_kien:
            for k, v in phu_kien['giay_dep'].items():
                data['Giày'].append({'id': k, 'name': v['ten'], 'file_prefix': v['file_prefix']})
                
        if 'trang_suc' in phu_kien:
            for k, v in phu_kien['trang_suc'].items():
                data['Phụ kiện'].append({'id': k, 'name': v['ten'], 'file_prefix': v['file_prefix']})
                    
        return data
    except Exception as e:
        st.error(f"Lỗi đọc dữ liệu: {e}")
        return {'Trang phục': [], 'Áo': [], 'Váy/Quần': [], 'Nón': [], 'Túi xách': [], 'Phụ kiện': [], 'Giày': []}

mock_data = load_json_data()
current_items = mock_data.get(current_step, [])

if current_step == 'Váy/Quần':
    vay_list = []
    quan_list = []
    for item in current_items:
        name_lower = item['name'].lower()
        if "váy" in name_lower or "đầm" in name_lower:
            vay_list.append(item)
        else:
            quan_list.append(item)
    current_items = vay_list + quan_list

# RENDER SẢN PHẨM (4 CỘT / HÀNG)
NUM_COLS = 4

for row_idx in range(0, len(current_items), NUM_COLS):
    row_items = current_items[row_idx:row_idx + NUM_COLS]
    cols = st.columns(NUM_COLS)
    
    for col_idx, item in enumerate(row_items):
        with cols[col_idx]:
            is_selected = False
            if st.session_state.selected_items[current_step] and st.session_state.selected_items[current_step]['id'] == item['id']:
                is_selected = True
            
            card_class = "product-card selected" if is_selected else "product-card"
            
            img_name = f"data/{item.get('file_prefix', '')}.png"
            item_img_base64 = get_base64_of_bin_file(img_name)
            
            if item_img_base64:
                img_src = f"data:image/png;base64,{item_img_base64}"
            else:
                img_src = f"https://via.placeholder.com/150x100/FFFFFF/123C46?text=No+Image"
            
            st.markdown(f"""
            <div class="{card_class}">
                <img src="{img_src}" alt="{item['name']}">
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