package com.appbit.backend.modules.auth.service;

import com.appbit.backend.modules.auth.dto.AuthResponse;
import com.appbit.backend.modules.auth.dto.LoginRequest;
import com.appbit.backend.modules.auth.dto.RegisterRequest;
import com.appbit.backend.modules.auth.dto.RegisterResponse;

public interface AuthService {

    RegisterResponse register(RegisterRequest request);

    AuthResponse login(LoginRequest request);

}