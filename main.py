import requests
from twilio.rest import Client


# Twilio Authentication
ACCOUNT_SID = 'AC911f113cfcd849f9d099a5136a2d83eb'
AUTH_TOKEN = '89df572676764e9f0ceebd8071e4725f'
client = Client(ACCOUNT_SID, AUTH_TOKEN)


# Covid Database API
county_request = requests.get('https://api.covidactnow.org/v2/county/06085.json?apiKey=c8275ae6f8074670ab819ba7937aa71a')
county_data = county_request.json()


# Gathering Data from API
weekly_new_cases = round(county_data['metrics']['weeklyNewCasesPer100k'])
vaccinated = "{:.0%}".format(county_data['metrics']['vaccinationsCompletedRatio'])
booster_shot = "{:.0%}".format(county_data['metrics']['vaccinationsAdditionalDoseRatio'])
unvaccinated_population = county_data['population'] - county_data['actuals']['vaccinationsCompleted']
unvaccinated = "{:.0%}".format(unvaccinated_population / county_data['population'])
lastUpdatedDate = county_data['lastUpdatedDate']


# Determine Risk Level of County
if weekly_new_cases < 200:
    riskLevel = 'Low 🟢'
elif 200 < weekly_new_cases < 2000:
    riskLevel = 'Medium 🟡'
else:
    riskLevel = 'High 🔴'


# SMS Text Sent to Phone
text_message = [f'\nDate: {lastUpdatedDate} \nRisk Level: {riskLevel} \nCase Rate: {weekly_new_cases} '
                f'\nUnvaccinated: {unvaccinated} \nFully Vaccinated: {vaccinated} \nBooster Shot: {booster_shot}']


# Send Covid Tracker to Phone
message = client.messages.create(
    body= text_message,
    from_= '+19035322609',
    to= '+14087075378'
)
