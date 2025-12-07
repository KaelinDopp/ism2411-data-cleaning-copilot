#Importing pandas libraries
import pandas as pd

#Loading the sales_data_raw.csv from data/raw/ using a function
#This is done in order to reference to the raw data in order to process the data until it creates a cleaned version
def load_data(file_path):
    #Returns the read file as the data to the data frame and skips bad lines to ensure the code doesn't crash
    return pd.read_csv(file_path, on_bad_lines='skip')

#Create a function that cleans the column names by standardizing the data through lower casing and replacing spaces with underscores
def clean_column_names(df):
    df_clean = df.copy()
    df_clean.columns = (
        df_clean.columns
        .str.strip() #removes the leading and trailing spaces
        .str.lower() #transforms all characters to lower case
        .str.replace(" ","_") #replaces spaces with underscores
    )
    
    #Rename qty to quantity for clarity
    if "qty" in df_clean.columns:
        df_clean = df_clean.rename(columns={"qty": "quantity"})

    #Removes the white spaces by stripping leading and trailing spaces from product names and categories
    text_cols = df_clean.select_dtypes(include="object").columns
    for col in text_cols:
        df_clean[col] = df_clean[col].str.strip()

    #Returns the cleaned dataframe
    return df_clean


#Drop rows with missing values in price and quantity columns in order to handle missing values consistently
def handle_missing_values(df):
    df_clean = df.copy()

    #Forces the values under price and quantity to be numeric and coerces errors to NaN
    for col in ["price", "quantity"]:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
    
    #Drops rows with NaN values in price and quantity columns
    df_clean = df_clean.dropna(subset=["price", "quantity"])

    #Return the cleaned dataframe
    return df_clean

#Removes the rows with invalid data such as negative prices or quantities to keep the data clear and logical
def remove_invalid_rows(df):
    df_clean = df.copy()

    #Remove negative prices from the data by removing any value less than 0
    if "price" in df_clean.columns:
        df_clean = df_clean[df_clean["price"] >= 0]

    #Removes negative quantities fromt the data by removing any value less than 0
    if "quantity" in df_clean.columns:
        df_clean = df_clean[df_clean["quantity"] >= 0]

    #Returns the cleaned dataframe
    return df_clean


#Script that allows the functions to run when the file is executed
if __name__ == "__main__":
    raw_path = "data/raw/sales_data_raw.csv"
    cleaned_path = "data/processed/sales_data_clean.csv"

    df_raw = load_data(raw_path)
    df_clean = clean_column_names(df_raw)
    df_clean = handle_missing_values(df_clean)
    df_clean = remove_invalid_rows(df_clean)
    df_clean.to_csv(cleaned_path, index=False)
    print("Cleaning complete. First few rows:")
    print(df_clean.head())