from datetime import datetime
from datetime import timedelta
from pytz import timezone 
import pandas as pd
import time
import schedule
import ReadDateFromGoogleSheets as rdfgs
import SendWhatsappWithSelenium as swws


# Schedule the message sending
def schedule_message(phone_number, message, hour, minute):
    schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(swws.send_message, phone_number, message)

# Send message to the qualified members
def send_message_to_qualified_members(message, df_date):
    hour, minute = 10, 30  # Send message at 10:30

    # Iterate through the DataFrame using itertuples()
    for row in df_date.itertuples():
        phone_nbr_string = "+91" + row.Phone_Number
        phone_number =  int(phone_nbr_string)
        schedule_message(phone_number, message, hour, minute)

# Qualify members on the basis of their expiry date of the membership
def qualify_members():
    df = rdfgs.ReadDataFromGoogleSheets()
    if df is None:
        print("No dataframe")
        return
    elif df.empty:
        print("No entries in dataframe")
        return
    else:
        df = df[['Name','Phone Number','End Date']]
        df.columns = ['Name', 'Phone_Number', 'End_Date']
    
    # Remove entries with empty column entries
    df = df.dropna()

    # Convert 'End Date' column to datetime type
    df['End_Date'] = pd.to_datetime(df['End_Date'], dayfirst='true')

    # Get the current date
    current_date = datetime.now((timezone("Asia/Kolkata"))).date()

    # Calculate the target date (7 days before the current date)
    target_date7 = current_date + timedelta(days=7)

    # Calculate the target date (3 days before the current date)
    target_date3 = current_date + timedelta(days=3)

    # Filter the DataFrame to get entries with the date exactly 7 days before the current date
    df_7days = df[df['End_Date'].dt.date == target_date7]

    # Filter the DataFrame to get entries with the date exactly 3 days before the current date
    df_3days = df[df['End_Date'].dt.date == target_date3]

    # Filter the DataFrame to get entries with the date exactly as the current date
    df_expired = df[df['End_Date'].dt.date == current_date]

    # Set the required messages to be sent as per respective days
    message_7days = "Dear Member,\nYour membership of Run Fitness Gym expires in 7 days."
    message_3days = "Dear Member,\nYour membership of Run Fitness Gym expires in 3 days."
    message_expired = "Dear Member,\nYour membership of Run Fitness Gym expires today."

    print(df_7days) 
    print(target_date7)
    print(df_3days)
    # Send message
    if not df_7days.empty:
        send_message_to_qualified_members(message_7days, df_7days)

    if not df_3days.empty:
        send_message_to_qualified_members(message_3days, df_3days)

    if not df_expired.empty:
        send_message_to_qualified_members(message_expired, df_expired)

# Call the qualify members method
qualify_members()

# Keep the app running
while True:
    schedule.run_pending()
    time.sleep(1)