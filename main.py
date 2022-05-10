import requests

response = requests.get('https://api.covidactnow.org/v2/county/06085.json?apiKey=c8275ae6f8074670ab819ba7937aa71a')
county_data = response.json()

# Gathering Data from API
state = county_data['state']
county = county_data['county']
weekly_new_cases = county_data['metrics']['weeklyNewCasesPer100k']
population = county_data['population']
one_dose = county_data['actuals']['vaccinationsInitiated']
one_dose_percentage = county_data['metrics']['vaccinationsInitiatedRatio']
vaccinated = county_data['actuals']['vaccinationsCompleted']
vaccinated_percentage = county_data['metrics']['vaccinationsCompletedRatio']
additional_dose = county_data['actuals']['vaccinationsAdditionalDose']
additional_dose_percentage = county_data['metrics']['vaccinationsAdditionalDoseRatio']
unvaccinated = int(population) - int(vaccinated)

print(county_data)
print(f'Weekly New Cases: {weekly_new_cases}')
print(f'County Population: {population}')
print(f'Unvaccinated: {unvaccinated}')
print(f'One Dose: {one_dose}')
print(f'Fully Vaccinated Percentage: {vaccinated_percentage}')
print(f'Booster Shot Percentage: {additional_dose_percentage}')
