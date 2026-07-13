package com.example.auth.config;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;
import java.util.stream.Collectors;

@Service
public class JwtService {

    // LƯU Ý: Với JJWT bản mới, chuỗi Secret Key phải dài từ 32 ký tự (256-bit) trở lên mới hợp lệ
    private final String SECRET_KEY = "dien_chuoi_secret_key_sieu_bao_mat_cua_ban_vao_day_phai_dai_tren_32_ky_tu"; 
    private final long EXPIRATION_TIME = 86400000; // 1 ngày

    public String generateToken(UserDetails userDetails) {
        // 1. Tạo mã khóa an toàn từ chuỗi Secret Key
        SecretKey key = Keys.hmacShaKeyFor(SECRET_KEY.getBytes(StandardCharsets.UTF_8));

        // 2. Lấy danh sách quyền của User
        String roles = userDetails.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .collect(Collectors.joining(","));

        // 3. Build chuỗi JWT theo cú pháp mới của JJWT 0.12.x
        return Jwts.builder()
                .subject(userDetails.getUsername())
                .claim("roles", roles) // Nhét quyền vào claim
                .issuedAt(new Date(System.currentTimeMillis()))
                .expiration(new Date(System.currentTimeMillis() + EXPIRATION_TIME))
                .signWith(key) // Ký bằng khóa vừa tạo
                .compact();
    }
}