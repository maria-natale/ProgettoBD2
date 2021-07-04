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