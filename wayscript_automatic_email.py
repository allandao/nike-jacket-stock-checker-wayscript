# Using Python3
# Reference: http://theautomatic.net/2019/01/19/scraping-data-from-javascript-webpage-python/

# import libraries
import urllib3
import requests
from bs4 import BeautifulSoup

# import HTMLSession from requests_html
from requests_html import HTMLSession

# specify the url
#pageURL = 'https://www.nike.com/t/sportswear-windrunner-hooded-windbreaker-qJlX5L/AR2191-380'
pageURL = ['https://www.nike.com/t/sportswear-windrunner-hooded-windbreaker-qJlX5L/AR2191-028',
'https://www.nike.com/t/sportswear-windrunner-hooded-windbreaker-qJlX5L/AR2191-010',
'https://www.nike.com/t/sportswear-windrunner-hooded-windbreaker-qJlX5L/AR2191-661',
'https://www.nike.com/t/sportswear-windrunner-hooded-windbreaker-qJlX5L/AR2191-380',
'https://www.nike.com/t/sportswear-windrunner-hooded-windbreaker-qJlX5L/AR2191-058']

# create an HTML Session object
session = HTMLSession()

currentPage = -1
for page in pageURL:
    currentPage += 1 # Python does not support ++
    # Use the object above to connect to needed webpage
    resp = session.get(page)

    # query the website and return the html to the variable ‘pageURL’
    #pageQueryResult = requests.get(pageURL)

    # ISSUE: sizing toggles are dynamically rendered
    # SOLUTION: Run JavaScript code on webpage and store the resulting HTML additions
    resp.html.render(timeout=20)
    # https://stackoverflow.com/questions/63653201/pyppeteer-errors-timeouterror-navigation-timeout-exceeded-8000-ms-exceeded
    # The above stores the updated HTML as in attribute in resp.html, so we access this
    # via resp.html.html

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(resp.html.html, "lxml")

    # Find the li element with the jacket's colorwave
    clothing_colorwave = soup.find('li', attrs={'class': 'description-preview__color-description'})
    # String email_stock_alert_text created on wayscript via 'Create Variable' in function steps
    email_stock_alert_text += '\n' + clothing_colorwave.text[7:len(clothing_colorwave.text)] + '\n'

    soldOutDiv = soup.find('div', attrs={'class': 'sold-out'})
    if (soldOutDiv == None):
        # soldOutDiv equaling None meaning there is no div of class sold-out found, which essentially
        # means the product is not sold out.
        # size_form is a specific parent div of all the divs containing the size pickers
        size_picker_form = soup.find('div', attrs={'class': 'mt2-sm css-12whm6j'})
        div_sizes = size_picker_form.find_all('div')

        for div in div_sizes:
            if not div.input.has_attr("disabled"):
                email_stock_alert_text += div.label.text + ' - in stock\n'
        
        email_stock_alert_text += pageURL[currentPage] + '\n'
        
    else:
        email_stock_alert_text += 'Sold out\n'

# \n originally for console version of code
email_stock_alert_text = email_stock_alert_text.replace('\n', '<br />')
# Note: html element can simply be inputted as a string, as email treats content as text/html
# If wayscript/email client or code were to create as text/plain, then \n would be properly be
# parsed as a new line, but since it is html, we use <br /> instead.





