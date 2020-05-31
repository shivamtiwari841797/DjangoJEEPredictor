import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

df16=pd.read_csv(BASE_DIR+'/dataset/2016.csv').sort_values(['College','Stream'])
df17=pd.read_csv(BASE_DIR+'/dataset/2017.csv').sort_values(['College','Stream'])
df18=pd.read_csv(BASE_DIR+'/dataset/2018.csv').sort_values(['College','Stream'])
dflist=[df16,df17,df18]

colleges=df16.College.unique()
#print(colleges)

Streams=df16.Stream.unique()
#print(Streams)

Categories=df16.Category.unique()
#print(Categories)

res=[]
for clg in colleges:
    for stream in Streams:
        for cat in Categories:
            l=[clg,stream,cat]
            sumc=0
            sumo=0
            for df in dflist:
                row=df[df['College'].isin(l)]
                row=row[row['Stream'].isin(l)]
                row=row[row['Category'].isin(l)]
                try:
                    sumo+=row.iloc[0].Opening_Rank
                    sumc+=row.iloc[0].Closing_Rank
                except:
                    pass
            avgo=sumo//3
            avgc=sumc//3
            if(avgo!=0 and avgc!=0):
                l.append(avgo)
                l.append(avgc)
                res.append(l)

result=pd.DataFrame(res)
result.columns=['College','Stream','Category','Opening_Rank','Closing_Rank']
result.to_csv(BASE_DIR+r'/ResultSet/result.csv')
#print(result)

class train_model:
    df=[]
    def __init__(self):
        df=result
    def getmodel():
        try:
            df.insert(3,'Probability',[0 for i in range(df.shape[0])])
        except:
            pass
        return df
        
class Data:
    def __init__(self):
        self.df=[df16,df17,df18]
    def getdata(self):
        return self.df

