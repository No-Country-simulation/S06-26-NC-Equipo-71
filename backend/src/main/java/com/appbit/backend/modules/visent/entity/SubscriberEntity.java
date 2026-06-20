package com.appbit.backend.modules.visent.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "subscribers")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class SubscriberEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "assinante_hash", nullable = false, unique = true, length = 64)
    private String assinanteHash;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "home_cluster_id", nullable = false)
    private ClusterEntity homeCluster;

    @Column(name = "income_cluster", nullable = false, length = 1)
    private String incomeCluster;

    @Column(name = "age_group", nullable = false, length = 10)
    private String ageGroup;

    @Column(name = "mobility_pattern", nullable = false, length = 20)
    private String mobilityPattern;

    @Column(name = "flag_flagship", nullable = false)
    private Boolean flagFlagship;
}