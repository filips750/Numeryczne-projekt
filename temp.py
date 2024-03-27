import pandas as pd

all_data = pd.read_csv("btcusd_d.csv")

x = all_data.iloc[:, [0, 1]]  # Extracting columns 0 and 1

# Save 'x' to CSV file
x.to_csv("x_data.csv", index=False)
