package com.example.gateway.filter;

import org.springframework.cloud.gateway.filter.GatewayFilterChain;
import org.springframework.cloud.gateway.filter.GlobalFilter;
import org.springframework.core.Ordered;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

@Component
public class GatewayLoggingFilter implements GlobalFilter, Ordered {

    @Override
    public Mono<Void> filter(
            ServerWebExchange exchange,
            GatewayFilterChain chain
    ) {

        String method = exchange
                .getRequest()
                .getMethod()
                .name();

        String originalUrl = exchange
                .getRequest()
                .getURI()
                .toString();

        String path = exchange
                .getRequest()
                .getURI()
                .getPath();

        long start = System.currentTimeMillis();

        System.out.println();
        System.out.println("==================================================");
        System.out.println("GATEWAY REQUEST");
        System.out.println("--------------------------------------------------");
        System.out.println("Method      : " + method);
        System.out.println("Original URL: " + originalUrl);
        System.out.println("Path        : " + path);

        return chain.filter(exchange)
                .doFinally(signal -> {

                    long duration =
                            System.currentTimeMillis() - start;

                    int status = exchange
                            .getResponse()
                            .getStatusCode() != null
                            ? exchange.getResponse()
                                    .getStatusCode()
                                    .value()
                            : 0;

                    System.out.println("--------------------------------------------------");
                    System.out.println("Status      : " + status);
                    System.out.println("Duration    : " + duration + " ms");
                    System.out.println("==================================================");
                    System.out.println();
                });
    }

    @Override
    public int getOrder() {
        return Ordered.HIGHEST_PRECEDENCE;
    }
}