import pandas as pd
import json
import unicodedata
import re

def normalize_key(text):
    """Hàm tự động tạo Key không dấu, cách nhau bằng gạch dưới (VD: Áo dài tân thời -> ao_dai_tan_thoi)"""
    text = str(text).strip()
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8').lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return '_'.join(text.split())

def create_rules_engine():
    # Đọc file CSV (đảm bảo đúng tên file của bạn)
    csv_file = 'data/phoi-do-chi-tiet.csv'
    
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file {csv_file}")
        return

    # Xóa các dòng rỗng và ký tự xuống dòng bị lỗi
    df = df.dropna(subset=['trang phục'])
    df['cách phối'] = df['cách phối'].astype(str).str.replace('\n', ' ')

    rules_engine = {}

    for index, row in df.iterrows():
        # Chuẩn hóa các cột thành key
        trang_phuc_key = normalize_key(row['trang phục'])
        gioi_tinh = normalize_key(row['giới tính'])
        phong_cach_key = normalize_key(row['phong cách'])
        
        mau_sac = str(row['màu']).strip()
        cach_phoi = str(row['cách phối']).strip()

        # Xây dựng cấu trúc cây thư mục JSON
        if trang_phuc_key not in rules_engine:
            rules_engine[trang_phuc_key] = {}
            
        if gioi_tinh not in rules_engine[trang_phuc_key]:
            rules_engine[trang_phuc_key][gioi_tinh] = {}
            
        if phong_cach_key not in rules_engine[trang_phuc_key][gioi_tinh]:
            rules_engine[trang_phuc_key][gioi_tinh][phong_cach_key] = []
            
        # Nạp công thức phối đồ vào
        rules_engine[trang_phuc_key][gioi_tinh][phong_cach_key].append({
            "mau_sac": mau_sac,
            "cong_thuc_goi_y": cach_phoi
        })

    # Ghi ra file luat_phoi_do.json
    output_path = 'data/luat_phoi_do.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(rules_engine, f, ensure_ascii=False, indent=4)
        
    print(f"✅ Tuyệt vời! Đã tạo thành công file {output_path} với cấu trúc siêu logic.")

if __name__ == "__main__":
    create_rules_engine()