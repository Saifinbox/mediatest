from flask import Flask, render_template, url_for, request, redirect, flash, Response,jsonify
from datetime import datetime
from flask_cors import CORS, cross_origin
from io import StringIO
#import cStringIO as StringIO
from PIL import Image, ImageFont, ImageDraw
import urllib3
import numpy as np
import dlib
import io
import pandas as pd
import json

app = Flask(__name__)
CORS(app)

def cat_uncat():
	xls = pd.ExcelFile('/home/inbox/Desktop/media/Development Data.xlsx')
	# Data = pd.read_csv('/home/inbox/Desktop/media/Development Data.csv')
	Data = pd.read_excel(xls, 'Source data')
	Data = Data.rename(columns={'Sub Category': 'Sub_Category'})
	Data = Data.rename(columns={'Esp/levers': 'Competetors'})
	Data['SOS'] = (Data['COST W GST'] / Data['Total Net Cost'])
	Data['SOV'] = Data['Brand Grps'] / sum(Data['Index Grps PBs 30 Sec'] + Data['Pb Grps'])
	Cat_Data = Data[(Data['Cat / non cat'] == 'Cat') | (Data['Cat / non cat'] == 'CAT')]
	NonCat_Data = Data[(Data['Cat / non cat'] == 'Non Cat') | (Data['Cat / non cat'] == 'NON CAT')]
	Detergents_Cat_lever = Cat_Data[(Cat_Data['Sub_Category'] == 'Detergents') & (Cat_Data['Competetors'] == 'Lever')]
	return Detergents_Cat_lever

def report():
	# xls = pd.ExcelFile('/home/inbox/Desktop/media/Development Data.xlsx')
	# Data = pd.read_csv('/home/inbox/Desktop/media/Development Data.csv')
	# Data = pd.read_excel(xls, 'Source data')
	# column_name=Data.columns.values
	# column_name= json.dumps(column_name)
	xls = pd.ExcelFile('/home/inbox/Desktop/media/Development Data.xlsx')
	# Data = pd.read_csv('/home/inbox/Desktop/media/Development Data.csv')
	Data = pd.read_excel(xls, 'Source data')
	Data = Data.rename(columns={'Sub Category': 'Sub_Category'})
	Data = Data.rename(columns={'Esp/levers': 'Competetors'})

	# Data['SOS'] = (Data[' COST W GST '] / Data[' Total Net Cost ']) * 0.1
	# Data['SOV'] = Data[' Brand Grps '] / sum(Data[' Index Grps PBs 30 Sec '] + Data[' Pb Grps '])

	# Data['SOS'] = (Data['COST W GST'] / Data['Total Net Cost']) * 0.1
	# Data['SOV'] = Data['Brand Grps'] / sum(Data['Index Grps PBs 30 Sec'] + Data['Pb Grps'])

	Data['SOS'] = (Data['COST W GST'] / Data['Total Net Cost'])
	Data['SOV'] = Data['Brand Grps'] / sum(Data['Index Grps PBs 30 Sec'] + Data['Pb Grps'])

	Cat_Data = Data[(Data['Cat / non cat'] == 'Cat') | (Data['Cat / non cat'] == 'CAT')]
	NonCat_Data = Data[(Data['Cat / non cat'] == 'Non Cat') | (Data['Cat / non cat'] == 'NON CAT')]

	Competetors = Data[Data['Competetors'] == 'Comp']
	Unilever = Data[Data['Competetors'] == 'Lever']
	hair = Data[(Data.Sub_Category == 'Hair Care')]
	Detegents = Data[(Data.Sub_Category == 'Detergents')]
	Personal_Wash = Data[(Data.Sub_Category == 'Personal Wash')]
	Ice_Cream = Data[(Data.Sub_Category == 'Ice Cream')]
	Face_Care = Data[(Data.Sub_Category == 'Face Care')]
	Noodles = Data[(Data.Sub_Category == 'Boullion (Noodles)')]
	Tea = Data[(Data.Sub_Category == 'Tea')]
	Cooking_Aids = Data[(Data.Sub_Category == 'Boullion (Cooking Aids)')]
	SCC_Margarine = Data[(Data.Sub_Category == 'SCC-Margarine')]
	Sauces = Data[(Data.Sub_Category == 'Sauces')]
	Water = Data[(Data.Sub_Category == 'Water')]
	# hair.groupby(['BRAND',hair.BRAND.unique()]).sum()
	hair_SOS = hair.groupby(['BRAND', 'SOS']).sum( )
	hair_SOV = hair.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Detegents_SOS = Detegents.groupby(['BRAND', 'SOS']).sum( )
	Detegents_SOV = Detegents.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Personal_Wash_SOS = Personal_Wash.groupby(['BRAND', 'SOS']).sum( )
	Personal_Wash_SOV = Personal_Wash.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Ice_Cream_SOS = Ice_Cream.groupby(['BRAND', 'SOS']).sum( )
	Ice_Cream_SOV = Ice_Cream.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Face_Care_SOS = Face_Care.groupby(['BRAND', 'SOS']).sum( )
	Face_Care_SOV = Face_Care.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Noodles_SOS = Noodles.groupby(['BRAND', 'SOS']).sum( )
	Noodles_SOV = Noodles.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Tea_SOS = Tea.groupby(['BRAND', 'SOS']).sum( )
	Tea_SOV = Tea.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Cooking_Aids_SOS = Cooking_Aids.groupby(['BRAND', 'SOS']).sum( )
	Cooking_Aids_SOV = Cooking_Aids.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	SCC_Margarine_SOS = SCC_Margarine.groupby(['BRAND', 'SOS']).sum( )
	SCC_Margarine_SOV = SCC_Margarine.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Sauces_SOS = Sauces.groupby(['BRAND', 'SOS']).sum( )
	Sauces_SOV = Sauces.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Water_SOS = Water.groupby(['BRAND', 'SOS']).sum( )
	Water_SOV = Water.groupby(['BRAND', 'SOV']).sum( )

	Com_hair = Competetors[(Competetors.Sub_Category == 'Hair Care')]
	Com_Detegents = Competetors[(Competetors.Sub_Category == 'Detergents')]
	Com_Personal_Wash = Competetors[(Competetors.Sub_Category == 'Personal Wash')]
	Com_Ice_Cream = Competetors[(Competetors.Sub_Category == 'Ice Cream')]
	Com_Face_Care = Competetors[(Competetors.Sub_Category == 'Face Care')]
	Com_Noodles = Competetors[(Competetors.Sub_Category == 'Boullion (Noodles)')]
	Com_Tea = Competetors[(Competetors.Sub_Category == 'Tea')]
	Com_Cooking_Aids = Competetors[(Competetors.Sub_Category == 'Boullion (Cooking Aids)')]
	Com_SCC_Margarine = Competetors[(Competetors.Sub_Category == 'SCC-Margarine')]
	Com_Sauces = Competetors[(Competetors.Sub_Category == 'Sauces')]
	Com_Water = Competetors[(Competetors.Sub_Category == 'Water')]

	Com_hair_SOS = Com_hair.groupby(['BRAND', 'SOS']).sum( )
	Com_hair_SOV = Com_hair.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Com_Detegents_SOS = Com_Detegents.groupby(['BRAND', 'SOS']).sum( )
	Com_Detegents_SOV = Com_Detegents.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Com_Personal_Wash_SOS = Com_Personal_Wash.groupby(['BRAND', 'SOS']).sum( )
	Com_Personal_Wash_SOV = Com_Personal_Wash.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Com_Ice_Cream_SOS = Com_Ice_Cream.groupby(['BRAND', 'SOS']).sum( )
	Com_Ice_Cream_SOV = Com_Ice_Cream.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Com_Face_Care_SOS = Com_Face_Care.groupby(['BRAND', 'SOS']).sum( )
	Com_Face_Care_SOV = Com_Face_Care.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Com_Noodles_SOS = Com_Noodles.groupby(['BRAND', 'SOS']).sum( )
	Com_Noodles_SOV = Com_Noodles.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Com_Tea_SOS = Com_Tea.groupby(['BRAND', 'SOS']).sum( )
	Com_Tea_SOV = Com_Tea.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Com_Cooking_Aids_SOS = Com_Cooking_Aids.groupby(['BRAND', 'SOS']).sum( )
	Com_Cooking_Aids_SOV = Com_Cooking_Aids.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Com_SCC_Margarine_SOS = Com_SCC_Margarine.groupby(['BRAND', 'SOS']).sum( )
	Com_SCC_Margarine_SOV = Com_SCC_Margarine.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Com_Sauces_SOS = Com_Sauces.groupby(['BRAND', 'SOS']).sum( )
	Com_Sauces_SOV = Com_Sauces.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Com_Water_SOS = Com_Water.groupby(['BRAND', 'SOS']).sum( )
	Com_Water_SOV = Com_Water.groupby(['BRAND', 'SOV']).sum( )

	Lever_hair = Unilever[(Unilever.Sub_Category == 'Hair Care')]
	Lever_Detegents = Unilever[(Unilever.Sub_Category == 'Detergents')]
	Lever_Personal_Wash = Unilever[(Unilever.Sub_Category == 'Personal Wash')]
	Lever_Ice_Cream = Unilever[(Unilever.Sub_Category == 'Ice Cream')]
	Lever_Face_Care = Unilever[(Unilever.Sub_Category == 'Face Care')]
	Lever_Noodles = Unilever[(Unilever.Sub_Category == 'Boullion (Noodles)')]
	Lever_Tea = Unilever[(Unilever.Sub_Category == 'Tea')]
	Lever_Cooking_Aids = Unilever[(Unilever.Sub_Category == 'Boullion (Cooking Aids)')]
	Lever_SCC_Margarine = Unilever[(Unilever.Sub_Category == 'SCC-Margarine')]
	Lever_Sauces = Unilever[(Unilever.Sub_Category == 'Sauces')]
	Lever_Water = Unilever[(Unilever.Sub_Category == 'Water')]

	Lever_hair_SOS = Lever_hair.groupby(['BRAND', 'SOS']).sum( )
	Lever_hair_SOV = Lever_hair.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Lever_Detegents_SOS = Lever_Detegents.groupby(['BRAND', 'SOS']).sum( )
	Lever_Detegents_SOV = Lever_Detegents.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Lever_Personal_Wash_SOS = Lever_Personal_Wash.groupby(['BRAND', 'SOS']).sum( )
	Lever_Personal_Wash_SOV = Lever_Personal_Wash.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Lever_Ice_Cream_SOS = Lever_Ice_Cream.groupby(['BRAND', 'SOS']).sum( )
	Lever_Ice_Cream_SOV = Lever_Ice_Cream.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Lever_Face_Care_SOS = Lever_Face_Care.groupby(['BRAND', 'SOS']).sum( )
	Lever_Face_Care_SOV = Lever_Face_Care.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Lever_Noodles_SOS = Lever_Noodles.groupby(['BRAND', 'SOS']).sum( )
	Lever_Noodles_SOV = Lever_Noodles.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Lever_Tea_SOS = Lever_Tea.groupby(['BRAND', 'SOS']).sum( )
	Lever_Tea_SOV = Lever_Tea.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Lever_Cooking_Aids_SOS = Lever_Cooking_Aids.groupby(['BRAND', 'SOS']).sum( )
	Lever_Cooking_Aids_SOV = Lever_Cooking_Aids.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Lever_SCC_Margarine_SOS = Lever_SCC_Margarine.groupby(['BRAND', 'SOS']).sum( )
	Lever_SCC_Margarine_SOV = Lever_SCC_Margarine.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Lever_Sauces_SOS = Lever_Sauces.groupby(['BRAND', 'SOS']).sum( )
	Lever_Sauces_SOV = Lever_Sauces.groupby(['BRAND', 'SOV']).sum( )
	# --------------------------------------------------------------
	Lever_Water_SOS = Lever_Water.groupby(['BRAND', 'SOS']).sum( )
	Lever_Water_SOV = Lever_Water.groupby(['BRAND', 'SOV']).sum( )


	column_name=Data.columns.values
	return 	Lever_hair_SOS['SOV']

def sub_categories():
	Data = pd.read_csv('/home/inbox/Desktop/media/Development Data.csv')
	Data = Data.rename(columns={'Sub Category': 'Sub_Category'})
	return Data['Sub_Category'].unique()


@app.route("/")
def landingpage():
    return render_template("elements_cards.html")

@app.route("/charts")
def emcharts():
    return render_template("charts.html")


@app.route("/emcharts")
def emmcharts():
    return render_template("emcharts.html")



@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    return render_template("dashboard.html")

@app.route('/elements_cards', methods=['GET','POST'])
def elements_cards():
    return render_template('elements_cards.html')

# @app.route('/charts_index', methods=['GET','POST'])
# def charts_index():
#     return render_template('index1.html')

@app.route('/index1', methods=['GET','POST'])
def index1():
    return render_template('index1.html')

@app.route('/pie1.html', methods=['GET','POST'])
def pie():
    return render_template('pie1.html')

@app.route('/pie2.html', methods=['GET','POST'])
def pie1():
    return render_template('pie2.html')

@app.route('/pie3.html', methods=['GET','POST'])
def pie2():
    return render_template('pie3.html')

@app.route('/pie4.html', methods=['GET','POST'])
def pie3():
    return render_template('pie4.html')

@app.route('/serial2.html', methods=['GET','POST'])
def serial2():
    return render_template('serial2.html')

@app.route('/serial1.html', methods=['GET','POST'])
def serial1():
    return render_template('serial1.html')

@app.route('/serial3.html', methods=['GET','POST'])
def serial3():
    return render_template('serial3.html')

@app.route('/xy.html', methods=['GET','POST'])
def xy():
    return render_template('xy.html')

@app.route('/radar.html', methods=['GET','POST'])
def radar():
    return render_template('radar.html')


@app.route('/funnel.html', methods=['GET','POST'])
def funnel():
    return render_template('funnel.html')

@app.route('/stock.html', methods=['GET','POST'])
def stock():
    return render_template('stock.html')


@app.route('/exports.css', methods=['GET','POST'])
def exports():
    return render_template('exports.css')


@app.route('/export.js', methods=['GET','POST'])
def js():
    return render_template('exports.js')


# @app.route('/stock.html', methods=['GET','POST'])
# def stock():
#     return render_template('stock.html')
''
#======================================================================
#report processing
# def report():
# 	# xls = pd.ExcelFile('/home/inbox/Desktop/media/Development Data.xlsx')
# 	Data = pd.read_csv('/home/inbox/Desktop/media/Development Data.csv')
# 	# Data = pd.read_excel(xls, 'Source data')
# 	column_name=Data.columns.values
# 	return column_name

#======================================================================

#======================================================================
#Dlib
@app.route('/index', methods=['GET','POST'])
def index():
    return render_template('index.html')

def gen(anom_type):
	if anom_type=="mobilephones":
		detector=dlib.simple_object_detector("detector.svm")
	elif anom_type=="ciggarette":
		detector=dlib.simple_object_detector("cigg_detector.svm")
	elif anom_type=="id":
		detector=dlib.simple_object_detector("ID_detector.svm")
	
	try:
		host = "10.15.2.7:8080/video"
		hoststr = 'http://' + host

		stream=urllib2.urlopen(hoststr)

		bytes=''

		while True:
			bytes+=stream.read(1024)
			a = bytes.find('\xff\xd8')
			b = bytes.find('\xff\xd9')
			if a!=-1 and b!=-1:
				jpg = bytes[a:b+2]
				bytes= bytes[b+2:]
				streamline = StringIO.StringIO(jpg)
				img = Image.open(streamline)
				


				#basewidth = 300
				#wpercent = (basewidth/float(img.size[0]))
				#hsize = int((float(img.size[1])*float(wpercent)))
				#img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)

				frame=np.array(img)		
				
				color = np.array([0, 255, 0], dtype=np.uint8)
				dets = detector(frame)
				for k, d in enumerate(dets):
					print("Mobile Detected")
					boundingbox=(d.left(), d.top()), (d.right(), d.bottom())
					im = Image.fromarray(frame)
					dr = ImageDraw.Draw(im)
					dr.rectangle(((d.left(),d.top()),(d.right(),d.bottom())), outline = "blue")
					frame=np.array(im)
				convjpg = Image.fromarray(frame)
				imgByteArr=io.BytesIO()
				convjpg.save(imgByteArr,format="jpeg")
				imgByteArr=imgByteArr.getvalue()				
				#print("-------------")
				#print(convjpg)
				#print(frame)
				yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + imgByteArr + b'\r\n')
	except Exception as e:
		pass

@app.route('/raspberry/<input_str>')
def raspberry(input_str):
	return Response(gen(input_str),
		mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/component', methods=['GET','POST'])
def component():
	# print(report())
	# a={1:'test',2:'testing'}
	# print(jsonify(a))
	return render_template('component.html')
	# return render_template('component.html',data=report().to_html(),categories=sub_categories())

@app.route('/component1', methods=['GET','POST'])
def component1():
	# print(cat_uncat())
	# a={1:'test',2:'testing'}
	# print(jsonify(a))
	return render_template('component1.html')



#========================================================================
#gis
@app.route('/gis', methods=['GET','POST'])
def gis():
    return render_template('gis.html')

@app.route('/mapWindow', methods=['GET','POST'])
def mapWindow():
    return render_template('mapWindow.html')
#========================================================================	
#@app.route('/singlepage', methods=['GET','POST'])
#def singlepage():
#    return render_template('singlepage.html')
#========================================================================
#Main Starts Here
if __name__ == "__main__":
    app.run(debug=True)
