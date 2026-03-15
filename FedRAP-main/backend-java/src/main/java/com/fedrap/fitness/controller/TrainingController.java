package com.fedrap.fitness.controller;

import com.fedrap.fitness.model.dto.ApiResponse;
import com.fedrap.fitness.model.dto.TrainingRecordRequest;
import com.fedrap.fitness.model.entity.TrainingHistory;
import com.fedrap.fitness.service.TrainingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

/**
 * 训练历史控制器
 */
@RestController
@RequestMapping("/training")
public class TrainingController {

    @Autowired
    private TrainingService trainingService;

    /**
     * 记录训练
     */
    @PostMapping("/record")
    public ResponseEntity<ApiResponse<TrainingHistory>> recordTraining(
            @RequestBody TrainingRecordRequest request) {
        try {
            TrainingHistory history = trainingService.recordTraining(request);
            return ResponseEntity.ok(ApiResponse.success("训练记录成功", history));
        } catch (Exception e) {
            return ResponseEntity.badRequest()
                    .body(ApiResponse.error(e.getMessage()));
        }
    }

    /**
     * 获取用户训练历史
     */
    @GetMapping("/history/{userId}")
    public ResponseEntity<ApiResponse<List<TrainingHistory>>> getTrainingHistory(
            @PathVariable Long userId) {
        try {
            List<TrainingHistory> history = trainingService.getUserTrainingHistory(userId);
            return ResponseEntity.ok(ApiResponse.success(history));
        } catch (Exception e) {
            return ResponseEntity.badRequest()
                    .body(ApiResponse.error(e.getMessage()));
        }
    }

    /**
     * 获取用户训练统计
     */
    @GetMapping("/stats/{userId}")
    public ResponseEntity<ApiResponse<Map<String, Object>>> getTrainingStats(
            @PathVariable Long userId) {
        try {
            Map<String, Object> stats = trainingService.getUserTrainingStats(userId);
            return ResponseEntity.ok(ApiResponse.success(stats));
        } catch (Exception e) {
            return ResponseEntity.badRequest()
                    .body(ApiResponse.error(e.getMessage()));
        }
    }
}
