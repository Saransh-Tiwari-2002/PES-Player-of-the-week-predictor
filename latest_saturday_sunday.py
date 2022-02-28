import datetime 
today = datetime.date.today()
last_sunday_offset = today.weekday() + 1  # convert day format mon-sun=0-6 => sun-sat=0-6 
last_sunday = int(str(today - datetime.timedelta(days=last_sunday_offset)).replace('-',''))
last_saturday=last_sunday-1
last_monday=last_sunday+1
