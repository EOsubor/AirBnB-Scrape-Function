# AirBnB-Scrape-Function

Function to scrape AirBnB listing details (Price, Total Price, Bedrooms, Amenities, Home Type, Lisitng Name & Alternate Lisitng Name)
Informtion is output to a CSV file (airbnb_file.csv)


I initially researched the packages which would be best for scraping static and dynamic pages(The requests library wouldn't be 
adequate). I settled on using BeautifulSoup, Selenium. 

I tried to implement a tool called ActionDrviers to automate the scrolling to different elements but couldn't get it to recognize the 
elements/buttons.
To work around this, I created a function to extract the amenities link from any given lisitngs. This way, I was able to extract the 
amenities without clicking the button.

After importing all the necessary packages,  I created multiple functions to handle extracting the required information
from the dynamic pages, extracting amenities and writing the subsequently produced dictionary to a pandas dataframe, where it can be
manipulated and cleaned properly.
