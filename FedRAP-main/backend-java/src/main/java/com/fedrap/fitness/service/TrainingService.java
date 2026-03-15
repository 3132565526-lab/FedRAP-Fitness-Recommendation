package com.fedrap.fitness.service;

import com.fedrap.fitness.model.dto.TrainingRecordRequest;
import com.fedrap.fitness.model.entity.Exercise;
import com.fedrap.fitness.model.entity.TrainingHistory;
import com.fedrap.fitness.model.entity.User;
import com.fedrap.fitness.repository.ExerciseRepository;
import com.fedrap.fitness.repository.TrainingHistoryRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 训练历史服务
 */
@Service
public class TrainingService {

    @Autowired
    private TrainingHistoryRepository trainingHistoryRepository;

    @Autowired
    private ExerciseRepository exerciseRepository;

    @Autowired
    private UserService userService;

    @Autowired
    private WorkoutPlanService workoutPlanService;

    /**
     * 记录训练
     */
    @Transactional
    public TrainingHistory recordTraining(TrainingRecordRequest request) {
        User user = userService.getUserById(request.getUserId());
        Exercise exercise = exerciseRepository.findById(request.getExerciseId())
                .orElseThrow(() -> new RuntimeException("动作不存在"));

        TrainingHistory history = new TrainingHistory();
        history.setUser(user);
        history.setExercise(exercise);
        history.setDuration(request.getDuration());
        history.setSets(request.getSets());
        history.setReps(request.getReps());
        history.setWeight(request.getWeight());
        history.setRating(request.getRating());
        history.setFatigueLevel(request.getFatigueLevel());
        history.setDifficultyFeedback(request.getDifficultyFeedback());
        history.setNotes(request.getNotes());
        history.setCaloriesBurned(request.getCaloriesBurned());
        history.setHeartRateAvg(request.getHeartRateAvg());
        history.setHeartRateMax(request.getHeartRateMax());
        history.setCompleted(true);

        TrainingHistory saved = trainingHistoryRepository.save(history);

        // 更新用户经验值和训练次数
        int expGained = calculateExperience(request);
        userService.addExperience(request.getUserId(), expGained);
        userService.incrementWorkoutCount(request.getUserId());

        // 训练完成后，从当前有效训练计划中自动移除该动作
        workoutPlanService.removeExerciseFromActivePlan(request.getUserId(), request.getExerciseId());

        return saved;
    }

    /**
     * 获取用户训练历史
     */
    public List<TrainingHistory> getUserTrainingHistory(Long userId) {
        return trainingHistoryRepository.findByUserIdOrderByTrainingDateDesc(userId);
    }

    /**
     * 获取用户训练统计
     */
    public Map<String, Object> getUserTrainingStats(Long userId) {
        Long totalWorkouts = trainingHistoryRepository.countCompletedWorkoutsByUserId(userId);
        Long totalCalories = trainingHistoryRepository.sumCaloriesByUserId(userId);

        Map<String, Object> stats = new HashMap<>();
        stats.put("totalWorkouts", totalWorkouts != null ? totalWorkouts : 0);
        stats.put("totalCalories", totalCalories != null ? totalCalories : 0);
        stats.put("recentHistory", trainingHistoryRepository
                .findByUserIdOrderByTrainingDateDesc(userId)
                .stream()
                .limit(10)
                .collect(java.util.stream.Collectors.toList()));

        return stats;
    }

    /**
     * 计算训练获得的经验值
     */
    private int calculateExperience(TrainingRecordRequest request) {
        int baseExp = 10;
        
        // 时长奖励
        if (request.getDuration() != null) {
            baseExp += request.getDuration() / 10;
        }
        
        // 完成度奖励
        if (request.getRating() != null && request.getRating() >= 4) {
            baseExp += 5;
        }
        
        return baseExp;
    }
}
