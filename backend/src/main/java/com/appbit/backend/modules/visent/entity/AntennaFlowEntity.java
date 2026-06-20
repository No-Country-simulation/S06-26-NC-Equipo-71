package com.appbit.backend.modules.visent.entity;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "antenna_flows")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AntennaFlowEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "origin_antenna_id", nullable = false)
    private AntennaEntity originAntenna;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "destination_antenna_id", nullable = false)
    private AntennaEntity destinationAntenna;

    @Column(name = "users_count", nullable = false)
    private Integer usersCount;

    @Column(name = "transitions_count", nullable = false)
    private Integer transitionsCount;

    @Column(name = "distance_km", precision = 8, scale = 3)
    private BigDecimal distanceKm;

    @Column(name = "predominant_period", length = 12)
    private String predominantPeriod;

    @Column(name = "pct_from_origin_cluster", precision = 6, scale = 1)
    private BigDecimal pctFromOriginCluster;

    @Column(name = "loaded_at", nullable = false)
    private LocalDateTime loadedAt;
}