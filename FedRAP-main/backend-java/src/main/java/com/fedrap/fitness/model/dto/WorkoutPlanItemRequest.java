package com.fedrap.fitness.model.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 训练计划条目请求
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class WorkoutPlanItemRequest {

    private Long userId;
    private Long exerciseId;
    private Integer sets;
    private Integer reps;
    private Integer duration;
}
