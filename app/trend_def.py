import base64
import jwt
import hashlib
import time
import requests
import json
import re
from datetime import datetime, timedelta
from data.config import StaticConfig, DynamicConfig


def retrieveImportantInfoFromLog(patterns, log):
    results = []
    for pattern_key, pattern_value in patterns.items():
        try:
            # If pattern detection is None, set it to 1 and continue
            if pattern_key == 'detections_pattern' and pattern_value == None:
                found_string = '1'
                results.append(found_string)
                continue

            found_string = re.findall(pattern_value, log)

            # If string is empty, set it to unknow
            if len(found_string) == 0:
                found_string = str(found_string)
                found_string = 'Unknow'

            # If string is not empty, convert it to a string
            elif len(found_string) > 0:
                found_string = str(found_string[0])

            # If string is 0.0.0.0, set it to unknow
            if found_string == '0.0.0.0' and pattern_key == 'endpoint_ip_pattern':
                found_string = 'Unknow'

            # Remove excessive backslashes
            if '\\\\\\\\' in found_string:
                found_string = found_string.replace('\\\\\\\\', '/')

            # Convert time to GMT +03:00
            if pattern_key == 'date_pattern':
                # Convert the date string to a datetime object
                date_object = datetime.strptime(found_string, StaticConfig.DATE_FORMATS['default_date_format'])

                # Adjust the time zone to GMT+03:00
                date_object = date_object + timedelta(hours=3)

                # Format the date in the desired format
                found_string = str(date_object.strftime(StaticConfig.DATE_FORMATS['brazil_date_format']))

        except Exception as e:
            print(e)
            continue

        # Append found strings to results list
        results.append(found_string)

    return results


def createChecksum(http_method, raw_url):
    string_to_hash = http_method.upper() + '|' + raw_url.lower() + '||'
    base64_string = base64.b64encode(hashlib.sha256(str.encode(string_to_hash)).digest()).decode('utf-8')
    return base64_string


def createJwtToken(application_id, api_key, http_method, raw_url, iat=time.time(), algorithm='HS256', version='V1'):
    payload = {'appid': application_id, 'iat': iat, 'version': version,'checksum': createChecksum(http_method, raw_url)}
    token = jwt.encode(payload, api_key, algorithm=algorithm)
    return token


def requestLogs():
    while True:
        # Create JWT Token
        print(f'/WebApp/api/v1/Logs/{DynamicConfig.selected_logtype['value']}?output_format=CEF&page_token=0&since_time={DynamicConfig.selected_timestamp}')
        jwt_token = createJwtToken(
            DynamicConfig.selected_client['application_id'],
            DynamicConfig.selected_client['api_key'],
            'GET',
            f'/WebApp/api/v1/Logs/{DynamicConfig.selected_logtype['value']}?output_format=CEF&page_token=0&since_time={
                DynamicConfig.selected_timestamp}',
            iat=time.time()
        )

        # Create headers
        headers = {
            'Authorization': 'Bearer ' + jwt_token,
            'Content-Type': 'application/json;charset=utf-8'
        }

        # Make the GET request to the API
        r = requests.get(
            DynamicConfig.selected_client['url'] +
            f'/WebApp/api/v1/Logs/{DynamicConfig.selected_logtype['value']}?output_format=CEF&page_token=0&since_time={
                DynamicConfig.selected_timestamp}',
            headers=headers,
            verify=False
        )

        # Check if error in GET request
        if r.status_code != 200:
            print(f"Erro: {str(r.status_code)}")
            break

        # Print the results
        json_output = json.dumps(r.json()["Data"]["Logs"], indent=4)
        logs_json_string = json_output.split(',')
        if StaticConfig.DEBUG == True:
            print(json_output)

        for log in logs_json_string:
            DynamicConfig.log_list.append(retrieveImportantInfoFromLog(DynamicConfig.selected_logtype_regex_patterns, log))

        # Continue getting the correct number of pages based on "since_time"
        nextlink = r.json()["Data"]["Next"]

        # Check if nextlink is None to break loop and stop retriving data from the current page
        if nextlink is None:
            break

        # If nextlink ins't None, keep getting data
        useQueryString = nextlink[nextlink.index('?'):]
