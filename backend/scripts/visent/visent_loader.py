import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from normalize_names import normalize_cluster, normalize_municipality


DATA_DIR = Path(os.getenv("VISENT_DATA_DIR", "/app/data/visent"))

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "appbit_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "50000"))

LOAD_MOBILITY = os.getenv("LOAD_MOBILITY", "false").lower() == "true"
LOAD_SEQUENCES = os.getenv("LOAD_SEQUENCES", "false").lower() == "true"

MAX_MOBILITY_ROWS = int(os.getenv("MAX_MOBILITY_ROWS", "100000"))
MAX_SEQUENCE_ROWS = int(os.getenv("MAX_SEQUENCE_ROWS", "100000"))


CLUSTERS = [
    {"code": "CBD_BEIRAMAR", "municipality": "Florianópolis", "lat": -27.5954, "lon": -48.5480, "profile": "Centro corporativo"},
    {"code": "CENTRO_HISTORICO", "municipality": "Florianópolis", "lat": -27.5970, "lon": -48.5482, "profile": "Turismo / serviços"},
    {"code": "TRINDADE", "municipality": "Florianópolis", "lat": -27.6011, "lon": -48.5320, "profile": "Residencial universitário"},
    {"code": "UFSC", "municipality": "Florianópolis", "lat": -27.5969, "lon": -48.5500, "profile": "Campus universitário"},
    {"code": "COQUEIROS", "municipality": "Florianópolis", "lat": -27.5820, "lon": -48.5700, "profile": "Residencial classe A"},
    {"code": "ESTREITO_CAPOEIRAS", "municipality": "Florianópolis", "lat": -27.5880, "lon": -48.5850, "profile": "Corredor comercial"},
    {"code": "AEROPORTO_HLZ", "municipality": "Florianópolis", "lat": -27.6700, "lon": -48.5470, "profile": "Aeroporto / logística"},
    {"code": "CAMPECHE", "municipality": "Florianópolis", "lat": -27.6800, "lon": -48.4800, "profile": "Expansão sul"},
    {"code": "LAGOA_CONCEICAO", "municipality": "Florianópolis", "lat": -27.6050, "lon": -48.4600, "profile": "Turismo / lazer"},
    {"code": "JURERE", "municipality": "Florianópolis", "lat": -27.4400, "lon": -48.5000, "profile": "Alto padrão balnear"},
    {"code": "CANASVIEIRAS", "municipality": "Florianópolis", "lat": -27.4250, "lon": -48.4700, "profile": "Turismo de massa"},
    {"code": "INGLESES", "municipality": "Florianópolis", "lat": -27.4350, "lon": -48.3950, "profile": "Residencial norte"},
    {"code": "NORTE_ILHA", "municipality": "Florianópolis", "lat": -27.4800, "lon": -48.4500, "profile": "Expansão norte"},
    {"code": "RESIDENCIAL_NORTE", "municipality": "Florianópolis", "lat": -27.5420, "lon": -48.5000, "profile": "Residencial expansão"},
    {"code": "SC401_CORREDOR", "municipality": "Florianópolis", "lat": -27.5600, "lon": -48.5180, "profile": "Corredor SC-401"},
    {"code": "SAO_JOSE_CENTRO", "municipality": "São José", "lat": -27.6100, "lon": -48.6180, "profile": "Centro de São José"},
    {"code": "SAO_JOSE_BARREIROS", "municipality": "São José", "lat": -27.6450, "lon": -48.6500, "profile": "Residencial sul SJ"},
    {"code": "SAO_JOSE_KOBRASOL", "municipality": "São José", "lat": -27.5950, "lon": -48.6300, "profile": "Comércio SJ"},
    {"code": "SAO_JOSE_ROCADO", "municipality": "São José", "lat": -27.5700, "lon": -48.6500, "profile": "Industrial SJ"},
    {"code": "PALHOCA_CENTRO", "municipality": "Palhoça", "lat": -27.6450, "lon": -48.6700, "profile": "Centro de Palhoça"},
    {"code": "PALHOCA_PEDRA_BRANCA", "municipality": "Palhoça", "lat": -27.6250, "lon": -48.6900, "profile": "Expansão Palhoça"},
    {"code": "PALHOCA_BR101_SUL", "municipality": "Palhoça", "lat": -27.6800, "lon": -48.7000, "profile": "Corredor BR-101 Sul"},
    {"code": "BIGUACU_BR101_NORTE", "municipality": "Biguaçu", "lat": -27.4950, "lon": -48.6550, "profile": "Corredor BR-101 Norte"},
    {"code": "VIA_EXPRESSA_CORREDOR", "municipality": "Florianópolis", "lat": -27.6200, "lon": -48.5800, "profile": "Via Expressa"},
    {"code": "SANTO_AMARO", "municipality": "Santo Amaro", "lat": -27.7100, "lon": -48.7800, "profile": "Interior sul"},
    {"code": "GOV_CELSO_RAMOS", "municipality": "Governador Celso Ramos", "lat": -27.3200, "lon": -48.5550, "profile": "Litoral norte"},
    {"code": "ANTONIO_CARLOS", "municipality": "Antônio Carlos", "lat": -27.5300, "lon": -48.7400, "profile": "Hortigranjeiro / rural"},
]


def build_engine():
    url = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url)


def csv_path(file_name: str) -> Path:
    path = DATA_DIR / file_name

    if not path.exists():
        raise FileNotFoundError(f"No existe el CSV: {path}")

    return path


def to_int(value):
    if pd.isna(value) or str(value).strip() == "":
        return None

    return int(float(value))


def to_float(value):
    if pd.isna(value) or str(value).strip() == "":
        return None

    return float(value)


def to_bool_01(value):
    return str(value).strip() == "1"


def normalize_period(value):
    if pd.isna(value):
        return None

    return str(value).strip().upper()


def insert_municipalities(connection):
    municipalities = {}

    for cluster in CLUSTERS:
        normalized_name = normalize_municipality(cluster["municipality"])
        municipalities[normalized_name] = cluster["municipality"]

    rows = [
        {"name": name, "normalized_name": normalized_name}
        for normalized_name, name in municipalities.items()
    ]

    connection.execute(
        text("""
            INSERT INTO municipalities (name, normalized_name)
            VALUES (:name, :normalized_name)
            ON CONFLICT (normalized_name) DO UPDATE
            SET name = EXCLUDED.name
        """),
        rows,
    )

    print(f"municipalities cargadas: {len(rows)}")


def get_municipality_ids(connection):
    result = connection.execute(
        text("SELECT id, normalized_name FROM municipalities")
    )

    return {row.normalized_name: row.id for row in result}


def insert_clusters(connection):
    municipality_ids = get_municipality_ids(connection)

    rows = []

    for cluster in CLUSTERS:
        normalized_municipality = normalize_municipality(cluster["municipality"])

        rows.append({
            "code": normalize_cluster(cluster["code"]),
            "municipality_id": municipality_ids[normalized_municipality],
            "centroid_lat": cluster["lat"],
            "centroid_lon": cluster["lon"],
            "profile": cluster["profile"],
        })

    connection.execute(
        text("""
            INSERT INTO clusters (
                code,
                municipality_id,
                centroid_lat,
                centroid_lon,
                profile
            )
            VALUES (
                :code,
                :municipality_id,
                :centroid_lat,
                :centroid_lon,
                :profile
            )
            ON CONFLICT (code) DO UPDATE
            SET municipality_id = EXCLUDED.municipality_id,
                centroid_lat = EXCLUDED.centroid_lat,
                centroid_lon = EXCLUDED.centroid_lon,
                profile = EXCLUDED.profile
        """),
        rows,
    )

    print(f"clusters cargados: {len(rows)}")


def get_cluster_ids(connection):
    result = connection.execute(
        text("SELECT id, code FROM clusters")
    )

    return {row.code: row.id for row in result}


def get_antenna_ids(connection):
    result = connection.execute(
        text("SELECT id, ecgi FROM antennas")
    )

    return {row.ecgi: row.id for row in result}


def get_subscriber_ids(connection):
    result = connection.execute(
        text("SELECT id, assinante_hash FROM subscribers")
    )

    return {row.assinante_hash: row.id for row in result}


def load_antennas(connection):
    path = csv_path("antenas_flp.csv")
    cluster_ids = get_cluster_ids(connection)

    df = pd.read_csv(path, dtype={"ecgi": str}, encoding="utf-8")
    df["cluster_code"] = df["cluster"].map(normalize_cluster)
    df["cluster_id"] = df["cluster_code"].map(cluster_ids)

    missing_clusters = (
        df[df["cluster_id"].isna()]["cluster_code"]
        .drop_duplicates()
        .tolist()
    )

    if missing_clusters:
        raise ValueError(f"Clusters de antenas no encontrados: {missing_clusters}")

    rows = []

    for _, row in df.iterrows():
        rows.append({
            "ecgi": str(row["ecgi"]).strip(),
            "cluster_id": int(row["cluster_id"]),
            "lat": to_float(row["lat"]),
            "lon": to_float(row["lon"]),
        })

    connection.execute(
        text("""
            INSERT INTO antennas (
                ecgi,
                cluster_id,
                lat,
                lon
            )
            VALUES (
                :ecgi,
                :cluster_id,
                :lat,
                :lon
            )
            ON CONFLICT (ecgi) DO UPDATE
            SET cluster_id = EXCLUDED.cluster_id,
                lat = EXCLUDED.lat,
                lon = EXCLUDED.lon
        """),
        rows,
    )

    print(f"antennas cargadas: {len(rows)}")


def load_subscribers(connection):
    path = csv_path("assinantes.csv")
    cluster_ids = get_cluster_ids(connection)

    total_rows = 0

    for chunk in pd.read_csv(path, dtype=str, chunksize=CHUNK_SIZE, encoding="utf-8"):
        chunk["home_cluster_code"] = chunk["home_cluster"].map(normalize_cluster)
        chunk["home_cluster_id"] = chunk["home_cluster_code"].map(cluster_ids)

        missing_clusters = (
            chunk[chunk["home_cluster_id"].isna()]["home_cluster_code"]
            .drop_duplicates()
            .tolist()
        )

        if missing_clusters:
            raise ValueError(f"Clusters de assinantes no encontrados: {missing_clusters}")

        rows = []

        for _, row in chunk.iterrows():
            rows.append({
                "assinante_hash": to_int(row["assinante_hash"]),
                "home_cluster_id": int(row["home_cluster_id"]),
                "income_cluster": str(row["income_cluster"]).strip().upper(),
                "age_group": str(row["age_group"]).strip(),
                "mobility_pattern": str(row["mobility_pattern"]).strip().upper(),
                "flag_flagship": to_bool_01(row["flag_flagship"]),
            })

        connection.execute(
            text("""
                INSERT INTO subscribers (
                    assinante_hash,
                    home_cluster_id,
                    income_cluster,
                    age_group,
                    mobility_pattern,
                    flag_flagship
                )
                VALUES (
                    :assinante_hash,
                    :home_cluster_id,
                    :income_cluster,
                    :age_group,
                    :mobility_pattern,
                    :flag_flagship
                )
                ON CONFLICT (assinante_hash) DO UPDATE
                SET home_cluster_id = EXCLUDED.home_cluster_id,
                    income_cluster = EXCLUDED.income_cluster,
                    age_group = EXCLUDED.age_group,
                    mobility_pattern = EXCLUDED.mobility_pattern,
                    flag_flagship = EXCLUDED.flag_flagship
            """),
            rows,
        )

        total_rows += len(rows)

    print(f"subscribers cargados: {total_rows}")


def truncate_fact_tables(connection):
    connection.execute(
        text("""
            TRUNCATE TABLE
                concentration_records,
                cluster_od_flows,
                antenna_flows,
                travel_time_stats
            RESTART IDENTITY
        """)
    )

    print("tablas analíticas chicas limpiadas")


def load_concentration_records(connection):
    path = csv_path("tensor_concentracao.csv")
    antenna_ids = get_antenna_ids(connection)

    total_rows = 0

    for chunk in pd.read_csv(
        path,
        dtype={"ecgi": str},
        chunksize=CHUNK_SIZE,
        encoding="utf-8",
    ):
        chunk["ecgi"] = chunk["ecgi"].astype(str).str.strip()
        chunk["antenna_id"] = chunk["ecgi"].map(antenna_ids)

        missing_antennas = (
            chunk[chunk["antenna_id"].isna()]["ecgi"]
            .drop_duplicates()
            .head(20)
            .tolist()
        )

        if missing_antennas:
            raise ValueError(f"Antenas no encontradas en concentration_records: {missing_antennas}")

        rows = []

        for _, row in chunk.iterrows():
            rows.append({
                "antenna_id": int(row["antenna_id"]),
                "day_date": row["day_date"],
                "session_period": normalize_period(row["periodo"]),
                "active_users": to_int(row["n_usuarios"]),
                "sessions_count": to_int(row["n_sessoes"]),
                "download_bytes": to_int(row["download_bytes"]),
                "upload_bytes": to_int(row["upload_bytes"]),
                "avg_session_duration_seconds": to_int(row["dur_media_s"]),
                "avg_drop_pct": to_float(row["drop_pct_medio"]),
                "avg_congestion": to_float(row["congestionamento_medio"]),
                "total_calls": to_int(row["chamadas_total"]),
                "total_messages": to_int(row["mensagens_total"]),
            })

        connection.execute(
            text("""
                INSERT INTO concentration_records (
                    antenna_id,
                    day_date,
                    session_period,
                    active_users,
                    sessions_count,
                    download_bytes,
                    upload_bytes,
                    avg_session_duration_seconds,
                    avg_drop_pct,
                    avg_congestion,
                    total_calls,
                    total_messages
                )
                VALUES (
                    :antenna_id,
                    :day_date,
                    :session_period,
                    :active_users,
                    :sessions_count,
                    :download_bytes,
                    :upload_bytes,
                    :avg_session_duration_seconds,
                    :avg_drop_pct,
                    :avg_congestion,
                    :total_calls,
                    :total_messages
                )
            """),
            rows,
        )

        total_rows += len(rows)

    print(f"concentration_records cargados: {total_rows}")


def load_cluster_od_flows(connection):
    path = csv_path("tensor_od.csv")
    cluster_ids = get_cluster_ids(connection)

    total_rows = 0

    for chunk in pd.read_csv(path, dtype=str, chunksize=CHUNK_SIZE, encoding="utf-8"):
        chunk["origin_code"] = chunk["cluster_origem"].map(normalize_cluster)
        chunk["destination_code"] = chunk["cluster_destino"].map(normalize_cluster)

        chunk["origin_cluster_id"] = chunk["origin_code"].map(cluster_ids)
        chunk["destination_cluster_id"] = chunk["destination_code"].map(cluster_ids)

        missing_origins = (
            chunk[chunk["origin_cluster_id"].isna()]["origin_code"]
            .drop_duplicates()
            .tolist()
        )

        missing_destinations = (
            chunk[chunk["destination_cluster_id"].isna()]["destination_code"]
            .drop_duplicates()
            .tolist()
        )

        if missing_origins or missing_destinations:
            raise ValueError(
                f"Clusters faltantes OD. Origen: {missing_origins}, Destino: {missing_destinations}"
            )

        rows = []

        for _, row in chunk.iterrows():
            rows.append({
                "origin_cluster_id": int(row["origin_cluster_id"]),
                "destination_cluster_id": int(row["destination_cluster_id"]),
                "same_cluster": to_bool_01(row["mesmo_cluster"]),
                "users_count": to_int(row["n_usuarios"]),
                "trips_count": to_int(row["n_viagens"]),
                "avg_distance_km": to_float(row["dist_media_km"]),
                "predominant_period": normalize_period(row["periodo_predominante"]),
            })

        connection.execute(
            text("""
                INSERT INTO cluster_od_flows (
                    origin_cluster_id,
                    destination_cluster_id,
                    same_cluster,
                    users_count,
                    trips_count,
                    avg_distance_km,
                    predominant_period
                )
                VALUES (
                    :origin_cluster_id,
                    :destination_cluster_id,
                    :same_cluster,
                    :users_count,
                    :trips_count,
                    :avg_distance_km,
                    :predominant_period
                )
            """),
            rows,
        )

        total_rows += len(rows)

    print(f"cluster_od_flows cargados: {total_rows}")


def load_antenna_flows(connection):
    path = csv_path("tensor_fluxo_vias.csv")
    antenna_ids = get_antenna_ids(connection)

    total_rows = 0

    for chunk in pd.read_csv(
        path,
        dtype={"ecgi_origem": str, "ecgi_destino": str},
        chunksize=CHUNK_SIZE,
        encoding="utf-8",
    ):
        chunk["ecgi_origem"] = chunk["ecgi_origem"].astype(str).str.strip()
        chunk["ecgi_destino"] = chunk["ecgi_destino"].astype(str).str.strip()

        chunk["origin_antenna_id"] = chunk["ecgi_origem"].map(antenna_ids)
        chunk["destination_antenna_id"] = chunk["ecgi_destino"].map(antenna_ids)

        missing_origins = (
            chunk[chunk["origin_antenna_id"].isna()]["ecgi_origem"]
            .drop_duplicates()
            .head(20)
            .tolist()
        )

        missing_destinations = (
            chunk[chunk["destination_antenna_id"].isna()]["ecgi_destino"]
            .drop_duplicates()
            .head(20)
            .tolist()
        )

        if missing_origins or missing_destinations:
            raise ValueError(
                f"Antenas faltantes en antenna_flows. Origen: {missing_origins}, Destino: {missing_destinations}"
            )

        rows = []

        for _, row in chunk.iterrows():
            rows.append({
                "origin_antenna_id": int(row["origin_antenna_id"]),
                "destination_antenna_id": int(row["destination_antenna_id"]),
                "users_count": to_int(row["n_usuarios"]),
                "transitions_count": to_int(row["n_transicoes"]),
                "distance_km": to_float(row["dist_km"]),
                "predominant_period": normalize_period(row["periodo_predominante"]),
                "pct_from_origin_cluster": to_float(row["pct_do_cluster_origem"]),
            })

        connection.execute(
            text("""
                INSERT INTO antenna_flows (
                    origin_antenna_id,
                    destination_antenna_id,
                    users_count,
                    transitions_count,
                    distance_km,
                    predominant_period,
                    pct_from_origin_cluster
                )
                VALUES (
                    :origin_antenna_id,
                    :destination_antenna_id,
                    :users_count,
                    :transitions_count,
                    :distance_km,
                    :predominant_period,
                    :pct_from_origin_cluster
                )
            """),
            rows,
        )

        total_rows += len(rows)

    print(f"antenna_flows cargados: {total_rows}")


def load_travel_time_stats(connection):
    path = csv_path("tensor_tempo_deslocamento.csv")
    cluster_ids = get_cluster_ids(connection)

    total_rows = 0

    for chunk in pd.read_csv(path, dtype=str, chunksize=CHUNK_SIZE, encoding="utf-8"):
        chunk["origin_code"] = chunk["cluster_origem"].map(normalize_cluster)
        chunk["destination_code"] = chunk["cluster_destino"].map(normalize_cluster)

        chunk["origin_cluster_id"] = chunk["origin_code"].map(cluster_ids)
        chunk["destination_cluster_id"] = chunk["destination_code"].map(cluster_ids)

        missing_origins = (
            chunk[chunk["origin_cluster_id"].isna()]["origin_code"]
            .drop_duplicates()
            .tolist()
        )

        missing_destinations = (
            chunk[chunk["destination_cluster_id"].isna()]["destination_code"]
            .drop_duplicates()
            .tolist()
        )

        if missing_origins or missing_destinations:
            raise ValueError(
                f"Clusters faltantes en travel_time_stats. Origen: {missing_origins}, Destino: {missing_destinations}"
            )

        rows = []

        for _, row in chunk.iterrows():
            rows.append({
                "origin_cluster_id": int(row["origin_cluster_id"]),
                "destination_cluster_id": int(row["destination_cluster_id"]),
                "same_cluster": to_bool_01(row["mesmo_cluster"]),
                "observations_count": to_int(row["n_observacoes"]),
                "avg_distance_km": to_float(row["dist_media_km"]),
                "p25_distance_km": to_float(row["dist_p25_km"]),
                "p75_distance_km": to_float(row["dist_p75_km"]),
                "predominant_period": normalize_period(row["periodo_predominante"]),
            })

        connection.execute(
            text("""
                INSERT INTO travel_time_stats (
                    origin_cluster_id,
                    destination_cluster_id,
                    same_cluster,
                    observations_count,
                    avg_distance_km,
                    p25_distance_km,
                    p75_distance_km,
                    predominant_period
                )
                VALUES (
                    :origin_cluster_id,
                    :destination_cluster_id,
                    :same_cluster,
                    :observations_count,
                    :avg_distance_km,
                    :p25_distance_km,
                    :p75_distance_km,
                    :predominant_period
                )
            """),
            rows,
        )

        total_rows += len(rows)

    print(f"travel_time_stats cargados: {total_rows}")



def truncate_mobility_records(connection):
    connection.execute(
        text("TRUNCATE TABLE mobility_records RESTART IDENTITY")
    )

    print("mobility_records limpiada")


def truncate_sequence_visits(connection):
    connection.execute(
        text("TRUNCATE TABLE sequence_visits RESTART IDENTITY")
    )

    print("sequence_visits limpiada")


def load_mobility_records(connection, max_rows: int | None):
    path = csv_path("tensor_mobilidade.csv")

    subscriber_ids = get_subscriber_ids(connection)
    antenna_ids = get_antenna_ids(connection)

    total_rows = 0

    for chunk in pd.read_csv(
        path,
        dtype={"assinante_hash": str, "ecgi": str},
        chunksize=CHUNK_SIZE,
        encoding="utf-8",
    ):
        if max_rows is not None and total_rows >= max_rows:
            break

        if max_rows is not None:
            remaining = max_rows - total_rows
            chunk = chunk.head(remaining)

        if chunk.empty:
            break

        chunk["assinante_hash_int"] = chunk["assinante_hash"].map(to_int)
        chunk["ecgi"] = chunk["ecgi"].astype(str).str.strip()

        chunk["subscriber_id"] = chunk["assinante_hash_int"].map(subscriber_ids)
        chunk["antenna_id"] = chunk["ecgi"].map(antenna_ids)

        missing_subscribers = (
            chunk[chunk["subscriber_id"].isna()]["assinante_hash"]
            .drop_duplicates()
            .head(20)
            .tolist()
        )

        missing_antennas = (
            chunk[chunk["antenna_id"].isna()]["ecgi"]
            .drop_duplicates()
            .head(20)
            .tolist()
        )

        if missing_subscribers or missing_antennas:
            raise ValueError(
                "Faltan relaciones en mobility_records. "
                f"Subscribers: {missing_subscribers}, Antennas: {missing_antennas}"
            )

        rows = []

        for _, row in chunk.iterrows():
            rows.append({
                "subscriber_id": int(row["subscriber_id"]),
                "antenna_id": int(row["antenna_id"]),
                "day_date": row["day_date"],
                "content_type": str(row["rg_type"]).strip().upper(),
                "network_type": str(row["rat_type"]).strip().upper(),
                "session_period": normalize_period(row["periodo_sessao"]),
                "sessions_count": to_int(row["n_sessoes"]),
                "total_duration_seconds": to_int(row["dur_total_s"]),
                "download_bytes": to_float(row["download_bytes"]),
                "upload_bytes": to_float(row["upload_bytes"]),
                "drop_pct": to_float(row["drop_pct"]),
                "congestion_level": to_float(row["congestionamento"]),
                "calls_count": to_int(row["chamadas"]),
                "voice_seconds": to_int(row["conversacao_seg"]),
                "voice_completion_rate": to_float(row["completamento_voz"]),
                "voice_congestion": to_float(row["cong_voz"]),
                "messages_count": to_int(row["mensagens"]),
                "sms_completion_rate": to_float(row["completamento_sms"]),
                "sms_congestion": to_float(row["cong_sms"]),
                "streaming_sessions": to_int(row["rg_streaming"]),
                "game_sessions": to_int(row["rg_game"]),
                "social_sessions": to_int(row["rg_social"]),
                "communication_sessions": to_int(row["rg_comunicacao"]),
                "other_sessions": to_int(row["rg_outros"]),
            })

        if rows:
            connection.execute(
                text("""
                    INSERT INTO mobility_records (
                        subscriber_id,
                        antenna_id,
                        day_date,
                        content_type,
                        network_type,
                        session_period,
                        sessions_count,
                        total_duration_seconds,
                        download_bytes,
                        upload_bytes,
                        drop_pct,
                        congestion_level,
                        calls_count,
                        voice_seconds,
                        voice_completion_rate,
                        voice_congestion,
                        messages_count,
                        sms_completion_rate,
                        sms_congestion,
                        streaming_sessions,
                        game_sessions,
                        social_sessions,
                        communication_sessions,
                        other_sessions
                    )
                    VALUES (
                        :subscriber_id,
                        :antenna_id,
                        :day_date,
                        :content_type,
                        :network_type,
                        :session_period,
                        :sessions_count,
                        :total_duration_seconds,
                        :download_bytes,
                        :upload_bytes,
                        :drop_pct,
                        :congestion_level,
                        :calls_count,
                        :voice_seconds,
                        :voice_completion_rate,
                        :voice_congestion,
                        :messages_count,
                        :sms_completion_rate,
                        :sms_congestion,
                        :streaming_sessions,
                        :game_sessions,
                        :social_sessions,
                        :communication_sessions,
                        :other_sessions
                    )
                """),
                rows,
            )

        total_rows += len(rows)
        print(f"mobility_records parcial: {total_rows}")

    print(f"mobility_records cargados: {total_rows}")


def load_sequence_visits(connection, max_rows: int | None):
    path = csv_path("tensor_sequencias.csv")

    subscriber_ids = get_subscriber_ids(connection)
    antenna_ids = get_antenna_ids(connection)

    total_rows = 0

    for chunk in pd.read_csv(
        path,
        dtype={"assinante_hash": str, "ecgi": str},
        chunksize=CHUNK_SIZE,
        encoding="utf-8",
    ):
        if max_rows is not None and total_rows >= max_rows:
            break

        if max_rows is not None:
            remaining = max_rows - total_rows
            chunk = chunk.head(remaining)

        if chunk.empty:
            break

        chunk["assinante_hash_int"] = chunk["assinante_hash"].map(to_int)
        chunk["ecgi"] = chunk["ecgi"].astype(str).str.strip()

        chunk["subscriber_id"] = chunk["assinante_hash_int"].map(subscriber_ids)
        chunk["antenna_id"] = chunk["ecgi"].map(antenna_ids)

        missing_subscribers = (
            chunk[chunk["subscriber_id"].isna()]["assinante_hash"]
            .drop_duplicates()
            .head(20)
            .tolist()
        )

        missing_antennas = (
            chunk[chunk["antenna_id"].isna()]["ecgi"]
            .drop_duplicates()
            .head(20)
            .tolist()
        )

        if missing_subscribers or missing_antennas:
            raise ValueError(
                "Faltan relaciones en sequence_visits. "
                f"Subscribers: {missing_subscribers}, Antennas: {missing_antennas}"
            )

        rows = []

        for _, row in chunk.iterrows():
            rows.append({
                "subscriber_id": int(row["subscriber_id"]),
                "antenna_id": int(row["antenna_id"]),
                "day_date": row["day_date"],
                "sequence_number": to_int(row["seq_num"]),
                "arrival_time": row["arrival_time"],
                "stay_seconds": to_int(row["permanencia_seg"]),
                "session_period": normalize_period(row["periodo_sessao"]),
                "distance_km_from_previous": to_float(row["distancia_km_anterior"]),
                "sessions_count": to_int(row["n_sessoes"]),
            })

        if rows:
            connection.execute(
                text("""
                    INSERT INTO sequence_visits (
                        subscriber_id,
                        antenna_id,
                        day_date,
                        sequence_number,
                        arrival_time,
                        stay_seconds,
                        session_period,
                        distance_km_from_previous,
                        sessions_count
                    )
                    VALUES (
                        :subscriber_id,
                        :antenna_id,
                        :day_date,
                        :sequence_number,
                        :arrival_time,
                        :stay_seconds,
                        :session_period,
                        :distance_km_from_previous,
                        :sessions_count
                    )
                """),
                rows,
            )

        total_rows += len(rows)
        print(f"sequence_visits parcial: {total_rows}")

    print(f"sequence_visits cargados: {total_rows}")


def print_counts(connection):
    tables = [
        "municipalities",
        "clusters",
        "antennas",
        "subscribers",
        "concentration_records",
        "cluster_od_flows",
        "antenna_flows",
        "travel_time_stats",
        "mobility_records",
        "sequence_visits",
    ]

    print("\nResumen:")

    for table in tables:
        count = connection.execute(
            text(f"SELECT COUNT(*) FROM {table}")
        ).scalar_one()

        print(f"{table}: {count}")


def main():
    engine = build_engine()

    with engine.begin() as connection:
        insert_municipalities(connection)
        insert_clusters(connection)
        load_antennas(connection)
        load_subscribers(connection)

        truncate_fact_tables(connection)

        load_concentration_records(connection)
        load_cluster_od_flows(connection)
        load_antenna_flows(connection)
        load_travel_time_stats(connection)

        if LOAD_MOBILITY:
            truncate_mobility_records(connection)
            max_rows = None if MAX_MOBILITY_ROWS <= 0 else MAX_MOBILITY_ROWS
            load_mobility_records(connection, max_rows)
        else:
            print("mobility_records omitido. Activar con LOAD_MOBILITY=true")

        if LOAD_SEQUENCES:
            truncate_sequence_visits(connection)
            max_rows = None if MAX_SEQUENCE_ROWS <= 0 else MAX_SEQUENCE_ROWS
            load_sequence_visits(connection, max_rows)
        else:
            print("sequence_visits omitido. Activar con LOAD_SEQUENCES=true")

        print_counts(connection)


if __name__ == "__main__":
    main()