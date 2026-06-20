package com.appbit.backend.modules.visent.repository;

import com.appbit.backend.modules.visent.entity.ClusterEntity;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface ClusterRepository extends JpaRepository<ClusterEntity, Long> {

    Optional<ClusterEntity> findByCode(String code);
}