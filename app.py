from flask import Flask, render_template
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import sys
app = Flask(__name__)


if len(sys.argv) > 1:
    cloudName = sys.argv[1]
else:
    cloudName = "*" 

def get_data():
    conn = sqlite3.connect('jobs_offers.db')
    

    query = f"SELECT quantityPracuj, numberJoin, quantityNFJ, numberProtocol, quantityAll FROM {cloudName}"
    df = pd.read_sql_query(query, conn)
    
    conn.close()
    return df


def create_plot(df):
    df['Total'] = df['quantityPracuj'] + df['numberJoin'] + df['quantityNFJ'] + df['numberProtocol']
    plt.figure()
    plt.title(f"Podział ofert dla {cloudName}")
    labels = ['Pracuj.pl', 'JustJoin', 'No Fluff Jobs', 'theProtocol']
    sizes = [df['quantityPracuj'].sum(), df['numberJoin'].sum(), df['quantityNFJ'].sum(), df['numberProtocol'].sum()]
    sum = int(df['quantityAll'])
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.text(0.5, -0.25, f"Suma ofert dla {cloudName} wynosi: {sum}", horizontalalignment='center', fontsize=12, transform=plt.gca().transAxes)
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    
    return image_base64



@app.route('/')
def index():
    df = get_data()
    plot = create_plot(df)
    return render_template('index.html', plot=plot)

if __name__ == '__main__':
    app.run(debug=True)