import requests

response = requests.get('https://api.covidactnow.org/v2/county/06085.json?apiKey=c8275ae6f8074670ab819ba7937aa71a')
county_data = response.json()
# print(county_data)
# print(county_data['annotations']['cases']['anomalies'])
# print(county_data['anomalies']['date'])

# population = county_data['population']
# state = county_data['state']
# county = county_data['county']
# one_dose_percentage = "{:.0%}".format(county_data['metrics']['vaccinationsInitiatedRatio'])

# Gathering Data from API
weekly_new_cases = round(county_data['metrics']['weeklyNewCasesPer100k'])
vaccinated = "{:.0%}".format(county_data['metrics']['vaccinationsCompletedRatio'])
booster_shot = "{:.0%}".format(county_data['metrics']['vaccinationsAdditionalDoseRatio'])
unvaccinated_population = county_data['population'] - county_data['actuals']['vaccinationsCompleted']
unvaccinated = "{:.0%}".format(unvaccinated_population / county_data['population'])
lastUpdatedDate = county_data['lastUpdatedDate']


if weekly_new_cases < 200:
    riskLevel = 'Low 🟢'
elif 200 < weekly_new_cases < 2000:
    riskLevel = 'Medium 🟡'
else:
    riskLevel = 'High 🔴'

# print(county_data)
# print(county_data['actuals'])
print(f'Current Date:      {lastUpdatedDate}\n')
print(f'Risk Level:        {riskLevel}')
print(f'Current Case Rate: {weekly_new_cases} per 100k\n')
print(f'Unvaccinated:      {unvaccinated}')
print(f'Fully Vaccinated:  {vaccinated}')
print(f'Booster Shot:      {booster_shot}')
