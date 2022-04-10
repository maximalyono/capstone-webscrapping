from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('tbody')
extract = table.find_all('a')

row_length = len(extract)

temp = [] #initiating a list 

for i in range(0, row_length, 2):
#insert the scrapping process here
    harga = extract[i].text.replace(',','')
    tanggal = extract[i+1].text.removeprefix("USD IDR rate for ")
    temp.append((harga, tanggal)) 

temp = temp[::-1]

#change into dataframe
data = pd.DataFrame(temp, columns = ('harga harian','tanggal'))

#insert data wrangling here
data['tanggal'] = data['tanggal'].astype('datetime64')
data['harga harian'] = data['harga harian'].astype('float64')
tabel_final = data.set_index('tanggal')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = round(tabel_final['harga harian'].mean(), 4) #be careful with the " and ' 

	# generate plot
	ax = tabel_final.plot(figsize = (9,4)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)
