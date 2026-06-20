package com.appbit.backend.modules.visent.repository;

import com.appbit.backend.modules.visent.entity.TravelTimeStatEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TravelTimeStatRepository extends JpaRepository<TravelTimeStatEntity, Long> {
}