import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import pandas as pd
import json

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY") 
client = genai.Client(api_key=API_KEY)

def tu_van_viet_phuc(cau_hoi_cua_user):
    # 1. Đọc dữ liệu từ file CSV
    try:
        df = pd.read_csv("data/trang-phuc.csv")
        csdl_string = df.to_string(index=False) 
    except Exception as e:
        return f'{{"loi": "Không thể đọc cơ sở dữ liệu: {e}"}}'

    # 2. Cài đặt System Instructions (Luật chơi của AI)
    system_instruction = f"""
    Bạn là một Stylist Gen Z năng động, am hiểu về trang phục truyền thống Việt Nam.
    Nhiệm vụ của bạn là tư vấn cách phối đồ Việt phục dựa trên CƠ SỞ DỮ LIỆU ĐƯỢC CUNG CẤP DƯỚI ĐÂY.

    Quy tắc sinh tử (Bắt buộc tuân thủ):
    1. KHÔNG BỊA ĐẶT (No Hallucination): Chỉ sử dụng thông tin có trong CSDL. Nếu người dùng hỏi về một loại trang phục hoặc thông tin không có trong bảng này, bạn phải tuân thủ nghiêm ngặt định dạng sau: Điền câu "Xin lỗi, hiện tại tủ đồ của mình chưa có dữ liệu về trang phục này, bạn thử chọn loại khác xem sao nha!" vào duy nhất trường "loi_khuyen_stylist". Các trường "phoi_hien_dai" và "phoi_mau" bắt buộc phải để trống (là chuỗi rỗng "").

    2. GIỌNG ĐIỆU (Tone): thân thiện, trẻ trung, có thể sử dụng các slang của Gen Z, TÔN TRỌNG lịch sử, không cợt nhả với ý nghĩa trang phục.

    3. ĐỊNH DẠNG ĐẦU RA (Output Format): Mọi câu trả lời của bạn phải được bọc trong định dạng JSON với cấu trúc sau để hệ thống web đọc được:
    {{
      "ten_trang_phuc": "",
      "loi_khuyen_stylist": "",
      "phoi_hien_dai": "",
      "phoi_mau": ""
    }}

    CƠ SỞ DỮ LIỆU:
    {csdl_string}
    """

    # 3. Gửi câu hỏi và nhận kết quả với cấu hình JSON
    response = client.models.generate_content(
        model='gemini-3-flash-preview',
        contents=cau_hoi_cua_user,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
        )
    )

    return response.text

if __name__ == "__main__":
    # Test case 1: Có trong CSDL
    cau_hoi_1 = "Tư vấn cho mình cách phối Áo Tấc nha bồ."
    print("Test 1 (Áo Tấc):")
    print(tu_van_viet_phuc(cau_hoi_1))
    print("-" * 50)

    # Test case 2: Không có trong CSDL
    cau_hoi_2 = "Phối Áo Chàm đi sự kiện giúp mình với."
    print("Test 2 (Áo Chàm):")
    print(tu_van_viet_phuc(cau_hoi_2))