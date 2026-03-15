package com.fedrap.fitness;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

/**
 * FedRAP 健身推荐系统主应用
 * 基于Spring Boot + 联邦学习的个性化健身计划推荐平台
 * 
 * @author FedRAP Team
 * @version 1.0.0
 */
@SpringBootApplication
@EnableJpaAuditing
public class FitnessRecommendationApplication {

    public static void main(String[] args) {
        SpringApplication.run(FitnessRecommendationApplication.class, args);
        System.out.println("===========================================");
        System.out.println("FedRAP 健身推荐系统启动成功!");
        System.out.println("API 地址: http://localhost:8080/api");
        System.out.println("H2 控制台: http://localhost:8080/api/h2-console");
        System.out.println("===========================================");
    }
}
