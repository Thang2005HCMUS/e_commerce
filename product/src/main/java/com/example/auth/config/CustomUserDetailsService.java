// package com.example.auth.config;
// import org.springframework.security.core.userdetails.User;
// import org.springframework.security.core.userdetails.UserDetails;
// import org.springframework.security.core.userdetails.UserDetailsService;
// import org.springframework.security.core.userdetails.UsernameNotFoundException;
// import org.springframework.security.provisioning.InMemoryUserDetailsManager;
// import org.springframework.stereotype.Service;

// @Service
// public class CustomUserDetailsService implements UserDetailsService {

//     private final InMemoryUserDetailsManager inMemoryManager;

//     public CustomUserDetailsService() {
//         // Nhấc dữ liệu tài khoản test từ SecurityConfig sang đây
//         UserDetails customer = User.withUsername("user_test")
//                 .password("{noop}123456") 
//                 .roles("CUSTOMER") 
//                 .build();

//         UserDetails admin = User.withUsername("admin_test")
//                 .password("{noop}123456")
//                 .roles("ADMIN") 
//                 .build();

//         this.inMemoryManager = new InMemoryUserDetailsManager(customer, admin);
//     }

//     @Override
//     public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
//         return inMemoryManager.loadUserByUsername(username);
//     }
// }