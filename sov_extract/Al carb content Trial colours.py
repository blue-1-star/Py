import pandas as pd
from scipy.stats import shapiro, levene, kruskal
import scikit_posthocs as sp
import matplotlib.pyplot as plt
import seaborn as sns

# Load and prepare data
# file_path = r'C:\Users\sofii\OneDrive\Рабочий стол\try\Carb Al mg per g.xlsx'
file_path = r"G:\My\sov\extract\Carb Al mg per g.xlsx"

data_cleaned = pd.read_excel(file_path).rename(columns={
    'Extraction method': 'Method',
    'mg of carbohydrates in 1 g of extract': 'Rep1',
    'Unnamed: 2': 'Rep2',
    'Unnamed: 3': 'Rep3',
    'Average mg of carbohydrates in 1 g of extract': 'Average'
})

# Convert and clean data
numeric_cols = ['Rep1', 'Rep2', 'Rep3', 'Average']
data_cleaned[numeric_cols] = data_cleaned[numeric_cols].apply(pd.to_numeric, errors='coerce')
data_cleaned = data_cleaned.dropna().sort_values('Method')
data_cleaned['Method'] = data_cleaned['Method'].astype(int)

# Prepare melted data for statistical tests
data_melted = data_cleaned.melt(
    id_vars=['Method'], 
    value_vars=['Rep1', 'Rep2', 'Rep3'], 
    var_name='Replicate', 
    value_name='Value'
)

# Statistical tests (using original replicates)
shapiro_test = shapiro(data_melted['Value'])
print(f"Shapiro-Wilk: p = {shapiro_test.pvalue:.4f}")

method_groups = [data_melted[data_melted['Method'] == m]['Value'] 
                 for m in sorted(data_melted['Method'].unique())]
                 
levene_test = levene(*method_groups)
kruskal_test = kruskal(*method_groups)

print(f"\nLevene's: p = {levene_test.pvalue:.4f}")
print(f"Kruskal-Wallis: p = {kruskal_test.pvalue:.4f}")

# Visualization setup
plt.figure(figsize=(10, 6))
ax = plt.gca()
custom_palette = sns.color_palette("Set2")  # Более мягкие цвета
# custom_palette = sns.color_palette("pastel")  # Пастельные оттенки
# custom_palette = sns.color_palette("tab10")  # 10 базовых цветов

# Create boxplot first
bp = sns.boxplot(
    x='Method', 
    y='Value', 
    data=data_melted, 
    palette=custom_palette,
    width=0.7,
    showfliers=False,
    ax=ax,
    order=sorted(data_melted['Method'].unique())  # Ensure specific order
)

# Customize boxes and medians using actual boxplot elements
for i, box in enumerate(bp.artists):
    method = int(bp.get_xticklabels()[i].get_text())
    edge_color = '#0744C9' if method % 2 == 1 else '#FB670B'
    
    # Box edges
    box.set_edgecolor(edge_color)
    box.set_linewidth(2)
    
    # Median lines
    median_line = bp.lines[i*5 + 4]
    median_line.set_color(edge_color)
    median_line.set_linewidth(2)

# Add average points
for i, method in enumerate(sorted(data_cleaned['Method'].unique())):
    edge_color = '#0744C9' if method % 2 == 1 else '#FB670B'
    method_data = data_cleaned[data_cleaned['Method'] == method]
    
    ax.scatter(
        x=i,  # Position based on boxplot order
        y=method_data['Average'].values[i],
        color=edge_color,
        edgecolor='black',
        s=100,
        zorder=10
    )

# Final formatting
plt.xlabel("Extraction Method", fontsize=12, labelpad=10)
plt.ylabel("Carbohydrate Content (mg/g extract)", fontsize=12, labelpad=10)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
sns.despine()

plt.tight_layout()
plt.savefig(r"G:\My\sov\extract\Carb Al mg per g.svg")
plt.show()