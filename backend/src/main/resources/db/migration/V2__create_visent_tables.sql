CREATE TABLE municipalities (
                                id BIGSERIAL PRIMARY KEY,
                                name VARCHAR(100) NOT NULL,
                                normalized_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE clusters (
                          id BIGSERIAL PRIMARY KEY,
                          code VARCHAR(80) NOT NULL UNIQUE,
                          municipality_id BIGINT NOT NULL,
                          centroid_lat NUMERIC(10, 6),
                          centroid_lon NUMERIC(10, 6),
                          profile VARCHAR(255),

                          CONSTRAINT fk_clusters_municipality
                              FOREIGN KEY (municipality_id)
                                  REFERENCES municipalities (id)
);

CREATE TABLE antennas (
                          id BIGSERIAL PRIMARY KEY,
                          ecgi VARCHAR(32) NOT NULL UNIQUE,
                          cluster_id BIGINT NOT NULL,
                          lat NUMERIC(10, 6) NOT NULL,
                          lon NUMERIC(10, 6) NOT NULL,

                          CONSTRAINT fk_antennas_cluster
                              FOREIGN KEY (cluster_id)
                                  REFERENCES clusters (id)
);

CREATE TABLE subscribers (
                             id BIGSERIAL PRIMARY KEY,
                             assinante_hash VARCHAR(64) NOT NULL UNIQUE,
                             home_cluster_id BIGINT NOT NULL,
                             income_cluster CHAR(1) NOT NULL,
                             age_group VARCHAR(10) NOT NULL,
                             mobility_pattern VARCHAR(20) NOT NULL,
                             flag_flagship BOOLEAN NOT NULL,

                             CONSTRAINT fk_subscribers_home_cluster
                                 FOREIGN KEY (home_cluster_id)
                                     REFERENCES clusters (id),

                             CONSTRAINT chk_subscribers_income_cluster
                                 CHECK (income_cluster IN ('A', 'B', 'C', 'D')),

                             CONSTRAINT chk_subscribers_mobility_pattern
                                 CHECK (mobility_pattern IN ('BAIXA', 'MODERADA', 'INTENSA'))
);

CREATE TABLE concentration_records (
                                       id BIGSERIAL PRIMARY KEY,
                                       antenna_id BIGINT NOT NULL,
                                       day_date DATE NOT NULL,
                                       session_period VARCHAR(12) NOT NULL,
                                       active_users INTEGER NOT NULL,
                                       sessions_count INTEGER NOT NULL,
                                       download_bytes BIGINT NOT NULL,
                                       upload_bytes BIGINT NOT NULL,
                                       avg_session_duration_seconds INTEGER,
                                       avg_drop_pct NUMERIC(8, 4),
                                       avg_congestion NUMERIC(6, 3),
                                       total_calls INTEGER,
                                       total_messages INTEGER,
                                       loaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

                                       CONSTRAINT fk_concentration_antenna
                                           FOREIGN KEY (antenna_id)
                                               REFERENCES antennas (id),

                                       CONSTRAINT chk_concentration_period
                                           CHECK (session_period IN ('MADRUGADA', 'MANHA', 'TARDE', 'NOITE'))
);

CREATE TABLE cluster_od_flows (
                                  id BIGSERIAL PRIMARY KEY,
                                  origin_cluster_id BIGINT NOT NULL,
                                  destination_cluster_id BIGINT NOT NULL,
                                  same_cluster BOOLEAN NOT NULL,
                                  users_count INTEGER NOT NULL,
                                  trips_count INTEGER NOT NULL,
                                  avg_distance_km NUMERIC(8, 3),
                                  predominant_period VARCHAR(12),
                                  loaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

                                  CONSTRAINT fk_cluster_od_origin_cluster
                                      FOREIGN KEY (origin_cluster_id)
                                          REFERENCES clusters (id),

                                  CONSTRAINT fk_cluster_od_destination_cluster
                                      FOREIGN KEY (destination_cluster_id)
                                          REFERENCES clusters (id),

                                  CONSTRAINT chk_cluster_od_period
                                      CHECK (
                                          predominant_period IS NULL
                                              OR predominant_period IN ('MADRUGADA', 'MANHA', 'TARDE', 'NOITE')
                                          )
);

CREATE TABLE antenna_flows (
                               id BIGSERIAL PRIMARY KEY,
                               origin_antenna_id BIGINT NOT NULL,
                               destination_antenna_id BIGINT NOT NULL,
                               users_count INTEGER NOT NULL,
                               transitions_count INTEGER NOT NULL,
                               distance_km NUMERIC(8, 3),
                               predominant_period VARCHAR(12),
                               pct_from_origin_cluster NUMERIC(6, 1),
                               loaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

                               CONSTRAINT fk_antenna_flows_origin_antenna
                                   FOREIGN KEY (origin_antenna_id)
                                       REFERENCES antennas (id),

                               CONSTRAINT fk_antenna_flows_destination_antenna
                                   FOREIGN KEY (destination_antenna_id)
                                       REFERENCES antennas (id),

                               CONSTRAINT chk_antenna_flows_period
                                   CHECK (
                                       predominant_period IS NULL
                                           OR predominant_period IN ('MADRUGADA', 'MANHA', 'TARDE', 'NOITE')
                                       )
);

CREATE TABLE travel_time_stats (
                                   id BIGSERIAL PRIMARY KEY,
                                   origin_cluster_id BIGINT NOT NULL,
                                   destination_cluster_id BIGINT NOT NULL,
                                   same_cluster BOOLEAN NOT NULL,
                                   observations_count INTEGER NOT NULL,
                                   avg_distance_km NUMERIC(8, 3),
                                   p25_distance_km NUMERIC(8, 3),
                                   p75_distance_km NUMERIC(8, 3),
                                   predominant_period VARCHAR(12),
                                   loaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

                                   CONSTRAINT fk_travel_time_origin_cluster
                                       FOREIGN KEY (origin_cluster_id)
                                           REFERENCES clusters (id),

                                   CONSTRAINT fk_travel_time_destination_cluster
                                       FOREIGN KEY (destination_cluster_id)
                                           REFERENCES clusters (id),

                                   CONSTRAINT chk_travel_time_period
                                       CHECK (
                                           predominant_period IS NULL
                                               OR predominant_period IN ('MADRUGADA', 'MANHA', 'TARDE', 'NOITE')
                                           )
);

CREATE TABLE mobility_records (
                                  id BIGSERIAL PRIMARY KEY,
                                  subscriber_id BIGINT NOT NULL,
                                  antenna_id BIGINT NOT NULL,
                                  day_date DATE NOT NULL,
                                  content_type VARCHAR(20) NOT NULL,
                                  network_type VARCHAR(10) NOT NULL,
                                  session_period VARCHAR(12) NOT NULL,
                                  sessions_count INTEGER NOT NULL,
                                  total_duration_seconds INTEGER NOT NULL,
                                  download_bytes REAL NOT NULL,
                                  upload_bytes REAL NOT NULL,
                                  drop_pct NUMERIC(8, 4),
                                  congestion_level NUMERIC(6, 3),
                                  calls_count INTEGER,
                                  voice_seconds INTEGER,
                                  voice_completion_rate NUMERIC(6, 3),
                                  voice_congestion NUMERIC(6, 3),
                                  messages_count INTEGER,
                                  sms_completion_rate NUMERIC(6, 3),
                                  sms_congestion NUMERIC(6, 3),
                                  streaming_sessions INTEGER,
                                  game_sessions INTEGER,
                                  social_sessions INTEGER,
                                  communication_sessions INTEGER,
                                  other_sessions INTEGER,
                                  loaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

                                  CONSTRAINT fk_mobility_subscriber
                                      FOREIGN KEY (subscriber_id)
                                          REFERENCES subscribers (id),

                                  CONSTRAINT fk_mobility_antenna
                                      FOREIGN KEY (antenna_id)
                                          REFERENCES antennas (id),

                                  CONSTRAINT chk_mobility_network_type
                                      CHECK (network_type IN ('NR', 'LTE', 'WCDMA')),

                                  CONSTRAINT chk_mobility_session_period
                                      CHECK (session_period IN ('MADRUGADA', 'MANHA', 'TARDE', 'NOITE'))
);

CREATE TABLE sequence_visits (
                                 id BIGSERIAL PRIMARY KEY,
                                 subscriber_id BIGINT NOT NULL,
                                 antenna_id BIGINT NOT NULL,
                                 day_date DATE NOT NULL,
                                 sequence_number SMALLINT NOT NULL,
                                 arrival_time TIMESTAMP NOT NULL,
                                 stay_seconds INTEGER,
                                 session_period VARCHAR(12) NOT NULL,
                                 distance_km_from_previous NUMERIC(8, 3),
                                 sessions_count INTEGER,
                                 loaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

                                 CONSTRAINT fk_sequence_visits_subscriber
                                     FOREIGN KEY (subscriber_id)
                                         REFERENCES subscribers (id),

                                 CONSTRAINT fk_sequence_visits_antenna
                                     FOREIGN KEY (antenna_id)
                                         REFERENCES antennas (id),

                                 CONSTRAINT chk_sequence_visits_session_period
                                     CHECK (session_period IN ('MADRUGADA', 'MANHA', 'TARDE', 'NOITE')),

                                 CONSTRAINT uq_sequence_visit
                                     UNIQUE (subscriber_id, day_date, sequence_number)
);

CREATE INDEX idx_clusters_municipality_id
    ON clusters (municipality_id);

CREATE INDEX idx_antennas_cluster_id
    ON antennas (cluster_id);

CREATE INDEX idx_subscribers_home_cluster_id
    ON subscribers (home_cluster_id);

CREATE INDEX idx_concentration_day_period
    ON concentration_records (day_date, session_period);

CREATE INDEX idx_concentration_antenna_day
    ON concentration_records (antenna_id, day_date);

CREATE INDEX idx_cluster_od_origin_cluster
    ON cluster_od_flows (origin_cluster_id);

CREATE INDEX idx_cluster_od_destination_cluster
    ON cluster_od_flows (destination_cluster_id);

CREATE INDEX idx_antenna_flows_origin_antenna
    ON antenna_flows (origin_antenna_id);

CREATE INDEX idx_antenna_flows_destination_antenna
    ON antenna_flows (destination_antenna_id);

CREATE INDEX idx_travel_time_origin_cluster
    ON travel_time_stats (origin_cluster_id);

CREATE INDEX idx_travel_time_destination_cluster
    ON travel_time_stats (destination_cluster_id);

CREATE INDEX idx_mobility_day_period
    ON mobility_records (day_date, session_period);

CREATE INDEX idx_mobility_subscriber_day
    ON mobility_records (subscriber_id, day_date);

CREATE INDEX idx_mobility_antenna_day
    ON mobility_records (antenna_id, day_date);

CREATE INDEX idx_mobility_network_type
    ON mobility_records (network_type);

CREATE INDEX idx_sequence_visits_subscriber_day
    ON sequence_visits (subscriber_id, day_date);

CREATE INDEX idx_sequence_visits_antenna_day
    ON sequence_visits (antenna_id, day_date);