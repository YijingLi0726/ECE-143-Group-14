import pandas as pd

df = pd.read_excel('Race and Ethnicity by Neighborhood in San Diego.xlsx', sheetname='Sheet1')  # sheetname is optional
df.to_csv('EthnicityByNeighborhoodInSD.csv', index=False)  # index=False prevents pandas to write row index