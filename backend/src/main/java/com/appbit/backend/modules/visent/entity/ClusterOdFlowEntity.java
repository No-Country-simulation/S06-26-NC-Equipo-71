package com.appbit.backend.modules.visent.entity;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "cluster_od_flows")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ClusterOdFlowEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "origin_cluster_id", nullable = false)
    private ClusterEntity originCluster;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "destination_cluster_id", nullable = false)
    private ClusterEntity destinationCluster;

    @Column(name = "same_cluster", nullable = false)
    private Boolean sameCluster;

    @Column(name = "users_count", nullable = false)
    private Integer usersCount;

    @Column(name = "trips_count", nullable = false)
    private Integer tripsCount;

    @Column(name = "avg_distance_km", precision = 8, scale = 3)
    private BigDecimal avgDistanceKm;

    @Column(name = "predominant_period", length = 12)
    private String predominantPeriod;

    @Column(name = "loaded_at", nullable = false)
    private LocalDateTime loadedAt;
}