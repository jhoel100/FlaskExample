#!/usr/bin/env python
from flask import Flask, jsonify, render_template
import csv
import pandas as pd
import numpy as np

app = Flask(__name__)

titanic_df = pd.read_csv("static/data/train.csv")
survived = titanic_df[(titanic_df['Survived']==1) 
                      & (titanic_df["Age"].notnull())]


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


@app.route('/api/coords/crime_type')
def get_coords_by_crime_type():
    grouped = crimes_sel.groupby("Primary Type")
    # print(np.array(grouped))
    class_labels = crimes_df['Primary Type'].unique()
    data = []
    for i in class_labels:
        data.append(grouped.get_group(i))

    separado = []
    for i in range(len(data)):
        separado.append(data[i].loc[:, ['Longitude', 'Latitude']])

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


@app.route('/api/coords/by_year')
def get_coords_by_year():
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

@app.route('/api/coords/by_month')
def get_coords_by_month():
    # by_year = crimes_sel.groupby("Year")
    class_labels = crimes_df['Year'].unique().tolist()
    years = {}
    for ix, row in crimes_df.dropna().iterrows():
        ilatitude = float(row['Latitude'])
        ilongitude = float(row['Longitude'])
        iyear = int(row['Year'])
        idate = datetime.strptime(row['Date'], '%m/%d/%Y %H:%M:%S %p')

        if iyear not in years:
            # years[iyear] = [[ilongitude, ilatitude]]
            years[iyear] = dict()
            years[iyear][idate.month] = [[ilongitude, ilatitude]]
        else:
            if idate.month not in years[iyear]:
                years[iyear][idate.month] = [[ilongitude, ilatitude]]
            else:
                years[iyear][idate.month].append([ilongitude, ilatitude])

    return jsonify(years)
  
  
@app.route('/get_piechart_data')
def get_piechart_data():
    class_labels = ['Class I', 'Class II', 'Class III']
    pclass_percent = calculate_percentage(survived.groupby('Pclass').size().values, survived['PassengerId'].count())*100
    pieChartData = []
    for index, item in enumerate(pclass_percent):
        eachData = {}
        eachData['category'] = class_labels[index]
        eachData['measure'] =  round(item,1)
        pieChartData.append(eachData)

    return jsonify(pieChartData)

@app.route('/get_barchart_data')
def get_barchart_data():
    age_labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79']
    survived["age_group"] = pd.cut(survived.Age, range(0, 81, 10), right=False, labels=age_labels)
    survived[['age_group', 'Pclass']]

    survivorFirstClass = survived[survived['Pclass']==1]
    survivorSecondClass = survived[survived['Pclass']==2]
    survivorThirdClass = survived[survived['Pclass']==3]

    survivorAllclassPercent = calculate_percentage(survived.groupby('age_group').size().values,survived['PassengerId'].count())*100
    survivorFirstclassPercent = calculate_percentage(survivorFirstClass.groupby('age_group').size().values,survivorFirstClass['PassengerId'].count())*100
    survivorSecondclassPercent = calculate_percentage(survivorSecondClass.groupby('age_group').size().values,survivorSecondClass['PassengerId'].count())*100
    survivorThirdclassPercent = calculate_percentage(survivorThirdClass.groupby('age_group').size().values,survivorThirdClass['PassengerId'].count())*100

    barChartData = []
    for index, item in enumerate(survivorAllclassPercent):
        eachBarChart = {}
        eachBarChart['group'] = "All"
        eachBarChart['category'] = age_labels[index]
        eachBarChart['measure'] = round(item,1)
        barChartData.append(eachBarChart)

    for index, item in enumerate(survivorFirstclassPercent):
        eachBarChart = {}
        eachBarChart['group'] = "Class I"
        eachBarChart['category'] = age_labels[index]
        eachBarChart['measure'] = round(item,1)
        barChartData.append(eachBarChart)

    for index, item in enumerate(survivorSecondclassPercent):
        eachBarChart = {}
        eachBarChart['group'] = "Class II"
        eachBarChart['category'] = age_labels[index]
        eachBarChart['measure'] = round(item,1)
        barChartData.append(eachBarChart)

    for index, item in enumerate(survivorThirdclassPercent):
        eachBarChart = {}
        eachBarChart['group'] = "Class III"
        eachBarChart['category'] = age_labels[index]
        eachBarChart['measure'] = round(item,1)
        barChartData.append(eachBarChart)
    
    return jsonify(barChartData)

@app.route('/get_map_data')
def get_map_data():
    return 1


if __name__ == '__main__':
    app.run(debug=True, port=5002)
