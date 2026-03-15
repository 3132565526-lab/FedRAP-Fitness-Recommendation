package com.fedrap.fitness.repository;

import com.fedrap.fitness.model.entity.WorkoutPlan;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * 训练计划数据访问层
 */
@Repository
public interface WorkoutPlanRepository extends JpaRepository<WorkoutPlan, Long> {
    
    List<WorkoutPlan> findByUserIdAndIsActiveTrueOrderByCreatedAtDesc(Long userId);
    
    List<WorkoutPlan> findByUserIdOrderByCreatedAtDesc(Long userId);
    
    List<WorkoutPlan> findByUserIdAndIsCompletedFalseAndIsActiveTrue(Long userId);
}
