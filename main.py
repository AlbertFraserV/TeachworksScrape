from Teachworks import Teachworks

teachworks = Teachworks()

teachworks.login()
teachworks.navigate_to_calendar_list()
sessions = teachworks.get_daily_sessions()
working_hours = teachworks.calculate_hours(sessions)

wages = (working_hours['test_prep']*teachworks.TEST_PREP_WAGE + working_hours['school']*teachworks.SCHOOL_WAGE)*(1-teachworks.TAX_RATE)
print(f"You made {str(round(wages,2))} after taxes today!")