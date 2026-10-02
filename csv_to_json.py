import csv
import json
import unicodedata
import os

def convert_csv_to_json():
    # Đảm bảo đường dẫn trỏ đúng vào thư mục data
    csv_file_path = 'data/trang-phuc.csv'
    json_file_path = 'data/trang_phuc.json'
    
    json_data = {}
    
    try:
        # Đọc file CSV
        with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ten = str(row.get('Tên trang phục', '')).strip()
                if not ten or ten.lower() == 'nan':
                    continue
                
                # Tự động tạo Key không dấu, cách nhau bằng dấu gạch dưới (VD: "Áo tứ thân" -> "ao_tu_than")
                key = unicodedata.normalize('NFKD', ten).encode('ASCII', 'ignore').decode('utf-8').lower()
                key = ''.join(c if c.isalnum() else '_' for c in key)
                key = '_'.join(filter(None, key.split('_')))
                
                # Bóc tách dữ liệu
                json_data[key] = {
                    "nhom": str(row.get('Nhóm', '')).strip(),
                    "ten": ten,
                    "gioi_tinh": str(row.get('Giới tính', '')).strip(),
                    "nguon_goc": str(row.get('Nguồn gốc (ngắn gọn)', '')).strip(),
                    "y_nghia": str(row.get('Ý nghĩa (ngắn gọn)', '')).strip(),
                    "dac_diem": str(row.get('Đặc điểm', '')).strip(),
                    "hoan_canh": str(row.get('Hoàn cảnh sử dụng', '')).strip(),
                    "cach_phoi_truyen_thong": str(row.get('Cách phối truyền thống', '')).strip(),
                    "cach_phoi_hien_dai": str(row.get('Cách phối hiện đại', '')).strip(),
                    "phoi_mau": str(row.get('Phối màu', '')).strip()
                }

        # Ghi ra file JSON
        with open(json_file_path, mode='w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)
            
        print("✅ Đã chuyển đổi thành công! Hãy kiểm tra file trang_phuc.json trong thư mục data.")
        
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file {csv_file_path}. Hãy chắc chắn TV1 đã để nó trong thư mục 'data/'.")

if __name__ == "__main__":
    convert_csv_to_json()