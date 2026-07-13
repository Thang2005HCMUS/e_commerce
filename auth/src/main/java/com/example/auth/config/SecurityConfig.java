package com.example.auth.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(auth -> auth
                // 1. Endpoint công khai (Ai cũng vào được)
                .requestMatchers("/auth/test").permitAll()
                
                // 2. Endpoint yêu cầu chỉ cần ĐĂNG NHẬP (Bất kỳ ai đã login đều vào được)
                .requestMatchers("/auth/any-user").authenticated()
                
                // 3. Endpoint yêu cầu quyền CUSTOMER
                .requestMatchers("/auth/customer-only").hasRole("CUSTOMER")
                
                // 4. Endpoint yêu cầu quyền ADMIN
                .requestMatchers("/auth/admin-only").hasRole("ADMIN")
                
                // Các request khác mặc định khóa lại
                .anyRequest().authenticated()
            )
            // Bật cửa sổ đăng nhập mặc định của trình duyệt/Postman
            .httpBasic(Customizer.withDefaults()); 
        
        return http.build();
    }

    // Tạo nhanh tài khoản lưu trong bộ nhớ (In-Memory) để test quyền
    @Bean
    public UserDetailsService userDetailsService() {
        UserDetails customer = User.withUsername("user_test")
                .password("{noop}123456") // {noop} nghĩa là mật khẩu thô không mã hóa (chỉ dùng để test)
                .roles("CUSTOMER") // Spring Security sẽ tự hiểu là ROLE_CUSTOMER
                .build();

        UserDetails admin = User.withUsername("admin_test")
                .password("{noop}123456")
                .roles("ADMIN") // Spring Security sẽ tự hiểu là ROLE_ADMIN
                .build();

        return new InMemoryUserDetailsManager(customer, admin);
    }
}