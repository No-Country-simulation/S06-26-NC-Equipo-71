package com.appbit.backend.modules.visent.entity;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Entity
@Table(name = "sequence_visits")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class SequenceVisitEntity {

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

    @Column(name = "sequence_number", nullable = false)
    private Short sequenceNumber;

    @Column(name = "arrival_time", nullable = false)
    private LocalDateTime arrivalTime;

    @Column(name = "stay_seconds")
    private Integer staySeconds;

    @Column(name = "session_period", nullable = false, length = 12)
    private String sessionPeriod;

    @Column(name = "distance_km_from_previous", precision = 8, scale = 3)
    private BigDecimal distanceKmFromPrevious;

    @Column(name = "sessions_count")
    private Integer sessionsCount;

    @Column(name = "loaded_at", nullable = false)
    private LocalDateTime loadedAt;
}