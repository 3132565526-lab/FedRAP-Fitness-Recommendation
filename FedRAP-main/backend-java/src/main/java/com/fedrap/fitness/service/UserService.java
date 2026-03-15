package com.fedrap.fitness.service;

import com.fedrap.fitness.model.dto.UserProfileUpdateRequest;
import com.fedrap.fitness.model.entity.User;
import com.fedrap.fitness.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 用户服务
 */
@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    /**
     * 根据ID获取用户
     */
    public User getUserById(Long userId) {
        return userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("用户不存在: " + userId));
    }

    /**
     * 更新用户资料
     */
    @Transactional
    public User updateUserProfile(Long userId, UserProfileUpdateRequest request) {
        User user = getUserById(userId);

        // 更新基本信息
        if (request.getAge() != null) user.setAge(request.getAge());
        if (request.getWeight() != null) user.setWeight(request.getWeight());
        if (request.getHeight() != null) user.setHeight(request.getHeight());
        if (request.getHeartRate() != null) user.setHeartRate(request.getHeartRate());
        if (request.getGender() != null) user.setGender(request.getGender());

        // 计算BMI
        if (user.getWeight() != null && user.getHeight() != null) {
            double heightInMeters = user.getHeight() / 100.0;
            user.setBmi(user.getWeight() / (heightInMeters * heightInMeters));
        }

        // 更新健身数据
        if (request.getFitnessLevel() != null) user.setFitnessLevel(request.getFitnessLevel());
        if (request.getExperienceYears() != null) user.setExperienceYears(request.getExperienceYears());
        if (request.getWeeklyFrequency() != null) user.setWeeklyFrequency(request.getWeeklyFrequency());
        if (request.getAvgSessionDuration() != null) user.setAvgSessionDuration(request.getAvgSessionDuration());

        // 更新健身目标
        if (request.getGoalWeightLoss() != null) user.setGoalWeightLoss(request.getGoalWeightLoss());
        if (request.getGoalMuscleGain() != null) user.setGoalMuscleGain(request.getGoalMuscleGain());
        if (request.getGoalEndurance() != null) user.setGoalEndurance(request.getGoalEndurance());
        if (request.getGoalFlexibility() != null) user.setGoalFlexibility(request.getGoalFlexibility());

        // 更新身体维度
        if (request.getChest() != null) user.setChest(request.getChest());
        if (request.getWaist() != null) user.setWaist(request.getWaist());
        if (request.getHips() != null) user.setHips(request.getHips());
        if (request.getLeftArm() != null) user.setLeftArm(request.getLeftArm());
        if (request.getRightArm() != null) user.setRightArm(request.getRightArm());
        if (request.getLeftThigh() != null) user.setLeftThigh(request.getLeftThigh());
        if (request.getRightThigh() != null) user.setRightThigh(request.getRightThigh());

        return userRepository.save(user);
    }

    /**
     * 增加用户经验值
     */
    @Transactional
    public void addExperience(Long userId, int exp) {
        User user = getUserById(userId);
        user.setExperience(user.getExperience() + exp);
        
        // 升级逻辑: 每100经验升1级
        int newLevel = user.getExperience() / 100 + 1;
        if (newLevel > user.getLevel()) {
            user.setLevel(newLevel);
        }
        
        userRepository.save(user);
    }

    /**
     * 增加完成训练次数
     */
    @Transactional
    public void incrementWorkoutCount(Long userId) {
        User user = getUserById(userId);
        user.setTotalWorkouts(user.getTotalWorkouts() + 1);
        userRepository.save(user);
    }
}
