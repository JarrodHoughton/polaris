import sys
from pyspark.sql import SparkSession
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import max
from pyspark.sql.functions import *
from awsglue.dynamicframe import DynamicFrame

from pyspark.sql.window import Window
from pyspark.sql.functions import rank
from pyspark.sql.functions import col
from pyspark.conf import SparkConf

DATABASE = "cranberry"
SOURCE_TABLE = "query_actions"
TARGET_TABLE = "query_actions_iceberg"

# Column to order the records by the latest updated time
ORDER_BY = "max_op_date"

# Unique columns to perform the merge
UNIQUE_COLS = ["sort_order", "query_id"]

# Schema of the target table
TARGET_SCHEMA = [
    {"Name": "sort_order", "Type": "int"},
    {"Name": "query_id", "Type": "string"},
    {"Name": "modified_date", "Type": "timestamp"},
    {"Name": "action_taken", "Type": "string"},
    {"Name": "system_id", "Type": "string"},
    {"Name": "transact_seq", "Type": "bigint"}
]









# Convert the target schema columns to an array of column names. Used to filter the unwanted columns from the source table 
TARGET_SCHEMA_COLUMNS = []

for column in TARGET_SCHEMA:
    TARGET_SCHEMA_COLUMNS.append(column.get('Name'))

conf = SparkConf()

## Please make sure to pass runtime argument --iceberg_job_catalog_warehouse with value as the S3 path
conf.set(
    "spark.sql.catalog.job_catalog.warehouse", args["iceberg_job_catalog_warehouse"]
)
conf.set("spark.sql.catalog.job_catalog", "org.apache.iceberg.spark.SparkCatalog")
conf.set(
    "spark.sql.catalog.job_catalog.catalog-impl",
    "org.apache.iceberg.aws.glue.GlueCatalog",
)
conf.set("spark.sql.catalog.job_catalog.io-impl", "org.apache.iceberg.aws.s3.S3FileIO")
conf.set(
    "spark.sql.extensions",
    "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
)
conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
conf.set("spark.sql.iceberg.handle-timestamp-without-timezone", "true")
conf.set("spark.executor.memoryOverhead", "512")
conf.set("spark.driver.memory", "12g")
conf.set("spark.sql.debug.maxToStringFields", 1000)
sc = SparkContext(conf=conf)
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# %%

## Read Input Table
IncrementalInputDyF = glueContext.create_dynamic_frame.from_catalog(
    database=DATABASE, table_name=SOURCE_TABLE, transformation_ctx="IncrementalInputDyF"
)
IncrementalInputDF = IncrementalInputDyF.toDF()

if not IncrementalInputDF.rdd.isEmpty():
    # Convert columns to the target table's schema

    for column in TARGET_SCHEMA:
        IncrementalInputDF = IncrementalInputDF.withColumn(
            column.get('Name'), col(column.get('Name')).cast(column.get('Type'))
        )

    # Apply De-duplication logic on input data, to pickup latest record based on timestamp and operation
    IDWindowDF = (
        Window.partitionBy(IncrementalInputDF.modified_date)
        .orderBy(IncrementalInputDF.last_update_time)
        .rangeBetween(-sys.maxsize, sys.maxsize)
    )

    # Add new columns to capture first and last OP value and what is the latest timestamp
    inputDFWithTS = IncrementalInputDF.withColumn(
        ORDER_BY, max(IncrementalInputDF.last_update_time).over(IDWindowDF)
    )

    # Filter out new records that are inserted, then select latest record from existing records and merge both to get deduplicated output
    NewInsertsDF = inputDFWithTS.filter("op = 'I'").dropDuplicates()

    UpdateDeleteDF = inputDFWithTS.filter("op IN ('U', 'D')")

    # Register the deduplicated input as temporary table to use in Iceberg Spark SQL statements
    NewInsertsDF.createOrReplaceTempView("incremental_input_data")
    # NewInsertsDF.show()


# %%
# Sort data by the latest max_op date for each unique row

partition_by = ""

for col in UNIQUE_COLS:
    partition_by += f"{col},"

partition_by = partition_by[:-1]

SortedInsertsDF = spark.sql(
    f"""
                SELECT s.*,
                ROW_NUMBER() OVER (PARTITION BY {partition_by}  ORDER BY s.{ORDER_BY} DESC) AS rn
                FROM incremental_input_data AS s
        """
)

SortedInsertsDF.createOrReplaceTempView("sorted_inserts_data")
# SortedInsertsDF.show()

# %%


# on match statement
on_match_statement = ""

for col in UNIQUE_COLS:
    on_match_statement += f"t.{col} = s.{col} AND "

# remove the last AND
on_match_statement = on_match_statement[:-5]
on_match_statement += " AND rn=1"

match_and_update = ""

# set all the columns equal on the insert

for column in IncrementalInputDF.columns:
    if column in TARGET_SCHEMA_COLUMNS and column not in UNIQUE_COLS:
        match_and_update += f"t.{column} = s.{column},"

# remove the last comma
match_and_update = match_and_update[:-1]

# not matched and insert
inserting_cols = ""
inserting_values = ""

for column in IncrementalInputDF.columns:
    if column in TARGET_SCHEMA_COLUMNS:
        inserting_cols += f"{column},"
        inserting_values += f"s.{column},"

# remove the last comma
inserting_cols = inserting_cols[:-1]
inserting_values = inserting_values[:-1]

no_match_insert = f"({inserting_cols}) VALUES ({inserting_values})"


merge_query = f"""
       MERGE INTO job_catalog.{DATABASE}.{TARGET_TABLE} t
        USING (
              SELECT * FROM sorted_inserts_data AS s 
              )
        ON {on_match_statement}
        WHEN MATCHED AND s.op = 'I' THEN UPDATE SET 
            {match_and_update}
        WHEN NOT MATCHED THEN INSERT
            {no_match_insert}
    """

print("GENERATED MERGE QUERY:", merge_query)

# Perform the mmerge with the full load data
IcebergMergeFullLoadOutputDF = spark.sql(merge_query)

job.commit()

# %%