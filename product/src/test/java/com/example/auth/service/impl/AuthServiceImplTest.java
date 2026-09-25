package com.example.auth.service.impl;

import com.example.auth.config.JwtService;
import com.example.auth.dto.request.LoginRequest;
import com.example.auth.dto.request.RegisterRequest;
import com.example.auth.dto.response.AuthResponse;
import com.example.auth.entity.Role;
import com.example.auth.entity.User;
import com.example.auth.repository.RoleRepository;
import com.example.auth.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

class AuthServiceImplTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private RoleRepository roleRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @Mock
    private AuthenticationManager authenticationManager;

    @Mock
    private JwtService jwtService;

    @InjectMocks
    private AuthServiceImpl authService;

    @BeforeEach
    void setUp() {
        // Khởi tạo các Mock object trước mỗi test case
        MockitoAnnotations.openMocks(this);
    }

    // ==========================================
    // TEST ĐĂNG KÝ (REGISTER)
    // ==========================================

    @Test
    void testRegister_Success() {
        // Given (Chuẩn bị dữ liệu)
        RegisterRequest request = new RegisterRequest();
        request.setUsername("newuser");
        request.setEmail("newuser@example.com");
        request.setPassword("password123");

        Role role = new Role();
        role.setName("ROLE_CUSTOMER");

        when(userRepository.existsByUsername("newuser")).thenReturn(false);
        when(userRepository.existsByEmail("newuser@example.com")).thenReturn(false);
        when(roleRepository.findByName("ROLE_CUSTOMER")).thenReturn(Optional.of(role));
        when(passwordEncoder.encode("password123")).thenReturn("encryptedPassword");

        // When (Thực thi hành động)
        String result = authService.register(request);

        // Then (Kiểm tra kết quả)
        assertEquals("Đăng ký tài khoản thành công!", result);
        verify(userRepository, times(1)).save(any(User.class));
    }

    @Test
    void testRegister_UsernameExists_ThrowsException() {
        // Given
        RegisterRequest request = new RegisterRequest();
        request.setUsername("existinguser");

        when(userRepository.existsByUsername("existinguser")).thenReturn(true);

        // When & Then
        RuntimeException exception = assertThrows(RuntimeException.class, () -> {
            authService.register(request);
        });

        assertEquals("Username đã tồn tại!", exception.getMessage());
        verify(userRepository, never()).save(any(User.class));
    }

    @Test
    void testRegister_EmailExists_ThrowsException() {
        // Given
        RegisterRequest request = new RegisterRequest();
        request.setUsername("validuser");
        request.setEmail("existing@example.com");

        when(userRepository.existsByUsername("validuser")).thenReturn(false);
        when(userRepository.existsByEmail("existing@example.com")).thenReturn(true);

        // When & Then
        RuntimeException exception = assertThrows(RuntimeException.class, () -> {
            authService.register(request);
        });

        assertEquals("Email đã tồn tại!", exception.getMessage());
        verify(userRepository, never()).save(any(User.class));
    }

    @Test
    void testRegister_RoleNotFound_ThrowsException() {
        // Given
        RegisterRequest request = new RegisterRequest();
        request.setUsername("validuser");
        request.setEmail("valid@example.com");

        when(userRepository.existsByUsername("validuser")).thenReturn(false);
        when(userRepository.existsByEmail("valid@example.com")).thenReturn(false);
        when(roleRepository.findByName("ROLE_CUSTOMER")).thenReturn(Optional.empty());

        // When & Then
        RuntimeException exception = assertThrows(RuntimeException.class, () -> {
            authService.register(request);
        });

        assertEquals("Quyền ROLE_CUSTOMER không tồn tại trong hệ thống!", exception.getMessage());
        verify(userRepository, never()).save(any(User.class));
    }

    // ==========================================
    // TEST ĐĂNG NHẬP (LOGIN)
    // ==========================================

    @Test
    void testLogin_Success() {
        // Given
        LoginRequest request = new LoginRequest();
        request.setUsername("user123");
        request.setPassword("correctPassword");

        Authentication authentication = mock(Authentication.class);
        UserDetails userDetails = mock(UserDetails.class);

        when(authenticationManager.authenticate(any(UsernamePasswordAuthenticationToken.class)))
                .thenReturn(authentication);
        when(authentication.getPrincipal()).thenReturn(userDetails);
        when(jwtService.generateToken(userDetails)).thenReturn("mocked-jwt-token");

        // When
        AuthResponse response = authService.login(request);

        // Then
        assertNotNull(response);
        assertEquals("mocked-jwt-token", response.getAccessToken());
        assertEquals("Bearer", response.getTokenType());
    }
}