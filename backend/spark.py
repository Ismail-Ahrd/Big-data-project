import os
from datetime import datetime
import pytz
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_timestamp, sum as _sum, date_format, split, col

spark = SparkSession.builder.appName("SalesAggregation").getOrCreate()

def process_logs(input_dir, output_base_dir):
    gmt_plus_1 = pytz.timezone("Etc/GMT-1")
    current_timestamp = datetime.now(gmt_plus_1).strftime('%Y%m%d%H')
    print("--------------------------------------------------------")
    print(current_timestamp)
    print("--------------------------------------------------------")
    log_dir_path = os.path.join(input_dir, current_timestamp)

    if not os.path.exists(log_dir_path):
        print(f"Log directory does not exist: {log_dir_path}")
        return

    log_files = [
        os.path.join(log_dir_path, f) for f in os.listdir(log_dir_path)
        if f.endswith('.txt') and not f.endswith('.crc')
    ]

    if not log_files:
        print(f"No log files found in directory: {log_dir_path}")
        return

    print(f"Found log files: {log_files}")  

    df = spark.read.text(log_files)

    print("Showing a few rows of the raw log data:")
    df.show(5, truncate=False)

    df_parsed = df.select(
        to_timestamp(df['value'].substr(1, 19), 'yyyy/MM/dd HH:mm:ss').alias('timestamp'),
        df['value'].substr(21, 100).alias('log_data')
    )

    print("Showing a few rows of the parsed data:")
    df_parsed.show(5, truncate=False)

    df_split = df_parsed.withColumn(
        "action", split(df_parsed['log_data'], r'\|')[0]  
    ).withColumn(
        "product", split(df_parsed['log_data'], r'\|')[1]  
    ).withColumn(
        "quantity", split(df_parsed['log_data'], r'\|')[2].cast('int')  
    ).withColumn(
        "price", split(df_parsed['log_data'], r'\|')[3].cast('double')  
    ).withColumn(
        "route", split(df_parsed['log_data'], r'\|')[4]  
    )

    print("Showing a few rows of the split data:")
    df_split.show(5, truncate=False)

    df_filtered = df_split.filter(df_split['action'] == 'buy')

    print("Showing a few rows of the filtered data (action == 'buy'):")
    df_filtered.show(5, truncate=False)

    df_filtered = df_filtered.withColumn('hour', date_format(df_filtered['timestamp'], 'yyyy/MM/dd HH'))

    print("Showing a few rows of the data with the hour column:")
    df_filtered.show(5, truncate=False)

    df_aggregated = df_filtered.groupBy(
        'hour',
        'product'
    ).agg(
        _sum(col('price') * col('quantity')).alias('total_price')  # Sum of price * quantity for each product
    )

    print("Showing a few rows of the aggregated data:")
    df_aggregated.show(5, truncate=False)

    df_output = df_aggregated.select(
        'hour', 'product', 'total_price'
    ).orderBy('hour')

    print("Showing the final output before writing to disk:")
    df_output.show(5, truncate=False)

    output_data = df_output.rdd.map(lambda row: f"{row['hour']}| {row['product']}| {row['total_price']}").collect()

    output_path = os.path.join(output_base_dir, current_timestamp + ".txt")

    with open(output_path, 'w') as f:
        for line in output_data:
            f.write(line + "\n")

    print(f"Data has been written to {output_path}")

input_dir = "/app/logs"  
output_base_dir = "/app/output"

while True:
    process_logs(input_dir, output_base_dir)
    
    time.sleep(3600)

spark.stop()
