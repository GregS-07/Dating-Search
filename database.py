import pandas as pd
import sqlite3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

spreadsheets = ["Female.csv", "Male.csv", "Nonbinary.csv"]
genders = ["Female", "Male", "nonbinary"]

def create_dataframes():
    dir = lambda name: "sample_data/" + name
    names = ["Male.csv", "Female.csv", "Nonbinary.csv"]
    dataframes = []

    for name in names:
        dataframes.append(pd.read_csv(dir(name)))

    return dataframes

def create_graphs():
    # plt.title("What Genders Are Sought After By Gender")

    # m_seeks, f_seeks, n_seeks = [m_df["Seeking"].value_counts().idxmax(), f_df["Seeking"].value_counts().idxmax(), n_df["Seeking"].value_counts().idxmax()]
    # percentages = [m_df['Seeking'].value_counts().max() / len(m_df) * 100,  f_df['Seeking'].value_counts().max() / len(f_df) * 100,  n_df['Seeking'].value_counts().max() / len(n_df) * 100]
    
    # plt.bar([m_seeks, f_seeks, n_seeks],percentages)
    # plt.savefig("static/images/graphs/seekedgenders.png")

    #-------------Pie Chart Of Seeked Genders-------------------------

    # Set y-axis to whole numbers  
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    
    m_df, f_df, n_df = create_dataframes()



    combined_df = pd.concat(create_dataframes(), ignore_index=True)

    seeking_genders = combined_df['Seeking'].value_counts().index.tolist()
    seeking_counts = combined_df['Seeking'].value_counts()
    total_people = len(combined_df)
    percentages = seeking_counts / total_people * 100
    
    plt.pie(percentages, labels=seeking_genders)
    plt.title("How Much Is Each Gender Sought After?")
    plt.savefig("static/images/graphs/seekedgenders_all.png")

    plt.clf()

    #----------Pie Chart Of Where People Live----------------

    combined_df = pd.concat(create_dataframes(), ignore_index=True)

    locations = combined_df['County'].value_counts().index.tolist()
    location_counts = combined_df['County'].value_counts()
    total_people = len(combined_df)
    percentages = location_counts / total_people * 100
    
    plt.pie(percentages, labels=locations)
    plt.title("Where Do Users Live?")
    plt.savefig("static/images/graphs/location_all.png")

create_graphs()

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