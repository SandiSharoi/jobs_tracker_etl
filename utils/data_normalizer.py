import pandas as pd
from datetime import datetime, timedelta
import pytz

class JobDataNormalizer:

    def __init__(self):
        self.standard_cols = [
            'title', 'company', 'location', 'salary',
            'job_type', 'work_arrangement', 'date_posted',
            'job_link', 'country', 'source'
        ]

    
    ## Foundit Singapore
    def founditsg(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.rename(columns={
            'title': 'title',
            'companyName': 'company',
            'locations': 'location',
            'salary': 'salary',
            'jobTypes': 'job_type',
            'postedBy': 'date_posted',
            'seoJdUrl': 'job_link'
        })

        # Convert job_type list to string
        df['job_type'] = df['job_type'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

        # Convert "X days ago" to datetime in UTC+6:30
        yangon_tz = pytz.timezone('Asia/Yangon')
        def convert_to_utc_plus_630(text):
            today = datetime.now(pytz.utc)
            if isinstance(text, str) and "day" in text:
                try:
                    days_ago = int(text.strip().split()[0])
                    converted = today - timedelta(days=days_ago)
                    return converted.astimezone(yangon_tz).strftime('%Y-%m-%d %H:%M:%S')
                except:
                    return None
            return None
        df['date_posted'] = df['date_posted'].apply(convert_to_utc_plus_630)

        # Add full URL to job_link
        df['job_link'] = df['job_link'].apply(lambda x: f"https://www.foundit.sg{x}" if isinstance(x, str) and not x.startswith("http") else x)

        # Add fixed values
        df['country'] = 'SG'
        df['work_arrangement'] = None
        df['source'] = 'founditsg'

        return df[self.standard_cols]

  
