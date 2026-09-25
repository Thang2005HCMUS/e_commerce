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
