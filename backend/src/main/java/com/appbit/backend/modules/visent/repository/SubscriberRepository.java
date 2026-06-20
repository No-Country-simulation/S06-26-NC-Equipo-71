package com.appbit.backend.modules.visent.repository;

import com.appbit.backend.modules.visent.entity.SubscriberEntity;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface SubscriberRepository extends JpaRepository<SubscriberEntity, Long> {

    Optional<SubscriberEntity> findByAssinanteHash(String assinanteHash);
}