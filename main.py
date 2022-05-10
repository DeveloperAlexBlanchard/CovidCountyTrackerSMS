import requests

response = requests.get('https://api.covidactnow.org/v2/county/06085.json?apiKey=c8275ae6f8074670ab819ba7937aa71a')
county_data = response.json()

# Gathering Data from API
state = county_data['state']
county = county_data['county']
weekly_new_cases = county_data['metrics']['weeklyNewCasesPer100k']
population = county_data['population']
one_dose_percentage = "{:.0%}".format(county_data['metrics']['vaccinationsInitiatedRatio'])
vaccinated = "{:.0%}".format(county_data['metrics']['vaccinationsCompletedRatio'])
booster_shot = "{:.0%}".format(county_data['metrics']['vaccinationsAdditionalDoseRatio'])
unvaccinated_population = county_data['population'] - county_data['actuals']['vaccinationsCompleted']
unvaccinated = "{:.0%}".format(unvaccinated_population / population)

print(county_data)
print(county_data['actuals'])
print(f'Weekly New Cases: {weekly_new_cases}')
print(f'Fully Vaccinated Percentage: {vaccinated}')
print(f'Booster Shot Percentage: {booster_shot}')
print(f'Unvaccinated Percentage: {unvaccinated}')
