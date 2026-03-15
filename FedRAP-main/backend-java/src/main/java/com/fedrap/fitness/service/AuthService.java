package com.fedrap.fitness.service;

import com.fedrap.fitness.model.dto.JwtResponse;
import com.fedrap.fitness.model.dto.LoginRequest;
import com.fedrap.fitness.model.dto.RegisterRequest;
import com.fedrap.fitness.model.dto.UserProfileUpdateRequest;
import com.fedrap.fitness.model.entity.User;
import com.fedrap.fitness.repository.UserRepository;
import com.fedrap.fitness.security.JwtTokenProvider;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 用户认证服务
 */
@Service
public class AuthService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private JwtTokenProvider tokenProvider;

    /**
     * 用户注册
     */
    @Transactional
    public JwtResponse register(RegisterRequest request) {
        // 检查用户名是否存在
        if (userRepository.existsByUsername(request.getUsername())) {
            throw new RuntimeException("用户名已存在");
        }

        // 检查邮箱是否存在
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new RuntimeException("邮箱已被注册");
        }

        // 创建新用户
        User user = new User();
        user.setUsername(request.getUsername());
        user.setEmail(request.getEmail());
        user.setPassword(passwordEncoder.encode(request.getPassword()));
        user.setAge(request.getAge());
        user.setWeight(request.getWeight());
        user.setHeight(request.getHeight());
        user.setGender(request.getGender());
        
        // 计算BMI
        if (request.getWeight() != null && request.getHeight() != null) {
            double heightInMeters = request.getHeight() / 100.0;
            user.setBmi(request.getWeight() / (heightInMeters * heightInMeters));
        }

        // 设置默认值
        user.setEnabled(true);
        user.setRole("USER");
        user.setLevel(1);
        user.setExperience(0);
        user.setTotalWorkouts(0);
        user.setFitnessLevel(0.3); // 默认初级
        user.setExperienceYears(0);
        user.setWeeklyFrequency(3);
        user.setAvgSessionDuration(45);
        user.setGoalWeightLoss(0.3);
        user.setGoalMuscleGain(0.3);
        user.setGoalEndurance(0.2);
        user.setGoalFlexibility(0.2);

        user = userRepository.save(user);

        // 生成JWT Token
        String token = tokenProvider.generateTokenFromUsername(user.getUsername());

        return new JwtResponse(token, user.getId(), user.getUsername(), user.getEmail(), user.getRole());
    }

    /**
     * 用户登录
     */
    public JwtResponse login(LoginRequest request) {
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.getUsername(), request.getPassword())
        );

        SecurityContextHolder.getContext().setAuthentication(authentication);
        String jwt = tokenProvider.generateToken(authentication);

        User user = userRepository.findByUsername(request.getUsername())
                .orElseThrow(() -> new RuntimeException("用户不存在"));

        return new JwtResponse(jwt, user.getId(), user.getUsername(), user.getEmail(), user.getRole());
    }

    /**
     * 获取当前用户
     */
    public User getCurrentUser() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        String username = authentication.getName();
        return userRepository.findByUsername(username)
                .orElseThrow(() -> new RuntimeException("用户不存在"));
    }
}
