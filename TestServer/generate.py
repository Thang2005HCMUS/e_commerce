import os
import re

def generate_files_from_txt(txt_file="content.txt"):
    if not os.path.exists(txt_file):
        print(f"Lỗi: Không tìm thấy file '{txt_file}'")
        return

    with open(txt_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern bắt chính xác đường dẫn nằm giữa 2 cụm ký tự
    pattern = r"<><>----------<><>\s*<([^>]+)>\s*<><>--------<><>\n*"
    
    # Split content theo pattern. 
    # Kết quả trả về danh sách: [text_truoc_match, filepath_1, content_1, filepath_2, content_2, ...]
    parts = re.split(pattern, content)

    # Bỏ qua phần tử đầu tiên (thường là khoảng trắng hoặc text linh tinh trước khi bắt đầu)
    for i in range(1, len(parts), 2):
        filepath = parts[i].strip()
        file_content = parts[i+1]

        # Xóa bớt khoảng trắng/dòng trống thừa ở cuối đoạn code
        if file_content.endswith('\n'):
            file_content = file_content.rstrip() + '\n'

        # Lấy ra đường dẫn thư mục cha
        dir_name = os.path.dirname(filepath)
        
        # Tạo thư mục nếu chưa tồn tại
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        # Ghi nội dung vào file
        with open(filepath, 'w', encoding='utf-8') as out_file:
            out_file.write(file_content)
            
        print(f"Đã tạo thành công: {filepath}")

if __name__ == "__main__":
    generate_files_from_txt("content-user.txt")