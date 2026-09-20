# Spark

Develops and runs Apache Spark jobs: spark-submit, interactive shells, SQL, and package management.

## Instructions

# Spark

Develops and operates Apache Spark batch jobs: submission, tuning, SQL analysis,
and debugging.

## When to Use

- Processing large datasets in batch
- Interactive analysis with pyspark/spark-shell
- Tuning shuffle and memory for slow jobs

## Real Commands

```bash
# Local development run
spark-submit --master local[4] --executor-memory 4g jobs/wordcount.py

# YARN cluster run
spark-submit --master yarn --deploy-mode cluster \
  --num-executors 8 --executor-cores 4 --executor-memory 8g etl.py

# With Python dependencies
spark-submit --master local[*] --py-files utils.py,models.zip job.py

# Spark SQL
spark-sql -f queries/aggregate.sql --conf spark.sql.shuffle.partitions=200

# Interactive
pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0
spark-shell --master yarn --deploy-mode client
```

## Tuning Cheat Sheet

- Total executors ~= cluster cores / 4
- Shuffle partitions ~= 2-4x executors x cores
- Use broadcast joins for small tables (`spark.sql.autoBroadcastJoinThreshold`)
- Cache hot DataFrames; unpersist after use
- Monitor via Spark UI port 4040

## Best Practices

- Test on a sample with `local[*]` before cluster runs
- Use `--py-files` for local modules
- Set `spark.sql.shuffle.partitions` explicitly
- Check for data skew in GROUP BY keys
- Persist intermediate results only when reused

## Example Response

For a slow job: reviews the Spark UI metrics, identifies shuffle-heavy stages or
skew, and applies tuning options with expected impact.

## Capabilities

### spark-submit
Submit batch jobs with cluster/local masters and dependencies

**Commands:**
- `spark-submit --master local[4] --executor-memory 4g jobs/wordcount.py`
- `spark-submit --master yarn --deploy-mode cluster --num-executors 8 --executor-cores 4 etl.py`
- `pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0`
- `spark-shell --master yarn --deploy-mode client -i setup.scala`
- `spark-sql -f queries/aggregate.sql --conf spark.sql.shuffle.partitions=200`

**Examples:**
- spark-submit --master local[*] --py-files utils.py job.py
- spark-submit --master k8s://https://k8s:6443 --deploy-mode cluster --conf spark.kubernetes.container.image=img job.py
- pyspark -i init.sql
