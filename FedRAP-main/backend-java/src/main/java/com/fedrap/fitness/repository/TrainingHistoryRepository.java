package com.fedrap.fitness.repository;

import com.fedrap.fitness.model.entity.TrainingHistory;
import com.fedrap.fitness.model.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

/**
 * 训练历史数据访问层
 */
@Repository
public interface TrainingHistoryRepository extends JpaRepository<TrainingHistory, Long> {
    
    List<TrainingHistory> findByUserOrderByTrainingDateDesc(User user);
    
    List<TrainingHistory> findByUserIdOrderByTrainingDateDesc(Long userId);
    
    @Query("SELECT th FROM TrainingHistory th WHERE th.user.id = :userId " +
           "AND th.trainingDate >= :startDate AND th.trainingDate <= :endDate " +
           "ORDER BY th.trainingDate DESC")
    List<TrainingHistory> findByUserIdAndDateRange(
        @Param("userId") Long userId,
        @Param("startDate") LocalDateTime startDate,
        @Param("endDate") LocalDateTime endDate
    );
    
    @Query("SELECT COUNT(th) FROM TrainingHistory th WHERE th.user.id = :userId AND th.completed = true")
    Long countCompletedWorkoutsByUserId(@Param("userId") Long userId);
    
    @Query("SELECT SUM(th.caloriesBurned) FROM TrainingHistory th WHERE th.user.id = :userId")
    Long sumCaloriesByUserId(@Param("userId") Long userId);
    
    @Query("SELECT th.exercise.id, COUNT(th) as count FROM TrainingHistory th " +
           "WHERE th.user.id = :userId AND th.completed = true " +
           "GROUP BY th.exercise.id ORDER BY count DESC")
    List<Object[]> findMostFrequentExercisesByUserId(@Param("userId") Long userId);
}
