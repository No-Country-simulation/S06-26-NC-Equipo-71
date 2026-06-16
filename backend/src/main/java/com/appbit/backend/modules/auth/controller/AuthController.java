package com.appbit.backend.modules.auth.controller;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.appbit.backend.modules.auth.dto.RegisterRequest;
import com.appbit.backend.modules.auth.dto.RegisterResponse;
import com.appbit.backend.modules.auth.service.AuthService;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    @PostMapping("/register")
    public ResponseEntity<RegisterResponse> register(
            @RequestBody RegisterRequest request) {

        RegisterResponse response = authService.register(request);

        return ResponseEntity.ok(response);
    }
}