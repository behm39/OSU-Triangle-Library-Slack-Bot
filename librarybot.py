import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import *

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Library').sheet1


# def main():
#     pprint(get_record_by_attribute('Status', 'Returned'))

# attribute must be a string, key can be anything
def get_record_by_attribute(attribute, key):
    all_records = get_all_records()
    if all_records:
        if attribute in all_records[0].keys():
            # search ignores case and white space.
            return [x for x in all_records if ''.join(str(key).lower().split()) in ''.join(str(x[attribute]).lower().split())]
    return None

# gets all records in the table
def get_all_records():
    temp_table = sheet.get_all_values()
    # table-specific cleanup / dynamic headers extraction
    headers = temp_table[2][1:]
    temp_table = temp_table[3:]
    # table is a list of dictionaries where each dictionary is a row in the table
    table = []
    for row in temp_table:
        row = row[1:]
        to_add = {}
        for i in range(len(headers)):
            to_add[headers[i]] = row[i]
        table.append(to_add)
    return table

