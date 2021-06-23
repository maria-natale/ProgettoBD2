import pandas as pd
from tqdm import tqdm




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

  pd.set_option('display.max_columns', 5)
  print(table)




if __name__=='__main__':
  #eliminate_rows()
  data_visualization()

