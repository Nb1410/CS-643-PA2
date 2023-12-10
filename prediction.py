from pyspark.sql import SparkSession
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import CrossValidatorModel

# Initialize Spark session with appropriate application name
spark_session = SparkSession.builder \
    .appName("WineQualityPredictionEvaluation") \
    .getOrCreate()

# Setting up Spark configuration for AWS S3 access
# Replace placeholder values with actual AWS credentials
spark_session.sparkContext._jsc.hadoopConfiguration().set("com.amazonaws.services.s3.enableV4", "true")
spark_session.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
spark_session.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider", "com.amazonaws.auth.InstanceProfileCredentialsProvider,com.amazonaws.auth.DefaultAWSCredentialsProviderChain")
spark_session.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "s3.us-east-1.amazonaws.com")

# Load the validation dataset from S3
validation_data = spark_session.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("sep", ";") \
    .load("s3a://cldassign2/ValidationDataset.csv")

# Confirm successful data load
if validation_data.count() > 0:
    print("Validation data successfully loaded from S3")
else:
    print("Error loading validation data")

# Mapping for renaming columns
column_rename_map = {
    # Define column rename mapping here
    # 'Original Column Name': 'New Column Name'
}

# Renaming columns in the DataFrame
for original_col, new_col in column_rename_map.items():
    validation_data = validation_data.withColumnRenamed(original_col, new_col)

# Function to load and evaluate a model from S3
def evaluate_model(model_path, data, metric="f1"):
    model = CrossValidatorModel.load(model_path)
    evaluator = MulticlassClassificationEvaluator(metricName=metric)
    f1_score = evaluator.evaluate(model.transform(data))
    print(f"F1 Score for model at {model_path}: {f1_score}")

# Evaluate Logistic Regression model
evaluate_model('s3a://cldassign2/LogisticRegression', validation_data)

# Evaluate Random Forest Classifier model
evaluate_model('s3a://cldassign2/RandomForestClassifier', validation_data)

# Evaluate Decision Tree Classifier model
evaluate_model('s3a://cldassign2/DecisionTreeClassifier', validation_data)

# Terminate the Spark session
spark_session.stop()

