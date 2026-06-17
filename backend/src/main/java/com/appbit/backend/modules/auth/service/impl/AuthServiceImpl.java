package com.appbit.backend.modules.auth.service.impl;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.appbit.backend.modules.auth.dto.AuthResponse;
import com.appbit.backend.modules.auth.dto.LoginRequest;
import com.appbit.backend.modules.auth.dto.RegisterRequest;
import com.appbit.backend.modules.auth.dto.RegisterResponse;
import com.appbit.backend.modules.auth.exception.EmailAlreadyExistsException;
import com.appbit.backend.modules.auth.exception.InvalidCredentialsException;
import com.appbit.backend.modules.auth.mapper.UserMapper;
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

        UserEntity user = UserMapper.toEntity(request);
        user.setPassword(passwordEncoder.encode(user.getPassword()));
        user.setRole(EnumRole.GESTOR_PUBLICO); // rol por defecto provisorio

        UserEntity savedUser = userRepository.save(user);

        return UserMapper.toRegisterResponse(savedUser);
    }

    @Override
    public AuthResponse login(LoginRequest request) {

        UserEntity user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(InvalidCredentialsException::new);

        if (!passwordEncoder.matches(
                request.getPassword(),
                user.getPassword())) {

            throw new InvalidCredentialsException();
        }

        return AuthResponse.builder()
                .token("jwt-token-aqui")
                .build();
    }

}
