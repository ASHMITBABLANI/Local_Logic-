import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score,classification_report
d=pd.read_csv("C:\\Users\\ashmi\\Downloads\\city_day2_.csv")
x=d[['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3','Benzene', 'Toluene', 'Xylene', 'AQI']]
y=d["Rank"]

scale=StandardScaler()

x=scale.fit_transform(x)

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.30,train_size=0.70,random_state=42)

model=LogisticRegression()

model.fit(x_train, y_train)

y_prd=model.predict(x_test)

print("Accuracy:",accuracy_score(y_test,y_prd))

print(classification_report(y_test, y_prd))

print("Enter air quality values to predict Rank:")
pm25 = float(input("PM2.5: "))
pm10 = float(input("PM10: "))
no = float(input("NO: "))
no2 = float(input("NO2: "))
nox = float(input("NOx: "))
nh3 = float(input("NH3: "))
co = float(input("CO: "))
so2 = float(input("SO2: "))
o3 = float(input("O3: "))
benzene = float(input("Benzene: "))
toluene = float(input("Toluene: "))
xylene = float(input("Xylene: "))
aqi = float(input("AQI: "))
data=pd.DataFrame([[pm25, pm10, no, no2, nox, nh3, co, so2, o3, benzene, toluene, xylene, aqi]],columns=['PM2.5','PM10','NO','NO2','NOx','NH3','CO','SO2','O3','Benzene','Toluene','Xylene','AQI'])
user_data_scaled=scale.transform(data)
user_prd=model.predict(user_data_scaled)
print("Rank:",user_prd[0])