import pandas as pd
import json
from json import JSONEncoder
import codecs
import re
import datetime, calendar

class Inspection:
  def __init__(self, inspection_data, description, risk):
    self.inspection_date = inspection_data
    self.description = description
    self.risk = risk

  

class Restaurant:
  def __init__(self, name, address, city, zipcode, cuisine_description, restaurant_type, phone, state):
    self.name = name
    self.address = address
    self.city = city
    self.zipcode = zipcode
    self.cuisine_description = cuisine_description
    self.restaurant_type = restaurant_type
    self.phone = phone
    self.state = state
    self.violations = []
  
  def add_violation(self, violation):
    self.violations.append(violation)

class RestaurantEncoder(JSONEncoder):
  def default(self, o):
    for key, value in list(o.__dict__.items()):
      if value is None:
        del o.__dict__[key]
    return o.__dict__


def read_file(filename, state):
  df = pd.read_csv(filename)
  df = df.sort_values(by = ['name', 'address', 'inspection_date'])
  restaurants = []
  df = df.where(pd.notnull(df), None)

  for i, row in df.iterrows():
    name = row['name']
    address = row['address']
    if len(restaurants) == 0 or (restaurants[len(restaurants)-1].name!=name and restaurants[len(restaurants)-1].address!=address):
      city = row['city']
      if city is not None:
        city = city.lower()
      zipcode = row['zipcode']
      cuisine_description = row['cuisine_description']
      restaurant_type = row['type']
      if restaurant_type is not None:
        restaurant_type = restaurant_type.lower()
      phone = row['phone']
      restaurant = Restaurant(name, address, city, zipcode, cuisine_description, restaurant_type, phone, state)
      restaurants.append(restaurant)
    date = row['inspection_date']
    violation = row['violation']
    risk = row['risk']
    restaurants[len(restaurants)-1].add_violation(Inspection(date, violation, risk))
    restaurant.violations.sort(key=lambda r: datetime.datetime.strptime(r.inspection_date, "%m/%d/%Y"),reverse=True)

  
  return restaurants


if __name__ == '__main__':
  l = read_file("/content/drive/MyDrive/datasetbd2/dataset_mod/dataset_all.csv", "New York")
  x = json.dumps(l, indent=4, cls = RestaurantEncoder)
  print(x)
  f = open("/content/drive/MyDrive/datasetbd2/dataset_mod/maria/ny.json", 'w')
  f.write(x)
  f.close()
  filename= "/content/drive/MyDrive/datasetbd2/dataset_mod/maria/ny.json"

  with open (filename, 'r' ) as f:
    content = f.read()
    content_new = re.sub('(\d{2})/(\d{2})/(\d{4})', r'\3-\1-\2', content, flags = re.M)
    print(content_new)
    f = open("/content/drive/MyDrive/datasetbd2/dataset_mod/maria/ny_datenew.json", 'w')
    f.write(content_new)
    f.close()
    #print(content)
  #print(json.dumps(l, indent=4, cls = RestaurantEncoder))"""





