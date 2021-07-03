import pandas as pd
import json
from json import JSONEncoder
import codecs
import re

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
      zipcode = row['zipcode']
      cuisine_description = row['cuisine_description']
      restaurant_type = row['type']
      phone = row['phone']
      restaurant = Restaurant(name, address, city, zipcode, cuisine_description, restaurant_type, phone, state)
      restaurants.append(restaurant)
    date = row['inspection_date']
    violation = row['violation']
    risk = row['risk']
    restaurants[len(restaurants)-1].add_violation(Inspection(date, violation, risk))
  
  return restaurants


if __name__ == '__main__':
  """l = read_file("/content/drive/MyDrive/datasetbd2/dataset_mod/dataset_all.csv", "Ney York")
  x = json.dumps(l, indent=4, cls = RestaurantEncoder)
  print(x)
  f = open("/content/drive/MyDrive/datasetbd2/dataset_mod/json/ny.json", 'w')
  f.write(x)
  f.close()"""
  filename= "C:/Users/maria/Downloads/json/la.json"

  with open (filename, 'r' ) as f:
    content = f.read()
    content_new = re.sub('(\d{4})-(\d{2})-(\d{2})', r'\3/\2/\1', "2020-02-12", flags = re.M)
    print(content_new)
    #print(content)
  #print(json.dumps(l, indent=4, cls = RestaurantEncoder))





