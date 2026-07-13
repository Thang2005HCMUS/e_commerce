FROM eclipse-temurin:17-jre-alpine
COPY target/auth*.jar app.jar
ENTRYPOINT ["java", "-jar", "/app.jar"]