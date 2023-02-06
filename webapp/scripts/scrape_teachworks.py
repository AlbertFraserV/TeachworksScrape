import sys
import os
sys.path.append(os.path.abspath("../src"))
from Teachworks import Teachworks
from database import Database

teachworks = Teachworks()
conn = Database()

teachworks.login()
teachworks.navigate_to_calendar_list()
sessions = teachworks.get_daily_sessions()
working_hours = teachworks.calculate_hours(sessions)

wages = (working_hours['test_prep']*teachworks.TEST_PREP_WAGE + working_hours['school']*teachworks.SCHOOL_WAGE)*(1-teachworks.TAX_RATE)
print(f"You made {str(round(wages,2))} after taxes today!")
sql = f"INSERT INTO daily_pay (daily_pay_date, daily_pay) VALUES('{teachworks.today}', {wages});"
conn.commit(sql)
teachworks.close_driver()