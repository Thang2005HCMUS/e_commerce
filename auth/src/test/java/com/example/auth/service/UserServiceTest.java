package com.example.auth.service;
import static org.mockito.Mockito.when;
import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;
import org.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class) // Chạy test thuần với Mockito, cực nhanh và không cần DB
class UserServiceTest {

    @Mock
    private UserRepository userRepository; // Giả lập Repository (DB)

    @InjectMocks
    private UserService userService; // Service chứa logic cần test

    @Test
    void testLogicNaoDo() {
        // 1. Định nghĩa dữ liệu giả lập (Khi gọi hàm ở DB thì trả về gì luôn)
        User mockUser = new User("admin", "status_active");
        when(userRepository.findByUsername("admin")).thenReturn(Optional.of(mockUser));

        // 2. Chạy logic thực tế cần test
        String result = userService.checkUserStatus("admin");

        // 3. Assert kết quả logic
        assertEquals("ACTIVE", result);
    }
}