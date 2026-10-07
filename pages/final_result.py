import streamlit as st
from PIL import Image, ImageDraw
import io
import os
import base64

# Cấu hình trang
st.set_page_config(page_title="Kết Quả Phối Đồ", layout="wide", initial_sidebar_state="collapsed")

# ==========================================
# 1. TRẠNG THÁI CHUNG & TIỆN ÍCH
# ==========================================
if 'theme' not in st.session_state:
    st.session_state.theme = 'light' 

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

# ==========================================
# 2. CSS GIAO DIỆN VÀ THEME ĐỒNG BỘ
# ==========================================
if st.session_state.theme == 'light':
    theme_css = f"""
    [data-testid="stAppViewContainer"] {{
        background-color: #F3EEE0 !important;
        background-image: none !important;
        overflow-x: hidden !important;
    }}
    .scrollable-pattern {{
        position: absolute; top: -3rem; left: 50%; transform: translateX(-50%);
        width: 100vw; height: 142px; 
        background-image: url('data:image/jpeg;base64,{img_base64}');
        background-size: 300px; background-repeat: repeat;
        filter: invert(1); opacity: 0.05; z-index: 0; pointer-events: none;
    }}
    .stMarkdown, p, span, div, h1, h2, h3, h4, h5, h6, label {{ color: #123C46 !important; font-weight: normal; }}
    .elodie-title {{ color: #D85A3F !important; }}
    
    [data-testid="stButton"] button, [data-testid="stDownloadButton"] button {{ background-color: transparent !important; border: 2px solid #D85A3F !important; }}
    [data-testid="stButton"] button p, [data-testid="stDownloadButton"] button p {{ color: #D85A3F !important; font-weight: bold !important; }}
    [data-testid="stButton"] button:hover, [data-testid="stDownloadButton"] button:hover {{ background-color: #D85A3F !important; }}
    [data-testid="stButton"] button:hover p, [data-testid="stDownloadButton"] button:hover p {{ color: #FFFFFF !important; }}
    
    div[data-testid="stButton"] > button[kind="primary"] {{ background-color: #D85A3F !important; border-color: #D85A3F !important; }}
    div[data-testid="stButton"] > button[kind="primary"] p {{ color: #FFFFFF !important; }}
    
    .content-box {{ background-color: #FFFFFF; color: #123C46 !important; border: 2px solid #559E9E; border-radius: 10px; padding: 25px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
    .highlight-text {{ color: #D85A3F; font-weight: bold; font-size: 1.1em; }}
    """
else:
    theme_css = f"""
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(120, 20, 20, 0.85), rgba(120, 20, 20, 0.9)) !important;
        overflow-x: hidden !important;
    }}
    .scrollable-pattern {{
        position: absolute; top: -3rem; left: 50%; transform: translateX(-50%);
        width: 100vw; height: 142px; 
        background-image: url('data:image/jpeg;base64,{img_base64}');
        background-size: 300px; background-repeat: repeat;
        opacity: 0.15; z-index: 0; pointer-events: none;
    }}
    .stMarkdown, p, span, div, h1, h2, h3, h4, h5, h6, label {{ color: #F1E3C8 !important; font-weight: normal; }}
    .elodie-title {{ color: #E53935 !important; }} 
    
    [data-testid="stButton"] button, [data-testid="stDownloadButton"] button {{ background-color: transparent !important; border: 2px solid #F1E3C8 !important; }}
    [data-testid="stButton"] button p, [data-testid="stDownloadButton"] button p {{ color: #F1E3C8 !important; font-weight: bold !important; }}
    [data-testid="stButton"] button:hover, [data-testid="stDownloadButton"] button:hover {{ background-color: #F1E3C8 !important; border-color: #F1E3C8 !important; }}
    [data-testid="stButton"] button:hover p, [data-testid="stDownloadButton"] button:hover p {{ color: #781414 !important; }}
    
    div[data-testid="stButton"] > button[kind="primary"] {{ background-color: #E53935 !important; border-color: #E53935 !important; }}
    div[data-testid="stButton"] > button[kind="primary"] p {{ color: #FFFFFF !important; }}
    
    .content-box {{ background-color: rgba(74, 12, 12, 0.8); color: #F1E3C8 !important; border: 2px solid rgba(241, 227, 200, 0.3); border-radius: 10px; padding: 25px; margin-bottom: 20px; }}
    .highlight-text {{ color: #E53935; font-weight: bold; font-size: 1.1em; }}
    """

custom_css = f"""
<style>
    html, body {{ overflow-x: hidden !important; }}
    
    @font-face {{ font-family: 'Elodie'; src: url(data:font/otf;charset=utf-8;base64,{font_base64}) format('opentype'); }}
    
    header[data-testid="stHeader"] {{ display: none !important; }}
    .block-container {{ position: relative; z-index: 1; padding-top: 2rem !important; }}
    
    /* ÉP KÍCH THƯỚC CHỮ BẰNG CLASS RIÊNG (Đã thu nhỏ lại cho vừa vặn) */
    h1.main-heading {{
        font-family: 'Elodie', sans-serif !important;
        font-size: 3.2rem !important; /* Đã giảm từ 4.5rem */
        text-align: center !important;
        letter-spacing: 2px !important;
        font-weight: normal !important;
        margin-bottom: 30px !important;
        line-height: 1.2 !important;
    }}
    
    h3.sub-heading {{
        font-family: 'Elodie', sans-serif !important;
        font-size: 2.2rem !important; /* Đã giảm từ 2.8rem */
        text-align: center !important;
        font-weight: normal !important;
        margin-top: 0 !important;
        margin-bottom: 20px !important;
    }}
    
    [data-testid="stButton"] button, [data-testid="stDownloadButton"] button {{ border-radius: 8px; transition: all 0.3s ease; padding: 6px 16px !important; position: relative; z-index: 2; display: flex; align-items: center; justify-content: center; }}
    [data-testid="stButton"] button p, [data-testid="stDownloadButton"] button p {{ font-size: 15px !important; margin: 0 !important; text-align: center; }}
    [data-testid="stButton"] button:hover, [data-testid="stDownloadButton"] button:hover {{ transform: translateY(-2px); }}
    
    {theme_css}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
st.markdown('<div class="scrollable-pattern"></div>', unsafe_allow_html=True)

# ==========================================
# 3. THANH ĐIỀU HƯỚNG TRÊN CÙNG
# ==========================================
top_left, top_mid, top_right = st.columns([1.5, 7.5, 1])
with top_left:
    if st.button("Trang chủ", use_container_width=True):
        st.switch_page("app.py")
with top_right:
    theme_label = "Sáng" if st.session_state.theme == 'dark' else "Tối"
    if st.button(theme_label, use_container_width=True):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()

st.markdown("<hr style='border: 1px solid rgba(241, 227, 200, 0.15); margin: 10px 0 20px 0; position: relative; z-index: 2;'>", unsafe_allow_html=True)

# ==========================================
# 4. HÀM TẠO ẢNH MOCKUP
# ==========================================
def create_mockup_image():
    img = Image.new('RGB', (800, 1200), color=(242, 242, 242))
    draw = ImageDraw.Draw(img)
    box_color = (136, 136, 136)
    
    draw.rectangle([40, 120, 480, 880], fill=box_color)
    draw.rectangle([510, 120, 760, 480], fill=box_color)
    draw.rectangle([510, 520, 760, 880], fill=box_color)
    draw.rectangle([40, 920, 260, 1160], fill=box_color)
    draw.rectangle([290, 920, 510, 1160], fill=box_color)
    draw.rectangle([540, 920, 760, 1160], fill=box_color)
    
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

# ==========================================
# 5. GIAO DIỆN CHÍNH
# ==========================================
st.markdown("<h1 class='main-heading elodie-title'>Preview trang phục</h1>", unsafe_allow_html=True)

mockup_bytes = create_mockup_image()

col1, col2 = st.columns([6, 4], gap="large")

with col1:
    st.image(mockup_bytes, use_container_width=True)

with col2:
    st.markdown(f"""
    <div class="content-box">
        <h3 class="sub-heading elodie-title highlight-text">MÔ TẢ BỘ ĐỒ</h3>
        <p class="highlight-text">Các item chính phối với item phụ tạo ra vibe, cá tính gì?</p>
        <p>
            Vibe: Giao thoa giữa truyền thống và phong cách hiện đại, năng động. <br><br>
            <i>(Bạn có thể lấy dữ liệu từ <b>st.session_state.selected_items</b> từ trang trước để tự động điền vào đây.)</i>
        </p>
        <br><br><br>
    </div>
    """, unsafe_allow_html=True)
    
    st.download_button(
        label="Tải ảnh",
        data=mockup_bytes,
        file_name="ket_qua_phoi_do.jpg",
        mime="image/jpeg",
        use_container_width=True
    )

    if st.button("Đánh giá", use_container_width=True):
        st.success("Cảm ơn bạn đã đánh giá!")

    if st.button("Quay về chỉnh sửa", type="primary", use_container_width=True):
        st.switch_page("pages/chatbot_phoi_do.py")