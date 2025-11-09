# APIOrchestra-VTB
VTB API HACK APIOrchestra 
# 🏦 APIOrchestra — Автоматизированное тестирование API-оркестров с ИИ

> **Тестируй бизнес-процессы, а не эндпоинты. Без кода. С ИИ. Локально.**

![APIOrchestra Demo](https://via.placeholder.com/800x400/1a1a2e/ffffff?text=APIOrchestra+Demo+Screenshot)

**Автор**: Дмитрий Крылосов, Уфа, Россия  
**Язык**: Java 17+ (Spring Boot), Python 3.x  
**Технологии**: Spring Boot 3, Swagger Parser, Requests, Dataclasses  
**Лицензия**: MIT  
**Статус**: Готово к запуску — работает на Ubuntu 20.04 с Java 17 и Python 3.8+

---

## 💡 Проблема

Современные цифровые сервисы (кредиты, оплата, открытие счетов) — это **цепочки REST API**, объединённые в бизнес-процессы.  
Но их тестирование остаётся **ручным, хрупким и неэффективным**:

- Тестировщики пишут кастомные скрипты под каждый сценарий.
- Изменение одного эндпоинта — крах всей цепочки.
- Нет визуального понимания: кто вызывает кого, какие данные передаются.
- Генерация тестовых данных — «по памяти», с ошибками.

**Результат**: баги в продакшене, потеря доверия клиентов, рост стоимости поддержки.

---

## 🚀 Решение: APIOrchestra

**APIOrchestra** — веб-приложение на Java (Spring Boot) с интеграцией Python-скриптов, которое **автомоматически тестирует сложные бизнес-процессы** на основе:

- **BPMN 2.0** — диаграммы процессов (например: «Оформление кредита»)
- **OpenAPI 3.0+** — спецификаций API-сервисов

> ✅ **Никакого кода. Только диаграммы. Только кнопка «Запустить».**

---


api-orchestra-complete/
├── src/
│ ├── main/
│ │ ├── java/
│ │ │ └── com/apiorchestra/Application.java
│ │ └── resources/
│ │ ├── application.yml
│ │ ├── openapi.yaml
│ │ └── process.bpmn
│ └── python/
│ └── virtual_bank_orchestrator.py
├── pom.xml
├── target/
│ └── api-orchestra-1.0.0.jar
└── docs/
├── video-script.md
└── presentation.pdf


---

## 🛠️ Как запустить (одним кликом)

### 🔧 Скопируй и запусти этот полный набор файлов

<details>
<summary>📋 Нажми, чтобы скопировать всё — Java + Python + конфиги</summary>

```bash
# Создаём папку проекта
mkdir -p ~/api-orchestra && cd ~/api-orchestra

# Создаём pom.xml
cat > pom.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.apiorchestra</groupId>
    <artifactId>api-orchestra</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <spring.boot.version>3.2.0</spring.boot.version>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-dependencies</artifactId>
                <version>${spring.boot.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <dependencies>
        <!-- Spring Boot Starter Web -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <!-- Lombok -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <scope>provided</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <executions>
                    <execution>
                        <goals>
                            <goal>repackage</goal>
                        </goals>
                        <configuration>
                            <mainClass>com.apiorchestra.Application</mainClass>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
EOF

# Создаём Application.java
mkdir -p src/main/java/com/apiorchestra
cat > src/main/java/com/apiorchestra/Application.java << 'EOF'
package com.apiorchestra;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.*;
import java.util.Map;

@SpringBootApplication
@RestController
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @PostMapping("/api/run-test")
    public Map<String, Object> runTest(
            @RequestParam("bpmn") MultipartFile bpmnFile,
            @RequestParam("openapi") MultipartFile openApiFile) {

        try {
            File tempBpmn = File.createTempFile("bpmn_", ".bpmn");
            bpmnFile.transferTo(tempBpmn);

            File tempOpenApi = File.createTempFile("openapi_", ".yaml");
            openApiFile.transferTo(tempOpenApi);

            ProcessBuilder pb = new ProcessBuilder("python3", "virtual_bank_orchestrator.py");
            pb.environment().put("BPMN_PATH", tempBpmn.getAbsolutePath());
            pb.environment().put("OPENAPI_PATH", tempOpenApi.getAbsolutePath());

            Process process = pb.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder output = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }

            int exitCode = process.waitFor();

            return Map.of(
                    "status", "completed",
                    "exit_code", exitCode,
                    "output", output.toString()
            );

        } catch (Exception e) {
            e.printStackTrace();
            return Map.of(
                    "status", "error",
                    "message", e.getMessage()
            );
        }
    }
}
EOF

# Создаём application.yml
mkdir -p src/main/resources
cat > src/main/resources/application.yml << 'EOF'
server:
  port: 8080

logging:
  level:
    com.apiorchestra: DEBUG
    org.springframework.web: INFO
EOF

# Создаём openapi.yaml
cat > src/main/resources/openapi.yaml << 'EOF'
openapi: 3.0.3
info:
  title: Virtual Bank API
  version: 2.0
  description: API Виртуального банка для хакатона "Оркестр"
servers:
  - url: https://vbank.open.bankingapi.ru
    description: Sandbox environment

paths:
  /auth/bank-token:
    post:
      summary: Получить токен доступа
      parameters:
        - name: client_id
          in: query
          required: true
          schema:
            type: string
            example: team111@app.hackaton.bankingapi.ru
        - name: client_secret
          in: query
          required: true
          schema:
            type: string
            example: Ib6tWUSQspi5YTLzkvSrTo18x0I2Wdq3
      responses:
        '200':
          description: Успешный ответ
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                  token_type:
                    type: string
                  expires_in:
                    type: integer

  /account-consents/request:
    post:
      summary: Создать согласие на доступ к счетам
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                client_id:
                  type: string
                  example: team111-01
                permissions:
                  type: array
                  items:
                    type: string
                  example: ["accounts", "balances", "transactions"]
                expire_time:
                  type: string
                  format: date-time
                  example: "2026-11-08T12:00:00Z"
      responses:
        '201':
          description: Успешно создано
          content:
            application/json:
              schema:
                type: object
                properties:
                  consent_id:
                    type: string
                    example: "consent-12345"

  /accounts:
    get:
      summary: Получить список счетов
      parameters:
        - name: X-Consent-ID
          in: header
          required: true
          schema:
            type: string
            example: consent-12345
      responses:
        '200':
          description: Список счетов
          content:
            application/json:
              schema:
                type: object
                properties:
                  accounts:
                    type: array
                    items:
                      type: object
                      properties:
                        account_id:
                          type: string
                        account_number:
                          type: string
                        currency:
                          type: string
                        status:
                          type: string
                        allowed_operations:
                          type: array
                          items:
                            type: string

  /payments:
    post:
      summary: Инициировать платеж
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                payment_id:
                  type: string
                  example: "pay-67890"
                amount:
                  type: string
                  example: "100.00"
                currency:
                  type: string
                  example: "RUB"
                consent_id:
                  type: string
                  example: "consent-12

## 📁 Структура проекта
