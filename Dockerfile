FROM ubuntu:latest

RUN apt -y update && apt -y install python3 python3-dev python3-pip python3-virtualenv openjdk-8-jdk wget
RUN (echo 'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64' >> ~/.bashrc && echo 'export PATH=$PATH:$JAVA_HOME/bin' >> ~/.bashrc)

COPY requirements.txt requirements.txt
COPY prediction.py prediction.py

ENV PYSPARK_DRIVER_PYTHON python3
ENV PYSPARK_PYTHON python3

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz && wget https://downloads.apache.org/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz  
RUN tar -xzvf hadoop-3.3.6.tar.gz && tar -xzvf spark-3.5.0-bin-hadoop3.tgz

RUN mv hadoop-3.3.6 /opt/hadoop
RUN (echo 'export HADOOP_HOME=/opt/hadoop' >> ~/.bashrc && echo 'export PATH=$PATH:$HADOOP_HOME/bin' >> ~/.bashrc)

RUN mv spark-3.5.0-bin-hadoop3 /opt/spark
RUN (echo 'export SPARK_HOME=/opt/spark' >> ~/.bashrc && echo 'export PATH=$PATH:$SPARK_HOME/bin' >> ~/.bashrc && echo 'export HADOOP_HOME=/opt/hadoop' >> ~/.bashrc && echo 'export PATH=$PATH:$HADOOP_HOME/bin' >> ~/.bashrc)


RUN /bin/bash -c "source ~/.bashrc"

ENTRYPOINT ["/opt/spark/bin/spark-submit", "--packages", "org.apache.hadoop:hadoop-aws:3.2.4", "prediction.py"]


