#!/usr/bin/env bash
set -e

# Tạo thư mục con
mkdir -p auth

# Tạo danh sách các file rỗng
touch auth/__init__.py \
      auth/database.py \
      auth/security.py \
      auth/schemas.py \
      auth/repository.py \
      auth/main.py

echo "Đã tạo xong cấu trúc auth/ trong thư mục hiện tại."