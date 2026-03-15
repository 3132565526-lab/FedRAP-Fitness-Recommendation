package com.fedrap.fitness.model.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 用户资料更新DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class UserProfileUpdateRequest {
    private Integer age;
    private Double weight;
    private Double height;
    private Integer heartRate;
    private String gender;

    private Double fitnessLevel;
    private Integer experienceYears;
    private Integer weeklyFrequency;
    private Integer avgSessionDuration;

    private Double goalWeightLoss;
    private Double goalMuscleGain;
    private Double goalEndurance;
    private Double goalFlexibility;

    private Double chest;
    private Double waist;
    private Double hips;
    private Double leftArm;
    private Double rightArm;
    private Double leftThigh;
    private Double rightThigh;
}
