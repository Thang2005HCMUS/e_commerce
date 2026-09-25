package com.example.auth.controller;

// import com.example.auth.config.JwtService;
import com.example.auth.dto.request.LoginRequest;
import com.example.auth.dto.request.RegisterRequest;
import com.example.auth.dto.response.AuthResponse;
import com.example.auth.service.AuthService;

import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
// import org.springframework.security.authentication.AuthenticationManager;
// import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
// import org.springframework.security.core.Authentication;
// import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;
@RestController
@RequestMapping("/auth")
public class AuthController {
//     private final AuthenticationManager authenticationManager;
//     private final JwtService jwtService;
//     public AuthController(AuthenticationManager authenticationManager, JwtService jwtService) {
//         this.authenticationManager = authenticationManager;
//         this.jwtService = jwtService;
//     }
    // 1. Link cũ công khai
    @GetMapping("/test")
    public String testAuthService() {
        return "auth service is ready";
    }

//     // 2. Chỉ cần đăng nhập thành công là vào được
//     @GetMapping("/any-user")
//     public String anyUser() {
//         return "Bạn đã đăng nhập thành công! Bất kỳ user nào cũng thấy được thông báo này.";
//     }

//     // 3. Chỉ tài khoản có quyền CUSTOMER mới vào được
//     @GetMapping("/customer-only")
//     public String customerOnly() {
//         return "Chào mừng quý khách! Đây là tính năng dành riêng cho CUSTOMER.";
//     }

//     // 4. Chỉ tài khoản có quyền ADMIN mới vào được
//     @GetMapping("/admin-only")
//     public String adminOnly() {
//         return "Khu vực quản trị! Đây là tính năng dành riêng cho ADMIN.";
//    }
//    @PostMapping("/login")
//     public ResponseEntity<AuthResponse> login(@Valid @RequestBody LoginRequest request) {
//         // 1. Xác thực username và password xem có đúng không
//         Authentication authentication = authenticationManager.authenticate(
//                 new UsernamePasswordAuthenticationToken(request.getUsername(), request.getPassword())
//         );

//         // 2. Nếu đúng, lấy thông tin UserDetails ra
//         UserDetails userDetails = (UserDetails) authentication.getPrincipal();

//         // 3. Sinh JWT Token
//         String token = jwtService.generateToken(userDetails);

//         // 4. Trả token về cho Client
//         return ResponseEntity.ok(new AuthResponse(token, "Bearer"));
//     }
    private final AuthService authService;
    public AuthController(AuthService authService) {
        this.authService = authService;
    }
    @PostMapping("/register")
    public ResponseEntity<String> register(@Valid @RequestBody RegisterRequest request) {
        String result = authService.register(request);
        return ResponseEntity.ok(result);
    }

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@Valid @RequestBody LoginRequest request) {
        AuthResponse response = authService.login(request);
        return ResponseEntity.ok(response);
    }
}