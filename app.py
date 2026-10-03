import streamlit as st
from streamlit_option_menu import option_menu

# 1. Left Rail (Nằm gọn ở phía trên cùng của thanh sidebar)
with st.sidebar:
    selected_menu = option_menu(
        menu_title=None, 
        options=["Home", "Phối đồ", "Lookbook"], 
        icons=["house", "search", "book"], 
        orientation="horizontal" # Đặt nằm ngang cho gọn, hoặc dọc tùy ý
    )
    st.divider() # Đường kẻ ngang phân cách

    # 2. Sidebar Filter (Bộ lọc nằm bên dưới menu)
    st.markdown("### Bộ lọc tìm kiếm")
    boid_canh = st.selectbox("Chọn bối cảnh:", ["Tết", "Đi học", "Lễ hội"]) #
    thoi_tiet = st.radio("Thời tiết:", ["Nóng", "Lạnh"]) #

# Chia màn hình: Cột trái (Main) rộng gấp đôi cột phải (Right Sidebar)
main_col, right_col = st.columns([2, 1])

#Dựng khu vực Main content
with main_col:
    tab_ao, tab_quan, tab_phukien = st.tabs(["Chọn Áo", "Chọn Quần/Váy", "Phụ kiện"]) 

# Hiển thị lướt và lưu trạng thái
# khởi tạo bộ nhớ tạm
if 'selected_ao' not in st.session_state:
    st.session_state['selected_ao'] = None
if 'selected_quan' not in st.session_state:
    st.session_state['selected_quan'] = None
# hiển thị danh sách trong tab áo
with tab_ao:
    col1, col2, col3 = st.columns(3) # Tạo 3 cột để show ảnh như wireframe

    # Giả sử bạn dùng vòng lặp đọc từ database.json
    with col1:
        st.image("assets/shirts/tu_than_01.png")
        if st.button("Chọn áo này", key="btn_ao_01"):
            st.session_state['selected_ao'] = "ao_01" # Lưu ID áo vào bộ nhớ

# Dựng khu vực Right Sidebar
from PIL import Image

with right_col:
    st.markdown("### Kết quả phối đồ")
    
    if st.session_state['selected_ao']:
        # Mở ảnh bằng thư viện PIL
        img_avatar = Image.open("assets/avatar_base.png").convert("RGBA")
        img_ao = Image.open("assets/shirts/tu_than_01.png").convert("RGBA")
        
        # Ghép ảnh áo đè lên avatar
        img_avatar.alpha_composite(img_ao)
        
        # Hiển thị ra Streamlit
        st.image(img_avatar, use_container_width=True) #

# logic kiểm tra và cảnh báo văn hóa
# Giả lập logic kiểm tra
    ao_dang_chon = st.session_state['selected_ao']
    quan_dang_chon = st.session_state['selected_quan']
    
    if ao_dang_chon == "ao_tu_than" and quan_dang_chon == "quan_jeans":
        # Hiển thị cảnh báo cách kết hợp làm sai lệch văn hóa
        st.error("Cảnh báo: Áo tứ thân truyền thống không nên phối cùng quần Jeans hiện đại. Bạn có thể cân nhắc váy đụp đen!")

# Đọc thông tin ngắn
st.info("Áo Tứ Thân là trang phục truyền thống của phụ nữ miền Bắc... (Nguồn gốc/ý nghĩa)") #[cite: 1]

