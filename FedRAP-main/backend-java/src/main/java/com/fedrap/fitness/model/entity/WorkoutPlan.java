package com.fedrap.fitness.model.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/**
 * 训练计划实体类
 */
@Entity
@Table(name = "workout_plans")
@Data
@NoArgsConstructor
@AllArgsConstructor
@EntityListeners(AuditingEntityListener.class)
@JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})
public class WorkoutPlan {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    @JsonIgnore
    private User user;

    @Column(nullable = false)
    private String planName;

    @Column(length = 1000)
    private String description;

    @ElementCollection
    @CollectionTable(name = "plan_exercises", joinColumns = @JoinColumn(name = "plan_id"))
    private List<PlanExerciseItem> exercises = new ArrayList<>();

    private Integer totalDuration; // 总时长(分钟)
    private Integer estimatedCalories; // 预估消耗卡路里

    private String difficulty; // BEGINNER, INTERMEDIATE, ADVANCED
    private String frequency; // DAILY, 3_TIMES_WEEK, 5_TIMES_WEEK

    private Boolean isActive = true;
    private Boolean isCompleted = false;

    @CreatedDate
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Embeddable
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class PlanExerciseItem {
        private Long exerciseId;
        private String exerciseName;
        private Integer sets;
        private Integer reps;
        private Integer duration;
        private Integer orderIndex;
    }
}
