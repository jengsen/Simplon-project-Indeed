from ScrapperIndeed import ScrapperIndeed
import pymongo
from pymongo import MongoClient
from selenium import webdriver

client = MongoClient('localhost', 27017)
db = client['Simplon_Indeed']
collection=db['job_offers']
city_to_scrap = ['Nantes', 'Lyon', 'Toulouse', 'Paris', 'Bordeaux']
work_to_scrap = ['data scientist', 'data analyst', 'développeur', 'business intelligence']

scrapperIndeed=ScrapperIndeed(collection)
scrapperIndeed.scrapp_searches(work_to_scrap, city_to_scrap)
