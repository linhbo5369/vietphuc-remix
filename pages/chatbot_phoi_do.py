import streamlit as st
import base64
import os
import json 
import sys

# Thêm thư mục gốc vào đường dẫn hệ thống để Python tìm thấy file ai_handler.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.chatbot_service import khoi_tao_chatbot, gui_tin_nhan

st.set_page_config(page_title="Chatbot phối đồ", layout="wide", initial_sidebar_state="collapsed")

if 'theme' not in st.session_state:
    st.session_state.theme = 'light' 
if 'current_step_index' not in st.session_state:
    st.session_state.current_step_index = 0

if 'selected_items' not in st.session_state:
    st.session_state.selected_items = {'Trang phục': None, 'Áo': None, 'Váy/Quần': None, 'Nón': None, 'Túi xách': None, 'Phụ kiện': [], 'Giày': None}

if 'user_gender' not in st.session_state:
    st.session_state.user_gender = None 
if 'user_color' not in st.session_state:
    st.session_state.user_color = None

# --- KHỞI TẠO BỘ NHỚ LỊCH SỬ CHAT VÀ LỜI CHÀO MỞ ĐẦU ---
if "chat_session" not in st.session_state:
    st.session_state.chat_session = khoi_tao_chatbot()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hé lô bồ tèo! ✨ Tui là Stylist AI của Việt Phục Remix đây. Bạn đã có dự định chọn loại Việt phục nào hay chưa?"}
    ]

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

def get_dynamic_image_path(item, user_gender, user_color_code):
    prefix = item.get('file_prefix', '')
    gioi_tinh_list = item.get('gioi_tinh', [])
    
    if "Nam" in gioi_tinh_list and "Nữ" in gioi_tinh_list:
        gender_tag = "unisex"
    elif "Nữ" in gioi_tinh_list:
        gender_tag = "nu"
    elif "Nam" in gioi_tinh_list:
        gender_tag = "nam"
    else:
        gender_tag = ""

    if gender_tag and user_color_code:
        exact_path = f"data/{prefix}_{gender_tag}_{user_color_code}.png"
        if os.path.exists(exact_path) or os.path.exists(os.path.join("..", exact_path)):
            return exact_path
            
    target_dir = 'data' if os.path.exists('data') else '../data'
    if os.path.exists(target_dir):
        for filename in os.listdir(target_dir):
            if filename.startswith(prefix) and filename.endswith('.png'):
                if gender_tag and f"_{gender_tag}_" in filename:
                    return f"data/{filename}"
                return f"data/{filename}"
                
    return f"data/{prefix}.png"

img_base64 = get_base64_of_bin_file('trongdong.jpg')
font_base64 = get_base64_of_bin_file('fontChu.otf') 

if st.session_state.theme == 'light':
    theme_css = f"""
    [data-testid="stAppViewContainer"] {{ background-color: #F3EEE0 !important; background-image: none !important; overflow-x: hidden !important; }}
    .scrollable-pattern {{ position: absolute; top: -3rem; left: 50%; transform: translateX(-50%); width: 100vw; height: 142px; background-image: url('data:image/jpeg;base64,{img_base64}'); background-size: 300px; background-repeat: repeat; filter: invert(1); opacity: 0.05; z-index: 0; pointer-events: none; }}
    .stMarkdown, p, span, div, h1, h2, h3, h4, h5, h6, label {{ color: #123C46 !important; font-weight: normal; }}
    .elodie-title {{ color: #D85A3F !important; }}
    [data-testid="stButton"] button {{ background-color: transparent !important; border: 2px solid #D85A3F !important; }}
    [data-testid="stButton"] button p {{ color: #D85A3F !important; font-weight: bold !important; }}
    [data-testid="stButton"] button:hover, [data-testid="stButton"] button:focus, [data-testid="stButton"] button:active {{ background-color: #D85A3F !important; }}
    [data-testid="stButton"] button:hover p, [data-testid="stButton"] button:focus p, [data-testid="stButton"] button:active p {{ color: #FFFFFF !important; }}
    .mockup-area {{ border: 3px solid #D85A3F; background-color: rgba(255, 255, 255, 0.55); }}
    .color-circle {{ border: 2px solid #123C46; }}
    
    /* GỠ BỎ NỀN ĐEN KHUNG CHAT TỔNG */
    div[data-testid="column"]:nth-of-type(3) div[data-testid="stVerticalBlockBorderWrapper"] {{ background-color: transparent !important; border: none !important; padding: 10px; }}
    
    /* CẬP NHẬT: SỬA LỖI MÀU CHỮ BỊ TÀNG HÌNH TRONG BONG BÓNG USER */
    .chat-bubble.user {{ background-color: #123C46 !important; border-radius: 20px 20px 0px 20px; }}
    .chat-bubble.user, .chat-bubble.user p, .chat-bubble.user span, .chat-bubble.user div, .chat-bubble.user b {{ color: #FFFFFF !important; }}
    
    .chat-bubble.bot {{ background-color: #FFFFFF !important; border: 1.5px solid #559E9E; border-radius: 20px 20px 20px 0px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
    .chat-bubble.bot, .chat-bubble.bot p, .chat-bubble.bot span, .chat-bubble.bot div, .chat-bubble.bot b {{ color: #123C46 !important; }}
    
    /* XÓA BỎ LỚP NỀN TỐI MẶC ĐỊNH CỦA Ô NHẬP LIỆU CHAT INPUT VÀ ÉP MÀU TRẮNG TƯƠI */
    div[data-testid="stChatInput"] > div {{ background-color: #FFFFFF !important; border: 2px solid #559E9E !important; border-radius: 15px !important; }}
    div[data-testid="stChatInput"] div[data-baseweb="textarea"], div[data-testid="stChatInput"] div[data-baseweb="base-input"] {{ background-color: transparent !important; }}
    div[data-testid="stChatInput"] textarea {{ background-color: transparent !important; color: #123C46 !important; -webkit-text-fill-color: #123C46 !important; caret-color: #D85A3F !important; font-weight: bold !important; font-size: 15px !important; }}
    div[data-testid="stChatInput"] textarea::placeholder {{ color: #8BA8A8 !important; -webkit-text-fill-color: #8BA8A8 !important; font-weight: normal !important; }}
    """
else:
    theme_css = f"""
    [data-testid="stAppViewContainer"] {{ background: linear-gradient(rgba(120, 20, 20, 0.85), rgba(120, 20, 20, 0.9)) !important; background-image: linear-gradient(rgba(120, 20, 20, 0.85), rgba(120, 20, 20, 0.9)) !important; overflow-x: hidden !important; }}
    .scrollable-pattern {{ position: absolute; top: -3rem; left: 50%; transform: translateX(-50%); width: 100vw; height: 142px; background-image: url('data:image/jpeg;base64,{img_base64}'); background-size: 300px; background-repeat: repeat; opacity: 0.15; z-index: 0; pointer-events: none; }}
    .stMarkdown, p, span, div, h1, h2, h3, h4, h5, h6, label {{ color: #F1E3C8 !important; font-weight: normal; }}
    .elodie-title {{ color: #E53935 !important; }} 
    [data-testid="stButton"] button {{ background-color: transparent !important; border: 2px solid #F1E3C8 !important; }}
    [data-testid="stButton"] button p {{ color: #F1E3C8 !important; font-weight: bold !important; }}
    [data-testid="stButton"] button:hover, [data-testid="stButton"] button:focus, [data-testid="stButton"] button:active {{ background-color: #F1E3C8 !important; border-color: #F1E3C8 !important; }}
    [data-testid="stButton"] button:hover p, [data-testid="stButton"] button:focus p, [data-testid="stButton"] button:active p {{ color: #781414 !important; }}
    .mockup-area {{ border: 3px solid #E53935; background-color: rgba(0, 0, 0, 0.2); }}
    .color-circle {{ border: 2px solid #F1E3C8; }}
    
    /* GỠ BỎ NỀN ĐEN KHUNG CHAT TỔNG */
    div[data-testid="column"]:nth-of-type(3) div[data-testid="stVerticalBlockBorderWrapper"] {{ background-color: transparent !important; border: none !important; padding: 10px; }}
    
    /* CẬP NHẬT: SỬA LỖI MÀU CHỮ BỊ TÀNG HÌNH TRONG BONG BÓNG USER */
    .chat-bubble.user {{ background-color: #E53935 !important; border-radius: 20px 20px 0px 20px; }}
    .chat-bubble.user, .chat-bubble.user p, .chat-bubble.user span, .chat-bubble.user div, .chat-bubble.user b {{ color: #FFFFFF !important; }}
    
    .chat-bubble.bot {{ background-color: rgba(0,0,0,0.6) !important; border: 1px solid #E53935; border-radius: 20px 20px 20px 0px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }}
    .chat-bubble.bot, .chat-bubble.bot p, .chat-bubble.bot span, .chat-bubble.bot div, .chat-bubble.bot b {{ color: #F1E3C8 !important; }}
    
    /* XÓA BỎ LỚP NỀN TỐI MẶC ĐỊNH CỦA Ô NHẬP LIỆU CHAT INPUT VÀ ÉP MÀU RIÊNG CHO DARK THEME */
    div[data-testid="stChatInput"] > div {{ background-color: rgba(0,0,0,0.5) !important; border: 1.5px solid #E53935 !important; border-radius: 15px !important; }}
    div[data-testid="stChatInput"] div[data-baseweb="textarea"], div[data-testid="stChatInput"] div[data-baseweb="base-input"] {{ background-color: transparent !important; }}
    div[data-testid="stChatInput"] textarea {{ background-color: transparent !important; color: #F1E3C8 !important; -webkit-text-fill-color: #F1E3C8 !important; caret-color: #E53935 !important; font-weight: bold !important; font-size: 15px !important; }}
    div[data-testid="stChatInput"] textarea::placeholder {{ color: #888888 !important; -webkit-text-fill-color: #888888 !important; font-weight: normal !important; }}
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
    .mockup-area {{ border-radius: 20px; height: 500px; display: flex; flex-direction: column; position: relative; z-index: 2; overflow: hidden; }}
    .white-box {{ border-radius: 8px; margin: 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); font-weight: bold; font-family: sans-serif; z-index: 20; color: #123C46; }}
    .color-circle {{ width: 35px; height: 35px; border-radius: 50%; margin-bottom: 15px; cursor: pointer; display: block; position: relative; z-index: 2; }}
    .product-card {{ border-radius: 10px; padding: 10px; text-align: center; position: relative; height: 230px; transition: all 0.2s; z-index: 2; margin-bottom: 15px; }}
    .product-card.selected::after {{ content: '✔'; position: absolute; bottom: 5px; left: 10px; font-size: 20px; font-weight: bold; }}
    .product-card img {{ width: 100%; height: 150px; object-fit: contain; border-radius: 5px; background-color: transparent; }}
    .product-name {{ margin-top: 10px; font-size: 14px; font-family: sans-serif; font-weight: bold !important; line-height: 1.3; }}
    
    /* CSS BỐ CỤC CHAT ROW */
    .chat-row {{ display: flex; width: 100%; margin-bottom: 15px; }}
    .chat-row.user {{ justify-content: flex-end; padding-left: 15%; }}
    .chat-row.bot {{ justify-content: flex-start; padding-right: 15%; }}
    .chat-bubble {{ padding: 12px 18px; max-width: 100%; font-size: 15px; line-height: 1.5; font-family: sans-serif; }}
    
    /* Làm đẹp thanh cuộn chat */
    div[data-testid="stVerticalBlockBorderWrapper"] > div {{ overflow-y: auto; overflow-x: hidden; scrollbar-width: thin; padding-right: 5px; }}
    {theme_css}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
st.markdown('<div class="scrollable-pattern"></div>', unsafe_allow_html=True)

top_left, top_mid, top_right, top_theme = st.columns([1.5, 6.5, 1, 1])
with top_left:
    if st.button("Trang chủ", use_container_width=True):
        st.switch_page("app.py")
with top_right:
    if st.button("Xuất", type="primary", use_container_width=True):
        st.switch_page("pages/final_result.py")
with top_theme:
    theme_label = "Sáng" if st.session_state.theme == 'dark' else "Tối"
    if st.button(theme_label, use_container_width=True):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()

st.markdown("<hr style='border: 1px solid rgba(241, 227, 200, 0.15); margin: 10px 0 20px 0; position: relative; z-index: 2;'>", unsafe_allow_html=True)

col_color, col_mockup, col_chat = st.columns([0.8, 6.2, 3])

with col_color:
    st.markdown('<div class="elodie-title" style="font-size: 24px !important; white-space: nowrap;">Màu</div>', unsafe_allow_html=True)
    colors = ['#E75A3A', '#7BC8C6', '#FCEBA7', '#0F4C5C', '#FFFFFF', '#000000']
    for c in colors:
        st.markdown(f'<div class="color-circle" style="background-color: {c};"></div>', unsafe_allow_html=True)

with col_mockup:
    mockup_positions = {
        'Trang phục': "top: 10%; left: 30%; transform: translateX(-50%); height: 75%; z-index: 2;",
        'Áo': "top: 15%; left: 70%; transform: translateX(-50%); height: 38%; z-index: 3;",
        'Váy/Quần': "top: 45%; left: 70%; transform: translateX(-50%); height: 48%; z-index: 1;",
        'Nón': "top: 5%; left: 70%; transform: translateX(-50%); height: 16%; z-index: 10;",
        'Túi xách': "top: 45%; left: 88%; transform: translateX(-50%); height: 22%; z-index: 5;",
        'Giày': "bottom: 15%; left: 70%; transform: translateX(-50%); height: 15%; z-index: 5;"
    }
    
    mockup_html = '<div class="mockup-area">'
    mockup_html += '<div class="elodie-title" style="position:absolute; top:10px; left: 50%; transform: translateX(-50%); z-index: 0; opacity: 0.8; text-shadow: 2px 2px 5px rgba(255,255,255,0.7);">Preview Mockup</div>'
    
    has_item = False
    for k, v in st.session_state.selected_items.items():
        if v: has_item = True
            
    if not has_item:
        mockup_html += '<div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 10; font-size: 16px; text-align: center; width: 100%;">Chưa có trang phục nào được chọn</div>'
    else:
        for k, v in st.session_state.selected_items.items():
            if v:
                if k == 'Phụ kiện':
                    for idx, acc in enumerate(v):
                        img_name = get_dynamic_image_path(acc, st.session_state.user_gender, st.session_state.user_color)
                        item_img_base64 = get_base64_of_bin_file(img_name)
                        if item_img_base64:
                            img_src = f"data:image/png;base64,{item_img_base64}"
                            name_lower = acc["name"].lower()
                            
                            if "thắt lưng" in name_lower or "đai" in name_lower:
                                pos_style = "top: 46%; left: 30%; transform: translateX(-50%); height: 6%; z-index: 6;"
                            elif "khăn" in name_lower or "trâm" in name_lower or "mũ phượng" in name_lower or "cánh chuồn" in name_lower:
                                pos_style = "top: 2%; left: 30%; transform: translateX(-50%); height: 12%; z-index: 5;"
                            elif "kính" in name_lower:
                                pos_style = "top: 15%; left: 15%; transform: translateX(-50%); height: 6%; z-index: 5;"
                            elif "khuyên" in name_lower:
                                pos_style = "top: 25%; left: 15%; transform: translateX(-50%); height: 8%; z-index: 5;"
                            elif "nhẫn" in name_lower or "đồng hồ" in name_lower or "vòng" in name_lower:
                                pos_style = "top: 35%; left: 15%; transform: translateX(-50%); height: 8%; z-index: 5;"
                            else:
                                pos_style = f"top: {45 + (idx * 5)}%; left: 15%; transform: translateX(-50%); height: 10%; z-index: 5;"
                                
                            mockup_html += f'<img src="{img_src}" style="position: absolute; {pos_style} object-fit: contain; filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));">'
                else:
                    img_name = get_dynamic_image_path(v, st.session_state.user_gender, st.session_state.user_color)
                    item_img_base64 = get_base64_of_bin_file(img_name)
                    if item_img_base64:
                        img_src = f"data:image/png;base64,{item_img_base64}"
                        pos_style = mockup_positions.get(k, "")
                        mockup_html += f'<img src="{img_src}" style="position: absolute; {pos_style} object-fit: contain; filter: drop-shadow(2px 4px 8px rgba(0,0,0,0.4));">'
        
        mockup_html += '<div style="position:absolute; bottom:8px; left:10px; right:10px; display:flex; flex-wrap:wrap; gap:6px; justify-content:center; z-index:20;">'
        for k, v in st.session_state.selected_items.items():
            if v:
                if k == 'Phụ kiện':
                    for acc in v:
                        mockup_html += f'<div class="white-box" style="font-size:11px; padding:4px 10px; background-color: rgba(255,255,255,0.85); border-radius: 15px;">✨ {acc["name"]}</div>'
                else:
                    mockup_html += f'<div class="white-box" style="font-size:11px; padding:4px 10px; background-color: rgba(255,255,255,0.85); border-radius: 15px;">✨ {v["name"]}</div>'
        mockup_html += '</div>'
    
    mockup_html += '</div>'
    st.markdown(mockup_html, unsafe_allow_html=True)

with col_chat:
    with st.container(height=500, border=False):
        st.markdown('<div class="elodie-title" style="margin-top:-10px; margin-bottom:20px;">Chatbot Tư Vấn</div>', unsafe_allow_html=True)
        
        # --- HỆ THỐNG RENDER CHAT DẠNG HTML (ZALO/MESSENGER STYLE) ---
        chat_log = st.container(height=360, border=False)
        with chat_log:
            chat_html = '<div style="display:flex; flex-direction:column; padding-bottom: 20px;">'
            for msg in st.session_state.messages:
                role_class = "user" if msg["role"] == "user" else "bot"
                
                content_html = ""
                if type(msg["content"]) is str:
                    content_html = msg["content"].replace('\n', '<br>')
                else:
                    resp = msg["content"]
                    if "loi" in resp:
                        content_html = f'<span style="color: red;">{resp["loi"]}</span>'
                    else:
                        if resp.get("ten_trang_phuc"): content_html += f"<b>👗 Trang phục:</b> {resp['ten_trang_phuc']}<br><br>"
                        if resp.get("loi_khuyen_stylist"): content_html += f"<b>💡 Lời khuyên:</b> {resp['loi_khuyen_stylist']}<br><br>"
                        if resp.get("phoi_hien_dai"): content_html += f"<b>✨ Phối hiện đại:</b> {resp['phoi_hien_dai']}<br><br>"
                        if resp.get("phoi_mau"): content_html += f"<b>🎨 Phối màu:</b> {resp['phoi_mau']}"
                
                chat_html += f'<div class="chat-row {role_class}"><div class="chat-bubble {role_class}">{content_html}</div></div>'
            chat_html += '</div>'
            st.markdown(chat_html, unsafe_allow_html=True)
        
        # Ô nhập tin nhắn
        if prompt := st.chat_input("Nhập tin nhắn cho AI..."):
            # Lọc từ khóa
            q_lower = prompt.lower()
            if "nam" in q_lower.split():
                st.session_state.user_gender = "Nam"
            elif "nữ" in q_lower or "nu" in q_lower.split():
                st.session_state.user_gender = "Nữ"
                
            colors_map = {"đỏ": "do", "đen": "den", "trắng": "trang", "xanh": "xanh", "vàng": "vang", "nâu": "nau", "tím": "tim", "cam": "cam", "be": "be", "xám": "xam"}
            for k, v in colors_map.items():
                if k in q_lower:
                    st.session_state.user_color = v
                    break

            # Lưu tin nhắn user và gọi AI
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.spinner("Stylist AI đang rep tin nhắn..."):
                ai_response_str = gui_tin_nhan(st.session_state.chat_session, prompt)
                try:
                    ai_data = json.loads(ai_response_str)
                    st.session_state.messages.append({"role": "assistant", "content": ai_data})
                except json.JSONDecodeError:
                    # Nếu AI trả lời chữ thuần (không phải JSON), lưu dạng chuỗi
                    st.session_state.messages.append({"role": "assistant", "content": ai_response_str})
            
            # Khởi động lại trang để render HTML mới
            st.rerun()

st.markdown("<hr style='border: 1px solid rgba(241, 227, 200, 0.15); margin: 10px 0 20px 0;'>", unsafe_allow_html=True)

nav_col1, nav_col2, nav_col3 = st.columns([1.5, 7, 1.5])
with nav_col1:
    if st.button("❮ Trước", disabled=(st.session_state.current_step_index == 0), use_container_width=True):
        st.session_state.current_step_index -= 1
        st.rerun()
        
with nav_col2:
    VISIBLE_TABS = 4
    start_idx = st.session_state.current_step_index - (VISIBLE_TABS // 2)
    if start_idx < 0: start_idx = 0
    if start_idx > len(steps) - VISIBLE_TABS: start_idx = max(0, len(steps) - VISIBLE_TABS)
        
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
            data['Trang phục'].append({'id': k, 'name': v['ten'], 'file_prefix': v['file_prefix'], 'gioi_tinh': v.get('gioi_tinh', [])})
            
        if 'ao_mac_trong' in phu_kien:
            for k, v in phu_kien['ao_mac_trong'].items():
                data['Áo'].append({'id': k, 'name': v['ten'], 'file_prefix': v['file_prefix'], 'gioi_tinh': v.get('gioi_tinh', [])})
        if 'ao_khoac' in phu_kien:
            for k, v in phu_kien['ao_khoac'].items():
                data['Áo'].append({'id': k, 'name': v['ten'], 'file_prefix': v['file_prefix'], 'gioi_tinh': v.get('gioi_tinh', [])})
                
        if 'quan_vay' in phu_kien:
            for k, v in phu_kien['quan_vay'].items():
                data['Váy/Quần'].append({'id': k, 'name': v['ten'], 'file_prefix': v['file_prefix'], 'gioi_tinh': v.get('gioi_tinh', [])})
                
        if 'phu_kien_dau_va_toc' in phu_kien:
            for k, v in phu_kien['phu_kien_dau_va_toc'].items():
                if "mũ" in v['ten'].lower() or "nón" in v['ten'].lower():
                    data['Nón'].append({'id': k, 'name': v['ten'], 'file_prefix': v['file_prefix'], 'gioi_tinh': v.get('gioi_tinh', [])})
                else:
                    data['Phụ kiện'].append({'id': k, 'name': v['ten'], 'file_prefix': v['file_prefix'], 'gioi_tinh': v.get('gioi_tinh', [])})
                
        if 'tui_xach' in phu_kien:
            for k, v in phu_kien['tui_xach'].items():
                data['Túi xách'].append({'id': k, 'name': v['ten'], 'file_prefix': v['file_prefix'], 'gioi_tinh': v.get('gioi_tinh', [])})
                
        if 'giay_dep' in phu_kien:
            for k, v in phu_kien['giay_dep'].items():
                data['Giày'].append({'id': k, 'name': v['ten'], 'file_prefix': v['file_prefix'], 'gioi_tinh': v.get('gioi_tinh', [])})
                
        if 'trang_suc' in phu_kien:
            for k, v in phu_kien['trang_suc'].items():
                data['Phụ kiện'].append({'id': k, 'name': v['ten'], 'file_prefix': v['file_prefix'], 'gioi_tinh': v.get('gioi_tinh', [])})
                    
        return data
    except Exception as e:
        st.error(f"Lỗi đọc dữ liệu: {e}")
        return {'Trang phục': [], 'Áo': [], 'Váy/Quần': [], 'Nón': [], 'Túi xách': [], 'Phụ kiện': [], 'Giày': []}

mock_data = load_json_data()
current_items = mock_data.get(current_step, [])

if st.session_state.user_gender:
    filtered_items = []
    for item in current_items:
        gioi_tinh_list = item.get('gioi_tinh', [])
        if not gioi_tinh_list or st.session_state.user_gender in gioi_tinh_list:
            filtered_items.append(item)
    current_items = filtered_items

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

NUM_COLS = 4

for row_idx in range(0, len(current_items), NUM_COLS):
    row_items = current_items[row_idx:row_idx + NUM_COLS]
    cols = st.columns(NUM_COLS)
    
    for col_idx, item in enumerate(row_items):
        with cols[col_idx]:
            if current_step == 'Phụ kiện':
                is_selected = any(i['id'] == item['id'] for i in st.session_state.selected_items['Phụ kiện'])
            else:
                is_selected = False
                if st.session_state.selected_items[current_step] and st.session_state.selected_items[current_step]['id'] == item['id']:
                    is_selected = True
            
            card_class = "product-card selected" if is_selected else "product-card"
            
            img_name = get_dynamic_image_path(item, st.session_state.user_gender, st.session_state.user_color)
            item_img_base64 = get_base64_of_bin_file(img_name)
            
            if item_img_base64:
                img_src = f"data:image/png;base64,{item_img_base64}"
            else:
                img_src = f"https://placehold.co/150x150/EEEEEE/31343C?text=No+Image"
            
            st.markdown(f"""
            <div class="{card_class}">
                <img src="{img_src}" alt="{item['name']}">
                <div class="product-name">{item['name']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            btn_label = "Hủy chọn" if is_selected else "Chọn"
            if st.button(btn_label, key=f"btn_{item['id']}", use_container_width=True):
                if current_step == 'Phụ kiện':
                    if is_selected:
                        st.session_state.selected_items['Phụ kiện'] = [i for i in st.session_state.selected_items['Phụ kiện'] if i['id'] != item['id']]
                    else:
                        st.session_state.selected_items['Phụ kiện'].append(item)
                else:
                    if is_selected:
                        st.session_state.selected_items[current_step] = None 
                    else:
                        st.session_state.selected_items[current_step] = item 
                st.rerun()