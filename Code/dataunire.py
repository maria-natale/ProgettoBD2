import pandas as pd

ny = pd.read_csv("C:/Users/maria/Desktop/file/DOHMH_New_York_City_Restaurant_Inspection_Results.csv", sep=',')

ch = pd.read_csv("C:/Users/maria/Desktop/file/Chicago_Food_Inspections.csv", sep=',')
#print(ch['Risk'].unique())
#print(ch['Facility Type'].unique())

names = ['Restaurant', 'Special Event', 'Bakery', 'Catering', 'RESTAURANT/GROCERY STORE' ,  'Mobile Food Preparer',
    'Mobile Prepared Food Vendor', 'tavern', 'COFFEE  SHOP',  'cafeteria', 'Grocery(Sushi prep)', 'Cafeteria',
    'Reataurant/Bar', 'GROCERY/RESTAURANT', 'Grocery & Restaurant', 'GROCERY/BAKERY', 'RESTAURANT/BAR', 'GROCERY& RESTAURANT',
    'COFFEE SHOP', 'coffee shop' , 'RESTAURANT AND LIQUOR', 'BREWPUB', 'Tavern', 'BAKERY/RESTAURANT', 
    'restaurant', 'Coffee shop', 'ROOFTOP/RESTAURANT', 'ROOFTOPS', 'smoothie bar','BAR','donut shop'
    'GROCERY/ RESTAURANT','GELATO SHOP',  'COFFEE ROASTER', 'GROCERY/CAFE', 'MOBILE FOOD DESSERTS VENDOR', 
    'GROCERY/TAVERN', 'RESTAURANT/BAKERY', 'grocery & restaurant', 'Tavern/Bar', 'Ice cream', 'BAKERY/ RESTAURANT',
    'TAVERN/LIQUOR']

ch_new = pd.DataFrame(columns = ch.columns)
for i, row in ch.iterrows():
    if row[4] in names:
        ch_new.loc[-1] = row
        ch_new.index+=1
print(ch_new.shape)