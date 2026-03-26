# ─── Stage 1: Build ───────────────────────────────
FROM eclipse-temurin:21-jdk-alpine AS builder

WORKDIR /build

# Gradle Wrapper + 의존성 레이어 캐싱
COPY gradlew .
COPY gradle/ gradle/
COPY build.gradle settings.gradle ./
RUN ./gradlew dependencies --no-daemon || true

COPY src/ src/
RUN ./gradlew bootJar --no-daemon -x test

# ─── Stage 2: Runtime ─────────────────────────────
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app
COPY --from=builder /build/build/libs/*.jar app.jar

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
