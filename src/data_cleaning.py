#Importing libraries
import pandas as pd

#Loading the sales_data_raw.csv from data/raw/ using a function
#This is done in order to reference to the raw data in order to process the data until it creates a cleaned version
def load_data(file_path):
    #Returns the read file as the data to the data frame
    return pd.read_csv(file_path)


def clean_column_names(df):
    df_clean = df.copy()

    df_clean.columns = (
        df_clean.columns
        .str.strip()
        .str.lower()
        .str.replace(" ","_")
    )

    text_cols = df_clean.select_dtypes(include="object").columns
    for col in text_cols:
        df_clean[col] = df_clean[col].str.strip()

    return df_clean


def handle_missing_values(df):
    df_clean = df.copy()

    for col in ["price", "quantity"]:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
    
    df_clean = df_clean.dropna(subset=["price", "quantity"])

    return df_clean


def remove_invalid_rows(df):
    df_clean = df.copy()

    if "price" in df_clean.columns:
        df_clean = df_clean[df_clean["price"] >= 0]

    if "quantity" in df_clean.columns:
        df_clean = df_clean[df_clean["quantity"] >= 0]

    return df_clean

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