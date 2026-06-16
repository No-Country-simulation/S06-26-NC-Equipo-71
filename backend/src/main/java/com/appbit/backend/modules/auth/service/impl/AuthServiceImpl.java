package com.appbit.backend.modules.auth.service.impl;

import java.time.LocalDateTime;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.appbit.backend.modules.auth.dto.RegisterRequest;
import com.appbit.backend.modules.auth.dto.RegisterResponse;
import com.appbit.backend.modules.auth.exception.EmailAlreadyExistsException;
import com.appbit.backend.modules.auth.service.AuthService;
import com.appbit.backend.modules.user.EnumRole;
import com.appbit.backend.modules.user.UserEntity;
import com.appbit.backend.modules.user.UserRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class AuthServiceImpl implements AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    @Transactional
    @Override
    public RegisterResponse register(RegisterRequest request) {

        if (userRepository.existsByEmail(request.getEmail())) {
            throw new EmailAlreadyExistsException(request.getEmail());
        }

        UserEntity user = UserEntity.builder()
                .fullName(request.getFullName())
                .email(request.getEmail())
                .password(passwordEncoder.encode(request.getPassword()))
                .role(EnumRole.GESTOR_PUBLICO) //rol de usuario provisorio
                .createdAt(LocalDateTime.now())
                .build();

        UserEntity savedUser = userRepository.save(user);

        return RegisterResponse.builder()
                .id(savedUser.getId())
                .email(savedUser.getEmail())
                .role(savedUser.getRole().name())
                .build();
    }

}
