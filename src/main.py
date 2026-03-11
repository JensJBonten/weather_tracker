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


for i in range (len(df.head())):
    print (f"Rad {i}:")
    print(df.iloc[i])
    print()
