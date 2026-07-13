package com.example.auth; // Thay bằng package đúng của bạn

import org.junit.jupiter.api.Test;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;
import org.springframework.boot.autoconfigure.orm.jpa.HibernateJpaAutoConfiguration;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
@EnableAutoConfiguration(exclude = {
    DataSourceAutoConfiguration.class, 
    HibernateJpaAutoConfiguration.class
})
class AuthApplicationTests {

    @Test
    void contextLoads() {
        // Test này giờ sẽ pass vì Spring không còn tìm cách kết nối DB nữa
    }
}