import pandas as pd
from scipy.stats import shapiro, levene, kruskal
import scikit_posthocs as sp
import matplotlib.pyplot as plt
import seaborn as sns
import os


# Step 1: Load the Excel File
# file_path = r'C:\Users\sofii\OneDrive\Рабочий стол\try\Total FL in extract NEW.xlsx'  # Update if file is in another directory
file_path = r"G:\Programming\Py\sov_extract\Data\Total FL in extract NEW.xlsx"
work_dir = os.path.join(os.path.dirname(__file__), 'Data')
# work_dir = r"G:\My\sov\extract\Data"
data = pd.read_excel(file_path)

# Step 2: Rename Columns for Clarity
data_cleaned = data.rename(columns={
    'Extraction method': 'Method',
    'mg of carbohydrates in total extract': 'Rep1',
    'Unnamed: 2': 'Rep2',
    'Unnamed: 3': 'Rep3',
    'Average mg of carbohydrates in total extract': 'Average'
})

# Step 3: Convert Relevant Columns to Numeric
data_cleaned[['Rep1', 'Rep2', 'Rep3', 'Average']] = data_cleaned[[
    'Rep1', 'Rep2', 'Rep3', 'Average'
]].apply(pd.to_numeric, errors='coerce')

# Drop rows with missing values
data_cleaned = data_cleaned.dropna()

# Step 4: Perform Shapiro-Wilk Test (Normality Test) on Averages
shapiro_test = shapiro(data_cleaned['Average'])
print(f"Shapiro-Wilk Test: p-value = {shapiro_test.pvalue}")
if shapiro_test.pvalue > 0.05:
    print("The data is normally distributed.")
else:
    print("The data is not normally distributed.")

# Step 5: Prepare Data for Levene's Test and Kruskal-Wallis Test
method_groups = [
    data_cleaned[data_cleaned['Method'] == method][['Rep1', 'Rep2', 'Rep3']].values.flatten()
    for method in data_cleaned['Method'].unique()
]

# Perform Levene's Test for Homogeneity of Variance
levene_test = levene(*method_groups)
print(f"Levene's Test: p-value = {levene_test.pvalue}")
if levene_test.pvalue > 0.05:
    print("The variances are equal across groups.")
else:
    print("The variances are not equal across groups.")

# Perform Kruskal-Wallis Test (Non-Parametric Test)
kruskal_test = kruskal(*method_groups)
print(f"Kruskal-Wallis Test: p-value = {kruskal_test.pvalue}")
if kruskal_test.pvalue < 0.05:
    print("There are significant differences between extraction methods.")
else:
    print("There are no significant differences between extraction methods.")

# Step 6: Perform Dunn's Test for Pairwise Comparisons
if kruskal_test.pvalue < 0.05:
    print("\nPerforming Dunn's Test for pairwise comparisons...")
    dunn_test_results = sp.posthoc_dunn(data_cleaned, val_col='Average', group_col='Method', p_adjust='bonferroni')

    # Print Dunn's Test Results
    print("\nDunn's Test Results (p-values):")
    print(dunn_test_results)

    # Save Dunn's Test Results to a CSV File
    # dunn_test_results.to_csv(r"C:\Users\sofii\OneDrive\Рабочий стол\try\dunn_test for total FL_results.csv")
    output_file = os.path.join(work_dir, f"dunn_test for total FL_results.csv")
    dunn_test_results.to_csv(output_file)

    print("\nDunn's test results saved as 'dunn_test_results.csv'.")

    # Heatmap of Dunn's Test Results
    plt.rcParams["font.family"] = "Times New Roman"
    plt.figure(figsize=(10, 8))
    sns.heatmap(dunn_test_results, annot=True, fmt=".3f", cmap="coolwarm", cbar=True)
    plt.xlabel("Method", labelpad= 10)
    plt.ylabel("Method", labelpad= 10)
    file_name= "Heat Map total carb FL.svg"
    file_name = os.path.join(work_dir,file_name)
    plt.savefig(file_name)
    # plt.savefig(r"C:\Users\sofii\OneDrive\Рабочий стол\try\Heat Map total carb FL.svg")
    #plt.show()
custom_palette = [
    "#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628",
    "#f781bf", "#999999", "#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3", "#a6d854",
    "#ffd92f", "#e5c494"
]

# Step 7: Visualization of Data (Boxplot)
plt.rcParams["font.family"] = "Times New Roman"
plt.figure(figsize=(6, 6))
sns.boxplot(data=data_cleaned, x='Method', y='Average', palette=custom_palette)
plt.xlabel("Extraction Method", fontsize=14, labelpad= 10)
plt.ylabel("Total carbohydrate content, mg", fontsize=14, labelpad=10)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
file_name= "Total carb_in_FL extract.svg"
file_name = os.path.join(work_dir,file_name)
# plt.savefig(r"C:\Users\sofii\OneDrive\Рабочий стол\try\Total carb_in_FL extract.svg")
# plt.savefig(r"C:\Users\sofii\OneDrive\Рабочий стол\try\Total carb_in_FL extract.svg")
#plt.show()