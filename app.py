import streamlit as st
import base64
import json

# Cấu hình trang cơ bản
st.set_page_config(page_title="Tam Tấu - Việt phục remix", layout="wide", initial_sidebar_state="collapsed")

# Khởi tạo trạng thái Theme chung cho toàn bộ web
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark' # Mặc định trang chủ là Tối

# Hàm chuyển đổi file (ảnh/font) sang Base64
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return ""

img_base64 = get_base64_of_bin_file('trongdong.jpg')
font_base64 = get_base64_of_bin_file('fontChu.otf') 

# -----------------------------
# 1. TẠO CSS ĐỘNG DỰA TRÊN THEME
# -----------------------------
if st.session_state.theme == 'dark':
    theme_css = f"""
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(120, 20, 20, 0.85), rgba(120, 20, 20, 0.95)); 
        color: #F1E3C8;
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
    
    .stMarkdown, p, span, div, h1, h2, h3, h4, h5, h6, label {{ color: #F1E3C8 !important; }}
    .nav-brand {{ color: #F1E3C8 !important; }}
    .nav-subtitle {{ color: #6C854B !important; }}
    .hero-line-1 {{ color: #6C854B !important; }}
    .hero-line-2 {{ color: #F1E3C8 !important; }}
    .hero-desc {{ color: #DBCDB5 !important; }}
    
    /* Giao diện nút bấm đồng bộ với chatbot_phoi_do */
    [data-testid="stButton"] button {{ background-color: transparent !important; border: 2px solid #F1E3C8 !important; }}
    [data-testid="stButton"] button p {{ color: #F1E3C8 !important; font-weight: bold !important; }}
    
    [data-testid="stButton"] button:hover, [data-testid="stButton"] button:focus, [data-testid="stButton"] button:active {{ 
        background-color: #F1E3C8 !important; 
        border-color: #F1E3C8 !important; 
    }}
    [data-testid="stButton"] button:hover p, [data-testid="stButton"] button:focus p, [data-testid="stButton"] button:active p {{ 
        color: #781414 !important; 
    }}
    
    .cta-button {{ color: #F1E3C8 !important; border: 2px solid #F1E3C8 !important; }}
    .cta-button:hover {{ background-color: #F1E3C8 !important; color: #781414 !important; }}
    
    .outfit-card {{ background-color: #4a0c0c !important; border: 1px solid rgba(241, 227, 200, 0.1) !important; }}
    .card-btn {{ background-color: rgba(120, 20, 20, 0.7) !important; color: #F1E3C8 !important; border: 1px solid #F1E3C8 !important; }}
    .card-btn:hover {{ background-color: #F1E3C8 !important; color: #781414 !important; }}
    .outfit-name {{ color: #F1E3C8 !important; }}
    h3.elodie-title {{ color: #6C854B !important; }}
    
    .slider-container::-webkit-scrollbar-track {{ background: rgba(241, 227, 200, 0.1); }}
    .slider-container::-webkit-scrollbar-thumb {{ background: #6C854B; }}
    .slider-container::-webkit-scrollbar-thumb:hover {{ background: #F1E3C8; }}
    .nav-arrow {{ background-color: rgba(108, 133, 75, 0.9); color: #F1E3C8; border: 2px solid #F1E3C8; }}
    .nav-arrow:hover {{ background-color: #F1E3C8; color: #781414; }}
    """
else:
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
        filter: invert(1) opacity(0.06);
        z-index: 0;
        pointer-events: none;
    }}

    .stMarkdown, p, span, div, h1, h2, h3, h4, h5, h6, label {{ color: #123C46 !important; }}
    .nav-brand {{ color: #D85A3F !important; }}
    .nav-subtitle {{ color: #559E9E !important; }}
    .hero-line-1 {{ color: #D85A3F !important; }}
    .hero-line-2 {{ color: #123C46 !important; }}
    .hero-desc {{ color: #123C46 !important; font-weight: 500; }}
    
    /* Giao diện nút bấm đồng bộ với chatbot_phoi_do */
    [data-testid="stButton"] button {{ background-color: transparent !important; border: 2px solid #D85A3F !important; }}
    [data-testid="stButton"] button p {{ color: #D85A3F !important; font-weight: bold !important; }}
    
    [data-testid="stButton"] button:hover, [data-testid="stButton"] button:focus, [data-testid="stButton"] button:active {{ 
        background-color: #D85A3F !important; 
    }}
    [data-testid="stButton"] button:hover p, [data-testid="stButton"] button:focus p, [data-testid="stButton"] button:active p {{ 
        color: #FFFFFF !important; 
    }}
    
    .cta-button {{ color: #D85A3F !important; border: 2px solid #D85A3F !important; }}
    .cta-button:hover {{ background-color: #D85A3F !important; color: #FFFFFF !important; }}
    
    .outfit-card {{ background-color: #FFFFFF !important; border: 2px solid #559E9E !important; }}
    .card-btn {{ background-color: #FFFFFF !important; color: #123C46 !important; border: 2px solid #559E9E !important; }}
    .card-btn:hover {{ background-color: #F3EEE0 !important; color: #123C46 !important; }}
    .outfit-name {{ color: #123C46 !important; }}
    h3.elodie-title {{ color: #D85A3F !important; }}
    
    .slider-container::-webkit-scrollbar-track {{ background: #DEE7E7; }}
    .slider-container::-webkit-scrollbar-thumb {{ background: #559E9E; }}
    .slider-container::-webkit-scrollbar-thumb:hover {{ background: #123C46; }}
    .nav-arrow {{ background-color: #FFFFFF; color: #123C46; border: 2px solid #559E9E; }}
    .nav-arrow:hover {{ background-color: #F3EEE0; }}
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
    
    .block-container {{ 
        padding-top: 2rem !important; 
        position: relative; 
        z-index: 1; 
    }}
    
    .nav-brand {{ font-family: 'Elodie', sans-serif; font-size: 34px; font-weight: normal; margin-bottom: -5px; letter-spacing: 2px; position: relative; z-index: 2; }}
    .nav-subtitle {{ font-size: 14px; font-style: italic; position: relative; z-index: 2; }}
    
    /* Thiết lập kích thước nút gọn gàng đồng bộ với chatbot_phoi_do */
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
    
    .hero-line-1 {{ font-family: 'Elodie', sans-serif; font-size: 4rem; font-weight: normal; line-height: 1.2; margin-bottom: 5px; }}
    .hero-line-2 {{ font-family: 'Elodie', sans-serif; font-size: 3.5rem; font-weight: normal; line-height: 1.2; margin-bottom: 25px; }}
    
    .hero-desc {{ font-size: 1.2rem; margin-bottom: 30px; font-family: sans-serif; }}
    .cta-button {{ display: inline-block; padding: 12px 28px; border-radius: 8px; text-decoration: none !important; font-weight: bold; font-size: 18px; transition: all 0.3s ease; font-family: sans-serif; }}
    .slider-container {{ display: flex; overflow-x: auto; gap: 20px; padding-bottom: 20px; scroll-snap-type: x mandatory; -ms-overflow-style: none; scrollbar-width: none; }}
    .slider-container::-webkit-scrollbar {{ display: none; }}
    .slider-item {{ flex: 0 0 280px; scroll-snap-align: start; }}
    .outfit-card {{ position: relative; width: 100%; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 16px rgba(0,0,0,0.6); margin-bottom: 10px; }}
    .outfit-card img {{ width: 100%; height: 380px; object-fit: cover; transition: all 0.3s ease; display: block; }}
    .outfit-card:hover img {{ filter: brightness(40%) blur(3px); }}
    .card-actions {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); display: flex; flex-direction: column; gap: 12px; opacity: 0; transition: opacity 0.3s ease; }}
    .outfit-card:hover .card-actions {{ opacity: 1; }}
    .card-btn {{ padding: 10px 24px; border-radius: 25px; text-align: center; text-decoration: none !important; font-weight: bold; font-size: 15px; cursor: pointer; transition: all 0.2s ease; font-family: sans-serif; }}
    .card-btn:hover {{ transform: scale(1.05); }}
    
    .outfit-name {{ text-align: center; font-family: 'Elodie', sans-serif; font-size: 1.5rem; font-weight: normal; margin-top: 5px; letter-spacing: 1px; }}
    h3.elodie-title {{ font-family: 'Elodie', sans-serif; margin-bottom: 20px; font-size: 2.2rem; font-weight: normal; }}
    
    .carousel-wrapper {{ position: relative; display: flex; align-items: center; padding: 0 50px; }}
    .nav-arrow {{ position: absolute; top: 42%; transform: translateY(-50%); border-radius: 50%; width: 45px; height: 45px; font-size: 20px; font-weight: bold; cursor: pointer; z-index: 10; display: flex; align-items: center; justify-content: center; transition: all 0.3s ease; }}
    .left-arrow {{ left: 0; }}
    .right-arrow {{ right: 0; }}
    {theme_css}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Chèn hoa văn chìm ngay đầu block-container để nó cuộn theo nội dung
st.markdown('<div class="scrollable-pattern"></div>', unsafe_allow_html=True)

# -----------------------------
# 2. THANH ĐIỀU HƯỚNG CÓ NÚT THEME
# -----------------------------
# Đã điều chỉnh lại tỷ lệ cột để các nút có đủ không gian hiển thị toàn bộ chữ
nav_col1, spacer, nav_col2, nav_col3, nav_col4 = st.columns([2.5, 3.5, 1.2, 1.8, 1])

with nav_col1:
    st.markdown('<div class="nav-brand">Tam Tấu</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-subtitle">Việt phục remix</div>', unsafe_allow_html=True)

with spacer:
    st.write("") 

with nav_col2:
    st.write("")
    st.button("Trang chủ", use_container_width=True)

with nav_col3:
    st.write("") 
    if st.button("Chatbot phối đồ", use_container_width=True):
        st.switch_page("pages/chatbot_phoi_do.py") 

with nav_col4:
    st.write("") 
    theme_label = "Sáng" if st.session_state.theme == 'dark' else "Tối"
    if st.button(theme_label, use_container_width=True):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()

st.markdown("<hr style='border: 1px solid rgba(241, 227, 200, 0.15); margin-top: 5px; margin-bottom: 40px; position: relative; z-index: 2;'>", unsafe_allow_html=True)

# -----------------------------
# 3. MAIN CONTENT & SLIDE BAR 
# -----------------------------
hero_col1, hero_col2 = st.columns([1.1, 1])

with hero_col1:
    st.markdown('<div class="hero-line-1">Việt phục remix</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-line-2">Sáng tạo những set đồ riêng</div>', unsafe_allow_html=True)
    st.markdown('<p class="hero-desc">Khám phá sự giao thoa giữa truyền thống và hiện đại. Tự do sáng tạo, mix & match các trang phục truyền thống Việt Nam mang đậm phong cách cá nhân của bạn.</p>', unsafe_allow_html=True)
    st.markdown('<a href="#chatbot-phoi-do" class="cta-button">Bắt đầu phối đồ</a>', unsafe_allow_html=True)

with hero_col2:
    st.info("[Khu vực chèn ảnh minh họa chính: Nên dùng ảnh PNG không nền (transparent) có tone Đỏ, Vàng đồng, hoặc Xanh lục trầm để hài hòa với giao diện]")

st.write("<br><br><br>", unsafe_allow_html=True)

st.markdown('<h3 class="elodie-title">Khám phá các set đồ phối sẵn</h3>', unsafe_allow_html=True)

outfits = [
    {"id": 1, "image_url": "https://via.placeholder.com/400x600/4a0c0c/F1E3C8?text=Set+1", "name": "Set Áo Tấc Hiện Đại"},
    {"id": 2, "image_url": "https://via.placeholder.com/400x600/4a0c0c/F1E3C8?text=Set+2", "name": "Set Nhật Bình Remix"},
    {"id": 3, "image_url": "https://via.placeholder.com/400x600/4a0c0c/F1E3C8?text=Set+3", "name": "Set Ngũ Thân Đi Dạo"},
    {"id": 4, "image_url": "https://via.placeholder.com/400x600/4a0c0c/F1E3C8?text=Set+4", "name": "Set Cổ Phục Lễ Hội"},
    {"id": 5, "image_url": "https://via.placeholder.com/400x600/4a0c0c/F1E3C8?text=Set+5", "name": "Set Giao Lĩnh Tự Do"},
    {"id": 6, "image_url": "https://via.placeholder.com/400x600/4a0c0c/F1E3C8?text=Set+6", "name": "Set Tứ Thân Phá Cách"}
]

try:
    with open('data/trang_phuc.json', 'r', encoding='utf-8') as file:
        loaded_data = json.load(file)
        if isinstance(loaded_data, list) and len(loaded_data) > 0 and isinstance(loaded_data[0], dict):
            outfits = loaded_data
except Exception as e:
    pass 

slider_html = '<div class="carousel-wrapper">'
slider_html += '<button class="nav-arrow left-arrow" id="btn-left">❮</button>'
slider_html += '<div class="slider-container" id="my-slider">'

for i, outfit in enumerate(outfits):
    if isinstance(outfit, dict):
        img_url = outfit.get('image_url', 'https://via.placeholder.com/400x600/4a0c0c/F1E3C8?text=Loi+Anh')
        name = outfit.get('name', 'Chưa có tên')
        item_id = outfit.get('id', i)
        
        slider_html += f"""<div class="slider-item">
<div class="outfit-card">
<img src="{img_url}" alt="{name}">
<div class="card-actions">
<a href="#chi-tiet-{item_id}" target="_self" class="card-btn">Chi tiết</a>
<a href="#chatbot-phoi-do" target="_self" class="card-btn">Phối đồ</a>
</div>
</div>
<div class="outfit-name">{name}</div>
</div>"""

slider_html += '</div>'
slider_html += '<button class="nav-arrow right-arrow" id="btn-right">❯</button>'
slider_html += '</div>'

js_code = """<img src="dummy" style="display:none;" onerror="(function(){ const slider = document.getElementById('my-slider'); const btnLeft = document.getElementById('btn-left'); const btnRight = document.getElementById('btn-right'); const scrollAmount = 320; if(btnLeft && btnRight && slider) { btnLeft.onclick = () => slider.scrollLeft -= scrollAmount; btnRight.onclick = () => { if (slider.scrollLeft + slider.clientWidth >= slider.scrollWidth - 10) { slider.scrollLeft = 0; } else { slider.scrollLeft += scrollAmount; } }; } if(window.autoScrollInterval) { clearInterval(window.autoScrollInterval); } window.autoScrollInterval = setInterval(() => { const s = document.getElementById('my-slider'); if(s) { if (s.scrollLeft + s.clientWidth >= s.scrollWidth - 10) { s.scrollLeft = 0; } else { s.scrollLeft += scrollAmount; } } }, 30000); })();">"""

st.markdown(slider_html + js_code, unsafe_allow_html=True)