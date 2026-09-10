import pandas as pd
import math
from app import app, db, Fragrance

df = pd.read_csv('data/perfumes.csv', sep=';', on_bad_lines='skip')

# Fix European-style decimals (comma -> period) in rating_value
df['Rating Value'] = df['Rating Value'].astype(str).str.replace(',', '.', regex=False)
df['Rating Value'] = pd.to_numeric(df['Rating Value'], errors='coerce')

# Convert to numeric and use Pandas Nullable Integer ('Int64')
df['Rating Count'] = pd.to_numeric(df['Rating Count'], errors='coerce').astype('Int64')
df['Year'] = pd.to_numeric(df['Year'], errors='coerce').astype('Int64')

def clean_int(val, min_val=None, max_val=None):
    """Safely extracts a Python int or None for PostgreSQL INTEGER columns."""
    if pd.isna(val) or val is None:
        return None
    try:
        val_int = int(val)
        if min_val is not None and val_int < min_val:
            return None
        if max_val is not None and val_int > max_val:
            return None
        return val_int
    except (ValueError, TypeError):
        return None

def clean_float(val):
    """Safely extracts a Python float or None."""
    if pd.isna(val) or val is None:
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None

def clean_str(val):
    """Safely extracts a cleaned string or None."""
    if pd.isna(val) or val is None:
        return None
    s = str(val).strip()
    return s if s and s.lower() != 'nan' else None

with app.app_context():
    for _, row in df.iterrows():
        fragrance = Fragrance(
            name=clean_str(row.get('Perfume')),
            brand=clean_str(row.get('Brand')),
            country=clean_str(row.get('Country')),
            gender=clean_str(row.get('Gender')),
            rating_value=clean_float(row.get('Rating Value')),
            # Restrict bounds to standard 32-bit signed integer limits
            rating_count=clean_int(row.get('Rating Count'), min_val=0, max_val=2147483647),
            year=clean_int(row.get('Year'), min_val=1000, max_val=2100),
            top_notes=clean_str(row.get('Top')),
            middle_notes=clean_str(row.get('Middle')),
            base_notes=clean_str(row.get('Base')),
            perfumer1=clean_str(row.get('Perfumer1')),
            perfumer2=clean_str(row.get('Perfumer2')),
            main_accord1=clean_str(row.get('mainaccord1')),
            main_accord2=clean_str(row.get('mainaccord2')),
            main_accord3=clean_str(row.get('mainaccord3')),
            main_accord4=clean_str(row.get('mainaccord4')),
            main_accord5=clean_str(row.get('mainaccord5')),
            url=clean_str(row.get('url')),
        )
        db.session.add(fragrance)

    db.session.commit()
    print(f"Imported {len(df)} fragrances.")