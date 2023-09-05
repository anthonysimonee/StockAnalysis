import pandas as pd

# Read tables from the URL
tables = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

# Assuming the first table is the one you're interested in
if len(tables) > 0:
    # Access a specific column by its name
    specific_column = tables[0]['Symbol']  # Replace 'Column Name' with the actual column name

    # Specify the filename for the CSV
    csv_filename = 'SNP500symbols.csv'

    # Write the specific column to a CSV file
    specific_column.to_csv(csv_filename, index=False)

    print(f"Values from '{specific_column.name}' column written to '{csv_filename}'.")
else:
    print("No tables found.")
