#!/usr/bin/env python
from flask import Flask, jsonify, render_template
import csv
import pandas as pd
import numpy as np

app = Flask(__name__)

crimes_df = pd.read_csv("static/data/Crimes.csv")
crimes_sel = crimes_df[(crimes_df["X Coordinate"].notnull())
                       & (crimes_df["Y Coordinate"].notnull())]


@app.route('/')
def index():
    return render_template('home.html')


def calculate_percentage(val, total):
    """calcula los procentajes del total"""
    percent = np.divide(val, total)
    return percent


@app.route('/api/coords_by_crime_type')
def get_year():
    grouped = crimes_sel.groupby("Primary Type")
    # print(np.array(grouped))
    class_labels = crimes_df['Primary Type'].unique()
    data = []
    for i in class_labels:
        data.append(grouped.get_group(i))

    separado = []
    for i in range(len(data)):
        separado.append(data[i].loc[:, ['Latitude', 'Longitude']])

    # JSon1 = []
    JSon1 = {}
    for i in range(len(separado)):
        # eachData = {}
        # eachData['category'] = class_labels[i]
        # eachData['data'] = separado[i].values.tolist()
        # JSon1.append(eachData)
        if class_labels[i] not in JSon1:
            JSon1[class_labels[i]] = separado[i].values.tolist()
    return jsonify(JSon1)


@app.route('/api/coords_by_year')
def get_crimes():
    grouped = crimes_sel.groupby("Year")
    class_labels = crimes_df['Year'].unique().tolist()
    data = []
    for i in class_labels:
        data.append(grouped.get_group(i))

    separado = []
    for i in range(len(data)):
        separado.append(data[i].loc[:, ['Latitude', 'Longitude']])

    # JSon1 = []
    JSon1 = {}
    for i in range(len(separado)):
        # eachData = {}
        # eachData['category'] = class_labels[i]
        # eachData['data'] = separado[i].values.tolist()
        # JSon1.append(eachData)
        if class_labels[i] not in JSon1:
            JSon1[class_labels[i]] = separado[i].values.tolist()
    return jsonify(JSon1)


if __name__ == '__main__':
    app.run(debug=True, port=5002)
