# TeachworksScrape
Scraping Teachworks to get daily wages

This was moreso a script for myself to track my earnings since most budgetting apps don't account for gig workers who make a different amount each week or day.

Anyone else using Teachworks, feel free to use it! I will eventually add more functionality to this.

Set up an .env in the same directoy as the script with the following values:

* USERNAME=teachworks login name
* PASS=teachworks password
* TESTPREP=Test prep hourly rate
* SCHOOL=School tutoring hourly rate
* TAX=What percentage of taxes are taken out of your check each week

## Pip Package Requirements:
* Selenium using Firefox
* BeautifulSoup
* DotEnv

# TODO
* Setup SQLITE DB
* Setup simple webapp to track everything
* Add in budgetting 
