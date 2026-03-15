package com.fedrap.fitness.controller;

import com.fedrap.fitness.model.dto.ApiResponse;
import com.fedrap.fitness.model.entity.Exercise;
import com.fedrap.fitness.repository.ExerciseRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 健身动作控制器
 */
@RestController
@RequestMapping("/exercises")
public class ExerciseController {

    @Autowired
    private ExerciseRepository exerciseRepository;

    /**
     * 获取所有活跃动作
     */
    @GetMapping("/list")
    public ResponseEntity<ApiResponse<List<Exercise>>> getAllExercises() {
        try {
            List<Exercise> exercises = exerciseRepository.findByIsActiveTrue();
            return ResponseEntity.ok(ApiResponse.success(exercises));
        } catch (Exception e) {
            return ResponseEntity.badRequest()
                    .body(ApiResponse.error(e.getMessage()));
        }
    }

    /**
     * 根据ID获取动作
     */
    @GetMapping("/{exerciseId}")
    public ResponseEntity<ApiResponse<Exercise>> getExerciseById(@PathVariable Long exerciseId) {
        try {
            Exercise exercise = exerciseRepository.findById(exerciseId)
                    .orElseThrow(() -> new RuntimeException("动作不存在"));
            return ResponseEntity.ok(ApiResponse.success(exercise));
        } catch (Exception e) {
            return ResponseEntity.badRequest()
                    .body(ApiResponse.error(e.getMessage()));
        }
    }

    /**
     * 按类别获取动作
     */
    @GetMapping("/category/{category}")
    public ResponseEntity<ApiResponse<List<Exercise>>> getExercisesByCategory(
            @PathVariable String category) {
        try {
            List<Exercise> exercises = exerciseRepository.findByCategoryAndIsActiveTrue(category);
            return ResponseEntity.ok(ApiResponse.success(exercises));
        } catch (Exception e) {
            return ResponseEntity.badRequest()
                    .body(ApiResponse.error(e.getMessage()));
        }
    }
}
