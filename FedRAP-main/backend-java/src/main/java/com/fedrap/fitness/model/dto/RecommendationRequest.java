package com.fedrap.fitness.model.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * 推荐请求DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class RecommendationRequest {
    private Long userId;
    private Integer topK = 10; // 推荐数量
    private String difficulty; // 难度过滤
    private String category; // 类别过滤
    private List<Long> excludeExerciseIds; // 排除的动作ID
}
