# Import necessary Spark libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, isnan
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier, DecisionTreeClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

# Initialize Spark session with necessary configuration
spark_session = SparkSession.builder \
    .master("local") \
    .appName("WineQualityAnalysis") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.2.2") \
    .getOrCreate()

# Configuring Spark to access AWS S3
# Replace placeholders with actual AWS credentials
spark_session.sparkContext._jsc.hadoopConfiguration().set("com.amazonaws.services.s3.enableV4", "true")
spark_session.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
spark_session.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider", "com.amazonaws.auth.InstanceProfileCredentialsProvider,com.amazonaws.auth.DefaultAWSCredentialsProviderChain")
spark_session.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", "your_access_key")
spark_session.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "your_secret_key")
spark_session.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "s3.us-east-1.amazonaws.com")

# Load datasets from S3
train_dataset = spark_session.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("sep", ";") \
    .load("s3a://cldassign2/TrainingDataset.csv")

validation_dataset = spark_session.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("sep", ";") \
    .load("s3a://cldassign2/ValidationDataset.csv")

# Validate successful data load
if train_dataset.count() > 0 and validation_dataset.count() > 0:
    print("Data successfully loaded from S3")
else:
    print("Data load error")

# Renaming columns for consistency
column_mappings = {
    # Add your column mappings here
    # 'Old Column Name': 'New Column Name'
}

# Applying column renaming
for old_name, new_name in column_mappings.items():
    train_dataset = train_dataset.withColumnRenamed(old_name, new_name)
    validation_dataset = validation_dataset.withColumnRenamed(old_name, new_name)

# Checking for missing values
for column in train_dataset.columns:
    missing_count = train_dataset.filter(col(column).isNull() | isnan(col(column))).count()
    print(f"Column '{column}' has {missing_count} missing values.")

# Splitting the training dataset
train_data, test_data = train_dataset.randomSplit([0.7, 0.3], seed=42)

# Data preprocessing steps
feature_assembler = VectorAssembler(
    inputCols=['fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar', 'chlorides',
               'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density', 'pH', 'sulphates', 'alcohol'],
    outputCol="assembled_features")

feature_scaler = StandardScaler(inputCol="assembled_features", outputCol="scaled_features")

# Initializing classification models
logistic_regression_model = LogisticRegression()
random_forest_model = RandomForestClassifier()
decision_tree_model = DecisionTreeClassifier(labelCol="label", featuresCol="scaled_features", seed=42)

# Constructing pipelines for each model
lr_pipeline = Pipeline(stages=[feature_assembler, feature_scaler, logistic_regression_model])
rf_pipeline = Pipeline(stages=[feature_assembler, feature_scaler, random_forest_model])
dt_pipeline = Pipeline(stages=[feature_assembler, feature_scaler, decision_tree_model])

# Hyperparameter tuning setup
param_grid = ParamGridBuilder().build()

# Model evaluation metric
model_evaluator = MulticlassClassificationEvaluator(metricName="f1")

# Cross-validation for Logistic Regression
cv_lr = CrossValidator(estimator=lr_pipeline, estimatorParamMaps=param_grid, evaluator=model_evaluator, numFolds=10)
cv_lr_model = cv_lr.fit(train_data)
print("F1 Score for Logistic Regression: ", model_evaluator.evaluate(cv_lr_model.transform(test_data)))

# Cross-validation for Random Forest
cv_rf = CrossValidator(estimator=rf_pipeline, estimatorParamMaps=param_grid, evaluator=model_evaluator, numFolds=10)
cv_rf_model = cv_rf.fit(train_data)
print("F1 Score for Random Forest: ", model_evaluator.evaluate(cv_rf_model.transform(test_data)))

# Cross-validation for Decision Tree
cv_dt = CrossValidator(estimator=dt_pipeline, estimatorParamMaps=param_grid, evaluator=model_evaluator, numFolds=10)
cv_dt_model = cv_dt.fit(train_data)
print("F1 Score for Decision Tree: ", model_evaluator.evaluate(cv_dt_model.transform(test_data)))

# Saving the models to S3
cv_lr_model.save("s3a://cldassign2/LogisticRegressionModel")
cv_rf_model.save("s3a://cldassign2/RandomForestModel")
cv_dt_model.save("s3a://cldassign2/DecisionTreeModel")

# Terminating the Spark session
spark_session.stop()

