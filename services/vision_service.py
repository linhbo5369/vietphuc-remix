import os
import json
from google.genai import types
from services.gemini_config import client

def quet_anh_tim_do(image_bytes):
    try:
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
        4. Bổ sung thêm giày hoặc túi hiện đại để chốt set đồ hoàn chỉnh (4 đến 6 món).
        
        BẮT BUỘC chỉ trả về một mảng JSON chứa chính xác tên file của set đồ cuối cùng. KHÔNG giải thích, KHÔNG viết thêm văn bản.
        Ví dụ: ["ao_tac_nu_tim.png", "quan_tay_ong_rong_den.png", "giay_af1_trang.png"]
        """
        
        image_part = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
        
        response = client.models.generate_content(
            model='gemini-3-flash-preview',
            contents=[image_part, prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.5 
            )
        )
        
        return json.loads(response.text)
        
    except Exception as e:
        print(f"Lỗi hệ thống Vision: {e}")
        return []