# Example Repo Used in Get Started with Data Engineering on Databricks


# GitHub Integration with Databricks

## 1. Connect GitHub to Databricks
1. In the Databricks workspace, click your **user icon** (top-right) → **User Settings**.
2. Go to the **Git Integration** tab.
3. Select **Git provider** as `GitHub`.
4. Enter a **GitHub personal access token** (PAT) with `repo` scope.  
   - Generate from GitHub: **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)** → **Generate new token**.
5. Click **Save**.

---

## 2. Fork a Public GitHub Repository
1. Go to the public repo you want in GitHub.
2. Click **Fork** → choose your account.

---

## 3. Clone the Fork into Databricks Repo
1. In Databricks workspace → **Repos** (left menu).
2. Click **Add Repo**.
3. Paste the HTTPS or SSH URL of your forked repo.
4. Select branch and **Create Repo**.

---

## 4. Commit & Push Changes from Databricks
1. Open the repo in Databricks.
2. Make your changes in a notebook (e.g., PySpark code).
3. From the notebook menu, click **File** → **Save Revision**.
4. In the Repo menu (top bar), click **Commit & Push**.
5. Add commit message, confirm, and push.

Example PySpark code you can commit:
```python
df = spark.read.csv("/databricks-datasets/airlines/part-00000", header=True, inferSchema=True)
df.groupBy("Origin").count().show()
```

---


# Working with Files in Databricks Free/Serverless Edition

## 1. Why DBFS paths fail in Serverless
In Community Edition, you could use:
```
%fs ls /FileStore/tables/
```
But in Free/Serverless Edition, **public DBFS root is disabled**, so `/FileStore` paths cause:
```
ExecutionError: Public DBFS root is disabled. Access is denied...
```
**Solution:** Use **Unity Catalog Volumes** (or `hive_metastore` volumes if Unity Catalog isn’t enabled).

---

## 2. Check which catalogs you have
```python
spark.sql("SHOW CATALOGS").show(truncate=False)
```
If `main` is missing, use `hive_metastore`.

---

## 3. Create a volume
```python
catalog = "hive_metastore"   # or "main" if you have it
schema = "default"
volume_name = "vol1"

spark.sql(f"CREATE VOLUME IF NOT EXISTS {catalog}.{schema}.{volume_name}")
```

---

## 4. Upload files to the volume
1. Go to **Data** → select catalog & schema → **Volumes**
2. Select your volume (e.g., `vol1`)
3. Click **Upload** and choose your file.

---

## 5. List files in the volume
```python
%fs ls /Volumes/hive_metastore/default/vol1
# or
dbutils.fs.ls("/Volumes/hive_metastore/default/vol1")
```

---

## 6. Read files from the volume
```python
file_name = "your_file.csv"

df = spark.read.format("csv") \\
    .option("inferSchema", True) \\
    .option("header", True) \\
    .load(f"/Volumes/{catalog}/{schema}/{volume_name}/{file_name}")

display(df)
```

---

## 7. Optional: Set default catalog/schema for SQL
```python
spark.sql("USE CATALOG hive_metastore")
spark.sql("USE SCHEMA default")
```
Still need full `/Volumes/<catalog>/<schema>/...` path when reading files.
