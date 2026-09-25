
from pathlib import Path

ROOT = Path("gateway")

FILES = {
    "settings.gradle.kts": r'''
rootProject.name = "gateway"
''',

    "build.gradle.kts": r'''
plugins {
    java

    id("org.springframework.boot") version "4.0.7"
    id("io.spring.dependency-management") version "1.1.7"
}

group = "com.example"
version = "0.0.1-SNAPSHOT"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

repositories {
    mavenCentral()
}

extra["springCloudVersion"] = "2025.0.0"

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-security")

    implementation(
        "org.springframework.cloud:spring-cloud-starter-gateway-server-webflux"
    )

    // JWT - giữ nguyên giống Auth Service
    implementation("io.jsonwebtoken:jjwt-api:0.12.6")
    runtimeOnly("io.jsonwebtoken:jjwt-impl:0.12.6")
    runtimeOnly("io.jsonwebtoken:jjwt-jackson:0.12.6")

    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.springframework.boot:spring-boot-starter-security-test")
}

dependencyManagement {
    imports {
        mavenBom(
            "org.springframework.cloud:spring-cloud-dependencies:${property("springCloudVersion")}"
        )
    }
}

tasks.withType<Test> {
    useJUnitPlatform()
}

tasks.getByName<Jar>("jar") {
    enabled = false
}
''',

    "src/main/resources/application.properties": r'''
server.port=8080

spring.application.name=gateway

# ==========================================================
# JWT
# ==========================================================

# Nên lấy từ environment variable khi chạy production
jwt.secret=${JWT_SECRET}
jwt.expiration=86400000

# ==========================================================
# AUTH SERVICE
# ==========================================================

spring.cloud.gateway.routes[0].id=auth-service
spring.cloud.gateway.routes[0].uri=http://localhost:8081
spring.cloud.gateway.routes[0].predicates[0]=Path=/auth/**

# ==========================================================
# USER SERVICE
# ==========================================================

spring.cloud.gateway.routes[1].id=user-service
spring.cloud.gateway.routes[1].uri=http://localhost:8082
spring.cloud.gateway.routes[1].predicates[0]=Path=/users/**

# ==========================================================
# ORDER SERVICE
# ==========================================================

spring.cloud.gateway.routes[2].id=order-service
spring.cloud.gateway.routes[2].uri=http://localhost:8083
spring.cloud.gateway.routes[2].predicates[0]=Path=/orders/**

# ==========================================================
# PRODUCT SERVICE
# ==========================================================

spring.cloud.gateway.routes[3].id=product-service
spring.cloud.gateway.routes[3].uri=http://localhost:8084
spring.cloud.gateway.routes[3].predicates[0]=Path=/products/**
''',

    "src/main/java/com/example/gateway/GatewayApplication.java": r'''
package com.example.gateway;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class GatewayApplication {

    public static void main(String[] args) {
        SpringApplication.run(GatewayApplication.class, args);
    }
}
''',

    "src/main/java/com/example/gateway/config/SecurityConfig.java": r'''
package com.example.gateway.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.reactive.EnableWebFluxSecurity;
import org.springframework.security.config.web.server.ServerHttpSecurity;
import org.springframework.security.web.server.SecurityWebFilterChain;

@Configuration
@EnableWebFluxSecurity
public class SecurityConfig {

    @Bean
    public SecurityWebFilterChain securityWebFilterChain(
            ServerHttpSecurity http
    ) {
        return http
                .csrf(ServerHttpSecurity.CsrfSpec::disable)
                .formLogin(ServerHttpSecurity.FormLoginSpec::disable)
                .httpBasic(ServerHttpSecurity.HttpBasicSpec::disable)
                .logout(ServerHttpSecurity.LogoutSpec::disable)
                .authorizeExchange(exchange -> exchange
                        .anyExchange()
                        .permitAll()
                )
                .build();
    }
}
''',

    "src/main/java/com/example/gateway/security/JwtService.java": r'''
package com.example.gateway.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jws;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;

@Service
public class JwtService {

    private final SecretKey secretKey;

    public JwtService(
            @Value("${jwt.secret}") String secret
    ) {
        this.secretKey = Keys.hmacShaKeyFor(
                secret.getBytes(StandardCharsets.UTF_8)
        );
    }

    public Jws<Claims> validateToken(String token) {

        return Jwts.parser()
                .verifyWith(secretKey)
                .build()
                .parseSignedClaims(token);
    }
}
''',

    "src/main/java/com/example/gateway/security/JwtGatewayFilter.java": r'''
package com.example.gateway.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jws;
import org.springframework.cloud.gateway.filter.GatewayFilterChain;
import org.springframework.cloud.gateway.filter.GlobalFilter;
import org.springframework.core.Ordered;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

@Component
public class JwtGatewayFilter implements GlobalFilter, Ordered {

    private final JwtService jwtService;

    public JwtGatewayFilter(JwtService jwtService) {
        this.jwtService = jwtService;
    }

    @Override
    public Mono<Void> filter(
            ServerWebExchange exchange,
            GatewayFilterChain chain
    ) {

        String path = exchange
                .getRequest()
                .getURI()
                .getPath();

        // ==================================================
        // AUTH SERVICE
        // Login / Register không cần JWT
        // ==================================================

        if (path.startsWith("/auth/")) {
            return chain.filter(exchange);
        }

        // ==================================================
        // Lấy Authorization header
        // ==================================================

        String authorization =
                exchange.getRequest()
                        .getHeaders()
                        .getFirst(HttpHeaders.AUTHORIZATION);

        if (authorization == null ||
                !authorization.startsWith("Bearer ")) {

            return unauthorized(exchange);
        }

        String token = authorization.substring(7).trim();

        if (token.isEmpty()) {
            return unauthorized(exchange);
        }

        // ==================================================
        // Verify JWT
        // ==================================================

        try {

            Jws<Claims> claims =
                    jwtService.validateToken(token);

            Claims payload = claims.getPayload();

            String userId = payload.getSubject();

            // ==================================================
            // Không trust header từ Client
            // Gateway tự set lại X-User-Id
            // ==================================================

            ServerWebExchange mutatedExchange =
                    exchange.mutate()
                            .request(request ->
                                    request.headers(headers -> {

                                        headers.remove("X-User-Id");

                                        if (userId != null) {
                                            headers.set(
                                                    "X-User-Id",
                                                    userId
                                            );
                                        }
                                    })
                            )
                            .build();

            return chain.filter(mutatedExchange);

        } catch (Exception e) {

            return unauthorized(exchange);
        }
    }

    private Mono<Void> unauthorized(
            ServerWebExchange exchange
    ) {

        exchange.getResponse()
                .setStatusCode(HttpStatus.UNAUTHORIZED);

        return exchange.getResponse().setComplete();
    }

    @Override
    public int getOrder() {
        return -100;
    }
}
''',

    "src/test/java/com/example/gateway/GatewayApplicationTests.java": r'''
package com.example.gateway;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class GatewayApplicationTests {

    @Test
    void contextLoads() {
    }
}
'''
}


def create_files():
    for relative_path, content in FILES.items():
        file_path = ROOT / relative_path

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path.write_text(
            content.strip() + "\n",
            encoding="utf-8"
        )

        print(f"Created: {file_path}")


if __name__ == "__main__":
    create_files()

    print()
    print("Gateway project created successfully.")
    print(f"Location: {ROOT.resolve()}")