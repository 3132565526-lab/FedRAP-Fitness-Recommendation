package com.fedrap.fitness.controller;

import com.fedrap.fitness.model.dto.ApiResponse;
import com.fedrap.fitness.model.dto.RecommendationItem;
import com.fedrap.fitness.model.dto.RecommendationRequest;
import com.fedrap.fitness.service.RecommendationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 推荐控制器
 */
@RestController
@RequestMapping("/recommendations")
public class RecommendationController {

    @Autowired
    private RecommendationService recommendationService;

    /**
     * 获取个性化推荐
     */
    @PostMapping
    public ResponseEntity<ApiResponse<List<RecommendationItem>>> getRecommendations(
            @RequestBody RecommendationRequest request) {
        try {
            List<RecommendationItem> recommendations = 
                    recommendationService.getRecommendations(request);
            return ResponseEntity.ok(ApiResponse.success(recommendations));
        } catch (Exception e) {
            return ResponseEntity.badRequest()
                    .body(ApiResponse.error(e.getMessage()));
        }
    }

    /**
     * 获取用户推荐（简化接口）
     */
    @GetMapping("/user/{userId}")
    public ResponseEntity<ApiResponse<List<RecommendationItem>>> getUserRecommendations(
            @PathVariable Long userId,
            @RequestParam(defaultValue = "10") Integer topK) {
        try {
            RecommendationRequest request = new RecommendationRequest();
            request.setUserId(userId);
            request.setTopK(topK);
            
            List<RecommendationItem> recommendations = 
                    recommendationService.getRecommendations(request);
            return ResponseEntity.ok(ApiResponse.success(recommendations));
        } catch (Exception e) {
            return ResponseEntity.badRequest()
                    .body(ApiResponse.error(e.getMessage()));
        }
    }
}
