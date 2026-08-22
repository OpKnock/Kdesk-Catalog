---
name: "spring"
description: "Spring Boot Java development. Real mvn/gradle CLI."
type: knowledge
triggers: ["spring"]
---

# spring

Spring Boot Java development. Real mvn/gradle CLI.

## Instructions

# Spring Boot

Spring Boot development using real CLI.

## When to Use

- Enterprise Java apps
- Microservices
- REST APIs

## Commands

```bash
# Create project (Maven)
mvn spring-boot:run

# Create project (Gradle)
./gradlew bootRun

# Build
mvn clean package
./gradlew build

# Run tests
mvn test
./gradlew test

# Run specific test
mvn test -Dtest=UserServiceTest

# Package
mvn package -DskipTests
```

## Application

```java
// src/main/java/com/example/DemoApplication.java
@SpringBootApplication
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}
```

## Controller

```java
// src/main/java/com/example/UserController.java
@RestController
@RequestMapping("/users")
public class UserController {
    
    @Autowired
    private UserService userService;
    
    @GetMapping
    public List<User> getAll() {
        return userService.findAll();
    }
    
    @GetMapping("/{id}")
    public User getById(@PathVariable Long id) {
        return userService.findById(id);
    }
    
    @PostMapping
    public User create(@RequestBody User user) {
        return userService.save(user);
    }
    
    @PutMapping("/{id}")
    public User update(@PathVariable Long id, @RequestBody User user) {
        return userService.update(id, user);
    }
    
    @DeleteMapping("/{id}")
    public void delete(@PathVariable Long id) {
        userService.delete(id);
    }
}
```

## Entity

```java
// src/main/java/com/example/User.java
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String name;
    
    @Column(nullable = false, unique = true)
    private String email;
    
    // getters and setters
}
```

## Repository

```java
// src/main/java/com/example/UserRepository.java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    List<User> findByNameContaining(String name);
}
```

## Service

```java
// src/main/java/com/example/UserService.java
@Service
@Transactional
public class UserService {
    
    @Autowired
    private UserRepository userRepository;
    
    public List<User> findAll() {
        return userRepository.findAll();
    }
    
    public User findById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));
    }
    
    public User save(User user) {
        return userRepository.save(user);
    }
}
```

## application.properties

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/mydb
spring.datasource.username=root
spring.datasource.password=password
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
```

## Capabilities

### spring
Spring Boot Java development. Real mvn/gradle CLI.

**Commands:**
- `mvn spring-boot:run`
- `./gradlew bootRun`
- `mvn clean package`
- `./gradlew build`
- `mvn test`
- `./gradlew test`
- `mvn test -Dtest=UserServiceTest`
- `mvn package -DskipTests`

**Examples:**
- mvn spring-boot:run
- ./gradlew bootRun
- mvn clean package
