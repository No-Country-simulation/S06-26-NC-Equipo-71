package com.appbit.backend.modules.visent.repository;

import com.appbit.backend.modules.visent.entity.AntennaEntity;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface AntennaRepository extends JpaRepository<AntennaEntity, Long> {

    Optional<AntennaEntity> findByEcgi(String ecgi);
}