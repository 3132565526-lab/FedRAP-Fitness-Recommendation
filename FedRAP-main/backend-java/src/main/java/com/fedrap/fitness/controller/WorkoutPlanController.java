package com.fedrap.fitness.controller;

import com.fedrap.fitness.model.dto.ApiResponse;
import com.fedrap.fitness.model.dto.WorkoutPlanItemRequest;
import com.fedrap.fitness.model.entity.WorkoutPlan;
import com.fedrap.fitness.service.WorkoutPlanService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * 训练计划控制器
 */
@RestController
@RequestMapping("/plans")
public class WorkoutPlanController {

    @Autowired
    private WorkoutPlanService workoutPlanService;

    /**
     * 获取用户当前训练计划
     */
    @GetMapping("/active/{userId}")
    public ResponseEntity<ApiResponse<WorkoutPlan>> getActivePlan(@PathVariable Long userId) {
        try {
            WorkoutPlan plan = workoutPlanService.getActivePlan(userId);
            return ResponseEntity.ok(ApiResponse.success(plan));
        } catch (Exception e) {
            return ResponseEntity.badRequest()
                    .body(ApiResponse.error(e.getMessage()));
        }
    }

    /**
     * 加入训练计划
     */
    @PostMapping("/items")
    public ResponseEntity<ApiResponse<WorkoutPlan>> addPlanItem(
            @RequestBody WorkoutPlanItemRequest request) {
        try {
            WorkoutPlan plan = workoutPlanService.addExerciseToPlan(request);
            return ResponseEntity.ok(ApiResponse.success("已加入训练计划", plan));
        } catch (Exception e) {
            return ResponseEntity.badRequest()
                    .body(ApiResponse.error(e.getMessage()));
        }
    }

    /**
     * 移除训练计划条目
     */
    @DeleteMapping("/{planId}/items/{exerciseId}")
    public ResponseEntity<ApiResponse<WorkoutPlan>> removePlanItem(
            @PathVariable Long planId,
            @PathVariable Long exerciseId,
            @RequestParam(required = false) Long userId) {
        try {
            WorkoutPlan plan = workoutPlanService.removeExerciseFromPlan(planId, exerciseId, userId);
            return ResponseEntity.ok(ApiResponse.success("已移除训练计划条目", plan));
        } catch (Exception e) {
            return ResponseEntity.badRequest()
                    .body(ApiResponse.error(e.getMessage()));
        }
    }
}
