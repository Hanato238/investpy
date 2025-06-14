import functions_framework
import investpy
import datetime
import json
import requests

@functions_framework.http
def get_indicators(request):
    now = datetime.datetime.now()
    next_month = now.month % 12 + 1
    year = now.year + (1 if next_month == 1 else 0)
    start_date = f"01/{next_month:02d}/{year}"
    end_date = f"28/{next_month:02d}/{year}" if next_month == 2 else f"30/{next_month:02d}/{year}"

    try:
        df = investpy.economic_calendar(from_date=start_date, to_date=end_date, countries=['japan'])
    except Exception as e:
        return f"Failed to fetch indicators: {str(e)}", 500

    gas_url = "https://script.google.com/macros/s/あなたのデプロイURL/exec"
    for _, row in df.iterrows():
        data = {
            "title": row['event'],
            "date": row['date'],
            "time": row['time'],
            "importance": row['importance'],
            "country": row['country']
        }
        requests.post(gas_url, json=data)
    
    return "Data sent to GAS", 200
