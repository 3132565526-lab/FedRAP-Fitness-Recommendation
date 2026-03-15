package com.fedrap.fitness.controller;

import com.fedrap.fitness.model.dto.ApiResponse;
import com.fedrap.fitness.model.dto.UserProfileUpdateRequest;
import com.fedrap.fitness.model.entity.User;
import com.fedrap.fitness.service.AuthService;
import com.fedrap.fitness.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * 用户控制器
 */
@RestController
@RequestMapping("/users")
public class UserController {

    @Autowired
    private UserService userService;

    @Autowired
    private AuthService authService;

    /**
     * 获取当前用户信息
     */
    @GetMapping("/me")
    public ResponseEntity<ApiResponse<User>> getCurrentUser() {
        try {
            User user = authService.getCurrentUser();
            return ResponseEntity.ok(ApiResponse.success(user));
        } catch (Exception e) {
            return ResponseEntity.badRequest()
                    .body(ApiResponse.error(e.getMessage()));
        }
    }

    /**
     * 获取用户信息
     */
    @GetMapping("/{userId}")
    public ResponseEntity<ApiResponse<User>> getUserById(@PathVariable Long userId) {
        try {
            User user = userService.getUserById(userId);
            return ResponseEntity.ok(ApiResponse.success(user));
        } catch (Exception e) {
            return ResponseEntity.badRequest()
                    .body(ApiResponse.error(e.getMessage()));
        }
    }

    /**
     * 更新用户资料
     */
    @PutMapping("/{userId}")
    public ResponseEntity<ApiResponse<User>> updateUserProfile(
            @PathVariable Long userId,
            @RequestBody UserProfileUpdateRequest request) {
        try {
            User user = userService.updateUserProfile(userId, request);
            return ResponseEntity.ok(ApiResponse.success("更新成功", user));
        } catch (Exception e) {
            return ResponseEntity.badRequest()
                    .body(ApiResponse.error(e.getMessage()));
        }
    }
}
