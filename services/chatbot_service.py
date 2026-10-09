import json
from google.genai import types
from services.gemini_config import client

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

    HIỂU DỮ LIỆU HỆ THỐNG (CHỈ DÙNG ĐỂ TƯ DUY, KHÔNG IN RA):
    - Mã ID/tên file trong dữ liệu được quy ước: [tên_trang_phục]_[giới_tính]_[màu_sắc] (Ví dụ: ao_tac_nam_do). Hãy dùng quy tắc này để tìm kiếm đồ trong JSON sao cho khớp với giới tính và màu sắc khách yêu cầu.

    LUẬT XỬ LÝ CỐT LÕI:
    1. BẮT LỖI SAI LỆCH LỊCH SỬ (QUAN TRỌNG): Khi người dùng yêu cầu phối đồ, BẮT BUỘC kiểm tra xem có sai kiến thức lịch sử, sai chuẩn mực cổ phục không (ví dụ: mặc quần rách, đồ hở hang với Việt phục).
       - NẾU PHÁT HIỆN SAI LỆCH, BẮT BUỘC THỰC HIỆN ĐÚNG THỨ TỰ 2 BƯỚC:
         + BƯỚC 1 (Nhắc nhở): Ngay câu mở đầu, PHẢI chỉ ra lỗi sai dựa trên lịch sử (Ví dụ: "Ê bồ ơi, theo quy chuẩn truyền thống thì cổ phục luôn đề cao sự chỉn chu, tuyệt đối không đi kèm với đồ rách đâu nha..."). TUYỆT ĐỐI KHÔNG ĐƯỢC BỎ QUA BƯỚC NÀY.
         + BƯỚC 2 (Đề xuất): Sau khi đã nhắc nhở, mới được phép gợi ý set đồ Remix thay thế và nói rõ đây là sự phá cách mang tính cá nhân.
       - NẾU YÊU CẦU CHUẨN MỰC: Tư vấn bình thường, không chèn cảnh báo.
    2. ĐỐI CHIẾU: 
       - Dữ liệu Phụ kiện: {json.dumps(phu_kien_data, ensure_ascii=False)}
       - Công thức phối đồ: {json.dumps(luat_phoi_data, ensure_ascii=False)}
    3. FALLBACK: Nếu hỏi trang phục KHÔNG CÓ, trả lời xin lỗi và mời đóng góp qua email vietphucremix.hcmus@gmail.com.

    QUY TẮC VĂN PHONG VÀ ĐỊNH DẠNG (BẮT BUỘC KHẮC KHOẢNG):
    - CỰC KỲ NGẮN GỌN: Đi thẳng vào vấn đề.
    - NGÔN NGỮ TỰ NHIÊN: Khi gọi tên trang phục, CHỈ được dùng tên tiếng Việt thông thường (ví dụ: Áo đối khâm màu đen). TUYỆT ĐỐI KHÔNG xuất hiện ID, key JSON, hay tên file hệ thống dưới bất kỳ hình thức nào.
    - TUYỆT ĐỐI KHÔNG MARKDOWN: Không bao giờ được sử dụng dấu sao (*), in đậm (**), hay dấu thăng (#).
    - DANH SÁCH SÁT NHAU: BẮT BUỘC sử dụng ký tự chấm tròn (•) để liệt kê item. Các dòng có dấu (•) phải nằm SÁT NHAU (chỉ dùng 1 lần phím Enter để xuống dòng). TUYỆT ĐỐI KHÔNG ĐƯỢC ĐỂ DÒNG TRỐNG XEN GIỮA CÁC MỤC LIỆT KÊ.
    - CÁCH DÒNG CỤC BỘ: Chỉ được chèn 1 dòng trống (Enter 2 lần) ở 2 vị trí: Trước khi bắt đầu danh sách chấm tròn, và sau khi kết thúc danh sách chấm tròn.
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

def tu_van_tu_form(chat_session, thong_tin_khach):
    prompt_an = f"""
    Khách hàng vừa hoàn thành form trắc nghiệm:
    - Loại đồ: {thong_tin_khach.get('loai_do', 'Chưa xác định')}
    - Giới tính: {thong_tin_khach.get('gioi_tinh', 'Chưa xác định')}
    - Sự kiện: {thong_tin_khach.get('su_kien', 'Chưa xác định')}
    - Năng lượng/Phong cách: {thong_tin_khach.get('nang_luong', 'Chưa xác định')}
    - Màu sắc: {thong_tin_khach.get('mau_sac', 'Chưa xác định')}

    Dựa vào dữ liệu kho đồ, hãy tư vấn:
    1. TỰ ĐỘNG BẮT LỖI: Kiểm tra xem loại đồ và yêu cầu của khách có dẫn đến sai lệch lịch sử không. Nếu có, hãy sửa lỗi trước rồi mới gợi ý set đồ. Nếu không, tư vấn bình thường.
    2. TUYỆT ĐỐI KHÔNG dùng ký tự markdown như *, **, #.
    3. NGÔN NGỮ TỰ NHIÊN: Trả lời bằng tên tiếng Việt thông thường, tuyệt đối không xuất hiện tên file data.
    4. DANH SÁCH SÁT NHAU: Liệt kê item bằng dấu chấm tròn (•) sát nhau, không để dòng trống xen giữa các mục.
    """
    return gui_tin_nhan(chat_session, prompt_an)