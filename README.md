# Log-Analysis
A reporting tool using the psycopg2 module to connect to the database.

## Requirements
Python3, posrgresql version 9.5.7 or higher, vagrant and Virtual Box.
 
## Run the project
Download the sql data file from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).
```
git clone https://github.com/vmath89/Log-Analysis.git
cd Log-Analysis
psql -d news -f newsdata.sql
``` 

The psql command will only work if a database called news is present in the database. If it is not present then create a database using the following command and then run the psql command again:
```
create database news;
```
To start the reporting tool, run the following command:
```
python3 news.py
```
The program is interactive and will prompt the user to enter a number whose value determines which of the report sections will be generated, or if the program needs to exit.

