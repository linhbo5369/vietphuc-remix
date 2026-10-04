import streamlit as st
import base64
import json

# Cấu hình trang cơ bản
st.set_page_config(page_title="Tam Tấu - Việt phục remix", layout="wide", initial_sidebar_state="collapsed")

# Hàm chuyển đổi file (ảnh/font) sang Base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 1. Đọc file ảnh họa tiết in chìm
try:
    img_base64 = get_base64_of_bin_file('trongdong.jpg')
except FileNotFoundError:
    img_base64 = "" 

# 2. Đọc file Font chữ
try:
    font_base64 = get_base64_of_bin_file('MTD-Elodie.otf') 
except FileNotFoundError:
    font_base64 = ""

# -----------------------------
# 1. CSS TÙY CHỈNH THEO THEME SƠN THEN & FONT ELODIE (CHỌN LỌC)
# -----------------------------
custom_css = f"""
<style>
    /* Khai báo Font chữ Elodie từ mã Base64 */
    @font-face {{
        font-family: 'Elodie';
        src: url(data:font/otf;charset=utf-8;base64,{font_base64}) format('opentype');
    }}

    /* Ép sát thanh điều hướng lên viền trên cùng */
    .block-container {{
        padding-top: 1.5rem !important;
    }}
    
    /* Ẩn header mặc định của Streamlit */
    header {{visibility: hidden;}}
    
    /* Đổi màu nền trang và TẠO HỌA TIẾT IN CHÌM */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(120, 20, 20, 0.85), rgba(120, 20, 20, 0.9)), 
                    url('data:image/png;base64,{img_base64}');
        background-size: 300px;
        background-repeat: repeat;
        color: #F1E3C8;
    }}

    /* Định dạng Navbar */
    .nav-brand {{
        font-family: 'Elodie', sans-serif;
        font-size: 42px; 
        font-weight: 900;
        color: #F1E3C8; 
        margin-bottom: -5px;
        letter-spacing: 2px;
    }}
    .nav-subtitle {{
        font-size: 14px;
        color: #6C854B; 
        font-style: italic;
    }}

    /* Tùy chỉnh nút bấm mặc định của Streamlit */
    [data-testid="stButton"] button {{
        background-color: transparent;
        color: #F1E3C8;
        border: 1px solid rgba(241, 227, 200, 0.3);
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        font-family: sans-serif; 
    }}
    [data-testid="stButton"] button:hover {{
        border-color: #F1E3C8;
        color: #781414; 
        background-color: #F1E3C8;
    }}

    /* Typography cho Hero Section */
    .hero-line-1 {{
        font-family: 'Elodie', sans-serif;
        font-size: 5rem;
        font-weight: 900;
        color: #6C854B; 
        line-height: 1.1;
        margin-bottom: 5px;
    }}
    .hero-line-2 {{
        font-family: 'Elodie', sans-serif;
        font-size: 4.5rem;
        font-weight: 900;
        color: #F1E3C8; 
        line-height: 1.1;
        margin-bottom: 25px;
    }}
    .hero-desc {{
        font-size: 1.2rem;
        color: #DBCDB5;
        margin-bottom: 30px;
        font-weight: 300;
        font-family: sans-serif; 
    }}

    /* Nút Call to Action chính */
    .cta-button {{
        display: inline-block;
        background-color: transparent; 
        color: #F1E3C8 !important; 
        border: 2px solid #F1E3C8;
        padding: 12px 28px;
        border-radius: 8px;
        text-decoration: none !important; 
        font-weight: bold;
        font-size: 18px;
        transition: all 0.3s ease;
        font-family: sans-serif;
    }}
    .cta-button:hover {{
        background-color: #F1E3C8; 
        color: #781414 !important; 
        transform: translateY(-2px);
    }}

    /* ---------------------------------------------------
       CSS MỚI: THANH TRƯỢT NGANG (SLIDE BAR) CHO SET ĐỒ
       --------------------------------------------------- */
    .slider-container {{
        display: flex;
        overflow-x: auto; /* Kích hoạt cuộn ngang */
        gap: 20px;
        padding-bottom: 20px;
        scroll-snap-type: x mandatory; /* Hỗ trợ snap (hút) khi cuộn trên điện thoại */
    }}

    /* Tùy chỉnh thanh cuộn ngang (Scrollbar) */
    .slider-container::-webkit-scrollbar {{
        height: 10px;
    }}
    .slider-container::-webkit-scrollbar-track {{
        background: rgba(241, 227, 200, 0.1); 
        border-radius: 10px;
    }}
    .slider-container::-webkit-scrollbar-thumb {{
        background: #6C854B; /* Màu xanh lục trầm */
        border-radius: 10px;
    }}
    .slider-container::-webkit-scrollbar-thumb:hover {{
        background: #F1E3C8; /* Đổi màu vàng đồng khi di chuột vào thanh cuộn */
    }}

    .slider-item {{
        flex: 0 0 280px; /* Chiều rộng cố định cho mỗi card, không bị bóp méo */
        scroll-snap-align: start;
    }}

    /* Định dạng Card hiển thị Set đồ */
    .outfit-card {{
        position: relative;
        width: 100%;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 8px 16px rgba(0,0,0,0.6);
        background-color: #4a0c0c;
        margin-bottom: 10px;
        border: 1px solid rgba(241, 227, 200, 0.1);
    }}
    
    .outfit-card img {{
        width: 100%;
        height: 380px;
        object-fit: cover;
        transition: all 0.3s ease;
        display: block;
    }}

    .outfit-card:hover img {{
        filter: brightness(40%) blur(3px);
    }}

    .card-actions {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        display: flex;
        flex-direction: column;
        gap: 12px;
        opacity: 0;
        transition: opacity 0.3s ease;
    }}

    .outfit-card:hover .card-actions {{
        opacity: 1;
    }}

    /* Style cho nút trong Card */
    .card-btn {{
        background-color: rgba(120, 20, 20, 0.7); 
        color: #F1E3C8 !important; 
        border: 1px solid #F1E3C8;
        padding: 10px 24px;
        border-radius: 25px;
        text-align: center;
        text-decoration: none !important;
        font-weight: bold;
        font-size: 15px;
        cursor: pointer;
        transition: all 0.2s ease;
        font-family: sans-serif;
    }}
    
    .card-btn:hover {{
        background-color: #F1E3C8;
        color: #781414 !important;
        transform: scale(1.05);
    }}

    /* Tên Set đồ (Dùng Font Elodie) */
    .outfit-name {{
        text-align: center;
        font-family: 'Elodie', sans-serif;
        font-size: 1.8rem;
        color: #F1E3C8;
        margin-top: 5px;
        letter-spacing: 1px;
    }}
    
    /* Tiêu đề H3 (Khám phá set đồ) */
    h3.elodie-title {{
        font-family: 'Elodie', sans-serif;
        color: #6C854B;
        margin-bottom: 20px;
        font-size: 2.5rem;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# -----------------------------
# 2. THANH ĐIỀU HƯỚNG (NAVBAR)
# -----------------------------
nav_col1, spacer, nav_col2, nav_col3 = st.columns([3, 5, 1.5, 1.5])

with nav_col1:
    st.markdown('<div class="nav-brand">Tam Tấu</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-subtitle">Việt phục remix</div>', unsafe_allow_html=True)

with nav_col2:
    st.write("") 
    st.button("Trang chủ", use_container_width=True)

with nav_col3:
    st.write("") 
    st.button("Chatbot phối đồ", use_container_width=True)

st.markdown("<hr style='border: 1px solid rgba(241, 227, 200, 0.15); margin-top: 5px; margin-bottom: 40px;'>", unsafe_allow_html=True)

# -----------------------------
# 3. MAIN CONTENT: HERO SECTION
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

# -----------------------------
# -----------------------------
# 4. SLIDE BAR (CAROUSEL): MŨI TÊN & TỰ ĐỘNG CHUYỂN
# -----------------------------
st.markdown('<h3 class="elodie-title">Khám phá các set đồ phối sẵn</h3>', unsafe_allow_html=True)

# Khởi tạo danh sách mặc định phòng khi bị lỗi
outfits = [
    {"id": 1, "image_url": "https://via.placeholder.com/400x600/4a0c0c/F1E3C8?text=Set+1", "name": "Set Áo Tấc Hiện Đại"},
    {"id": 2, "image_url": "https://via.placeholder.com/400x600/4a0c0c/F1E3C8?text=Set+2", "name": "Set Nhật Bình Remix"},
    {"id": 3, "image_url": "https://via.placeholder.com/400x600/4a0c0c/F1E3C8?text=Set+3", "name": "Set Ngũ Thân Đi Dạo"},
    {"id": 4, "image_url": "https://via.placeholder.com/400x600/4a0c0c/F1E3C8?text=Set+4", "name": "Set Cổ Phục Lễ Hội"},
    {"id": 5, "image_url": "https://via.placeholder.com/400x600/4a0c0c/F1E3C8?text=Set+5", "name": "Set Giao Lĩnh Tự Do"},
    {"id": 6, "image_url": "https://via.placeholder.com/400x600/4a0c0c/F1E3C8?text=Set+6", "name": "Set Tứ Thân Phá Cách"}
]

# Thử đọc JSON
try:
    with open('data/trang_phuc.json', 'r', encoding='utf-8') as file:
        loaded_data = json.load(file)
        if isinstance(loaded_data, list) and len(loaded_data) > 0 and isinstance(loaded_data[0], dict):
            outfits = loaded_data
except Exception as e:
    pass 

# CSS tùy chỉnh cho khung mũi tên và ẩn thanh cuộn
slider_css = """
<style>
.carousel-wrapper {
    position: relative;
    display: flex;
    align-items: center;
    padding: 0 50px; /* Chừa chỗ hai bên cho mũi tên */
}

/* Ẩn thanh cuộn mặc định */
.slider-container {
    display: flex;
    overflow-x: auto;
    gap: 20px;
    scroll-behavior: smooth; /* Hiệu ứng cuộn mượt */
    width: 100%;
    padding-bottom: 20px;
    -ms-overflow-style: none;  /* Ẩn trên IE/Edge */
    scrollbar-width: none;  /* Ẩn trên Firefox */
}
.slider-container::-webkit-scrollbar {
    display: none; /* Ẩn trên Chrome/Safari */
}

/* Nút mũi tên điều hướng */
.nav-arrow {
    position: absolute;
    top: 42%;
    transform: translateY(-50%);
    background-color: rgba(108, 133, 75, 0.9); /* Màu xanh lục trầm của theme */
    color: #F1E3C8;
    border: 2px solid #F1E3C8;
    border-radius: 50%;
    width: 45px;
    height: 45px;
    font-size: 20px;
    font-weight: bold;
    cursor: pointer;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}
.nav-arrow:hover {
    background-color: #F1E3C8;
    color: #781414; /* Đỏ Sơn Then */
}
.left-arrow { left: 0; }
.right-arrow { right: 0; }
</style>
"""

# Tạo khung HTML (Các thẻ HTML phải sát lề trái)
slider_html = slider_css + '<div class="carousel-wrapper">'
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

# Kịch bản JavaScript đã được nén thành 1 dòng (ép Streamlit chạy ngầm, không in ra text)
js_code = """<img src="dummy" style="display:none;" onerror="(function(){ const slider = document.getElementById('my-slider'); const btnLeft = document.getElementById('btn-left'); const btnRight = document.getElementById('btn-right'); const scrollAmount = 320; if(btnLeft && btnRight && slider) { btnLeft.onclick = () => slider.scrollLeft -= scrollAmount; btnRight.onclick = () => { if (slider.scrollLeft + slider.clientWidth >= slider.scrollWidth - 10) { slider.scrollLeft = 0; } else { slider.scrollLeft += scrollAmount; } }; } if(window.autoScrollInterval) { clearInterval(window.autoScrollInterval); } window.autoScrollInterval = setInterval(() => { const s = document.getElementById('my-slider'); if(s) { if (s.scrollLeft + s.clientWidth >= s.scrollWidth - 10) { s.scrollLeft = 0; } else { s.scrollLeft += scrollAmount; } } }, 30000); })();">"""

# Xuất code ra giao diện
st.markdown(slider_html + js_code, unsafe_allow_html=True)
