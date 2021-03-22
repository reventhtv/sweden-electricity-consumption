import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

fields = ['Period', 'Avräknad (kWh)']
df_nuclear = pd.read_excel("RawData/nuclearPowerProduktionsStatistik.xlsx", usecols=fields)
df_nuclear.rename(columns={"Avräknad (kWh)":"nuclearPower"}, inplace=True)
#print(df_nuclear.head(5))

df_solar = pd.read_excel("RawData/solarPowerProduktionsStatistik.xlsx", usecols=fields)
df_solar.rename(columns={"Avräknad (kWh)":"solarPower"}, inplace=True)
#print(df_solar.head(5))

df_hydro = pd.read_excel("RawData/HydroPowerProduktionsStatistik.xlsx", usecols=fields)
df_hydro.rename(columns={"Avräknad (kWh)":"hydroPower"}, inplace=True)
#print(df_hydro.head(5))

df_wind = pd.read_excel("RawData/windPowerProduktionsStatistik.xlsx", usecols=fields)
df_wind.rename(columns={"Avräknad (kWh)":"windPower"}, inplace=True)
#print(df_wind.head(5))

df = df_nuclear.merge(df_solar, on=['Period'], how='left')


df1 = df.merge(df_hydro, on=['Period'], how='left')


df2 = df1.merge(df_wind, on=['Period'], how='left')
#print(df2.head(10))
#print(df2.columns)

#print(df2.iloc[:, 1:5])
df2['TotalPower'] = df2.iloc[:, 1:5].sum(axis=1)

#Convert kWh to mWh
df_mHw = df2.iloc[:, 1:6] / 1000
#df_mHw['Period'] = df2['Period']

df_mHw.insert(0,"Period",df2.Period, True)
df_mHw.nuclearPower = np.round(df_mHw.nuclearPower)
df_mHw.windPower = np.round(df_mHw.windPower)
df_mHw.TotalPower = np.round(df_mHw.TotalPower)
df_mHw.hydroPower = np.round(df_mHw.hydroPower)

print(df_mHw)
df_mHw.to_csv("data/sweden-electricity-production.csv", index=False)
##Check missing values
#print(df2.isnull().sum()) # There are no missing values to clean or impute

'''
Electricity Consumption Data for sweden 
'''
df_2015 = pd.read_csv("RawData/consumption-se-areas_2015_hourly.csv")
#print(df_2015.head(24))

df_2016 = pd.read_csv("RawData/consumption-se-areas_2016_hourly.csv")
#print(df_2016.head(24))

df_2017 = pd.read_csv("RawData/consumption-se-areas_2017_hourly.csv")
#print(df_2017.head(24))

df_2018 = pd.read_csv("RawData/consumption-se-areas_2018_hourly.csv")
#print(df_2018.head(24))

df_2019 = pd.read_csv("RawData/consumption-se-areas_2019_hourly.csv")
#print(df_2019.head(24))

df_2020 = pd.read_csv("RawData/consumption-se-areas_2020_hourly.csv")
#print(df_2020.head(24))

df_2021 = pd.read_csv("RawData/consumption-se-areas_2021_hourly.csv")

df_all = [df_2015, df_2016, df_2017, df_2018, df_2019, df_2020, df_2021]

df_master = pd.concat(df_all)
df_master.rename(columns={"Unnamed: 0":"Date"}, inplace=True)

df_master['TotalPowerProduction'] = df_mHw['TotalPower']
print(df_master)
print(df_master.info())
df_master.to_csv("data/sweden-electricity-consumption.csv", index=False)

'''
df_main = df_mHw.join(df_master)
print(df_main)
df_main.to_csv("data/sweden-electricity-data.csv")
'''

#print(df_master['Date'][0:8800])
df_elec = pd.read_csv("data/sweden-electricity-consumption.csv", parse_dates=['Date'], index_col=['Date'])
print(df_elec.info())
print(df_elec.index.values)

'''
sns.lineplot(x=df_elec[0:17600].index.values, y=df_elec['SE'][0:17600], label='Consumption')
sns.lineplot(x=df_elec[0:17600].index.values, y=df_elec['TotalPowerProduction'][0:17600], label='Production')
#sns.lineplot(x=df_mHw['Period'][0:17600], y=df_mHw['TotalPower'][0:17600], label='Production', color='rebeccapurple',linestyle='dashed', alpha=0.8)
plt.xlabel('Date')
plt.ylabel('Electricity (MWh)')
#plt.show()
'''

# url containing the dataset
url = 'https://bolin.su.se/data/stockholm/files/stockholm-historical-weather-observations-2017/' \
      'temperature/daily/stockholm_daily_mean_temperature_1756_2017.txt'

column_names = ['Year','Month','Day','Temperature_Raw','Temperature_Processed_1',
                'Temperature_Processed_2','Data_ID']
# Reading the Data
temperatures_raw = pd.read_csv(url,sep ='\s+',names = column_names)

temperatures_raw.to_csv("data/stockholm-daily-weather-data.csv", index=False)
print(temperatures_raw.columns)

temperatures_hourly = pd.read_csv("data/smhi-stockholm-hourly.csv")

text = open("data/smhi-stockholm-hourly.csv", "r")
text = ''.join([i for i in text]).replace(";", ",")
x = open("data/smhi-stockholm-hourly.csv","w")
x.writelines(text)
x.close()
#print(x)
#print(temperatures_hourly["Datum"])
year_after_2015 = temperatures_hourly[temperatures_hourly["Datum"] > "2014-12-31"]
#print(year_after_2015)

df_elec_specific = df_elec[(df_elec["Hours"] == "06 - 07") | (df_elec["Hours"] == "18 - 19")]
#print(df_elec_specific)

temperatures_hourly_2021 = pd.read_csv("data/smhi-stockholm-hourly-2021.csv")
text = open("data/smhi-stockholm-hourly-2021.csv", "r")
text = ''.join([i for i in text]).replace(";", ",")
x = open("data/smhi-stockholm-hourly-2021.csv","w")
x.writelines(text)
x.close()
#print(temperatures_hourly_2021.loc[39:])

df_stockholm_2021 = temperatures_hourly_2021.loc[39:]

df_weather_all = [year_after_2015, df_stockholm_2021]

df_weather_2015_2021 = pd.concat(df_weather_all, ignore_index=True)

df_weather_2015_2021.pop("Kvalitet")
df_weather_2015_2021 = df_weather_2015_2021[(df_weather_2015_2021["Tid (UTC)"] == "06:00:00") | (df_weather_2015_2021["Tid (UTC)"] == "18:00:00")]

#df_weather_2015_2021.to_csv("data/stockholm-weather-2015-2021.csv", index=False)

df_weather_2015_2021["Datum"] = pd.to_datetime(df_weather_2015_2021.Datum)
df_weather_2015_2021.rename(columns={"Datum":"Date"}, inplace=True)
df_weather_2015_2021 = df_weather_2015_2021.reset_index()
df_weather_2015_2021.drop("index",axis=1, inplace=True)
df_weather_2015_2021.to_csv("data/stockholm-weather-2015-2021.csv", index=False)

print(df_weather_2015_2021)

df_elec_master = df_elec_specific.reset_index()
#df_elec_master["Date"] = pd.to_datetime(df_elec_master["Date"].dt.strftime("%y-%m-%d"))
df_elec_master["Date"] = df_weather_2015_2021.Date
print(df_elec_master)


#df_elec_result = df_weather_2015_2021.merge(df_elec_master, on=['Hours'], how="left")
#print(df_elec_result)


#df_weather_2015_2021.pop("Tid (UTC)")
df_elec_result = pd.concat([df_elec_master,df_weather_2015_2021], axis=1)
print(df_elec_result)

df_elec_result.to_csv("data/result.csv", index=False)

df_final = pd.read_csv("data/result.csv", parse_dates=['Date'], index_col=['Date'])

sns.scatterplot(x='Lufttemperatur',y='SE3',data=df_final,palette="mako", alpha = 0.5)
plt.title('Temperature vs Demand')
plt.savefig('plots/stockholm_electricity_tempVsconsumption.png')
plt.show()

