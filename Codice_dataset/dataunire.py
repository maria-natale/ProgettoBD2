import pandas as pd
from tqdm import tqdm
import numpy as np



la = pd.read_csv("/content/drive/MyDrive/datasetbd2/inspections.csv", sep=',')
la_violations = pd.read_csv("/content/drive/MyDrive/datasetbd2/violations.csv", sep=',')
#print(ch['Risk'].unique())
#print(ch['Facility Type'].unique())


def eliminate_rows():
  ch = pd.read_csv("/content/drive/MyDrive/datasetbd2/Food_Inspections.csv", sep=',')
  names = ['Restaurant', 'Special Event', 'Bakery', 'Catering', 'RESTAURANT/GROCERY STORE' ,  'Mobile Food Preparer',
    'Mobile Prepared Food Vendor', 'tavern', 'COFFEE  SHOP',  'cafeteria', 'Grocery(Sushi prep)', 'Cafeteria',
    'Reataurant/Bar', 'GROCERY/RESTAURANT', 'Grocery & Restaurant', 'GROCERY/BAKERY', 'RESTAURANT/BAR', 'GROCERY& RESTAURANT',
    'COFFEE SHOP', 'coffee shop' , 'RESTAURANT AND LIQUOR', 'BREWPUB', 'Tavern', 'BAKERY/RESTAURANT', 
    'restaurant', 'Coffee shop', 'ROOFTOP/RESTAURANT', 'ROOFTOPS', 'smoothie bar','BAR','donut shop'
    'GROCERY/ RESTAURANT','GELATO SHOP',  'COFFEE ROASTER', 'GROCERY/CAFE', 'MOBILE FOOD DESSERTS VENDOR', 
    'GROCERY/TAVERN', 'RESTAURANT/BAKERY', 'grocery & restaurant', 'Tavern/Bar', 'Ice cream', 'BAKERY/ RESTAURANT',
    'TAVERN/LIQUOR']

  ch_new = pd.DataFrame(columns = ch.columns)
  for i, row in tqdm(ch.iterrows()):
      if row[4] in names:
          ch_new.loc[-1] = row
          ch_new.index+=1

  ch_new.to_csv("/content/drive/MyDrive/datasetbd2/chicago_new.csv", index = False)


def data_visualization():
  #pd.set_option('display.max_rows', None)
  ny = pd.read_csv("/content/drive/MyDrive/datasetbd2/DOHMH_New_York_City_Restaurant_Inspection_Results.csv", sep=',')
  table = pd.DataFrame(columns = ['grade', 'min_score', 'max_score'])
  grades = ny['GRADE'].unique()
  for grade in grades:
    df = ny.loc[ny['GRADE'] == grade]
    column = df['SCORE']
    max_value = column.max()
    min_value = column.min()
    table.loc[-1] = [grade, min_value, max_value]
    table.index+=1
    #if grade == 'C':
    #  print(column)

  
  ch = pd.read_csv("/content/drive/MyDrive/datasetbd2/chicago_new.csv")
  pd.set_option('display.max_columns', 20)
  #print(ch.sort_values(by = 'DBA Name')[['Inspection ID', 'DBA Name', 'License #', 'Inspection Date',  'Violations']])
  #print(ch.duplicated(subset = ['DBA Name', 'Inspection Date']).value_counts())
  print(table)




def union_newyork(df):
  ny = pd.read_csv("/content/drive/MyDrive/datasetbd2/DOHMH_New_York_City_Restaurant_Inspection_Results.csv", sep=',')
  grades = {
    'A': 'Risk 3 (Low)',
    'B': 'Risk 2 (Medium)',
    'C': 'Risk 1 (High)',
    'Not Yet Graded': 'Not Yet Graded',
    'Z': 'Not Yet Graded',
    'P': 'Not Yet Graded'
  }
  ny = ny.where(pd.notnull(ny), None)

  for i, row in tqdm(ny.iterrows()):
    new_row = []
    new_row.append(row['DBA'])
    if row['BUILDING'] is not None:
      new_row.append(row['BUILDING']+' '+row['STREET'])
    else:
      new_row.append(row['STREET'])
    new_row.append(row['BORO'])
    new_row.append(row['ZIPCODE'])
    new_row.append(row['PHONE'])
    new_row.append(np.nan)
    new_row.append(row['CUISINE DESCRIPTION'])
    new_row.append(row['INSPECTION DATE'])
    new_row.append(row['VIOLATION DESCRIPTION'])
    risk = grades[row['GRADE']] if row['GRADE'] is not None else 'Not Yet Graded'
    new_row.append(risk)
    df.loc[-1]=new_row
    df.index+=1

  print(df)
  df.to_csv("/content/drive/MyDrive/datasetbd2/dataset_mod/dataset_all.csv", index = False)
  return df


if __name__=='__main__':
  #eliminate_rows()
  #data_visualization()
  columns = ['name', 'address', 'city', 'zipcode', 'phone', 'type', 'cuisine_description',
    'inspection_date', 'violation', 'risk']
  df = pd.DataFrame(columns = columns)
  df = union_newyork(df)


