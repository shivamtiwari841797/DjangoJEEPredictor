import scipy.stats as stats
import math
from django.shortcuts import render
from django.http import HttpResponse
from .train import train_model, Data
from IPython.display import HTML
import matplotlib.pyplot as plt, mpld3
import matplotlib
import pandas as pd
import numpy as np
import os
import statistics  as st
import scipy.stats
import json


# Create your views here.
def home(request):
	return render(request,'index1.html')

def result(request):
	rank = request.POST['rank']
	caste = request.POST['caste']
	if rank == '' :
		return HttpResponse("Fill the rank field")
	if caste == 'select' :
		return HttpResponse("choose the correct caste")
	if(int(rank)<1):
		return HttpResponse("Incorrect Rank Entered")
	df=train_model.getmodel()
	l=[caste]
	#df=df.sort_values(['Category','Closing_Rank'])
	df=df[df['Category'].isin(l)]
	#df=df[(df['Closing_Rank']>=int(rank)) & (df['Opening_Rank']<=int(rank))]
	df=df[df['Opening_Rank']>=int(rank)]
	#df=df[['College','Stream']]
	#df.set_index('College', inplace=True)
	df=df.sort_values('Stream')
	df.reset_index(drop=True, inplace=True)
	if(df.shape[0]==0):
		return HttpResponse("Sorry.. You can get no college with this category rank")
	#return HttpResponse('<style>.dataframe{position:absolute;top:40px;left:20%;}table {font-family: arial, sans-serif;border-collapse: collapse;width: 50%;}td{onclick:'templates/plot.html';border: 1px solid #dddddd;text-align: left;padding: 8px;}th{border: 1px solid #dddddd;text-align: left;padding: 8px;}tr:nth-child(even) {background-color: #dddddd;}</style>You can get :\n\n\n'+df.to_html())
	
	dat=Data()
	dataList=dat.getdata()
	df16=dataList[0]
	df17=dataList[1]
	df18=dataList[2]

	colleges=df16.College.unique()
	Streams=df16.Stream.unique()
	Categories=df16.Category.unique()
	ylist=[df16,df17,df18]

	for col in colleges:
		for stream in Streams:
			for cat in Categories:
				l=[col,stream,cat]
				rankList=[]
				for yearData in ylist:
					row=yearData[yearData['College'].isin(l)]
					row=row[row['Stream'].isin(l)]
					row=row[row['Category'].isin(l)]
					try:
						rankList.append(row.iloc[0].Opening_Rank)
						rankList.append(row.iloc[0].Closing_Rank)
					except:
						pass
				if(len(rankList)>0):
					mu = st.mean(rankList)
					sigma = st.stdev(rankList)
					var = float(sigma)**2
					denom = (2*math.pi*var)**.5
					num = math.exp(-(float(rank)-float(mu))**2/(2*var))
					p=num/denom
					p=p*100
					p=round(p,3)


					#p=NormalDist(mu, sigma).pdf(rank)
					#p=scipy.stats.norm(mu, sigma).pdf(rank)
					try:
						ind=df[(df['College'] == col ) & (df['Category'] == cat) & (df['Stream'] == stream)].head().index
						ind=ind[0]
						df.loc[ind,'Probability']=p
					except:
						pass

	df=df[['College','Stream','Probability']]
	df=df.sort_values(['Probability'],ascending=False)
	df=df[:10]
	return render(request,'table.html',{'df':df.values.tolist(),'cat':caste})
	#return HttpResponse(df.to_html())

def plot(request):

	if request.method == 'POST' and request.is_ajax():
	    #name = request.POST.get('name')
	    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	    clg=request.POST.get('clg')
	    stream=request.POST.get('stream')
	    cat=request.POST.get('cat')
	    dat=Data()
	    dataList=dat.getdata()
	    df16=dataList[0]
	    df17=dataList[1]
	    df18=dataList[2]
	    l=[clg,stream,cat]
	    ylist=[df16,df17,df18]
	    orankList=[]
	    crankList=[]

	    for yearData in ylist:
	    	row=yearData[yearData['College'].isin(l)]
	    	row=row[row['Stream'].isin(l)]
	    	row=row[row['Category'].isin(l)]
	    	orankList.append(row.iloc[0].Opening_Rank)
	    	crankList.append(row.iloc[0].Closing_Rank)

	    y_pos=['2016','2017','2018']

	    matplotlib.use("Agg")

	    ops = pd.Series(orankList)
	    plt.rcParams["figure.figsize"] = (5,3)
	    plt.bar(y_pos,orankList)
	    plt.xlabel('Year')
	    plt.ylabel('Rank')
	    figo, axo = plt.subplots()
	    ops.plot.bar()
	    ob = mpld3.fig_to_html(figo)
	    plt.savefig(BASE_DIR+r'/static/plots/ob_'+clg+'_'+stream+'_'+cat+'.png')
	    

	    cs = pd.Series(crankList)
	    plt.rcParams["figure.figsize"] = (5,3)
	    plt.bar(y_pos,crankList)
	    plt.xlabel('Year')
	    plt.ylabel('Rank')
	    figc, axc = plt.subplots()
	    cs.plot.bar()
	    cb = mpld3.fig_to_html(figc)
	    plt.savefig(BASE_DIR+r'/static/plots/cb_'+clg+'_'+stream+'_'+cat+'.png')
	    

	    mu = st.mean(orankList)
	    plt.rcParams["figure.figsize"] = (5,3)
	    sigma = st.stdev(orankList)
	    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
	    fig1, ax1 = plt.subplots()
	    ax1.plot(x, stats.norm.pdf(x, mu, sigma))
	    on= mpld3.fig_to_html(fig1)
	    plt.savefig(BASE_DIR+r'/static/plots/on_'+clg+'_'+stream+'_'+cat+'.png')
	    

	    cmu = st.mean(crankList)
	    plt.rcParams["figure.figsize"] = (5,3)
	    csigma = st.stdev(crankList)
	    cx = np.linspace(cmu - 3*csigma, cmu + 3*csigma, 100)
	    fig2, ax2 = plt.subplots()
	    ax2.plot(cx, stats.norm.pdf(cx, cmu, csigma))
	    cn= mpld3.fig_to_html(fig2)
	    plt.savefig(BASE_DIR+r'/static/plots/cn_'+clg+'_'+stream+'_'+cat+'.png')
	    
	    #return HttpResponse(json.dumps({'clg':clg,'stream':stream,'cat':cat,'ob':ob,'cb':cb,'on':on,'cn':cn,'mu':mu,'sigma':sigma}), content_type="application/json")
	    return render(request,'Plotalt.html',{'clg':clg,'stream':stream,'cat':cat,'ob':ob,'cb':cb,'on':on,'cn':cn,'mu':mu,'sigma':sigma})
	else :
		return render_to_response('table.html', locals())

	#return render_to_response('table.html',{'clg':clg,'stream':stream,'cat':cat,'ob':ob,'cb':cb,'on':on,'cn':cn,'mu':mu,'sigma':sigma})
	#return render(request,'.html',{'clg':clg,'stream':stream,'cat':cat,'ob':ob,'cb':cb,'on':on,'cn':cn,'mu':mu,'sigma':sigma})

def plotalt(request):

		clg=request.GET['clg']
		stream=request.GET['stream']
		cat=request.GET['cat']
		dat=Data()
		dataList=dat.getdata()
		df16=dataList[0]
		df17=dataList[1]
		df18=dataList[2]
		l=[clg,stream,cat]
		ylist=[df16,df17,df18]
		orankList=[]
		crankList=[]

		for yearData in ylist:
			row=yearData[yearData['College'].isin(l)]
			row=row[row['Stream'].isin(l)]
			row=row[row['Category'].isin(l)]
			orankList.append(row.iloc[0].Opening_Rank)
			crankList.append(row.iloc[0].Closing_Rank)

		plt.rcParams["figure.figsize"] = (5,3)
		y_pos=['2016','2017','2018']
		ops = pd.Series(orankList)
		plt.bar(y_pos,orankList)
		plt.xlabel('Year')
		plt.ylabel('Rank')
		figo, axo = plt.subplots()
		ops.plot.bar()
		ob = mpld3.fig_to_html(figo)
		

		cs = pd.Series(crankList)
		plt.bar(y_pos,crankList)
		plt.xlabel('Year')
		plt.ylabel('Rank')
		figc, axc = plt.subplots()
		cs.plot.bar()
		cb = mpld3.fig_to_html(figc)
		

		mu = st.mean(orankList)
		sigma = st.stdev(orankList)
		x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
		fig1, ax1 = plt.subplots()
		ax1.plot(x, stats.norm.pdf(x, mu, sigma))
		on= mpld3.fig_to_html(fig1)
		

		cmu = st.mean(crankList)
		csigma = st.stdev(crankList)
		cx = np.linspace(cmu - 3*csigma, cmu + 3*csigma, 100)
		fig2, ax2 = plt.subplots()
		ax2.plot(cx, stats.norm.pdf(cx, cmu, csigma))
		cn= mpld3.fig_to_html(fig2)
		
		#return HttpResponse(json.dumps({'clg':clg,'stream':stream,'cat':cat,'ob':ob,'cb':cb,'on':on,'cn':cn,'mu':mu,'sigma':sigma}), content_type="application/json")
		return render(request,'Plot.html',{'clg':clg,'stream':stream,'cat':cat,'ob':ob,'cb':cb,'on':on,'cn':cn,'mu':mu,'sigma':sigma})