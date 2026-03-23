import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("data\Dagens lengde (2).xlsx")


print(f"antall kolonner: {len(df.columns)}")
print(f"antall rader: {len(df)}")
print()

print("Kolonner: ")
for kolonne in df.columns:
    print(f"- {kolonne}")
    
print("\nFørste 5 rader: ")
print(df.head())
 

for i in range(5):
    print (f"Rad {i}:")
    print(df.iloc[i])
    print()
    
    
df.columns = ["Date", "day_length", "sunrise", "sunset", "daily_increase", "total_increase"]
df["date"] = pd.to_datetime(df["Date"], format="%d.%m.%y")
df["day_length"] = pd.to_timedelta(df("day_length"))
df["daily_increase"] = pd.to_timedelta(df("daily_increase"))
df["total_increase"] = pd.to_timedelta(df("total_increase"))
df["sunrise"] = pd.to_datetime(df["sunrise"], format="%H:%M:%S")
df["sunset"] = pd.to_datetime(df["sunset"], format="%H:%M:%S")