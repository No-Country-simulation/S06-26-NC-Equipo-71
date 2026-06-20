package com.appbit.backend.modules.visent.repository;

import com.appbit.backend.modules.visent.entity.MobilityRecordEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface MobilityRecordRepository extends JpaRepository<MobilityRecordEntity, Long> {
}