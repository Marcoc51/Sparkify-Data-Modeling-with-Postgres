# Sparkify Data Modeling with Postgres

## Introduction

This repository contains the data modeling and ETL pipeline for Sparkify, a music streaming startup. The goal of this database is to support Sparkify's analytical needs by storing and organizing their data in a way that allows for efficient querying and analysis.

## Running the Python Scripts

To run the Python scripts, you will need to have Python and Postgres installed on your machine. You will also need to create a database named `sparkifydb`. Once these prerequisites are met, you can run the following command to create the necessary tables and load the data:<br>
* `python create_tables.py`
* `python etl.py`

## Repository Contents

1. `create_tables.py`: This script is used to create the necessary tables in the `sparkifydb` database.
2. `etl.py`: This script is used to extract data from JSON logs and song data files, transform the data, and load it into the appropriate tables in the `sparkifydb` database.
3. `sql_queries.py`: This script contains the SQL queries used in the `create_tables.py` and `etl.py` scripts.
4. `data/`: This directory in `data.zip` contains the JSON logs and song data files that are used as input for the ETL pipeline.
5. `test.ipynb`: Jupyter notebook that contains test case to check if the data is loaded into tables correctly.
6. `ERD.py`: This script creates the ERD for the `sparkifydb` database.

## Database Schema Design and ETL Pipeline

* The database schema consists of a star schema with one fact table (songplays) and four dimension tables (users, songs, artists, time). The fact table, songplays, contains information about each song play and references the primary keys of the dimension tables. This design allows for efficient querying and analysis of the data, as all relevant data for a song play is contained in one row of the songplays table and the related data can be easily accessed by joining with the dimension tables.

* The ETL pipeline extracts data from the JSON logs and song data files, transforms the data (such as converting timestamps to a more usable format), and loads it into the appropriate tables in the `sparkifydb` database. The pipeline is designed to be flexible and able to handle new data being added to the input files without disrupting the existing data in the database.

## Entity Relationship Diagram
 
 <p align="left">
<img src="https://github.com/Marcoc51/Sparkify-Data-Modeling-with-Postgres/blob/main/sparkifydb_erd.png" style="height: 500px; width:750px;"/>
</p>
