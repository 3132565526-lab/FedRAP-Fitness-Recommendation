package com.fedrap.fitness.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fedrap.fitness.model.dto.RecommendationItem;
import com.fedrap.fitness.model.entity.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 模型推理服务 - 调用Python训练好的FedRAP模型
 */
@Service
public class ModelInferenceService {

    private static final Logger logger = LoggerFactory.getLogger(ModelInferenceService.class);
    private final ObjectMapper objectMapper = new ObjectMapper();

    @Value("${fedrap.model.python-path:python}")
    private String pythonPath;

    @Value("${fedrap.model.script-path:model_inference.py}")
    private String scriptPath;

    @Value("${fedrap.model.enabled:true}")
    private boolean modelEnabled;

    /**
     * 使用训练好的模型获取推荐
     */
    public List<RecommendationItem> getModelRecommendations(User user, int topK) {
        if (!modelEnabled) {
            logger.info("模型推理已禁用，返回空列表");
            return new ArrayList<>();
        }

        try {
            // 构建用户特征JSON
            Map<String, Object> userProfile = buildUserProfile(user);
            String userProfileJson = objectMapper.writeValueAsString(userProfile);

            // 调用Python脚本
            ProcessBuilder processBuilder = new ProcessBuilder(
                pythonPath,
                scriptPath,
                userProfileJson,
                String.valueOf(topK)
            );

            // 设置工作目录为项目根目录
            File workingDir = new File(System.getProperty("user.dir")).getParentFile();
            if (!workingDir.exists() || !new File(workingDir, scriptPath).exists()) {
                workingDir = new File(System.getProperty("user.dir"));
            }
            processBuilder.directory(workingDir);

            processBuilder.redirectErrorStream(true);
            Process process = processBuilder.start();

            // 读取输出
            StringBuilder output = new StringBuilder();
            try (BufferedReader reader = new BufferedReader(
                    new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    output.append(line);
                }
            }

            int exitCode = process.waitFor();
            if (exitCode != 0) {
                logger.error("Python脚本执行失败，退出码: {}, 输出: {}", exitCode, output);
                return new ArrayList<>();
            }

            // 解析JSON结果
            String jsonOutput = output.toString();
            JsonNode result = objectMapper.readTree(jsonOutput);

            if (!result.has("success") || !result.get("success").asBoolean()) {
                String error = result.has("error") ? result.get("error").asText() : "未知错误";
                logger.error("模型推理失败: {}", error);
                return new ArrayList<>();
            }

            // 转换推荐结果
            List<RecommendationItem> recommendations = new ArrayList<>();
            JsonNode recsNode = result.get("recommendations");
            if (recsNode != null && recsNode.isArray()) {
                for (JsonNode rec : recsNode) {
                    RecommendationItem item = new RecommendationItem();
                    item.setExerciseId(rec.get("exerciseId").asLong());
                    item.setScore(rec.get("score").asDouble());
                    item.setExerciseName(rec.has("name") ? rec.get("name").asText() : "");
                    item.setCategory(rec.has("category") ? rec.get("category").asText() : "");
                    item.setIntensity(rec.has("intensity") ? rec.get("intensity").asDouble() : 0.5);
                    item.setRecommendedDuration(rec.has("duration") ? rec.get("duration").asInt() : 30);
                    item.setDifficulty(rec.has("difficulty") ? rec.get("difficulty").asDouble() : 0.5);
                    recommendations.add(item);
                }
            }

            logger.info("模型推理成功，返回{}条推荐", recommendations.size());
            return recommendations;

        } catch (Exception e) {
            logger.error("模型推理异常", e);
            return new ArrayList<>();
        }
    }

    /**
     * 构建用户特征Map
     */
    private Map<String, Object> buildUserProfile(User user) {
        Map<String, Object> profile = new HashMap<>();
        profile.put("age", user.getAge() != null ? user.getAge() : 30);
        profile.put("weight", user.getWeight() != null ? user.getWeight() : 70.0);
        profile.put("height", user.getHeight() != null ? user.getHeight() : 170.0);
        profile.put("bmi", user.getBmi() != null ? user.getBmi() : 24.0);
        profile.put("heartRate", user.getHeartRate() != null ? user.getHeartRate() : 75);
        profile.put("fitnessLevel", user.getFitnessLevel() != null ? user.getFitnessLevel() : 0.5);
        profile.put("goalWeightLoss", user.getGoalWeightLoss() != null ? user.getGoalWeightLoss() : 0.3);
        profile.put("goalMuscleGain", user.getGoalMuscleGain() != null ? user.getGoalMuscleGain() : 0.3);
        profile.put("goalEndurance", user.getGoalEndurance() != null ? user.getGoalEndurance() : 0.2);
        profile.put("goalFlexibility", user.getGoalFlexibility() != null ? user.getGoalFlexibility() : 0.2);
        profile.put("experienceYears", user.getExperienceYears() != null ? user.getExperienceYears() : 1);
        profile.put("weeklyFrequency", user.getWeeklyFrequency() != null ? user.getWeeklyFrequency() : 3);
        profile.put("avgSessionDuration", user.getAvgSessionDuration() != null ? user.getAvgSessionDuration() : 45);
        return profile;
    }
}
