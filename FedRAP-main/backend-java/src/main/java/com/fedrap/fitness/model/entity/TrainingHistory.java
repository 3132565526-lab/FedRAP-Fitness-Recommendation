package com.fedrap.fitness.model.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDateTime;

/**
 * 训练历史记录实体类
 */
@Entity
@Table(name = "training_history")
@Data
@NoArgsConstructor
@AllArgsConstructor
@EntityListeners(AuditingEntityListener.class)
@JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})
public class TrainingHistory {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    @JsonIgnore
    private User user;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "exercise_id", nullable = false)
    @JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})
    private Exercise exercise;

    // 训练详情
    private Integer duration; // 实际训练时长(分钟)
    private Integer sets; // 完成组数
    private Integer reps; // 每组次数
    private Double weight; // 使用重量(kg)

    // 训练反馈
    private Integer rating; // 评分 1-5
    private Double fatigueLevel; // 疲劳度 0.0-1.0
    private Double difficultyFeedback; // 难度反馈 0.0-1.0
    private String notes; // 训练备注

    // 训练效果
    private Integer caloriesBurned; // 消耗卡路里
    private Integer heartRateAvg; // 平均心率
    private Integer heartRateMax; // 最大心率

    private Boolean completed = true; // 是否完成

    @CreatedDate
    @Column(nullable = false, updatable = false)
    private LocalDateTime trainingDate;
}
