package com.appbit.backend.modules.visent.repository;

import com.appbit.backend.modules.visent.entity.MunicipalityEntity;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface MunicipalityRepository extends JpaRepository<MunicipalityEntity, Long> {

    Optional<MunicipalityEntity> findByNormalizedName(String normalizedName);
}