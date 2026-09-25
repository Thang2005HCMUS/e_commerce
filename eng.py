import re
import os

def tach_tu_vung_obsidian(file_path, output_dir="vocab_files"):
    if not os.path.exists(file_path):
        print(f"Không tìm thấy file: {file_path}")
        return

    # Tạo thư mục chứa các file từ vựng riêng lẻ nếu chưa có
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Tách nội dung file tổng thành từng khối dựa trên đường kẻ ngang ----
    blocks = re.split(r'\n-+\s*\n', content)
    
    parsed_words = []
    # Bước 1: Quét trước toàn bộ danh sách từ vựng để làm từ điển liên kết
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        # Tìm từ vựng ở đầu khối (ví dụ: "Drought(n):" hoặc "dried up (v):")
        match = re.match(r'^([a-zA-Z\s\-\']+)(?:\([a-z\s]+\))?\s*:', block)
        if match:
            word = match.group(1).strip()
            parsed_words.append((word, block))

    # Sắp xếp từ dài đến ngắn để tránh thay thế đè từ ngắn lên từ dài
    vocab_list = sorted([w[0] for w in parsed_words], key=len, reverse=True)

    # Bước 2: Xử lý nội dung và tạo file riêng lẻ cho từng từ
    for word, original_block in parsed_words:
        # Thay thế các từ liên quan xuất hiện trong ví dụ/link thành dạng [[Từ_Khóa]]
        processed_content = original_block
        
        for vocab in vocab_list:
            # Không tự liên kết chính nó
            if vocab.lower() == word.lower():
                continue
                
            # Regex tìm từ độc lập (không nằm trong [[ ]] sẵn và không phải là một phần của từ khác)
            pattern = rf'(?<!\[\[)\b{re.escape(vocab)}(?:ing|ed|s)?\b(?!\]\])'
            
            def replace_with_link(m):
                matched_str = m.group(0)
                # Đưa về dạng link chuẩn của từ gốc trong Obsidian
                for v in vocab_list:
                    if matched_str.lower().startswith(v.lower()) and v.lower() != word.lower():
                        suffix = matched_str[len(v):]
                        return f"[[{v}]]{suffix}"
                return f"[[{matched_str}]]"
                
            processed_content = re.sub(pattern, replace_with_link, processed_content, flags=re.IGNORECASE)

        # Sửa lại định dạng phần Link: cho đẹp mắt
        # Chuyển các dòng link thường thành định dạng danh sách của Obsidian [[link]]
        lines = processed_content.split('\n')
        new_lines = []
        in_link_section = False
        for line in lines:
            if line.strip().startswith("Link:"):
                in_link_section = True
                new_lines.append(line)
                continue
            if in_link_section and line.strip() and not line.strip().startswith("-"):
                # Nếu có từ trong phần Link mà chưa có [[ ]], tự động thêm vào
                link_word = line.strip()
                if not link_word.startswith("[["):
                    # Tìm từ chuẩn trong danh sách từ vựng để map đúng link viết hoa/thường
                    matched_vocab = next((v for v in vocab_list if v.lower() == link_word.lower()), link_word)
                    new_lines.append(f"- [[{matched_vocab}]]")
                else:
                    new_lines.append(f"- {link_word}")
            else:
                new_lines.append(line)
        
        final_content = '\n'.join(new_lines)
        
        # Tạo file .md riêng cho từ này (ví dụ: "Shortages.md")
        file_name = f"{word}.md"
        # Tránh lỗi ký tự đặc biệt trong tên file nếu có
        file_name = "".join(c for c in file_name if c.isalnum() or c in (' ', '.', '_', '-')).strip()
        file_path = os.path.join(output_dir, file_name)
        
        with open(file_path, 'w', encoding='utf-8') as out_f:
            out_f.write(final_content)
            
    print(f"Đã tách thành công! Toàn bộ {len(parsed_words)} file từ vựng đã được lưu tại thư mục: '{output_dir}/'")

if __name__ == "__main__":
    tach_tu_vung_obsidian("document.md")