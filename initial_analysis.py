import marimo

__generated_with = "0.8.7"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import numpy as np
    return mo, np, pd


@app.cell
def __(mo):
    mo.md("""# Initial data analysis""")
    return


@app.cell
def __(pd):
    df_0 = pd.read_csv('data_qc.csv')
    return df_0,


@app.cell
def __(df_0, np, pd):
    def clean_text(x):
        if isinstance(x, str):  # Check if the value is a string
            return x.replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')
        return x  # If not a string, return as is

    def trim_text(x):
        if isinstance(x, str):  # Check if the value is a string
            return x.strip()
        return x  # If not a string, return as is

    df_1 = df_0.drop('database_id', axis=1)
    # Apply the function to all columns
    df = df_1.map(clean_text)
    df = df.map(trim_text)
    # df = df.dropna(subset=['database_name'])
    df.replace('Unavailable', '', inplace=True)
    df['valid_from'] = pd.to_numeric(df['valid_from'], errors='coerce')
    df['valid_to'] = pd.to_numeric(df['valid_to'], errors='coerce')
    # df['database_host'] = ''
    # df['referenced_database'] = ''
    df['creation_date'] = pd.to_datetime(df['creation_date'], format='mixed', dayfirst=True)
    df['last_updated'] = pd.to_datetime(df['last_updated'], format='mixed', dayfirst=True)
    df[['individualized_data', 'identifiable_individuals', 'indigenous_data', 'indigenous_community_permission']] = df[['individualized_data', 'identifiable_individuals', 'indigenous_data', 'indigenous_community_permission']].replace({'Yes': True, 'No': False})
    df['identifiable_individuals'] = df['identifiable_individuals'].apply(lambda x: x if x in [True, False] else np.nan)
    return clean_text, df, df_1, trim_text


@app.cell
def __(df):
    df
    return


@app.cell
def __(df):
    df['database_owner'].unique()
    return


@app.cell
def __(df, mo):
    owner_count = len(df['database_owner'].unique())
    mo.md(f'Database owner count: {owner_count}')
    return owner_count,


@app.cell
def __(df):
    df['type_entity'].unique()
    return


@app.cell
def __(df, mo):
    entity_type_count = len(df['type_entity'].unique())
    mo.md(f'Entity Type count: {entity_type_count}')
    return entity_type_count,


@app.cell
def __(df):
    df['license'].unique()
    return


@app.cell
def __(df, mo):
    license_count = len(df['license'].unique())
    mo.md(f'License count: {license_count}')
    return license_count,


@app.cell
def __(df, mo):
    theme_count = len(df['theme'].unique())
    mo.md(f'Theme count: {theme_count}')
    return theme_count,


@app.cell
def __(df):
    df['primary_discipline'].unique()
    return


@app.cell
def __(df):
    df['location_relevance'].unique()
    return


@app.cell
def __(df):
    first_entry = df.iloc[93]
    print(first_entry['contact_detail'])
    return first_entry,


@app.cell
def __(df):
    df['limits_of_use'].unique()
    return


if __name__ == "__main__":
    app.run()
