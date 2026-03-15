package com.fedrap.fitness.model.entity;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDateTime;

/**
 * 用户实体类
 */
@Entity
@Table(name = "users")
@Data
@NoArgsConstructor
@AllArgsConstructor
@EntityListeners(AuditingEntityListener.class)
@JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 50)
    private String username;

    @Column(nullable = false, unique = true, length = 100)
    private String email;

    @Column(nullable = false)
    private String password;

    // 个人基本信息
    private Integer age;
    private Double weight; // kg
    private Double height; // cm
    private Double bmi;
    private Integer heartRate;
    private String gender; // MALE, FEMALE, OTHER

    // 健身等级和经验
    private Double fitnessLevel; // 0.0-1.0
    private Integer experienceYears;
    private Integer weeklyFrequency; // 每周训练频率
    private Integer avgSessionDuration; // 平均训练时长(分钟)

    // 健身目标 (0.0-1.0)
    private Double goalWeightLoss;
    private Double goalMuscleGain;
    private Double goalEndurance;
    private Double goalFlexibility;

    // 身体维度数据 (cm)
    private Double chest;
    private Double waist;
    private Double hips;
    private Double leftArm;
    private Double rightArm;
    private Double leftThigh;
    private Double rightThigh;

    // 等级系统
    private Integer level = 1;
    private Integer experience = 0;
    private Integer totalWorkouts = 0;

    // 账号状态
    @Column(nullable = false)
    private Boolean enabled = true;

    @Column(nullable = false)
    private String role = "USER"; // USER, TRAINER, ADMIN

    @CreatedDate
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    private LocalDateTime updatedAt;
}
