from flask import Flask, render_template, request
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import tkinter as tk
from threading import Thread
import json

app = Flask(__name__)

def run_tkinter_app():
    root = tk.Tk()
    
    root.mainloop()

tkinter_thread = Thread(target=run_tkinter_app)
tkinter_thread.start()

def get_data(cloudName):
    if cloudName is None:
        return pd.DataFrame()
    with open('jobs_offers.json', 'r') as file:
        data = json.load(file)
    
    provider_data = data['cloudprovider'].get(cloudName, {})
    
    if not provider_data:
        return pd.DataFrame()


    df = pd.DataFrame([provider_data])
    df = df.rename(columns={
        'pracuj': 'quantityPracuj', 
        'justjoin': 'numberJoin', 
        'nfj': 'quantityNFJ', 
        'theprotocol': 'numberProtocol'
    })
    df['quantityAll'] = df.sum(axis=1)
    return df

def create_plot(df, cloudName):
    df['Total'] = df['quantityPracuj'] + df['numberJoin'] + df['quantityNFJ'] + df['numberProtocol']
    data = {
        'Pracuj.pl': df['quantityPracuj'].sum(),
        'JustJoin': df['numberJoin'].sum(),
        'No Fluff Jobs': df['quantityNFJ'].sum(),
        'theProtocol': df['numberProtocol'].sum()
    }
    total = sum(data.values())
    
    sorted_data = sorted(data.items(), key=lambda item: item[1], reverse=True)
    labels = [f"{label} ({(size / total) * 100:.1f}%)" for label, size in sorted_data if size > 0]
    sizes = [size for label, size in sorted_data if size > 0]
    legend_labels = [f"{label} - {size} offers" for label, size in sorted_data if size > 0]
    plt.figure(figsize=(8, 6))
    plt.title(f"Podział ofert dla {cloudName}")
    wedges, texts = plt.pie(sizes, labels=labels, startangle=140)
    plt.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(1, 0.8))
    sum_offers = int(df['quantityAll'])
    plt.axis('equal')
    plt.text(0.5, -0.1, f"Total offers for {cloudName} is: {sum_offers}", horizontalalignment='center', fontsize=12, transform=plt.gca().transAxes)
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()

    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()

    return image_base64

def get_dataWebsite(websiteName):
    if websiteName is None:
        return pd.DataFrame(), 0  
    with open('jobs_offers.json', 'r') as file:
        data = json.load(file)
    
    website_data = data['offerswebsite'].get(websiteName, {})
    
    if not website_data:
        return pd.DataFrame(), 0

    dw = pd.DataFrame(list(website_data.items()), columns=['portal_name', 'quantity'])
    dwSum = dw['quantity'].sum()

    return dw, dwSum


def create_plot_website(dw, dwSum, websiteName):
    if dw.empty:
        return None

    filtered_dw = dw[dw['portal_name'] != 'all']
    
    filtered_dw = filtered_dw.sort_values(by='quantity', ascending=False)

    if filtered_dw.empty:
        return None

    chart_data = filtered_dw[filtered_dw['quantity'] > 0]
    sizes = chart_data['quantity'].tolist()
    labels_with_percents = [
        f"{row['portal_name']} ({(row['quantity'] / dwSum) * 100:.1f}%)"
        for _, row in chart_data.iterrows()
    ]

    legend_labels = [
        f"{row['portal_name']} - {row['quantity']} offers"
        for _, row in filtered_dw.iterrows()
    ]

    plt.figure(figsize=(8, 6))
    plt.title(f"Podział ofert na {websiteName}")
    wedges, texts = plt.pie(sizes, labels=labels_with_percents, startangle=140)
    
    custom_wedges = [plt.Patch(color=plt.cm.viridis(i/len(sizes)), label=label)
                     for i, label in enumerate(legend_labels)]
    
    plt.legend(custom_wedges, legend_labels, loc="center left", bbox_to_anchor=(1, 0.8))
    plt.axis('equal')

    
    adjusted_total = filtered_dw['quantity'].sum()
    plt.text(0.5, -0.1, f"Łączna liczba ofert na {websiteName} to: {adjusted_total}", horizontalalignment='center', fontsize=12, transform=plt.gca().transAxes)

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
        dw, dwSum = get_dataWebsite(websiteName) 
        plotWebiste = create_plot_website(dw, dwSum, websiteName)  
        return render_template('index.html', plotWebiste=plotWebiste, websiteName=websiteName)
    
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)