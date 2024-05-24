import pywhatkit
 
phone_nbr = "+918450937773"

try: 
    pywhatkit.sendwhatmsg_instantly(phone_nbr, 
                        "Test message from Python!", 
                        15, tab_close=True)
except:
    # handling exception 
    # and printing error message
    print("An Unexpected Error!")
