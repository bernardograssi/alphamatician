from bs4 import BeautifulSoup
import pandas as pd
import xlsxwriter
import requests

# Create dataframe
df = pd.DataFrame(columns=["Job Title", "Job Location", "Job ID"])

# Page variable to use in url
page = 1
while True:
    # Request data from the website
    r = requests.get("https://jobs.walgreens.com/search-jobs/results?ActiveFacetID=6252001-5855797-5855051&CurrentPage=" + str(page) + "&RecordsPerPage=1000&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&CustomFacetName=&FacetTerm=&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search&SortCriteria=0&SortDirection=0&SearchType=5&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf=")

    # Convert request body into json and get all the data under the 'results' key
    j = r.json()['results']
    soup = BeautifulSoup(j, 'html.parser') # Create BeautifulSoup object to parse html
    locations = [s.get_text() for s in soup.findAll("span", {"class": "job-location"})] # Get locations from request
    titles = [s.get_text() for s in soup.findAll("h2")] # Get titles from request
    ids = [i.attrs['data-job-id'] for i in soup.findAll("a") if i.has_attr("data-job-id")] # Get IDs from request
    page += 1 # Increment page by 1

    # For each location and title, create a list containing both and add it as a row to the dataframe
    for t, l, jid in zip(titles, locations, ids):
        row = list([t, l, jid])
        df.loc[len(df)] = row

    # If no more jobs are found, get out of the loop
    if len(locations) == 0:
        break

# Write to excel and set cells width to fit all the data we need
writer = pd.ExcelWriter("alphamatician.xlsx", engine="xlsxwriter")
df["Job Location"] = df["Job Location"].apply(lambda x: x + "PR" if x.endswith(", ") else x)
df.to_excel(writer, index=False)
worksheet = writer.sheets['Sheet1']
worksheet.set_column("A:A", 50)
worksheet.set_column("B:B", 30)
worksheet.set_column("C:C", 15)
writer.save()