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

    filtered_dw = filtered_dw.sort_values(by='quantity', ascending=False)
    sizes = filtered_dw['quantity'].tolist()
    total = sum(sizes)

    labels_with_percents = [f"{row['portal_name']} ({(row['quantity'] / total) * 100:.1f}%)" for _, row in filtered_dw.iterrows()]
    legend_labels = [f"{row['portal_name']} - {row['quantity']} offers" for _, row in filtered_dw.iterrows()]

    plt.figure(figsize=(8, 6))
    plt.title(f"Podział ofert dla {websiteName}")
    wedges, texts = plt.pie(sizes, labels=labels_with_percents, startangle=140)[0:2]
    plt.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(1, 0.8))
    plt.axis('equal')
    plt.text(0.5, -0.1, f"Total offers for {websiteName} is: {dwSum}", horizontalalignment='center', fontsize=12, transform=plt.gca().transAxes)

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