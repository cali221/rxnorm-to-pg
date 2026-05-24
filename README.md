## Description
Python scripts to download and load RxNorm prescribable content, as described [here](https://www.nlm.nih.gov/research/umls/rxnorm/docs/prescribe.html), to a PostgreSQL database.
<br><br>
**Note:**
This tool was developed to work with RxNorm prescribable content releases that were current on May 24–25, 2026. It may not work with future releases.
<br><br>
This product uses publicly available data courtesy of the U.S. National Library of Medicine (NLM), National Institutes of Health, Department of Health and Human Services; NLM is not responsible for the product and does not endorse or recommend this or any other product.

## Citation
Nelson SJ, Zeng K, Kilbourne J, Powell T, Moore R. Normalized names for clinical drugs: RxNorm at 6 years. J Am Med Inform Assoc. 2011 Jul-Aug;18(4)441-8. doi: 10.1136/amiajnl-2011-000116. Epub 2011 Apr 21. PubMed PMID: 21515544; PubMed Central PMCID: PMC3128404.

## Steps to run
### Step 1 
Create a .env in the root directory of this project, copy the following into the .env file and fill it with your credentials and desired schema instead:
```
PG_USER='your postgres user here'
PG_PASSWORD='your postgres password here'
PG_HOST='your postgres host here'
PG_DATABASE='your postgres database'
PG_PORT='your postgres port'
SCHEMA='your schema name'
```
### Step 2
Create a new virtual environment:
```
python -m venv venv
```
Then activate the virtual environment using the appropriate commmand. For example:
- For Windows Powershell use: ```.\venv\Scripts\Activate.ps1```
- For Windows Command Prompt use: ```venv\Scripts\activate.bat```
- For MacOS or Linux use: ```source venv/bin/activate```
### Step 3
Install required dependencies:
```
pip install -r requirements.txt
```
### Step 4
While at the root directory of this project, run:
```
python main.py
```
### Step 5
You will see a menu like:
```
------------ MAIN MENU ------------
1. Download current RxNorm prescribable content
2. Load RxNorm data into PostgreSQL database
3. Quit

Your choice: 
```
You can then input a number accordingly to proceed
