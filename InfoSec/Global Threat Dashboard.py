import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and clean data
csv_path =   # Change this to your actual CSV path
df = pd.read_csv(csv_path)
df.columns = df.columns.str.strip()

# Strip leading/trailing whitespace in string columns
for col in df.select_dtypes(include='object'):
    df[col] = df[col].str.strip()

# Convert numerical columns
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Financial Loss (in Million $)'] = pd.to_numeric(df['Financial Loss (in Million $)'], errors='coerce')
df['Incident Resolution Time (in Hours)'] = pd.to_numeric(df['Incident Resolution Time (in Hours)'], errors='coerce')
df['Number of Affected Users'] = pd.to_numeric(df['Number of Affected Users'], errors='coerce')

# Drop rows with critical missing data
df.dropna(subset=['Year', 'Financial Loss (in Million $)',
                  'Incident Resolution Time (in Hours)',
                  'Number of Affected Users'], inplace=True)

# Remove negative or invalid entries
df = df[df['Financial Loss (in Million $)'] >= 0]
df = df[df['Incident Resolution Time (in Hours)'] >= 0]
df = df[df['Number of Affected Users'] >= 0]

# Cap outliers (99th percentile)
df['Financial Loss (in Million $)'] = df['Financial Loss (in Million $)'].clip(upper=df['Financial Loss (in Million $)'].quantile(0.99))
df['Incident Resolution Time (in Hours)'] = df['Incident Resolution Time (in Hours)'].clip(upper=df['Incident Resolution Time (in Hours)'].quantile(0.99))
df['Number of Affected Users'] = df['Number of Affected Users'].clip(upper=df['Number of Affected Users'].quantile(0.99))

# === 1. Financial Loss Over Time ===
plt.figure(figsize=(12,6))
sns.lineplot(data=df.groupby('Year')['Financial Loss (in Million $)'].sum().reset_index(),
             x='Year', y='Financial Loss (in Million $)', marker='o')
plt.title('Total Financial Loss Over Time')
plt.ylabel('Financial Loss (Million $)')
plt.grid(True)
plt.tight_layout()
plt.show()

# === 2. Incidents by Country ===
plt.figure(figsize=(14,6))
top_countries = df['Country'].value_counts().head(10).index
tmp = df[df['Country'].isin(top_countries)]
sns.countplot(data=tmp, y='Country', order=top_countries)
plt.title('Top 10 Countries by Number of Cyber Incidents')
plt.xlabel('Incident Count')
plt.tight_layout()
plt.show()

# === 3. Financial Loss by Industry ===
plt.figure(figsize=(12,6))
industry_agg = df.groupby('Target Industry')['Financial Loss (in Million $)'].sum().sort_values(ascending=False).head(10)
sns.barplot(x=industry_agg.values, y=industry_agg.index)
plt.title('Top 10 Industries by Financial Loss')
plt.xlabel('Total Financial Loss (Million $)')
plt.tight_layout()
plt.show()

# === 4. Boxplot: Resolution Time by Defense Mechanism ===
plt.figure(figsize=(14,6))
top_mechanisms = df['Defense Mechanism Used'].value_counts().head(10).index
tmp = df[df['Defense Mechanism Used'].isin(top_mechanisms)]
sns.boxplot(data=tmp, x='Defense Mechanism Used', y='Incident Resolution Time (in Hours)')
plt.xticks(rotation=45)
plt.title('Resolution Time by Defense Mechanism')
plt.tight_layout()
plt.show()

# === 5. Attack Types Distribution ===
plt.figure(figsize=(12,6))
sns.countplot(data=df, y='Attack Type', order=df['Attack Type'].value_counts().index[:10])
plt.title('Top 10 Most Common Attack Types')
plt.tight_layout()
plt.show()
