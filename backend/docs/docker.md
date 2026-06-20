# Docker - DB para el dataset Visent

Este documento resume los comandos principales para levantar la base de datos PostgreSQL y cargar el dataset Vísent en el entorno local.

## 1. Levantar PostgreSQL

Desde la carpeta `backend`:

```bash
docker compose up -d postgres
```

## 2. Bajar los contenedores

```bash
docker compose down
```

---

## 3. Bajar contenedores y borrar datos

> Cuidado: este comando elimina el volumen de PostgreSQL y borra los datos cargados.

```bash
docker compose down -v
```

Después de usar este comando, hay que volver a levantar PostgreSQL y cargar los datos nuevamente.


---

## 4. Ubicación de los CSVs

Antes de ejecutar el loader, los archivos CSV del dataset Vísent deben estar dentro de:
```bash
backend/data/visent
```
---

## 5. Ejecutar el loader básico de Vísent

Este comando carga las tablas principales del dataset Vísent.

```bash
docker compose --profile loader run --rm visent-loader
```

Carga principalmente:

* `municipalities`
* `clusters`
* `antennas`
* `subscribers`
* `concentration_records`
* `cluster_od_flows`
* `antenna_flows`
* `travel_time_stats`

Por defecto, las tablas más pesadas pueden quedar omitidas.

---

## 6. Cargar `mobility_records` con límite de filas

Para cargar solo 10.000 registros de `mobility_records`:

```bash
docker compose --profile loader run --rm -e LOAD_MOBILITY=true -e MAX_MOBILITY_ROWS=10000 visent-loader
```

Para cargar todos los registros de `mobility_records`:

```bash
docker compose --profile loader run --rm -e LOAD_MOBILITY=true -e MAX_MOBILITY_ROWS=0 visent-loader
```

---

## 7. Cargar `sequence_visits` con límite de filas

Para cargar solo 10.000 registros de `sequence_visits`:

```bash
docker compose --profile loader run --rm -e LOAD_SEQUENCES=true -e MAX_SEQUENCE_ROWS=10000 visent-loader
```

Para cargar todos los registros de `sequence_visits`:

```bash
docker compose --profile loader run --rm -e LOAD_SEQUENCES=true -e MAX_SEQUENCE_ROWS=0 visent-loader
```

---

## 8. Cargar `mobility_records` y `sequence_visits` juntas

```bash
docker compose --profile loader run --rm -e LOAD_MOBILITY=true -e MAX_MOBILITY_ROWS=10000 -e LOAD_SEQUENCES=true -e MAX_SEQUENCE_ROWS=10000 visent-loader
```

---

## 9. Verificar cantidad de registros

Entrar a PostgreSQL:

```bash
docker exec -it appbit_postgres_local psql -U postgres -d appbit_db
```

Ejecutar:

```sql
SELECT 'municipalities' AS table_name, COUNT(*) AS rows_count FROM municipalities
UNION ALL
SELECT 'clusters', COUNT(*) FROM clusters
UNION ALL
SELECT 'antennas', COUNT(*) FROM antennas
UNION ALL
SELECT 'subscribers', COUNT(*) FROM subscribers
UNION ALL
SELECT 'concentration_records', COUNT(*) FROM concentration_records
UNION ALL
SELECT 'cluster_od_flows', COUNT(*) FROM cluster_od_flows
UNION ALL
SELECT 'antenna_flows', COUNT(*) FROM antenna_flows
UNION ALL
SELECT 'travel_time_stats', COUNT(*) FROM travel_time_stats
UNION ALL
SELECT 'mobility_records', COUNT(*) FROM mobility_records
UNION ALL
SELECT 'sequence_visits', COUNT(*) FROM sequence_visits;
```

