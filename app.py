from flask import Flask, render_template, request
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import tkinter as tk
from threading import Thread


app = Flask(__name__)

def run_tkinter_app():
    root = tk.Tk()
    
    root.mainloop()

tkinter_thread = Thread(target=run_tkinter_app)
tkinter_thread.start()

def get_data(cloudName):
    if cloudName is None:
        return pd.DataFrame() 
    conn = sqlite3.connect('jobs_offers.db')
    query = f"SELECT quantityPracuj, numberJoin, quantityNFJ, numberProtocol, quantityAll FROM \"{cloudName}\""
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def create_plot(df, cloudName):
    df['Total'] = df['quantityPracuj'] + df['numberJoin'] + df['quantityNFJ'] + df['numberProtocol']
    data = {
        'Pracuj.pl': df['quantityPracuj'].sum(),
        'JustJoin': df['numberJoin'].sum(),
        'No Fluff Jobs': df['quantityNFJ'].sum(),
        'theProtocol': df['numberProtocol'].sum()
    }
    labels = []
    sizes = []
    for label, size in data.items():
        if size > 0:
            labels.append(label)
            sizes.append(size)
    plt.figure()
    plt.title(f"Podział ofert dla {cloudName}")
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)

    sum = int(df['quantityAll'])
    plt.text(0.5, -0.25, f"Total offers for {cloudName} is: {sum}", horizontalalignment='center', fontsize=12, transform=plt.gca().transAxes)

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    
    return image_base64
def get_dataWebiste(websiteName):
    if websiteName is None:
        return pd.DataFrame()  
    conn = sqlite3.connect('jobs_offers.db')
    query = f"SELECT portal_name, quantity FROM \"{websiteName}\""
    querySum = f"SELECT SUM(quantity) as total FROM \"{websiteName}\""  
    dw = pd.read_sql_query(query, conn)
    dwSum = pd.read_sql_query(querySum, conn)['total'].iloc[0]
    if dwSum is None:
        dwSum = 0  
    conn.close()
    return dw, int(dwSum)


def create_plot_website(dw, dwSum, websiteName):
    if dw.empty:
        return None
    filtered_dw = dw[dw['quantity'] > 0]

    if filtered_dw.empty:
        return None

    labels = filtered_dw['portal_name'].tolist()
    sizes = filtered_dw['quantity'].tolist()

    plt.title(f"Podział ofert dla {websiteName}")
    plt.figure()
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.text(0.5, -0.25, f"Total offers for {websiteName} is: {dwSum}", horizontalalignment='center', fontsize=12, transform=plt.gca().transAxes)

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()

    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()

    return image_base64



@app.route('/', methods=['GET'])
def index():
    cloudName = request.args.get('cloudName')
    websiteName = request.args.get('websiteName')
    plot = None
    plotWebiste = None
    if cloudName:
        df = get_data(cloudName)
        plot = create_plot(df, cloudName)
        return render_template('index.html', plot=plot, cloudName=cloudName)
    elif websiteName:
        dw, dwSum = get_dataWebiste(websiteName) 
        plotWebiste = create_plot_website(dw, dwSum, websiteName)  
        return render_template('index.html', plotWebiste=plotWebiste, websiteName=websiteName)
    
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)