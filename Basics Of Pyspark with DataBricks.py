# Databricks notebook source
# MAGIC %md
# MAGIC ### HELLO FROM DATA BRICKS

# COMMAND ----------

# MAGIC %md
# MAGIC #### _DATA READING_:
# MAGIC ##### spark.read is dataframe reader api in pyspark to read the data from deffrent source and use .formate(csv,parquet,api,) then option() used for schema and header  load() take url to read the data set

# COMMAND ----------

# MAGIC %md
# MAGIC ###### USING DBUTILS CHECK THE PATH OF TABLE IN FILE STORE PATH 

# COMMAND ----------

# MAGIC %md
# MAGIC Step-by-Step: Upload & Read Files in Free Databricks (Serverless)
# MAGIC
# MAGIC
# MAGIC 1️⃣ Create a Managed Volume
# MAGIC Run this in a cell in your notebook (replace vol1 with your preferred name):

# COMMAND ----------

spark.sql("SHOW CATALOGS").show(truncate=False)


# COMMAND ----------

catalog = "workspace"      # default catalog in free edition
schema = "default"    # default schema
volume_name = "general_volume"  # your volume name

spark.sql(f"""
CREATE VOLUME IF NOT EXISTS {catalog}.{schema}.{volume_name}
""")


# COMMAND ----------

# MAGIC %md
# MAGIC 2️⃣ Upload Your File to the Volume
# MAGIC In the Databricks workspace UI, go to:
# MAGIC Data → Volumes
# MAGIC Navigate to workspace > default >general_volume('your created volume name')
# MAGIC Click Upload and choose your CSV file.
# MAGIC This uploads your file to:

# COMMAND ----------

# MAGIC %md
# MAGIC  3️⃣  Notes & Gotchas
# MAGIC Don’t use /FileStore/ or dbfs:/ — these paths are blocked in serverless.
# MAGIC You can also use databricks-datasets for sample data:
# MAGIC

# COMMAND ----------

# MAGIC %fs ls /Volumes/workspace/default/general_volume/
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC 4️⃣ Read the File in PySpark
# MAGIC After upload, read it like this:

# COMMAND ----------

df = spark.read.format("csv") \
    .option("header", True) \
    .option("inferSchema", True) \
    .load("/Volumes/workspace/default/general_volume/BigMart_Sales.csv")

display(df)

# COMMAND ----------

df.show() #formate is ugly

# COMMAND ----------

df.display() #output formate display is look better 

# COMMAND ----------

# MAGIC %md
# MAGIC #### _READ JSON DATA_

# COMMAND ----------

# MAGIC %md
# MAGIC WE USE \ for lack of space in cell  or continue the code 

# COMMAND ----------

df_json = spark.read.format('json').option('inferSchema',True)\
                    .option('header',True)\
                    .option('mutiline',False)\
                    .load('/Volumes/workspace/default/general_volume/drivers.json')

# COMMAND ----------

df_json.display()

# COMMAND ----------

df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Schema Define 

# COMMAND ----------

df_json.printSchema()

# COMMAND ----------

df.printSchema() #after running we can see the schema and also have nullable value means we need to handle the null value 

# COMMAND ----------

# MAGIC %md
# MAGIC ######## IF YOU WANT TO CHNAGE THE SCHEMA TYPE IN DATAFRAME WE HAVE 2 WAY USING DDL AND StructType()

# COMMAND ----------

# MAGIC %md
# MAGIC #### DDL Schema
# MAGIC  

# COMMAND ----------

# MAGIC %md
# MAGIC print the dataframes columns

# COMMAND ----------

df.schema.names

# COMMAND ----------

# MAGIC %md
# MAGIC ###### we use ''' beacuse we have multiline schema  & we change the schema of item_weight double to string.

# COMMAND ----------

my_ddl_schema = ''' 
                    Item_Identifier STRING,
                    Item_Weight STRING,  
                    Item_Fat_Content STRING,
                    Item_Visibility DOUBLE,
                    Item_Type STRING,
                    Item_MRP DOUBLE,
                    Outlet_Identifier STRING,
                    Outlet_Establishment_Year INTEGER,
                    Outlet_Size STRING,
                    Outlet_Location_Type STRING,
                    Outlet_Type STRING,
                    Item_Outlet_Sales DOUBLE
                '''    

# COMMAND ----------

# MAGIC %md
# MAGIC now here we apply our updated schema to df  dataframe and this time we dont use the option(inferschema) we use .schema(schema_name)

# COMMAND ----------

df = spark.read.format('csv').schema(my_ddl_schema).option('header',True).load('/Volumes/workspace/default/general_volume/drivers.json')

# COMMAND ----------

df.printSchema()

# COMMAND ----------

df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC Above we change the data type of weight double to string for the practical purpouse now chnage it to normal form 

# COMMAND ----------

my_ddl_schema = ''' 
                    Item_Identifier STRING,
                    Item_Weight DOUBLE,  
                    Item_Fat_Content STRING,
                    Item_Visibility DOUBLE,
                    Item_Type STRING,
                    Item_MRP DOUBLE,
                    Outlet_Identifier STRING,
                    Outlet_Establishment_Year INTEGER,
                    Outlet_Size STRING,
                    Outlet_Location_Type STRING,
                    Outlet_Type STRING,
                    Item_Outlet_Sales DOUBLE
                ''' 

# COMMAND ----------

df = spark.read.format('csv').schema(my_ddl_schema).option('header',True).load('/Volumes/workspace/default/general_volume/BigMart_Sales.csv')

# COMMAND ----------

df.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ### SELECT 

# COMMAND ----------

# MAGIC %md
# MAGIC usually it is fine to use select and make another dataframe using some specific columns but COL Object is effective approch beacuse in aggregation and function opration on oftern used and easy to use 

# COMMAND ----------

# MAGIC %md
# MAGIC ### ALIAS 
# MAGIC same as we used in sql statement referrefed column actual name with other name

# COMMAND ----------

from pyspark.sql.functions import col
df.select(col('Item_Identifier').alias('ID')).display()

# COMMAND ----------

df.select('Item_Identifier','Item_Weight','Item_Fat_Content','Item_Visibility','Item_Type').display();

# COMMAND ----------

df.filter(col('Item_Weight').isNull()).display()

# COMMAND ----------

df.display()

# COMMAND ----------

df.filter((col('Item_Fat_Content')=='Regular') & (col('Item_Type')=='Canned')).display();
