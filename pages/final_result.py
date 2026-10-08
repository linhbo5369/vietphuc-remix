import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os
import base64

st.set_page_config(page_title="Kết Quả Phối Đồ", layout="wide", initial_sidebar_state="collapsed")

if 'theme' not in st.session_state:
    st.session_state.theme = 'light' 

if 'selected_items' not in st.session_state:
    st.session_state.selected_items = {'Trang phục': None, 'Áo': None, 'Váy/Quần': None, 'Nón': None, 'Túi xách': None, 'Phụ kiện': [], 'Giày': None}

def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file): target_path = bin_file
    elif os.path.exists(os.path.join(os.path.dirname(__file__), '..', bin_file)): target_path = os.path.join(os.path.dirname(__file__), '..', bin_file)
    else: return ""
    with open(target_path, 'rb') as f: data = f.read()
    return base64.b64encode(data).decode()

def get_dynamic_image_path(item, user_gender, user_color_code):
    prefix = item.get('file_prefix', '')
    if prefix == "chan_vay_xep_ly_dai": prefix = "chan_vay_dap_ly"
    gioi_tinh_list = item.get('gioi_tinh', [])
    
    if "Nam" in gioi_tinh_list and "Nữ" in gioi_tinh_list: gender_tag = "unisex"
    elif "Nữ" in gioi_tinh_list: gender_tag = "nu"
    elif "Nam" in gioi_tinh_list: gender_tag = "nam"
    else: gender_tag = ""

    active_color = st.session_state.get("active_color_filter") or user_color_code

    if gender_tag and active_color:
        exact_path = f"data/{prefix}_{gender_tag}_{active_color}.png"
        if os.path.exists(exact_path) or os.path.exists(os.path.join("..", exact_path)): return exact_path
            
    target_dir = 'data' if os.path.exists('data') else '../data'
    if os.path.exists(target_dir):
        if active_color:
            for filename in os.listdir(target_dir):
                if filename.startswith(prefix) and filename.endswith('.png') and f"_{active_color}" in filename: return f"data/{filename}"
        if gender_tag:
            for filename in os.listdir(target_dir):
                if filename.startswith(prefix) and filename.endswith('.png') and f"_{gender_tag}_" in filename: return f"data/{filename}"
        for filename in os.listdir(target_dir):
            if filename.startswith(prefix) and filename.endswith('.png'): return f"data/{filename}"
                
    return f"data/{prefix}.png"

img_base64 = get_base64_of_bin_file('trongdong.jpg')
font_base64 = get_base64_of_bin_file('fontChu.otf') 

if st.session_state.theme == 'light':
    theme_css = f"""
    [data-testid="stAppViewContainer"] {{ background-color: #F3EEE0 !important; background-image: none !important; overflow-x: hidden !important; }}
    .scrollable-pattern {{ position: absolute; top: -3rem; left: 50%; transform: translateX(-50%); width: 100vw; height: 142px; background-image: url('data:image/jpeg;base64,{img_base64}'); background-size: 300px; background-repeat: repeat; filter: invert(1); opacity: 0.05; z-index: 0; pointer-events: none; }}
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
    
    div[data-testid="stTextArea"] > div {{ background-color: #FFFFFF !important; border: 2px solid #559E9E !important; border-radius: 15px !important; }}
    div[data-testid="stTextArea"] textarea {{ background-color: transparent !important; color: #123C46 !important; caret-color: #D85A3F !important; }}
    div[data-testid="stTextArea"] textarea::placeholder {{ color: #9E9E9E !important; opacity: 1 !important; }}
    """
else:
    theme_css = f"""
    [data-testid="stAppViewContainer"] {{ background: linear-gradient(rgba(120, 20, 20, 0.85), rgba(120, 20, 20, 0.9)) !important; overflow-x: hidden !important; }}
    .scrollable-pattern {{ position: absolute; top: -3rem; left: 50%; transform: translateX(-50%); width: 100vw; height: 142px; background-image: url('data:image/jpeg;base64,{img_base64}'); background-size: 300px; background-repeat: repeat; opacity: 0.15; z-index: 0; pointer-events: none; }}
    .stMarkdown, p, span, div, h1, h2, h3, h4, h5, h6, label {{ color: #F1E3C8 !important; font-weight: normal; }}
    
    .elodie-title {{ color: #6C854B !important; }} 
    [data-testid="stButton"] button, [data-testid="stDownloadButton"] button {{ background-color: transparent !important; border: 2px solid #F1E3C8 !important; }}
    [data-testid="stButton"] button p, [data-testid="stDownloadButton"] button p {{ color: #F1E3C8 !important; font-weight: bold !important; }}
    [data-testid="stButton"] button:hover, [data-testid="stDownloadButton"] button:hover {{ background-color: #F1E3C8 !important; border-color: #F1E3C8 !important; }}
    [data-testid="stButton"] button:hover p, [data-testid="stDownloadButton"] button:hover p {{ color: #781414 !important; }}
    div[data-testid="stButton"] > button[kind="primary"] {{ background-color: #6C854B !important; border-color: #6C854B !important; }}
    div[data-testid="stButton"] > button[kind="primary"] p {{ color: #FFFFFF !important; }}
    .content-box {{ background-color: rgba(74, 12, 12, 0.8); color: #F1E3C8 !important; border: 2px solid rgba(241, 227, 200, 0.3); border-radius: 10px; padding: 25px; margin-bottom: 20px; }}
    .highlight-text {{ color: #6C854B; font-weight: bold; font-size: 1.1em; }}
    
    div[data-testid="stTextArea"] > div {{ background-color: rgba(0,0,0,0.5) !important; border: 1.5px solid #6C854B !important; border-radius: 15px !important; }}
    div[data-testid="stTextArea"] textarea {{ background-color: transparent !important; color: #F1E3C8 !important; caret-color: #6C854B !important; }}
    div[data-testid="stTextArea"] textarea::placeholder {{ color: #A0B090 !important; opacity: 0.8 !important; }}
    """

custom_css = f"""
<style>
    html, body {{ overflow-x: hidden !important; }}
    @font-face {{ font-family: 'Elodie'; src: url(data:font/otf;charset=utf-8;base64,{font_base64}) format('opentype'); }}
    header[data-testid="stHeader"] {{ display: none !important; }}
    .block-container {{ position: relative; z-index: 1; padding-top: 2rem !important; }}
    h1.main-heading {{ font-family: 'Elodie', sans-serif !important; font-size: 3.2rem !important; text-align: center !important; letter-spacing: 2px !important; font-weight: normal !important; margin-bottom: 30px !important; line-height: 1.2 !important; }}
    h3.sub-heading {{ font-family: 'Elodie', sans-serif !important; font-size: 2.2rem !important; text-align: center !important; font-weight: normal !important; margin-top: 0 !important; margin-bottom: 20px !important; }}
    [data-testid="stButton"] button, [data-testid="stDownloadButton"] button {{ border-radius: 8px; transition: all 0.3s ease; padding: 6px 16px !important; position: relative; z-index: 2; display: flex; align-items: center; justify-content: center; }}
    [data-testid="stButton"] button p, [data-testid="stDownloadButton"] button p {{ font-size: 15px !important; margin: 0 !important; text-align: center; }}
    [data-testid="stButton"] button:hover, [data-testid="stDownloadButton"] button:hover {{ transform: translateY(-2px); }}
    
    div[data-testid="stFeedback"] {{ 
        display: flex !important; 
        justify-content: center !important; 
        align-items: center !important; 
        width: 100% !important; 
        margin: 15px 0 35px 0 !important; 
    }}
    div[data-testid="stFeedback"] > div, div[data-testid="stFeedback"] fieldset {{ 
        display: flex !important; 
        justify-content: center !important; 
        width: 100% !important; 
        transform: scale(1.6); 
    }}
    {theme_css}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
st.markdown('<div class="scrollable-pattern"></div>', unsafe_allow_html=True)

top_left, top_mid, top_right = st.columns([1.5, 7.5, 1])
with top_left:
    if st.button("Trang chủ", use_container_width=True): st.switch_page("app.py")
with top_right:
    theme_label = "Sáng" if st.session_state.theme == 'dark' else "Tối"
    if st.button(theme_label, use_container_width=True):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()

st.markdown("<hr style='border: 1px solid rgba(241, 227, 200, 0.15); margin: 10px 0 20px 0; position: relative; z-index: 2;'>", unsafe_allow_html=True)

def tao_anh_grid_ootd():
    canvas_w, canvas_h = 800, 1200
    img = Image.new('RGB', (canvas_w, canvas_h), color=(242, 242, 242))
    
    boxes = {
        'Trang phục': [40, 120, 480, 880],
        'Áo': [510, 120, 760, 480],
        'Váy/Quần': [510, 520, 760, 880],
        'Nón': [40, 920, 260, 1160],
        'Túi xách': [290, 920, 510, 1160],
        'Giày': [540, 920, 760, 1160],
    }
    box_color = (200, 200, 200)
    
    draw = ImageDraw.Draw(img)
    font_path = "data/fontChu.otf" if os.path.exists("data/fontChu.otf") else "../data/fontChu.otf"
    try:
        font = ImageFont.truetype(font_path, 40)
        draw.text((canvas_w/2, 60), "GỢI Ý PHỐI ĐỒ / OOTD", font=font, fill=(0,0,0), anchor="mm")
    except: pass

    u_gender = st.session_state.get('user_gender', None)
    u_color = st.session_state.get('user_color', None)

    def paste_image_into_box(item_dict, box_coords):
        if not item_dict:
            draw.rectangle(box_coords, fill=box_color, outline=(150,150,150), width=2)
            return
            
        img_path = get_dynamic_image_path(item_dict, u_gender, u_color)
        real_path = img_path if os.path.exists(img_path) else os.path.join('..', img_path)
        
        try:
            item_img = Image.open(real_path).convert("RGBA")
            box_w = box_coords[2] - box_coords[0]
            box_h = box_coords[3] - box_coords[1]
            item_img.thumbnail((box_w - 20, box_h - 20), Image.Resampling.LANCZOS)
            paste_x = box_coords[0] + (box_w - item_img.width) // 2
            paste_y = box_coords[1] + (box_h - item_img.height) // 2
            draw.rectangle(box_coords, fill=(255,255,255), outline=(200,200,200), width=2)
            img.paste(item_img, (paste_x, paste_y), mask=item_img)
        except Exception as e:
            draw.rectangle(box_coords, fill=box_color)

    sel = st.session_state.selected_items
    paste_image_into_box(sel.get('Trang phục'), boxes['Trang phục'])
    paste_image_into_box(sel.get('Áo'), boxes['Áo'])
    paste_image_into_box(sel.get('Váy/Quần'), boxes['Váy/Quần'])
    paste_image_into_box(sel.get('Nón'), boxes['Nón'])
    paste_image_into_box(sel.get('Túi xách'), boxes['Túi xách'])
    paste_image_into_box(sel.get('Giày'), boxes['Giày'])
    
    if sel.get('Phụ kiện'):
        base_y = 130
        for acc in sel['Phụ kiện']:
            acc_box = [50, base_y, 150, base_y + 100]
            paste_image_into_box(acc, acc_box)
            base_y += 110

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()

st.markdown("<h1 class='main-heading elodie-title'>Bảng tổng hợp OOTD của bồ nè!</h1>", unsafe_allow_html=True)

mockup_bytes = tao_anh_grid_ootd()

# CẬP NHẬT TÊN FILE TẢI VỀ
ten_file_tai_ve = "VietPhuc_remix.jpg"
if st.session_state.selected_items['Trang phục']:
    ten_viet_phuc = st.session_state.selected_items['Trang phục']['name']
    import re
    # Giữ lại ký tự tiếng Việt, loại bỏ ký tự đặc biệt hệ thống không cho phép, thay khoảng trắng bằng gạch dưới
    clean_name = re.sub(r'[\\/*?:"<>|]', '', ten_viet_phuc.strip()).replace(' ', '_')
    ten_file_tai_ve = f"{clean_name}_remix.jpg"

col1, col2 = st.columns([5, 5], gap="large")

with col1:
    # ĐÃ XÓA CHỮ "Grid Mix & Match"
    st.image(mockup_bytes, use_container_width=True)

with col2:
    ai_desc = ""
    if 'ai_response' in st.session_state and isinstance(st.session_state.ai_response, dict):
        resp = st.session_state.ai_response
        if "loi_khuyen_stylist" in resp: ai_desc += f"<p><b>💡 Lời khuyên từ AI:</b><br> {resp['loi_khuyen_stylist']}</p>"
        if "phoi_hien_dai" in resp: ai_desc += f"<p><b>👗 Vibe trang phục:</b><br> {resp['phoi_hien_dai']}</p>"
        
    if not ai_desc: ai_desc = "<p><i>Bồ chưa chat với Stylist AI để lấy nhận xét chi tiết cho bộ đồ này. Hãy thử nhắn tin trên khung chat nhé!</i></p>"

    st.markdown(f"""
    <div class="content-box">
        <h3 class="sub-heading elodie-title highlight-text">MÔ TẢ BỘ ĐỒ</h3>
        {ai_desc}
    </div>
    """, unsafe_allow_html=True)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        st.download_button(
            label="⬇ Tải ảnh OOTD",
            data=mockup_bytes,
            file_name=ten_file_tai_ve,
            mime="image/jpeg",
            use_container_width=True
        )
    with col_btn2:
        if st.button("✏ Quay về chỉnh sửa", type="primary", use_container_width=True):
            st.switch_page("pages/chatbot_phoi_do.py")
            
    st.markdown("<br><hr style='border-color: rgba(120,120,120,0.2);'><br>", unsafe_allow_html=True)
    
    st.markdown("<h3 class='elodie-title' style='text-align: center; font-size: 24px !important;'>Đánh giá trải nghiệm của bồ</h3>", unsafe_allow_html=True)
    
    col_star1, col_star2, col_star3 = st.columns([1, 2, 1])
    with col_star2:
        rating = st.feedback("stars")
        
    comment = st.text_area("Để lại góp ý cho tụi mình nha:", placeholder="Giao diện xịn xò, nhưng ước gì có thêm áo Nhật Bình màu xanh lá...", height=100)
    
    if st.button("Gửi đánh giá", use_container_width=True):
        if rating is not None:
            st.success("💖 Cảm ơn bồ đã đánh giá! Tụi mình sẽ ghi nhận để làm web xịn hơn nữa.")
        else:
            st.warning("Bồ quên bấm chọn số sao (⭐) kìa!")