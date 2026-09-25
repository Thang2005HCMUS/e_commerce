import os


def clone_java_contents():
    # File kết quả sẽ được tạo ở thư mục hiện tại
    output_filename = "content.txt"

    # Mở file content.txt với chế độ ghi (w) và định dạng utf-8 để tránh lỗi font
    with open(output_filename, "w", encoding="utf-8") as outfile:
        # os.walk('.') sẽ duyệt qua toàn bộ thư mục hiện tại và các thư mục con
        for root, dirs, files in os.walk("."):
            for file in files:
                # Kiểm tra nếu file có đuôi .java
                if file.endswith(".java"):
                    # Lấy đường dẫn đầy đủ của file
                    file_path = os.path.join(root, file)

                    try:
                        # Đọc nội dung của file .java
                        with open(file_path, "r", encoding="utf-8") as infile:
                            content = infile.read()

                        # Ghi tiêu đề đường dẫn và nội dung vào file content.txt
                        outfile.write(f"======{file_path}======\n")
                        outfile.write(content)
                        outfile.write(
                            "\n\n"
                        )  # Thêm dòng trống để phân tách giữa các file

                        print(f"Đã gom file: {file_path}")

                    except Exception as e:
                        # Xử lý trường hợp file lỗi font hoặc không có quyền đọc
                        print(f"Không thể đọc file {file_path}. Lỗi: {e}")


if __name__ == "__main__":
    clone_java_contents()
    print("--- Hoàn thành! ---")