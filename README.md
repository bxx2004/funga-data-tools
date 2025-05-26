# FUNGA-data-tools

this repo is for data processing of FUNGA's data

## Features

Here's a list of features included in this project:

| Name                | Description                |
|---------------------|----------------------------|
| download.py         | Download public data       |
| count.py            | compute json data count    |
| clean_data.py       | distinct the download data |
| fasta-id-extract.py | -                          |
| j2c.py              | transfer .json to .csv     |
| merge_reference.py  | -                          |
| renumber.py         | renumber platform id       |
| zt2c.py             | processor of zhangtao      |
| embedding.py        | embed dataset              |
| uploadVector.py     | upload data to milvusDB    |

## WorkFlow
##### For PostgreSQL
- download -> count -> clean_data -> merge_reference -> count -> renumber -> j2c
##### For MilvusDB
- download -> count -> clean_data -> merge_reference -> count -> renumber -> zt2c -> embedding.py -> uploadVector