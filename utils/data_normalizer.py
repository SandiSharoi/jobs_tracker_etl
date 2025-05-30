import pandas as pd
from datetime import datetime, timedelta
import pytz
import numpy as np

def parse_salary_founditSG(s):
    if not isinstance(s, str) or not s.strip():
        return ('N/A', 'N/A', 'N/A', 'N/A')

    try:
        parts = s.strip().split()
        if '-' in parts[0]:
            min_str, max_str = parts[0].split('-')
            currency = parts[1] if len(parts) > 1 else 'N/A'
            min_salary = int(min_str.replace(',', '').strip())
            max_salary = int(max_str.replace(',', '').strip())
            avg_salary = (min_salary + max_salary) // 2
            return (avg_salary, min_salary, max_salary, currency)
        else:
            salary = int(parts[0].replace(',', '').strip())
            currency = parts[1] if len(parts) > 1 else 'N/A'
            return (salary, 'N/A', 'N/A', currency)
    except:
        return ('N/A', 'N/A', 'N/A', 'N/A')

class JobDataNormalizer:

    def __init__(self):
        self.standard_cols = [
            'title', 'company', 'location', 'role', 'functions', 'salary',
            'minimum_salary', 'maximum_salary', 'currency',
            'job_type', 'work_arrangement', 'date_posted',
            'job_link', 'country', 'source'
        ]

    # Convert "X days ago", "X hours ago", or "just now" to UTC+6:30 date
    def convert_to_utc_plus_630(self, text):
        yangon_tz = pytz.timezone('Asia/Yangon')
        today = datetime.now(pytz.utc).astimezone(yangon_tz)

        if not isinstance(text, str) or not text.strip():
            return today.strftime('%Y-%m-%d')  # Default to today

        text = text.lower().strip()

        try:
            if "day" in text:
                number = int(''.join(filter(str.isdigit, text)))
                date_result = today - timedelta(days=number)
                return date_result.strftime('%Y-%m-%d')
            elif "hour" in text or "just now" in text:
                return today.strftime('%Y-%m-%d')
        except:
            pass

        return today.strftime('%Y-%m-%d')  # Fallback to today



    # Handle missing values
    def fill_missing_foundit_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        # Replace empty strings with np.nan
        df.replace('', np.nan, inplace=True)

        # Fill all np.nan values with 'N/A'
        df.fillna('N/A', inplace=True)

        return df


    ## Foundit Singapore
    def founditsg(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.rename(columns={
            'title': 'title',
            'companyName': 'company',
            'locations': 'location',
            'roles': 'role',
            'functions': 'functions',
            'salary': 'salary',
            'jobTypes': 'job_type',
            'postedBy': 'date_posted',
            'seoJdUrl': 'job_link'

        })

        # Convert job_type list to string
        df['role'] = df['role'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

         # Convert job_type list to string
        df['functions'] = df['functions'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)       

        # Convert job_type list to string
        df['job_type'] = df['job_type'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

        # Convert "X days ago" to datetime in UTC+6:30
        df['date_posted'] = df['date_posted'].apply(self.convert_to_utc_plus_630)

        # Add full URL to job_link
        df['job_link'] = df['job_link'].apply(
            lambda x: f"https://www.foundit.sg{x}" if isinstance(x, str) and not x.startswith("http") else x
        )


        # df[['salary', 'minimum_salary', 'maximum_salary', 'currency']] = df['salary'].apply(parse_salary_founditSG).apply(pd.Series)
        df[['salary', 'minimum_salary', 'maximum_salary', 'currency']] = df['salary'] \
            .apply(parse_salary_founditSG).apply(pd.Series)

        # Add fixed values
        df['country'] = 'SG'
        df['work_arrangement'] = None
        df['source'] = 'founditsg'

        # Apply missing value filler
        df = self.fill_missing_foundit_fields(df)



        return df[self.standard_cols]