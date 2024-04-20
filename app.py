from flask import Flask, render_template, request
import pandas as pd
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

def getDataCloud(cloudName):
    if cloudName is None:
        return pd.DataFrame()
    with open('jobs_offers.json', 'r') as file:
        data = json.load(file)
    
    provider_data = data['cloudprovider'].get(cloudName, {})
    
    if not provider_data:
        return pd.DataFrame()

    provider_data.pop('all', None)
    df = pd.DataFrame([provider_data])
    df = df.rename(columns={
        'pracuj': 'quantityPracuj', 
        'justjoin': 'numberJoin', 
        'nfj': 'quantityNFJ', 
        'theprotocol': 'numberProtocol'
    })

    return df

def createPlotCloud(df, cloudName):
    df['quantityAll'] = df[['quantityPracuj', 'numberJoin', 'quantityNFJ', 'numberProtocol']].sum(axis=1)

    data = {
        'Pracuj.pl': df['quantityPracuj'].sum(),
        'JustJoin': df['numberJoin'].sum(),
        'No Fluff Jobs': df['quantityNFJ'].sum(),
        'theProtocol': df['numberProtocol'].sum()
    }

    total = df['quantityAll'].iloc[0]
    
    sorted_data = sorted(data.items(), key=lambda item: item[1], reverse=True)
    labels = [f"{label} ({(size / total) * 100:.1f}%)" for label, size in sorted_data if size > 0]
    sizes = [size for label, size in sorted_data if size > 0]
    legend_labels = [f"{label} - {size} offers" for label, size in sorted_data]

    plt.figure(figsize=(8, 6))
    plt.title(f"Job Offers Distribution for {cloudName}")
    wedges, texts = plt.pie(sizes, labels=labels, startangle=140)
    plt.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(1, 0.8))
    plt.axis('equal')
    plt.text(0.5, -0.1, f"Total offers for {cloudName}: {total}", horizontalalignment='center', fontsize=12, transform=plt.gca().transAxes)
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()

    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()

    return image_base64

def getDataWebsite(jobPlatform):
    if jobPlatform is None:
        return pd.DataFrame()
    with open('jobs_offers.json', 'r') as file:
        data = json.load(file)
    
    platform_data = data['offerswebsite'].get(jobPlatform, {})
    
    if not platform_data:
        return pd.DataFrame()

    total_offers = platform_data.pop('all', None)
    df = pd.DataFrame(list(platform_data.items()), columns=['CloudProvider', 'Offers'])
    return df, total_offers

def createPlotWebsite(df, total_offers, jobPlatform):

    df = df.sort_values(by='Offers', ascending=False)

    plot_data = df[df['Offers'] > 0]

    labels = [f"{row['CloudProvider']} ({row['Offers'] / total_offers * 100:.1f}%)" for index, row in plot_data.iterrows()]
    sizes = plot_data['Offers'].tolist()
    
   
    legend_labels = [f"{row['CloudProvider']} - {row['Offers']} offers" for index, row in df.iterrows()]

    plt.figure(figsize=(8, 6))
    plt.title(f"Job Offers Distribution for {jobPlatform}")
    wedges, texts = plt.pie(sizes, labels=labels, startangle=140)
    plt.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(1, 0.8))
    plt.axis('equal')
    plt.text(0.5, -0.1, f"Total offers for {jobPlatform}: {total_offers}", horizontalalignment='center', fontsize=12, transform=plt.gca().transAxes)
    
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
        df = getDataCloud(cloudName)
        plot = createPlotCloud(df, cloudName)
        return render_template('index.html', plot=plot, cloudName=cloudName)
    elif websiteName:
        dw, dwSum = getDataWebsite(websiteName) 
        plotWebiste = createPlotWebsite(dw, dwSum, websiteName)  
        return render_template('index.html', plotWebiste=plotWebiste, websiteName=websiteName)
    
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)