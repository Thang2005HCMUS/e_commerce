package com.example.auth.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/auth")
public class AuthController {

    // 1. Link cũ công khai
    @GetMapping("/test")
    public String testAuthService() {
        return "auth service is ready";
    }

    // 2. Chỉ cần đăng nhập thành công là vào được
    @GetMapping("/any-user")
    public String anyUser() {
        return "Bạn đã đăng nhập thành công! Bất kỳ user nào cũng thấy được thông báo này.";
    }

    // 3. Chỉ tài khoản có quyền CUSTOMER mới vào được
    @GetMapping("/customer-only")
    public String customerOnly() {
        return "Chào mừng quý khách! Đây là tính năng dành riêng cho CUSTOMER.";
    }

    // 4. Chỉ tài khoản có quyền ADMIN mới vào được
    @GetMapping("/admin-only")
    public String adminOnly() {
        return "Khu vực quản trị! Đây là tính năng dành riêng cho ADMIN.";
    }
}