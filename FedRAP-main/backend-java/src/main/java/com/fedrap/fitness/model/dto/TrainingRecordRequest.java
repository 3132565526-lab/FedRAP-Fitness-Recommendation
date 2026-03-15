package com.fedrap.fitness.model.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 训练记录请求DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class TrainingRecordRequest {
    private Long userId;
    private Long exerciseId;
    private Integer duration;
    private Integer sets;
    private Integer reps;
    private Double weight;
    private Integer rating;
    private Double fatigueLevel;
    private Double difficultyFeedback;
    private String notes;
    private Integer caloriesBurned;
    private Integer heartRateAvg;
    private Integer heartRateMax;
}
