package com.appbit.backend.modules.visent.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "clusters")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ClusterEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 80)
    private String code;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "municipality_id", nullable = false)
    private MunicipalityEntity municipality;

    @Column(name = "centroid_lat", precision = 10, scale = 6)
    private BigDecimal centroidLat;

    @Column(name = "centroid_lon", precision = 10, scale = 6)
    private BigDecimal centroidLon;

    @Column(length = 255)
    private String profile;
}