import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Nạp biến môi trường và khởi tạo kết nối API
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") 
client = genai.Client(api_key=API_KEY)

# ==========================================
# PHẦN 1: CHATBOT TƯ VẤN (Đọc từ file JSON)
# ==========================================
def khoi_tao_chatbot():
    try:
        with open("data/phu_kien.json", "r", encoding="utf-8") as f:
            phu_kien_data = json.load(f)
        with open("data/luat_phoi_do.json", "r", encoding="utf-8") as f:
            luat_phoi_data = json.load(f)
    except Exception as e:
        print(f"Lỗi đọc dữ liệu: {e}")
        return None

    system_instruction = f"""
    Bạn là Stylist Việt Phục Remix - một Gen Z năng động, am hiểu về trang phục truyền thống.
    Nhiệm vụ của bạn là tư vấn phối đồ dựa trên dữ liệu JSON cung cấp.
    Quy tắc đặt tên file hệ thống: [tên_trang_phục]_[giới_tính]_[màu_sắc] (Ví dụ: aotac_nam_do).

    LUẬT XỬ LÝ CỐT LÕI:
    1. MỞ ĐẦU: Khi người dùng mới vào, LUÔN LUÔN mở đầu bằng câu hỏi: "Bạn đã có dự định chọn loại Việt phục nào hay chưa?"
    2. ĐỐI CHIẾU: Dựa vào câu trả lời của người dùng, đối chiếu nghiêm ngặt với:
       - Dữ liệu Phụ kiện: {json.dumps(phu_kien_data, ensure_ascii=False)}
       - Công thức phối đồ: {json.dumps(luat_phoi_data, ensure_ascii=False)}
    3. FALLBACK: Nếu người dùng hỏi về một loại trang phục KHÔNG CÓ trong dữ liệu JSON, bạn phải trả lời: "Ôi tiếc quá, tủ đồ Việt Phục Remix của tụi mình hiện chưa lưu trữ thông tin về trang phục này rồi. Nhưng tụi mình cực kỳ muốn cập nhật thêm đó! Nếu bồ có tư liệu hay gợi ý cách phối đồ nào xịn xò, đừng ngần ngại gửi email đóng góp cho nhóm qua địa chỉ vietphucremix.hcmus@gmail.com nha. Tụi mình vô cùng trân trọng sự hỗ trợ của bồ! ✨"
    4. PHONG CÁCH: Trả lời ngắn gọn, thân thiện kiểu Gen Z, tôn trọng lịch sử. Trực tiếp gợi ý các item trùng khớp với giới tính, phong cách và màu sắc trong dữ liệu.
    """

    chat_session = client.chats.create(
        model='gemini-3-flash-preview',
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7
        )
    )
    return chat_session

def gui_tin_nhan(chat_session, tin_nhan_user):
    try:
        response = chat_session.send_message(tin_nhan_user)
        return response.text
    except Exception as e:
        return "Máy chủ đang quá tải chút xíu, bồ gửi lại tin nhắn nha!"

# ==========================================
# PHẦN 2: DỮ LIỆU SET ĐỒ PHỐI SẴN
# ==========================================
def lay_danh_sach_set_san():
    # Định nghĩa cứng các set đồ có sẵn để TV2 gọi ra hiển thị trực tiếp
    return {
        "set_ao_tac_hien_dai": ["ao_tac_nam_den.png", "quan_lua_ong_rong_den.png", "giay_tay_den.png"],
        "set_nhat_binh_remix": ["ao_nhat_binh_nu_do.png", "chan_vay_xep_ly_den.png", "guoc_moc.png"],
        "set_ngu_than_di_dao": ["ao_ngu_than_tay_chen_be.png", "quan_ong_rong_trang.png", "tui_may_tre_dan.png"],
        "set_co_phuc_le_hoi": ["ao_tac_nu_do.png", "quan_lua_ong_rong_trang.png", "khan_dong_do.png"]
    }

# ==========================================
# PHẦN 3: AI VISION TÌM ĐỒ QUA ẢNH (BÓC TÁCH LAYER & REMIX)
# ==========================================
def quet_anh_tim_do(image_bytes):
    try:
        # Tự động quét file trong thư mục data (bỏ qua json/py)
        danh_sach_file = [f for f in os.listdir("data/") if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        prompt = f"""
        Bạn là Stylist của hệ thống "Việt Phục Remix" - nơi giao thoa giữa trang phục truyền thống và thời trang hiện đại.
        Dưới đây là danh sách tên các file item đang có sẵn trong kho:
        {danh_sach_file}
        
        Nhiệm vụ của bạn khi phân tích bức ảnh:
        1. BÓC TÁCH TỪNG LỚP (Layering): Phân tích kỹ TOÀN BỘ các lớp trang phục trên người mẫu bao gồm: Áo khoác ngoài, Áo mặc trong, Quần/Váy bên dưới và Phụ kiện. Ghi nhận cả MÀU SẮC của từng lớp.
        2. Nhận diện cốt lõi: Ưu tiên tìm các item truyền thống lớp ngoài và phụ kiện lấy ra tên file giống kiểu dáng và màu sắc nhất.
        3. Thay thế thông minh (Remix) & Xử lý Layer: 
           - CHỈ bổ sung lớp áo mặc trong (yếm, croptop, hai dây...) NẾU TRONG ẢNH THỰC SỰ ĐỂ LỘ LỚP ÁO TRONG. 
           - Nếu trang phục trong ảnh là dạng cài kín cổ hoặc không để lộ lớp lót, TUYỆT ĐỐI KHÔNG tự ý thêm áo mặc trong để tránh làm bộ đồ bị cồng kềnh, nóng nực.
           - Nếu ảnh có váy đụp/quần thụng truyền thống mà kho thiếu, hãy thay bằng quần tây/chân váy hiện đại có màu tương tự.
        4. Bổ sung thêm giày hoặc túi hiện đại để chốt set đồ hoàn chỉnh.
        
        BẮT BUỘC chỉ trả về một mảng JSON chứa chính xác tên file của set đồ cuối cùng. KHÔNG giải thích, KHÔNG viết thêm văn bản.
        Ví dụ: ["ao_tac_nu_tim.png", "quan_tay_ong_rong_den.png", "giay_af1_trang.png"]
        """
        
        # Đóng gói ảnh từ luồng byte để đưa vào Gemini
        image_part = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
        
        response = client.models.generate_content(
            model='gemini-3-flash-preview',
            contents=[image_part, prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                # Nhiệt độ 0.5 để AI đủ linh hoạt khi tìm đồ hiện đại bù vào
                temperature=0.5 
            )
        )
        
        # Tự bóc tách JSON và trả về list python thuần cho TV2
        return json.loads(response.text)
        
    except Exception as e:
        print(f"Lỗi hệ thống Vision: {e}")
        # Lỗi mạng hoặc AI quá tải thì trả về mảng rỗng, giao diện TV2 sẽ không bị sập
        return []