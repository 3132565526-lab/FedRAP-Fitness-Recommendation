package com.fedrap.fitness.service;

import com.fedrap.fitness.model.dto.RecommendationItem;
import com.fedrap.fitness.model.dto.RecommendationRequest;
import com.fedrap.fitness.model.entity.Exercise;
import com.fedrap.fitness.model.entity.TrainingHistory;
import com.fedrap.fitness.model.entity.User;
import com.fedrap.fitness.repository.ExerciseRepository;
import com.fedrap.fitness.repository.TrainingHistoryRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.stream.Collectors;

/**
 * 智能推荐服务
 * 基于用户画像和训练历史的个性化推荐算法
 */
@Service
public class RecommendationService {

    @Autowired
    private ExerciseRepository exerciseRepository;

    @Autowired
    private TrainingHistoryRepository trainingHistoryRepository;

    @Autowired
    private UserService userService;

    @Autowired
    private ModelInferenceService modelInferenceService;

    /**
     * 生成个性化推荐
     */
    public List<RecommendationItem> getRecommendations(RecommendationRequest request) {
        User user = userService.getUserById(request.getUserId());
        
        // 尝试使用训练好的模型
        List<RecommendationItem> modelRecommendations = modelInferenceService.getModelRecommendations(
            user, request.getTopK()
        );
        
        // 如果模型推荐成功且有结果，使用模型推荐
        if (!modelRecommendations.isEmpty()) {
            // 补充完整的动作信息
            for (RecommendationItem item : modelRecommendations) {
                exerciseRepository.findById(item.getExerciseId()).ifPresent(exercise -> {
                    item.setExerciseName(exercise.getName());
                    item.setDescription(exercise.getDescription());
                    item.setCategory(exercise.getCategory());
                    item.setTargetMuscle(exercise.getTargetMuscle());
                    item.setEquipment(exercise.getEquipment());
                    item.setDifficulty(exercise.getDifficulty());
                    item.setIntensity(exercise.getIntensity());
                    item.setRecommendedSets(exercise.getRecommendedSets());
                    item.setRecommendedReps(exercise.getRecommendedReps());
                    item.setRecommendedDuration(exercise.getRecommendedDuration());
                    item.setImageUrl(exercise.getImageUrl());
                    item.setVideoUrl(exercise.getVideoUrl());
                });
            }
            return modelRecommendations;
        }
        
        // 否则使用规则推荐算法
        List<Exercise> allExercises = exerciseRepository.findByIsActiveTrue();

        // 获取用户训练历史
        List<TrainingHistory> history = trainingHistoryRepository
                .findByUserIdOrderByTrainingDateDesc(request.getUserId());

        // 过滤条件
        List<Exercise> filteredExercises = filterExercises(allExercises, request);

        // 计算推荐分数
        List<RecommendationItem> recommendations = new ArrayList<>();
        for (Exercise exercise : filteredExercises) {
            double score = calculateRecommendationScore(exercise, user, history);
            
            RecommendationItem item = new RecommendationItem();
            item.setExerciseId(exercise.getId());
            item.setExerciseName(exercise.getName());
            item.setCategory(exercise.getCategory());
            item.setTargetMuscle(exercise.getTargetMuscle());
            item.setDifficulty(exercise.getDifficulty());
            item.setIntensity(exercise.getIntensity());
            item.setScore(score);
            item.setRecommendedSets(exercise.getRecommendedSets());
            item.setRecommendedReps(exercise.getRecommendedReps());
            item.setRecommendedDuration(exercise.getRecommendedDuration());
            item.setImageUrl(exercise.getImageUrl());
            item.setVideoUrl(exercise.getVideoUrl());
            
            recommendations.add(item);
        }

        // 按分数排序并返回TopK
        return recommendations.stream()
                .sorted((a, b) -> Double.compare(b.getScore(), a.getScore()))
                .limit(request.getTopK())
                .collect(Collectors.toList());
    }

    /**
     * 过滤动作
     */
    private List<Exercise> filterExercises(List<Exercise> exercises, RecommendationRequest request) {
        return exercises.stream()
                .filter(e -> {
                    // 排除指定动作
                    if (request.getExcludeExerciseIds() != null && 
                        request.getExcludeExerciseIds().contains(e.getId())) {
                        return false;
                    }
                    
                    // 类别过滤
                    if (request.getCategory() != null && 
                        !request.getCategory().equals(e.getCategory())) {
                        return false;
                    }
                    
                    return true;
                })
                .collect(Collectors.toList());
    }

    /**
     * 计算推荐分数
     * 综合考虑：用户目标匹配度、难度适配、训练历史、多样性
     */
    private double calculateRecommendationScore(Exercise exercise, User user, List<TrainingHistory> history) {
        double score = 0.0;

        // 1. 用户目标匹配度 (权重: 40%)
        double goalMatch = calculateGoalMatch(exercise, user);
        score += goalMatch * 0.4;

        // 2. 难度适配度 (权重: 25%)
        double difficultyMatch = calculateDifficultyMatch(exercise, user);
        score += difficultyMatch * 0.25;

        // 3. 训练历史偏好 (权重: 20%)
        double historyPreference = calculateHistoryPreference(exercise, history);
        score += historyPreference * 0.2;

        // 4. 多样性奖励 (权重: 15%)
        double diversityBonus = calculateDiversityBonus(exercise, history);
        score += diversityBonus * 0.15;

        return score;
    }

    /**
     * 计算目标匹配度
     */
    private double calculateGoalMatch(Exercise exercise, User user) {
        double match = 0.0;

        // 减脂目标
        if (user.getGoalWeightLoss() != null && exercise.getSuitabilityWeightLoss() != null) {
            match += user.getGoalWeightLoss() * exercise.getSuitabilityWeightLoss();
        }

        // 增肌目标
        if (user.getGoalMuscleGain() != null && exercise.getSuitabilityMuscleGain() != null) {
            match += user.getGoalMuscleGain() * exercise.getSuitabilityMuscleGain();
        }

        // 耐力目标
        if (user.getGoalEndurance() != null && exercise.getSuitabilityEndurance() != null) {
            match += user.getGoalEndurance() * exercise.getSuitabilityEndurance();
        }

        // 柔韧性目标
        if (user.getGoalFlexibility() != null && exercise.getSuitabilityFlexibility() != null) {
            match += user.getGoalFlexibility() * exercise.getSuitabilityFlexibility();
        }

        return Math.min(match, 1.0); // 归一化到[0,1]
    }

    /**
     * 计算难度适配度
     */
    private double calculateDifficultyMatch(Exercise exercise, User user) {
        double userLevel = user.getFitnessLevel() != null ? user.getFitnessLevel() : 0.5;
        double exerciseDifficulty = exercise.getDifficulty() != null ? exercise.getDifficulty() : 0.5;

        // 理想情况：动作难度略高于用户水平（挑战但不过分）
        double diff = Math.abs(exerciseDifficulty - (userLevel + 0.1));
        return Math.max(0, 1.0 - diff * 2);
    }

    /**
     * 计算训练历史偏好
     */
    private double calculateHistoryPreference(Exercise exercise, List<TrainingHistory> history) {
        if (history.isEmpty()) {
            return 0.5; // 新用户给中等分数
        }

        // 查找该动作的历史记录
        Optional<TrainingHistory> lastRecord = history.stream()
                .filter(h -> h.getExercise().getId().equals(exercise.getId()))
                .findFirst();

        if (lastRecord.isPresent()) {
            TrainingHistory record = lastRecord.get();
            
            // 根据历史评分调整
            double ratingScore = record.getRating() != null ? record.getRating() / 5.0 : 0.6;
            
            // 避免过度推荐最近完成的动作
            long daysSinceLastTraining = java.time.Duration.between(
                record.getTrainingDate(), 
                java.time.LocalDateTime.now()
            ).toDays();
            
            double recencyPenalty = Math.min(daysSinceLastTraining / 7.0, 1.0);
            
            return ratingScore * 0.7 + recencyPenalty * 0.3;
        }

        // 同类别的历史偏好
        double categoryPreference = history.stream()
                .filter(h -> exercise.getCategory().equals(h.getExercise().getCategory()))
                .mapToDouble(h -> h.getRating() != null ? h.getRating() / 5.0 : 0.5)
                .average()
                .orElse(0.5);

        return categoryPreference;
    }

    /**
     * 计算多样性奖励
     */
    private double calculateDiversityBonus(Exercise exercise, List<TrainingHistory> history) {
        if (history.isEmpty()) {
            return 1.0; // 新用户鼓励尝试
        }

        // 检查该动作是否在最近训练过
        long recentTrainingCount = history.stream()
                .limit(10) // 最近10次训练
                .filter(h -> h.getExercise().getId().equals(exercise.getId()))
                .count();

        // 训练次数越多，多样性奖励越低
        return Math.max(0, 1.0 - recentTrainingCount * 0.3);
    }
}
