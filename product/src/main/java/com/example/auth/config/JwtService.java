package com.example.auth.config;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Value;
import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;
import java.util.stream.Collectors;
import io.jsonwebtoken.Claims;
import java.util.function.Function;

@Service
public class JwtService {

    // LƯU Ý: Với JJWT bản mới, chuỗi Secret Key phải dài từ 32 ký tự (256-bit) trở lên mới hợp lệ
    @Value("${jwt.secret}")
    private String SECRET_KEY;
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
    private SecretKey getSigningKey() {
    return Keys.hmacShaKeyFor(SECRET_KEY.getBytes(StandardCharsets.UTF_8));
}

// 1. Lấy Username từ Token
public String extractUsername(String token) {
    return extractClaim(token, Claims::getSubject);
}

// 2. Lấy thời gian hết hạn từ Token
public Date extractExpiration(String token) {
    return extractClaim(token, Claims::getExpiration);
}

// 3. Hàm trích xuất Claim tổng quát
public <T> T extractClaim(String token, Function<Claims, T> claimsResolver) {
    final Claims claims = Jwts.parser()
            .verifyWith(getSigningKey())
            .build()
            .parseSignedClaims(token)
            .getPayload();
    return claimsResolver.apply(claims);
}

// 4. Kiểm tra Token đã hết hạn chưa (So sánh exp với giờ hiện tại)
private Boolean isTokenExpired(String token) {
    return extractExpiration(token).before(new Date());
}

// 5. Kiểm tra Token có hợp lệ không (Đúng user và chưa hết hạn)
public Boolean validateToken(String token, UserDetails userDetails) {
    final String username = extractUsername(token);
    return (username.equals(userDetails.getUsername()) && !isTokenExpired(token));
}
}