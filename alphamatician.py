from selenium import webdriver
import pandas as pd
import xlsxwriter

# Get the driver working
options = webdriver.ChromeOptions()
options.add_argument('lang=pt-br')
driver = webdriver.Chrome(executable_path=r'C:\Users\berna\Downloads\chromedriver_win32 (1)\chromedriver.exe',
                          options=options)

# Access the desired website
driver.get('https://www.walgreensbootsalliance.com/careers/global-brands-careers/opportunities-us')

# Get the block that contains the data we are looking for
all_elements = driver.find_element_by_class_name("clearfix.text-formatted.field.field--name-field-content.field--type-text-long.field--label-hidden.field__item")

# Get the job titles
titles = [x.text for x in all_elements.find_elements_by_tag_name("h5")]

# Get the job locations and job descriptions
locations_and_descriptions = all_elements.find_elements_by_tag_name("p")

# Initialize count variable and lists used to store locations and descriptions
count = 0
dataset = []
locations = []
descriptions = []

# Add locations to the locations list and add descriptions to descriptions list
# Every 3rd element is useless to us, so skip them
for i in locations_and_descriptions:
    if count % 3 == 0:
        locations.append(i.text)
    elif (count - 1) % 3 == 0:
        descriptions.append(i.text)
    count += 1

# Create dataframe
df = pd.DataFrame(columns = ["Job Title", "Job Location", "Job Description"])

# Create the rows of the dataframe
for i in range (0, len(titles)):
    dataset.append(titles[i])
    dataset.append(locations[i])
    dataset.append(descriptions[i])
    df.loc[i] = dataset
    dataset.clear()

# Export dataframe to Excel
writer = pd.ExcelWriter("alphamatician.xlsx", engine="xlsxwriter")
df.to_excel(writer, index=False)

# Set the width of the cells for better visualization
worksheet = writer.sheets['Sheet1']
worksheet.set_column('A:A', 50)
worksheet.set_column('B:B', 15)
worksheet.set_column('C:C', 200)
writer.save()