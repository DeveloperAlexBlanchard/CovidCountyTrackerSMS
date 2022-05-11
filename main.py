import requests
import csv
from twilio.rest import Client

# Twilio Authentication
ACCOUNT_SID = 'AC911f113cfcd849f9d099a5136a2d83eb'
AUTH_TOKEN = '433716f7777cfd1f48ba62e144530d05'
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Covid Database API
county_request = requests.get('https://api.covidactnow.org/v2/county/06085.json?apiKey=c8275ae6f8074670ab819ba7937aa71a')
county_data = county_request.json()


# Gathering Data from API
daily_cases = round(county_data['metrics']['weeklyNewCasesPer100k'])
vaccinated = "{:.0%}".format(county_data['metrics']['vaccinationsCompletedRatio'])
booster_shot = "{:.0%}".format(county_data['metrics']['vaccinationsAdditionalDoseRatio'])
unvaccinated_population = county_data['population'] - county_data['actuals']['vaccinationsCompleted']
unvaccinated = "{:.0%}".format(unvaccinated_population / county_data['population'])
lastUpdatedDate = county_data['lastUpdatedDate']


# Determine Risk Level of County
if daily_cases < 200:
    riskLevel = 'Low 🟢'
elif 200 < daily_cases < 549:
    riskLevel = 'Medium 🟡'
else:
    riskLevel = 'High 🔴'


# Santa Clara County Mask Mandate is Based Daily Cases, if Cases Remain under 550, it will not be Enforced. However, If we Achieve 550+, then the Mask Mandate Goes Back into Effect.
if daily_cases >= 550:
    maskMandate = 'Santa Clara County has exceeded 550 daily cases, and the mask mandate may be/stay enacted until' \
                  'the number falls lower. Until then, (Company) is required to provide CDC materials (masks, hand ' \
                  'sanitizer, and gloves) to all employees that come into the office.'
else:
    maskMandate = 'Santa Clara County has remained under 550 daily cases, and the mask mandate is currently not in effect until ' \
                  'the numbers start to grow. At this time, masks are not required while indoors or in large crowds.'


# CSV file that Contains Past Dates and their Data to Compare against Most Recent.
with open('history.csv', 'a') as File:
    writer = csv.writer(File)
    writer.writerow([lastUpdatedDate, daily_cases])
    File.close()


# SMS Text Sent to Phone
text_message = [f'.\nSANTA CLARA COUNTY \nCDC UPDATE AS OF \n{lastUpdatedDate} \n\n\nRISK LEVEL: {riskLevel} \nCASE RATE: {daily_cases} '
                f'\n\n\nUNVACCINATED: {unvaccinated} \nFULLY VACCINATED: {vaccinated} \nBOOSTER SHOT: {booster_shot} '
                f'\n\n\n{maskMandate}']


# Send Covid Tracker to Phone
message = client.messages.create(
    body= text_message,
    from_= '+19035322609',
    to= "MY PHONE NUMBER"
)
