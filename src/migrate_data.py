import pandas as pd
import numpy as np
from .models import *
from .utils import *

df_0 = pd.read_csv('nl_data.csv')

def clean_text(x):
    if isinstance(x, str):  # Check if the value is a string
        return x.replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')
    return x  # If not a string, return as is

def trim_text(x):
    if isinstance(x, str):  # Check if the value is a string
        return x.strip()
    return x  # If not a string, return as is

df_0 = df_0.drop('database_id', axis=1)
# Apply the function to all columns
df = df_0.map(clean_text)
df = df.map(trim_text)
df = df.dropna(subset=['database_name'])
df.replace('Unavailable', '', inplace=True)
# df.fillna('', inplace=True)
df['valid_from'] = pd.to_numeric(df['valid_from'], errors='coerce')
df['valid_to'] = pd.to_numeric(df['valid_to'], errors='coerce')
df['database_host'] = ''
df['referenced_database'] = ''
df['creation_date'] = pd.to_datetime(df['creation_date'], format='mixed', dayfirst=True)
df['last_updated'] = pd.to_datetime(df['last_updated'], format='mixed', dayfirst=True)
df[['individualized_data', 'identifiable_individuals', 'indigenous_data', 'indigenous_community_permission']] = df[['individualized_data', 'identifiable_individuals', 'indigenous_data', 'indigenous_community_permission']].replace({'Yes': True, 'No': False})
df['identifiable_individuals'] = df['identifiable_individuals'].apply(lambda x: x if x in [True, False] else np.nan)
df['limits_of_use'] = df['limits_of_use'].where(pd.notna(df['limits_of_use']), '')
# df['database_owner'] = df['database_owner'].where(pd.notna(df['database_owner']), None)
# df['primary_discipline'] = df['primary_discipline'].where(pd.notna(df['primary_discipline']), None)
# df['secondary_discipline'] = df['secondary_discipline'].where(pd.notna(df['secondary_discipline']), None)
# df['secondary_discipline'] = df['secondary_discipline'].where(pd.notna(df['secondary_discipline']), None)
df.replace({np.nan: None}, inplace=True)

# print(df.columns.values)
# print(df.head())
# print(len(df.index))
# first_entry = df.iloc[0]
for i in range(len(df)):
    first_entry = df.iloc[i]
    data_formats = list(map(find_or_create_data_format, first_entry['data_format'].split(', ')))
    data_types = list(map(find_or_create_data_type, first_entry['data_type'].split(', ')))
    # print(first_entry)
    print(data_formats[0])
    print(list(data_types))

    languages = list(map(find_or_create_language, first_entry['language'].split(', ')))
    print(languages)

    theme = find_or_create_theme(first_entry['theme'])
    print(theme)

    discipline = process_discipline(first_entry)
    location = process_location(first_entry['location_relevance'])

    contact = process_contact(first_entry['contact_type'], first_entry['contact_detail'])
    # admin = process_entity(first_entry['maintenance'])
    owner = process_entity(first_entry['database_owner']) if first_entry['database_owner'] else None
    sponsor = process_entity_sponsor(first_entry['sponsor'], first_entry['type_entity']) if first_entry['database_owner'] else None
    # host = process_entity(first_entry['database_host'])

    print(first_entry['limits_of_use'])
    metadata = Metadata(
        name=first_entry['database_name'],
        url=first_entry['url'],
        province_code=first_entry['province_code'],
        description=first_entry['description'],
        valid_from=first_entry['valid_from'],
        valid_to=first_entry['valid_to'],
        visibility=first_entry['visibility'],
        access_type=first_entry['access_type'],
        usage_url=first_entry['user_guide_url'],
        license=first_entry['license'],
        usage_limit=first_entry['limits_of_use'] if ['limits_of_use'] else '',
        location_id=location.id,
        data_formats=data_formats,
        data_types=data_types,
        languages=languages,
        theme_id=theme.id,
        discipline_id=discipline.id if discipline else None,
        host_id=None,
        admin_id=None, # admin.id
        owner_id=owner.id if owner else None,
        contact_id=contact.id if contact else None,
    )

    create_metadata(metadata)
    print(metadata)
