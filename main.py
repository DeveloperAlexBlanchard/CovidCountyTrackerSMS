from datetime import datetime
import requests
import csv
from twilio.rest import Client
import pandas as pd


# NUMBER 1:
# As a user, I want to know how many county is doing compared to others (Or just list counties in the high risk)


# Twilio Authentication
ACCOUNT_SID = 'AC911f113cfcd849f9d099a5136a2d83eb'
AUTH_TOKEN = 'AUTH_TOKEN'
client = Client(ACCOUNT_SID, AUTH_TOKEN)


# Every day at 8:00 AM, Send SMS Message to Phone with Current Updated CDC Information
now = datetime.now()
current_time = now.strftime("%H:%M")
print(current_time)
if current_time == '08:00':


    # Covid Database API
    county_request = requests.get('https://api.covidactnow.org/v2/county/06085.json?apiKey=AUTH_TOKEN')
    county_data = county_request.json()


    # Gathering Data from API
    daily_cases = round(county_data['metrics']['weeklyNewCasesPer100k'])
    vaccinated = "{:.0%}".format(county_data['metrics']['vaccinationsCompletedRatio'])
    booster_shot = "{:.0%}".format(county_data['metrics']['vaccinationsAdditionalDoseRatio'])
    unvaccinated_population = county_data['population'] - county_data['actuals']['vaccinationsCompleted']
    unvaccinated = "{:.0%}".format(unvaccinated_population / county_data['population'])
    TodayDate = county_data['lastUpdatedDate']


    # Determine Risk Level of County
    if daily_cases < 200:
        riskLevel = 'Low 🟢'
        riskDesc = 'County Case Rates have remained at an alltime low, and masks are not mandatory. All social events such as ' \
               'bars, restaurants, and other indoor social gatherings will remain open. Masking is optional, but encouraged ' \
               'to practice safety.'
    elif 200 < daily_cases < 549:
        riskLevel = 'Medium 🟡'
        riskDesc = 'County Case Rates have become more common, but not at a dangerous level. While the mask mandate is optional, county ' \
               'residents are encouraged to mask up when going out in public. All social events such as bars, restaurants, and other ' \
               'indoor social gatherings will remain open. However, if cases continue to rise, then these events may be shut down.'
    else:
        riskLevel = 'High 🔴'
        riskDesc = 'County Case Rates are at an all time high, and masks are mandatory. All social events, bars, restaurants, ' \
               'and other indoor social gathering are to be discontinued until cases are reduced. Furthermore, all businesses ' \
               'that are do not provide governmental, or food, services are to be shutdown effective immediately. Employees are now required to work from home, ' \
               'until further notice.'


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
        writer.writerow([TodayDate, daily_cases])
        File.close()


    # Open the same CSV file from earlier, but instead of adding onto it, we're going to read it.
    with open('history.csv', 'r') as File:
        csvreader = csv.reader(File)
        header = next(csvreader)
        rows = []
        for row in csvreader:
            rows.append(row)
        print(rows)
        File.close()


    # Showcase if Cases have Risen or Dropped since Yesterday
    yesterday_cases = 232
    difference = abs(daily_cases - yesterday_cases)
    up_down = None
    caseDiff = None
    if daily_cases > yesterday_cases:
        up_down = '🔺'
        caseDiff = f'County Covid Cases have risen by {difference} cases since yesterday.'
    elif daily_cases < yesterday_cases:
        up_down = '🔻'
        caseDiff = f'County Covid Cases have dropped by {difference} cases since yesterday.'
    else:
        up_down = ''
        caseDiff = f'County Covid Cases have remained at the same number since yesterday.'

    # SMS Text Sent to Phone
    text_message = [f'.\n\nSANTA CLARA COUNTY \nCDC UPDATE AS OF \n{TodayDate}\n\n----------------------------'
                    f'\n\nRISK LEVEL: \n{riskLevel}\n\n{riskDesc}\n\n----------------------------'
                    f'\n\nCASE RATE: \n{daily_cases}{up_down}\n\n{caseDiff}\n\n----------------------------'
                    f'\n\nUNVACCINATED: \n{unvaccinated} \n\nFULLY VACCINATED: \n{vaccinated} \n\nBOOSTER SHOT: \n{booster_shot}\n\n----------------------------'
                    f'\n\n{maskMandate}']


    # Send Covid Tracker SMS
    message = client.messages.create(
        body= text_message,
        from_= '+19035322609',
        to= "MY PHONE NUMBER"
    )


else:
    pass
