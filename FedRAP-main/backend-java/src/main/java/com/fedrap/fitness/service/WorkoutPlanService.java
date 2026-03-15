package com.fedrap.fitness.service;

import com.fedrap.fitness.model.dto.WorkoutPlanItemRequest;
import com.fedrap.fitness.model.entity.Exercise;
import com.fedrap.fitness.model.entity.User;
import com.fedrap.fitness.model.entity.WorkoutPlan;
import com.fedrap.fitness.model.entity.WorkoutPlan.PlanExerciseItem;
import com.fedrap.fitness.repository.ExerciseRepository;
import com.fedrap.fitness.repository.WorkoutPlanRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * 训练计划服务
 */
@Service
public class WorkoutPlanService {

    @Autowired
    private WorkoutPlanRepository workoutPlanRepository;

    @Autowired
    private ExerciseRepository exerciseRepository;

    @Autowired
    private UserService userService;

    /**
     * 获取用户当前有效训练计划
     */
    public WorkoutPlan getActivePlan(Long userId) {
        List<WorkoutPlan> activePlans = workoutPlanRepository
                .findByUserIdAndIsCompletedFalseAndIsActiveTrue(userId);
        return activePlans.isEmpty() ? null : activePlans.get(0);
    }

    /**
     * 向训练计划添加动作
     */
    @Transactional
    public WorkoutPlan addExerciseToPlan(WorkoutPlanItemRequest request) {
        if (request.getUserId() == null || request.getExerciseId() == null) {
            throw new RuntimeException("用户或动作不能为空");
        }

        User user = userService.getUserById(request.getUserId());
        Exercise exercise = exerciseRepository.findById(request.getExerciseId())
                .orElseThrow(() -> new RuntimeException("动作不存在"));

        WorkoutPlan plan = ensureActivePlan(user);
        List<PlanExerciseItem> items = plan.getExercises();
        if (items == null) {
            items = new ArrayList<>();
        }

        Optional<PlanExerciseItem> existing = items.stream()
                .filter(item -> request.getExerciseId().equals(item.getExerciseId()))
                .findFirst();

        if (existing.isPresent()) {
            PlanExerciseItem item = existing.get();
            if (request.getSets() != null) {
                item.setSets(request.getSets());
            }
            if (request.getReps() != null) {
                item.setReps(request.getReps());
            }
            if (request.getDuration() != null) {
                item.setDuration(request.getDuration());
            }
        } else {
            PlanExerciseItem item = new PlanExerciseItem();
            item.setExerciseId(exercise.getId());
            item.setExerciseName(exercise.getName());
            item.setSets(request.getSets() != null ? request.getSets() : exercise.getRecommendedSets());
            item.setReps(request.getReps() != null ? request.getReps() : exercise.getRecommendedReps());
            item.setDuration(request.getDuration() != null ? request.getDuration() : exercise.getRecommendedDuration());
            item.setOrderIndex(items.size() + 1);
            items.add(item);
        }

        plan.setExercises(items);
        recalcTotals(plan);
        return workoutPlanRepository.save(plan);
    }

    /**
     * 从训练计划移除动作
     */
    @Transactional
    public WorkoutPlan removeExerciseFromPlan(Long planId, Long exerciseId, Long userId) {
        WorkoutPlan plan = workoutPlanRepository.findById(planId)
                .orElseThrow(() -> new RuntimeException("训练计划不存在"));

        if (userId != null && !userId.equals(plan.getUser().getId())) {
            throw new RuntimeException("无权限操作该训练计划");
        }

        List<PlanExerciseItem> items = plan.getExercises();
        if (items != null) {
            items = items.stream()
                    .filter(item -> !exerciseId.equals(item.getExerciseId()))
                    .collect(Collectors.toList());

            for (int i = 0; i < items.size(); i++) {
                items.get(i).setOrderIndex(i + 1);
            }
        }

        plan.setExercises(items);
        recalcTotals(plan);
        return workoutPlanRepository.save(plan);
    }

    /**
     * 从用户当前有效计划中移除指定动作（用于训练完成后自动移除）
     */
    @Transactional
    public void removeExerciseFromActivePlan(Long userId, Long exerciseId) {
        if (userId == null || exerciseId == null) {
            return;
        }

        WorkoutPlan activePlan = getActivePlan(userId);
        if (activePlan == null || activePlan.getExercises() == null || activePlan.getExercises().isEmpty()) {
            return;
        }

        List<PlanExerciseItem> items = activePlan.getExercises().stream()
                .filter(item -> !exerciseId.equals(item.getExerciseId()))
                .collect(Collectors.toList());

        if (items.size() == activePlan.getExercises().size()) {
            // 计划中没有该动作，无需保存
            return;
        }

        for (int i = 0; i < items.size(); i++) {
            items.get(i).setOrderIndex(i + 1);
        }

        activePlan.setExercises(items);
        recalcTotals(activePlan);
        workoutPlanRepository.save(activePlan);
    }

    private WorkoutPlan ensureActivePlan(User user) {
        WorkoutPlan activePlan = getActivePlan(user.getId());
        if (activePlan != null) {
            return activePlan;
        }

        WorkoutPlan plan = new WorkoutPlan();
        plan.setUser(user);
        plan.setPlanName("个人训练计划");
        plan.setDescription("个人自选训练计划");
        plan.setIsActive(true);
        plan.setIsCompleted(false);
        plan.setExercises(new ArrayList<>());
        recalcTotals(plan);
        return workoutPlanRepository.save(plan);
    }

    private void recalcTotals(WorkoutPlan plan) {
        List<PlanExerciseItem> items = plan.getExercises();
        if (items == null || items.isEmpty()) {
            plan.setTotalDuration(0);
            plan.setEstimatedCalories(0);
            return;
        }

        List<Long> exerciseIds = items.stream()
                .map(PlanExerciseItem::getExerciseId)
                .collect(Collectors.toList());

        Map<Long, Exercise> exerciseMap = new HashMap<>();
        exerciseRepository.findAllById(exerciseIds)
                .forEach(exercise -> exerciseMap.put(exercise.getId(), exercise));

        int totalDuration = 0;
        int estimatedCalories = 0;

        for (PlanExerciseItem item : items) {
            int duration = item.getDuration() != null ? item.getDuration() : 0;
            totalDuration += duration;

            Exercise exercise = exerciseMap.get(item.getExerciseId());
            if (exercise != null && exercise.getCaloriesPerMinute() != null) {
                estimatedCalories += duration * exercise.getCaloriesPerMinute();
            }
        }

        plan.setTotalDuration(totalDuration);
        plan.setEstimatedCalories(estimatedCalories);
    }
}
