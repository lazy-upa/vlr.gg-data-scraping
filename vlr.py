import requests
from bs4 import BeautifulSoup
import pandas as pd

try:
    url = input("Enter the url of the stats page of the event: ")
    file_name = input("Enter the name for your csv file: ")

    data_src = requests.get(url).text
    soup = BeautifulSoup(data_src, "html.parser")

    tables = soup.find('table', class_='wf-table mod-stats mod-scroll')
    th = tables.find_all("th")

    headers = []
    for i in th:
        title = i.text
        headers.append(title)

    df = pd.DataFrame(columns=headers)
    tr_data = tables.find_all("tr")[1:]

    for row in tr_data:
        data = row.find_all('td')
        row_data = [td.text.strip() for td in data]
        df.loc[len(df)] = row_data

    df['Player'].str.replace("\n", " ", regex=True)
    df[['Player', 'Team']] = df['Player'].str.split(expand=True)

    cols = headers.copy()
    cols.insert(1, "Team") 

    df = df[cols] 

    df.to_csv(file_name, index=False)

except:
    print("Some error occured")

finally:
    print("CSV file saved successfully!")