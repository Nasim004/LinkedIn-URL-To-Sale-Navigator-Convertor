import gspread
from linkedin_api import Linkedin
from linkedin_api import Linkedin
from dotenv import dotenv_values
from urllib.parse import unquote
from urllib.parse import urlparse, urlencode
from oauth2client.service_account import ServiceAccountCredentials

# env_vars = dotenv_values('.env')
# username = env_vars.get('username')
# password = env_vars.get('password')

username = "Username of LinkedIn account"
password = 'Password of LinkedIn account'



try:
    api = Linkedin(username=username, password=password)
except:
    print("username or password is incorrect")
    exit()


sales_navigator_base_url = 'https://www.linkedin.com/sales/company/'

try:
    google_sheet_credentials = r"Google credentials path here"
except:
    print('Credential file not found')

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    google_sheet_credentials, scope)
gc = gspread.authorize(credentials)


sheet_url = 'Google sheet url'
sheet = gc.open_by_url(sheet_url).sheet1


column = 1
sales_column = 2
linkedin_urls = sheet.col_values(column)[1:]
newly_added_cell = len(sheet.col_values(sales_column)[1:]) + 1

linkedin_urls = sheet.col_values(column)[newly_added_cell:]
company_names = [unquote(urlparse(url).path.split('/')[-1])
                 for url in linkedin_urls]

sales_navigator_urls = []
for index, company_name in enumerate(company_names, start=newly_added_cell):
    if not company_name:
        continue
    try:
        company_details = api.get_company(company_name)
        company_id = company_details['followingInfo']['entityUrn'].split(
            ':')[-1]
        sales_navigator_url = sales_navigator_base_url + company_id
        sheet.update_cell(index+1, sales_column, sales_navigator_url)
    except KeyError as e:
        print(
            f"Error occurred for company: {company_name}. Skipping to next company.")
        continue
exit()
