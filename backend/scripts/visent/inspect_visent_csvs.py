import os
from pathlib import Path

import pandas as pd


DATA_DIR = Path(os.getenv("VISENT_DATA_DIR", "/app/data/visent"))

FILES = [
    "antenas_flp.csv",
    "assinantes.csv",
    "tensor_concentracao.csv",
    "tensor_od.csv",
    "tensor_fluxo_vias.csv",
    "tensor_tempo_deslocamento.csv",
    "tensor_mobilidade.csv",
    "tensor_sequencias.csv",
]

EXPECTED_COLUMNS = {
    "antenas_flp.csv": [
        "ecgi",
        "cluster",
        "municipio",
        "lat",
        "lon",
    ],
    "assinantes.csv": [
        "assinante_hash",
        "home_cluster",
        "home_municipio",
        "income_cluster",
        "age_group",
        "mobility_pattern",
        "flag_flagship",
    ],
    "tensor_concentracao.csv": [
        "ecgi",
        "cluster",
        "municipio",
        "day_date",
        "periodo",
        "n_usuarios",
        "n_sessoes",
        "download_bytes",
        "upload_bytes",
        "dur_media_s",
        "drop_pct_medio",
        "congestionamento_medio",
        "chamadas_total",
        "mensagens_total",
        "lat",
        "lon",
    ],
    "tensor_od.csv": [
        "cluster_origem",
        "municipio_origem",
        "lat_origem",
        "lon_origem",
        "cluster_destino",
        "municipio_destino",
        "lat_destino",
        "lon_destino",
        "mesmo_cluster",
        "n_usuarios",
        "n_viagens",
        "dist_media_km",
        "periodo_predominante",
    ],
    "tensor_fluxo_vias.csv": [
        "ecgi_origem",
        "lat_origem",
        "lon_origem",
        "cluster_origem",
        "municipio_origem",
        "ecgi_destino",
        "lat_destino",
        "lon_destino",
        "cluster_destino",
        "municipio_destino",
        "n_usuarios",
        "n_transicoes",
        "dist_km",
        "periodo_predominante",
        "pct_do_cluster_origem",
    ],
    "tensor_tempo_deslocamento.csv": [
        "cluster_origem",
        "cluster_destino",
        "mesmo_cluster",
        "n_observacoes",
        "dist_media_km",
        "dist_p25_km",
        "dist_p75_km",
        "periodo_predominante",
    ],
    "tensor_mobilidade.csv": [
        "assinante_hash",
        "day_date",
        "ecgi",
        "cluster",
        "municipio",
        "rg_type",
        "rat_type",
        "periodo_sessao",
        "n_sessoes",
        "dur_total_s",
        "download_bytes",
        "upload_bytes",
        "drop_pct",
        "congestionamento",
        "chamadas",
        "conversacao_seg",
        "completamento_voz",
        "mensagens",
        "income_cluster",
        "age_group",
        "flag_flagship",
        "cong_voz",
        "completamento_sms",
        "cong_sms",
        "rg_streaming",
        "rg_game",
        "rg_social",
        "rg_comunicacao",
        "rg_outros",
    ],
    "tensor_sequencias.csv": [
        "assinante_hash",
        "day_date",
        "seq_num",
        "ecgi",
        "cluster",
        "municipio",
        "lat",
        "lon",
        "arrival_time",
        "permanencia_seg",
        "periodo_sessao",
        "distancia_km_anterior",
        "n_sessoes",
    ],
}


def validate_columns(file_name: str, actual_columns: list[str]) -> None:
    expected_columns = EXPECTED_COLUMNS[file_name]

    missing_columns = [
        column for column in expected_columns
        if column not in actual_columns
    ]

    extra_columns = [
        column for column in actual_columns
        if column not in expected_columns
    ]

    if not missing_columns:
        print("Columnas esperadas: OK")
    else:
        print("Columnas faltantes:")
        print(missing_columns)

    if extra_columns:
        print("Columnas extra:")
        print(extra_columns)


def inspect_file(file_name: str) -> None:
    path = DATA_DIR / file_name

    print(f"\n=== {file_name} ===")

    if not path.exists():
        print(f"No existe: {path}")
        return

    df = pd.read_csv(
        path,
        nrows=5,
        dtype=str,
        encoding="utf-8",
    )

    actual_columns = df.columns.tolist()

    print("Columnas:")
    print(actual_columns)

    validate_columns(file_name, actual_columns)

    print("\nPrimeras filas:")
    print(df.head())


def main() -> None:
    print(f"Directorio de datos: {DATA_DIR}")

    for file_name in FILES:
        inspect_file(file_name)


if __name__ == "__main__":
    main()