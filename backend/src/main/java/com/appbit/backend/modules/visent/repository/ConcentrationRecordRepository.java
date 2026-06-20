package com.appbit.backend.modules.visent.repository;

import com.appbit.backend.modules.visent.entity.ConcentrationRecordEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ConcentrationRecordRepository extends JpaRepository<ConcentrationRecordEntity, Long> {
}