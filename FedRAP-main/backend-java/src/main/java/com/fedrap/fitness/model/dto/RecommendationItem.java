package com.fedrap.fitness.model.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 推荐结果项DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class RecommendationItem {
    private Long exerciseId;
    private String exerciseName;
    private String description;
    private String category;
    private String targetMuscle;
    private String equipment;
    private Double difficulty;
    private Double intensity;
    private Double score; // 推荐分数
    private Integer recommendedSets;
    private Integer recommendedReps;
    private Integer recommendedDuration;
    private String imageUrl;
    private String videoUrl;
}
