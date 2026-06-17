package com.appbit.backend.modules.auth.service;

import com.appbit.backend.modules.user.UserEntity;

public interface JwtService {

    String generateToken(UserEntity user);

    String extractUsername(String token);

    public boolean isTokenValid(String token, String email);

}
