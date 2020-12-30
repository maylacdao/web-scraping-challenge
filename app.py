from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from config import password, username
import scrape_mars
