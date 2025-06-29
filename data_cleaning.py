import pandas as pd
import numpy as np

def load_data(url):
    return pd.read_csv(url)

def rename_col_names(df):
    df.columns=df.columns.str.strip().str.lower().str.replace(" ","_")
    df.rename(columns={'st': 'state'}, inplace=True)
    return df
    

def clean_inconsistent_values(df):
    df['gender']=df['gender'].str.strip().str.lower().map({'f':'F','m':'M','femal':'F','male':'M','female':'F'})
    
    state_mapping={'Cali':'California','AZ':'Arizona','WA':'Washington'}
    df['state']=df['state'].replace(state_mapping)
    
    df['education']=df['education'].str.strip().replace({'Bachelors':'Bachelor'})

    df['customer_lifetime_value'] = df['customer_lifetime_value'].str.replace('%', '', regex=False)
    
    df['vehicle_class'] = df['vehicle_class'].replace({
    'Sports Car': 'Luxury',
    'Luxury SUV': 'Luxury',
    'Luxury Car': 'Luxury'
    })
    return df
      

def fix_data_types(df):
    def extract_complaints(value):
        try:
           return int(str(value).split('/')[1])
        except:
           return 0

    df['number_of_open_complaints'] = df['number_of_open_complaints'].apply(extract_complaints)
    df['number_of_open_complaints'] = pd.to_numeric(df['number_of_open_complaints'], errors='coerce')
    df['customer_lifetime_value'] = pd.to_numeric(df['customer_lifetime_value'], errors='coerce')
    return df

def handle_null_values(df):
    df = df.dropna(subset=['customer'])
    df['customer_lifetime_value']=df['customer_lifetime_value'].fillna(df['customer_lifetime_value'].mean())
    df['gender']=df['gender'].fillna(df['gender'].mode()[0])
    return df
    


def convert_numeric_to_int(df):
    numerical_cols=['customer_lifetime_value','income','monthly_premium_auto','number_of_open_complaints','total_claim_amount']
    for col in numerical_cols:
        df[col]=df[col].apply(int)
    return df

def clean_and_format_data(url):
    df = load_data(url)
    df = rename_col_names(df)
    df = clean_inconsistent_values(df)
    df = fix_data_types(df)
    df = handle_null_values(df)
    df = convert_numeric_to_int(df)
    return df