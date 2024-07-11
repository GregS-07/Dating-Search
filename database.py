import pandas as pd
import sqlite3

spreadsheets = ["Female.csv", "Male.csv", "Nonbinary.csv"]

# Establishing connection to database
def conn_db():
    db_name = "database.db"
    conn = sqlite3.connect(db_name)
    return conn

def create_database():
    with conn_db() as conn:
        cursor = conn.cursor()

        # Iterating over spreadsheets
        for spreadsheet in spreadsheets:
            df = pd.read_csv(spreadsheet)
            name = spreadsheet.replace(".csv", "")
            df.to_sql(name, conn, index=False)

def sheets_to_csv():
    excel_file = 'data.xlsx' # Path to spreadsheet 

    xls = pd.ExcelFile(excel_file, engine="openpyxl")

    # Iterating over spreadsheets 
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        csv_file = f"{sheet_name}.csv"
        df.to_csv(csv_file, index=False)

create_database()

