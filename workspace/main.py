import functions_framework
import investpy
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

@functions_framework.http
def get_indicators(request):
    start_date_dt = datetime.now()
    end_date_dt = start_date_dt + timedelta(days=28)
    print(start_date_dt)
    print(end_date_dt)

    try:
        df = investpy.economic_calendar(
            from_date=start_date_dt.strftime("%d/%m/%Y"),
            to_date=end_date_dt.strftime("%d/%m/%Y"),
            countries=['japan']
        )
        filtered_df = df[df['importance'].isin(['high', 'medium'])]
        print(filtered_df)
    except Exception as e:
        return f"Failed to fetch indicators: {str(e)}", 500

    gas_url = os.environ.get('GAS_WEBHOOK_URL')

    params = {
        'apiKey' : os.environ.get('API_KEY'),
        'startDate': start_date_dt.strftime("%Y/%m/%d"),
        'endDate': end_date_dt.strftime("%Y/%m/%d"),
    }

    data = []
    for _, row in filtered_df.iterrows():
        date_string = row['date'] + " " + row['time']
        start_time = datetime.strptime(date_string, "%d/%m/%Y %H:%M")
        end_time = start_time + timedelta(minutes=15)
        data.append({
            "title": row['event'],
            "startTime": start_time.strftime("%Y/%m/%d %H:%M:%S"),
            "endTIme": end_time.strftime("%Y/%m/%d %H:%M:%S"),
            "country": row['zone']
        })
    print(data)
    #response = requests.post(gas_url, params=params, json=data)
    #print(f'Status Code: {response.status_code}, Response Text: {response.text}')
    return "Data sent to GAS", 200
