# Installing Apache Spark on Windows

## Docker Image
You can access the Docker image at [Docker Image Link](https://hub.docker.com/repository/docker/nb1410/cs643-nb-pa2/general).

## Install Apache Spark
### Step 1: Install Java
Apache Spark requires Java. You can download and install the latest version of Java from [Oracle's website](https://www.oracle.com/java/technologies/javase-jdk11-downloads.html).

### Step 2: Install Apache Spark
1. Download Apache Spark from the [official website](https://spark.apache.org/downloads.html).
2. Extract the contents of the downloaded file to a directory on your system, e.g., `C:\spark`.

### Step 3: Install Hadoop (Optional)
Apache Spark can run without Hadoop but if needed, you can download it from [Apache Hadoop's official website](https://hadoop.apache.org/releases.html).

### Step 4: Set Environment Variables
1. Set `SPARK_HOME` to point to your Spark installation directory, e.g., `C:\spark`.
2. If you installed Hadoop, set `HADOOP_HOME` to its installation directory.
3. Add `%SPARK_HOME%\bin` to your system's `Path` variable.

### Step 5: Verify Installation
Open Command Prompt and type `spark-shell`. If Spark is installed correctly, the Spark shell prompt will appear.

# Installing AWS-CLI on Windows

## Step 1: Download AWS-CLI
Download the AWS Command Line Interface from [AWS's website](https://aws.amazon.com/cli/).

## Step 2: Install AWS-CLI
1. Run the downloaded installer.
2. Follow the on-screen instructions to complete the installation.

## Step 3: Verify Installation
Open Command Prompt and type the following commands to verify the installation:

```bash
aws --version
```
# AWS EMR Cluster Setup

## Creating an EMR Cluster

1. **Access EC2 Dashboard**: Navigate to the EC2 section and select 'Create Cluster'.
2. **Cluster Name**: Enter a name for your cluster.
3. **Select EMR Release**: Choose 'emr-6.15.0' or a suitable release.
4. **Cluster Configuration**: Add an instance group to form a 4-node cluster.
5. **Security and Key Pair**: Configure the security settings and select an Amazon EC2 key pair for SSH access.
6. **Define Roles**:
    - Amazon EMR service role: Use 'EMR_DefaultRole'.
    - EC2 instance profile for Amazon EMR: Use 'EMR_DefaultRole'.
7. **Create the Cluster**: Finalize the setup by creating the cluster.

**Note**: Post-creation, adjust the EC2 instance security settings to open port 22 and set a custom IP address.

## Connecting to EMR Instance

1. **SSH Connection**: 
    ```bash
    ssh -i [Security Key] [Instance Name]
    ```
2. **Transferring Files to EMR Instance**:
    - Exit the EMR instance.
    - Use the following command:
        ```bash
        scp -i [Security Key] [Local Path] [Server Path]
        ```
    - Reconnect to the server using the SSH command.

3. **Virtual Environment Setup**:
    - Navigate to your project folder.
    - Create a virtual environment:
        ```bash
        python -m venv venv
        ```
    - Activate the virtual environment:
        ```bash
        source venv/bin/activate
        ```
    - Install dependencies:
        ```bash
        pip install -r requirements.txt
        ```
    - Run your script:
        ```bash
        python training.py
        ```

# Prediction Setup on AWS EC2 Instance

## EC2 Instance Setup

1. **Launch an EC2 Instance**: Follow the standard steps to launch an instance in EC2.
2. **Connect via SSH**: 
    ```bash
    ssh [SSH command details]
    ```

## Software Installation

1. **Install Java** (required for Apache Spark and Hadoop):
    ```bash
    sudo apt update
    sudo apt install openjdk-8-jdk
    ```
    - Add environment variables:
        ```bash
        export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
        export PATH=$PATH:$JAVA_HOME/bin
        ```
2. **Install AWS CLI**:
    ```bash
    sudo apt update
    sudo apt install awscli
    ```
    - Configure AWS CLI:
        ```bash
        aws configure
        ```

3. **Install Hadoop**:
    - Download and extract:
        ```bash
        wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
        tar -xzvf hadoop-3.3.6.tar.gz
        sudo mv hadoop-3.3.6 /opt/hadoop
        ```
    - Configure environment variables and test the installation:
        ```bash
        export HADOOP_HOME=/opt/hadoop
        export PATH=$PATH:$HADOOP_HOME/bin
        hadoop version
        ```

4. **Install Spark**:
    - Download and extract:
        ```bash
        wget https://downloads.apache.org/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz
        tar -xzvf spark-3.5.0-bin-hadoop3.tgz
        sudo mv spark-3.5.0-bin-hadoop3 /opt/spark
        ```
    - Configure environment variables and test the installation:
        ```bash
        export SPARK_HOME=/opt/spark
        export PATH=$PATH:$SPARK_HOME/bin
        export HADOOP_HOME=/opt/hadoop
        export PATH=$PATH:$HADOOP_HOME/bin
        spark-shell
        ```

## Python Environment Setup

1. **Install Python**: Download and install Python from [python.org](https://www.python.org/downloads/).
2. **Install `virtualenv`**:
    ```bash
    pip install virtualenv
    ```
3. **Create and Activate Virtual Environment**:
    - Create:
        ```bash
        python -m venv venv
        ```
    - Activate:
        ```bash
        source venv/bin/activate
        ```
4. **Install Dependencies and Run Script**:
    ```bash
    pip install -r requirements.txt
    spark-submit --packages org.apache.hadoop:hadoop-aws:3.2.2 [file_name.py]
    ```