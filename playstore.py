import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("C:\\Users\\nitin\\AppData\\Roaming\\Microsoft\\Windows\\Network Shortcuts\\playstore_orders.csv")
df.columns = df.columns.str.strip()
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'], errors='coerce')
df['year'] = df['Order Date'].dt.year

sales_2021 = df[df['year'] == 2021].groupby('Stock Keeping Unit Name')['Quantity Ordered'].sum()
sales_2022 = df[df['year'] == 2022].groupby('Stock Keeping Unit Name')['Quantity Ordered'].sum()

sales_diff = pd.DataFrame({
    '2021': sales_2021,
    '2022': sales_2022
}).fillna(0)

sales_diff['difference'] = sales_diff['2022'] - sales_diff['2021']
sales_diff['percent_change'] = ((sales_diff['difference']) / sales_diff['2021'].replace(0, pd.NA)) * 100

top_10_decrease = sales_diff.sort_values('difference').head(10)
top_10_decrease.to_csv("top_10_sales_decrease.csv")

top_10_decrease['difference'].abs().plot(
    kind='bar',
    title='Top 10 Sales Decreases (Absolute)',
    color='red'
)
plt.ylabel('Sales Decrease')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("sales_decrease_chart.png")
plt.show()

top_10_increase = sales_diff.sort_values('difference', ascending=False).head(10)
top_10_increase.to_csv("top_10_sales_increase.csv")

top_10_increase['difference'].abs().plot(
    kind='bar',
    title='Top 10 Sales Increases (Absolute)',
    color='green'
)
plt.ylabel('Sales Increase')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("sales_increase_chart.png")
plt.show()


df['month'] = df['Order Date'].dt.month

monthly_sales = df[df['year'].isin([2021, 2022])].groupby(['year', 'month'])['Quantity Ordered'].sum().unstack(0)

monthly_sales.plot(
    kind='line',
    marker='o',
    title='Monthly Sales Trend: 2021 vs 2022'
)

plt.xlabel('Month')
plt.ylabel('Total Quantity Ordered')
plt.xticks(ticks=range(1, 13), labels=[
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
])
plt.grid(True)
plt.tight_layout()
plt.savefig("monthly_sales_trend.png")
plt.show()
