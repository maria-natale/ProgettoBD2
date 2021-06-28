import pandas as pd
from tqdm import tqdm
import numpy as np
import os




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




def union_newyork(df_old, columns):
  ny = pd.read_csv("/content/drive/MyDrive/datasetbd2/DOHMH_New_York_City_Restaurant_Inspection_Results.csv", sep=',')
  grades = {
    'A': 'Risk 3 (Low)',
    'B': 'Risk 2 (Medium)',
    'C': 'Risk 1 (High)',
    'Not Yet Graded': 'Not Yet Graded',
    'Z': 'Not Yet Graded',
    'P': 'Not Yet Graded'
  }
  df = pd.DataFrame(columns = columns)
  ny = ny.where(pd.notnull(ny), None)
  ny = ny.loc[50001:100000,:]
  #399918
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
  df = pd.concat([df_old, df])
  df.to_csv("/content/drive/MyDrive/datasetbd2/dataset_mod/dataset_all.csv", index = False)

  return df


def union_la(df_old, columns):
  la = pd.read_csv("/content/drive/MyDrive/datasetbd2/inspections.csv", sep=',')
  la_violations = pd.read_csv("/content/drive/MyDrive/datasetbd2/violations.csv", sep=',')
  grades = {
    'A': 'Risk 3 (Low)',
    'B': 'Risk 2 (Medium)',
    'C': 'Risk 1 (High)',
    'Not Yet Graded': 'Not Yet Graded',
    ' ': 'Not Yet Graded'
  }
  
  la = la.loc[40001:80000, :]
  df = pd.DataFrame(columns = columns)
  #191371
  for i, row in tqdm(la.iterrows()):
    new_row = []
    new_row.append(row['facility_name'])
    new_row.append(row['facility_address'])
    new_row.append(row['facility_city'])
    new_row.append(row['facility_zip'])
    new_row.append(np.nan)
    new_row.append(np.nan)
    new_row.append(np.nan)
    new_row.append('activity_date')
    violation_description = la_violations.loc[la_violations['serial_number'] == row['serial_number']]
    new_row.append(violation_description)
    new_row.append(grades[row['grade']])
    df.loc[-1]=new_row
    df.index+=1

  print(df)
  df = pd.concat([df_old, df])
  df.to_csv("/content/drive/MyDrive/datasetbd2/dataset_mod/dataset_all_la.csv", index = False)

  return df



def union_chicago(df_old, columns):
  chicago = pd.read_csv("/content/drive/MyDrive/datasetbd2/chicago_new.csv", sep=',')
  grades = {
    'All': 'Not Yet Graded',
    'Risk 3 (Low)': 'Risk 3 (Low)',
    'Risk 2 (Medium)': 'Risk 2 (Medium)',
    'Risk 1 (High)': 'Risk 1 (High)',
    'Not Yet Graded': 'Not Yet Graded',
    ' ': 'Not Yet Graded'
  }
  chicago = chicago.where(pd.notnull(chicago), None)
  chicago = chicago.loc[30001:65000, :]
  #105272
  df = pd.DataFrame(columns = columns)
  
  for i, row in tqdm(chicago.iterrows()):
    new_row = []
    new_row.append(row['DBA Name'])
    new_row.append(row['Address'])
    new_row.append(row['City'])
    new_row.append(row['Zip'])
    new_row.append(np.nan)
    restaurant_type = row['Facility Type'] if row['Facility Type'] is not None else np.nan
    new_row.append(restaurant_type) 
    new_row.append(np.nan)
    new_row.append('Inspection Date')
    violation_description = row['Violations'] if row['Violations'] is not None else np.nan
    new_row.append(violation_description)
    new_row.append(grades[row['Risk']])
    df.loc[-1]=new_row
    df.index+=1

  print(df)
  df = pd.concat([df_old, df])
  df.to_csv("/content/drive/MyDrive/datasetbd2/dataset_mod/dataset_all_chicago.csv", index = False)

  return df


def execute_ny(columns):
  if os.path.isfile("/content/drive/MyDrive/datasetbd2/dataset_mod/dataset_all.csv"):
    df = pd.read_csv("/content/drive/MyDrive/datasetbd2/dataset_mod/dataset_all.csv")
  else:
    df = pd.DataFrame(columns = columns)
  print(df.shape)
  #df = union_newyork(df, columns)


def execute_la(columns):
  if os.path.isfile("/content/drive/MyDrive/datasetbd2/dataset_mod/dataset_all_la.csv"):
    df = pd.read_csv("/content/drive/MyDrive/datasetbd2/dataset_mod/dataset_all_la.csv")
  else:
    df = pd.DataFrame(columns = columns)
  print(df.shape)
  df = union_la(df, columns)
  print(df.shape)


def execute_chicago(columns):
  if os.path.isfile("/content/drive/MyDrive/datasetbd2/dataset_mod/dataset_all_chicago.csv"):
    df = pd.read_csv("/content/drive/MyDrive/datasetbd2/dataset_mod/dataset_all_chicago.csv")
  else:
    df = pd.DataFrame(columns = columns)
  print(df.shape)
  df = union_chicago(df, columns)
  print(df.shape)


if __name__=='__main__':
  #eliminate_rows()
  #data_visualization()
  columns = ['name', 'address', 'city', 'zipcode', 'phone', 'type', 'cuisine_description',
    'inspection_date', 'violation', 'risk']
  
  #execute_ny(columns)
  #execute_la(columns)
  execute_chicago(columns) 

  """eseguire los angeles come è messo e poi le successive iterazioni fino ad arrivare a 191371"""
  """eseguire chicago come è messo da 30000 a 65000. Dopo eseguire da 65001 a 105272"""



