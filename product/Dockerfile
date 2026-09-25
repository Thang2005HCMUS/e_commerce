FROM eclipse-temurin:17-jre-alpine

# Gradle lưu file jar ở build/libs/ thay vì target/
COPY build/libs/auth-*.jar app.jar

ENTRYPOINT ["java", "-jar", "/app.jar"]