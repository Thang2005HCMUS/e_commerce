package com.example.auth;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

// Loại trừ cấu hình AutoConfiguration của DB bằng cách gọi trực tiếp qua tên chuỗi (String), 
// giúp tránh việc phải import các class không tồn tại trong class-path của Test.
@SpringBootTest(properties = {
    "spring.autoconfigure.exclude=org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration,org.springframework.boot.autoconfigure.orm.jpa.HibernateJpaAutoConfiguration"
})
class AuthApplicationTests {

    @Test
    void contextLoads() {
        // Test chạy thành công khi Spring Context load được mà không cần kết nối DB thật
    }

}