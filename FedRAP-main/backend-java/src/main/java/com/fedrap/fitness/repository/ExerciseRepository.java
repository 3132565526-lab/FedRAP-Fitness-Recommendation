package com.fedrap.fitness.repository;

import com.fedrap.fitness.model.entity.Exercise;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * 健身动作数据访问层
 */
@Repository
public interface ExerciseRepository extends JpaRepository<Exercise, Long> {
    
    List<Exercise> findByIsActiveTrue();
    
    List<Exercise> findByCategory(String category);
    
    List<Exercise> findByCategoryAndIsActiveTrue(String category);
    
    @Query("SELECT e FROM Exercise e WHERE e.isActive = true AND e.difficulty <= :maxDifficulty")
    List<Exercise> findByMaxDifficulty(@Param("maxDifficulty") Double maxDifficulty);
    
    @Query("SELECT e FROM Exercise e WHERE e.isActive = true AND " +
           "(:category IS NULL OR e.category = :category) AND " +
           "(:minDifficulty IS NULL OR e.difficulty >= :minDifficulty) AND " +
           "(:maxDifficulty IS NULL OR e.difficulty <= :maxDifficulty)")
    List<Exercise> findByFilters(
        @Param("category") String category,
        @Param("minDifficulty") Double minDifficulty,
        @Param("maxDifficulty") Double maxDifficulty
    );
}
