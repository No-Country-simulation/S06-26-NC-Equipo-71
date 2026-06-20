package com.appbit.backend.modules.visent.entity;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Entity
@Table(name = "concentration_records")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ConcentrationRecordEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "antenna_id", nullable = false)
    private AntennaEntity antenna;

    @Column(name = "day_date", nullable = false)
    private LocalDate dayDate;

    @Column(name = "session_period", nullable = false, length = 12)
    private String sessionPeriod;

    @Column(name = "active_users", nullable = false)
    private Integer activeUsers;

    @Column(name = "sessions_count", nullable = false)
    private Integer sessionsCount;

    @Column(name = "download_bytes", nullable = false)
    private Long downloadBytes;

    @Column(name = "upload_bytes", nullable = false)
    private Long uploadBytes;

    @Column(name = "avg_session_duration_seconds")
    private Integer avgSessionDurationSeconds;

    @Column(name = "avg_drop_pct", precision = 8, scale = 4)
    private BigDecimal avgDropPct;

    @Column(name = "avg_congestion", precision = 6, scale = 3)
    private BigDecimal avgCongestion;

    @Column(name = "total_calls")
    private Integer totalCalls;

    @Column(name = "total_messages")
    private Integer totalMessages;

    @Column(name = "loaded_at", nullable = false)
    private LocalDateTime loadedAt;
}