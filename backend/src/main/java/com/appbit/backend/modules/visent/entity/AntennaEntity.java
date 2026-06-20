package com.appbit.backend.modules.visent.entity;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;

@Entity
@Table(name = "antennas")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AntennaEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 32)
    private String ecgi;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "cluster_id", nullable = false)
    private ClusterEntity cluster;

    @Column(nullable = false, precision = 10, scale = 6)
    private BigDecimal lat;

    @Column(nullable = false, precision = 10, scale = 6)
    private BigDecimal lon;
}