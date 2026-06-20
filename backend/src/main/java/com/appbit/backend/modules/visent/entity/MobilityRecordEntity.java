package com.appbit.backend.modules.visent.entity;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Entity
@Table(name = "mobility_records")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class MobilityRecordEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "subscriber_id", nullable = false)
    private SubscriberEntity subscriber;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "antenna_id", nullable = false)
    private AntennaEntity antenna;

    @Column(name = "day_date", nullable = false)
    private LocalDate dayDate;

    @Column(name = "content_type", nullable = false, length = 20)
    private String contentType;

    @Column(name = "network_type", nullable = false, length = 10)
    private String networkType;

    @Column(name = "session_period", nullable = false, length = 12)
    private String sessionPeriod;

    @Column(name = "sessions_count", nullable = false)
    private Integer sessionsCount;

    @Column(name = "total_duration_seconds", nullable = false)
    private Integer totalDurationSeconds;

    @Column(name = "download_bytes", nullable = false)
    private Double downloadBytes;

    @Column(name = "upload_bytes", nullable = false)
    private Double uploadBytes;

    @Column(name = "drop_pct", precision = 8, scale = 4)
    private BigDecimal dropPct;

    @Column(name = "congestion_level", precision = 6, scale = 3)
    private BigDecimal congestionLevel;

    @Column(name = "calls_count")
    private Integer callsCount;

    @Column(name = "voice_seconds")
    private Integer voiceSeconds;

    @Column(name = "voice_completion_rate", precision = 6, scale = 3)
    private BigDecimal voiceCompletionRate;

    @Column(name = "voice_congestion", precision = 6, scale = 3)
    private BigDecimal voiceCongestion;

    @Column(name = "messages_count")
    private Integer messagesCount;

    @Column(name = "sms_completion_rate", precision = 6, scale = 3)
    private BigDecimal smsCompletionRate;

    @Column(name = "sms_congestion", precision = 6, scale = 3)
    private BigDecimal smsCongestion;

    @Column(name = "streaming_sessions")
    private Integer streamingSessions;

    @Column(name = "game_sessions")
    private Integer gameSessions;

    @Column(name = "social_sessions")
    private Integer socialSessions;

    @Column(name = "communication_sessions")
    private Integer communicationSessions;

    @Column(name = "other_sessions")
    private Integer otherSessions;

    @Column(name = "loaded_at", nullable = false)
    private LocalDateTime loadedAt;
}