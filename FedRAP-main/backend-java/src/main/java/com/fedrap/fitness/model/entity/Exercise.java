package com.fedrap.fitness.model.entity;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 健身动作实体类
 */
@Entity
@Table(name = "exercises")
@Data
@NoArgsConstructor
@AllArgsConstructor
@JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})
public class Exercise {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String name;

    @Column(length = 1000)
    private String description;

    private String category; // 类别: STRENGTH, CARDIO, FLEXIBILITY, BALANCE
    private String targetMuscle; // 目标肌群
    private String equipment; // 所需器材

    // 难度和强度
    private Double difficulty; // 0.0-1.0
    private Double intensity; // 0.0-1.0
    private Integer caloriesPerMinute; // 每分钟消耗卡路里

    // 适用目标
    private Double suitabilityWeightLoss; // 0.0-1.0
    private Double suitabilityMuscleGain;
    private Double suitabilityEndurance;
    private Double suitabilityFlexibility;

    // 推荐时长
    private Integer recommendedDuration; // 分钟
    private Integer recommendedSets; // 组数
    private Integer recommendedReps; // 每组次数

    // 视频和图片资源
    private String videoUrl;
    private String imageUrl;

    @Column(length = 2000)
    private String instructions; // 动作要领

    private Boolean isActive = true;
}
