"""
CodeAlpha - Data Science Internship
Task 2: Unemployment Analysis with Python
-------------------------------------------
Clean, explore and visualize India's unemployment rate data, investigate the
impact of Covid-19 on unemployment, and identify key patterns/trends.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.width", 120)

# ---------------------------------------------------------
# 1. Load and clean the data
# ---------------------------------------------------------
df1 = pd.read_csv("Unemployment_in_India.csv")
df2 = pd.read_csv("Unemployment_Rate_upto_11_2020.csv")

# strip whitespace from column names
df1.columns = [c.strip() for c in df1.columns]
df2.columns = [c.strip() for c in df2.columns]

# drop duplicate "Region.1" column in df2 and rows with missing data in df1
df2 = df2.drop(columns=["Region.1"])
df1 = df1.dropna()

# strip whitespace from string/object columns
for d in (df1, df2):
    for col in d.select_dtypes(include="object").columns:
        d[col] = d[col].str.strip()

# parse dates
df1["Date"] = pd.to_datetime(df1["Date"], format="%d-%m-%Y")
df2["Date"] = pd.to_datetime(df2["Date"], format="%d-%m-%Y")

df1["Month"] = df1["Date"].dt.month
df2["Month"] = df2["Date"].dt.month

print("Dataset 1 (Unemployment in India) shape:", df1.shape)
print(df1.head())
print("\nDataset 2 (Unemployment Rate up to 11-2020) shape:", df2.shape)
print(df2.head())

RATE = "Estimated Unemployment Rate (%)"
EMPLOYED = "Estimated Employed"
PARTICIPATION = "Estimated Labour Participation Rate (%)"

# ---------------------------------------------------------
# 2. Overall statistics
# ---------------------------------------------------------
print("\nOverall unemployment rate statistics (Dataset 1):")
print(df1[RATE].describe())

# ---------------------------------------------------------
# 3. Trend over time (national average)
# ---------------------------------------------------------
monthly_avg = df1.groupby("Date")[RATE].mean().reset_index()

plt.figure(figsize=(10, 5))
plt.plot(monthly_avg["Date"], monthly_avg[RATE], marker="o", color="darkred")
plt.axvspan(pd.Timestamp("2020-03-01"), pd.Timestamp("2020-06-01"),
            color="grey", alpha=0.3, label="Covid-19 Lockdown period")
plt.title("Average Estimated Unemployment Rate Over Time (India)")
plt.xlabel("Date")
plt.ylabel("Unemployment Rate (%)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("unemployment_trend_overall.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------
# 4. Covid-19 impact: pre vs during lockdown
# ---------------------------------------------------------
pre_covid = df1[df1["Date"] < "2020-03-01"][RATE].mean()
during_covid = df1[(df1["Date"] >= "2020-03-01") & (df1["Date"] <= "2020-06-01")][RATE].mean()
post_covid = df1[df1["Date"] > "2020-06-01"][RATE].mean()

print("\nAverage unemployment rate:")
print(f"  Before Covid (< Mar 2020): {pre_covid:.2f}%")
print(f"  During lockdown (Mar-Jun 2020): {during_covid:.2f}%")
print(f"  After lockdown (> Jun 2020): {post_covid:.2f}%")

plt.figure(figsize=(6, 4))
plt.bar(["Pre-Covid", "During Lockdown", "Post-Lockdown"],
        [pre_covid, during_covid, post_covid],
        color=["steelblue", "firebrick", "seagreen"])
plt.ylabel("Average Unemployment Rate (%)")
plt.title("Covid-19 Impact on Unemployment Rate")
plt.tight_layout()
plt.savefig("unemployment_covid_impact.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------
# 5. Rural vs Urban comparison
# ---------------------------------------------------------
area_avg = df1.groupby("Area")[RATE].mean()
print("\nAverage unemployment rate by Area:")
print(area_avg)

plt.figure(figsize=(5, 4))
area_avg.plot(kind="bar", color=["orange", "purple"])
plt.ylabel("Average Unemployment Rate (%)")
plt.title("Unemployment Rate: Rural vs Urban")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("unemployment_rural_vs_urban.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------
# 6. Region-wise comparison (top 10 highest average unemployment)
# ---------------------------------------------------------
region_avg = df1.groupby("Region")[RATE].mean().sort_values(ascending=False)
print("\nTop 10 regions by average unemployment rate:")
print(region_avg.head(10))

plt.figure(figsize=(8, 6))
region_avg.head(10).plot(kind="barh", color="teal")
plt.xlabel("Average Unemployment Rate (%)")
plt.title("Top 10 States/Regions by Average Unemployment Rate")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("unemployment_top10_regions.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------
# 7. Monthly seasonal pattern
# ---------------------------------------------------------
monthly_pattern = df1.groupby("Month")[RATE].mean()
plt.figure(figsize=(7, 4))
monthly_pattern.plot(kind="line", marker="o", color="navy")
plt.xlabel("Month")
plt.ylabel("Average Unemployment Rate (%)")
plt.title("Seasonal Pattern of Unemployment Rate (by Month)")
plt.xticks(range(1, 13))
plt.tight_layout()
plt.savefig("unemployment_seasonal_pattern.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------
# 8. Region-wise map data (Dataset 2 has lat/long) - regional bubble chart
# ---------------------------------------------------------
region_geo = df2.groupby(["Region", "longitude", "latitude"])[RATE].mean().reset_index()

plt.figure(figsize=(8, 8))
plt.scatter(region_geo["longitude"], region_geo["latitude"],
            s=region_geo[RATE] * 20, alpha=0.6, c=region_geo[RATE], cmap="Reds")
for _, row in region_geo.iterrows():
    plt.annotate(row["Region"], (row["longitude"], row["latitude"]), fontsize=7)
plt.colorbar(label="Avg Unemployment Rate (%)")
plt.title("Regional Unemployment Rate (Bubble size/color = rate)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.tight_layout()
plt.savefig("unemployment_regional_map.png", dpi=150, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------
# 9. Correlation between employment indicators
# ---------------------------------------------------------
plt.figure(figsize=(5, 4))
sns.heatmap(df1[[RATE, EMPLOYED, PARTICIPATION]].corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Between Employment Indicators")
plt.tight_layout()
plt.savefig("unemployment_correlation.png", dpi=150, bbox_inches="tight")
plt.close()

print("\nAll charts saved successfully.")
