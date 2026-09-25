-- Dòng này giúp tránh bị lỗi trùng lặp dữ liệu khi khởi động lại app nhiều lần
INSERT INTO roles (name) 
VALUES ('ROLE_CUSTOMER'), ('ROLE_ADMIN') 
ON CONFLICT (name) DO NOTHING;
