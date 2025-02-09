import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

def process_data(file):
    """Функция обработки данных для фукоидана или альгината."""
    sheet_name = "Sheet1"
    xls = pd.ExcelFile(file)
    df = xls.parse(sheet_name=sheet_name)
    df = df.drop(columns='Combined Yield')
    df = df.rename(columns={df.columns.values[0]: 'Method'})
    df['Method'] = df['Method'].astype(str).str.replace('method_', '', regex=False)
    df['Extraction Technique'] = df['Extraction Technique'].astype(str).str[0]
    df = df.assign(
        Method=df['Method'].astype('category'),
        Solvent_Type=df['Solvent'].astype('category'),
        Extraction_Technique=df['Extraction Technique'].astype('category')
    )
    df1 = (
        df.drop(columns=['Replicate Number'])
          .groupby('Method', group_keys=False)
          .apply(lambda group: group.assign(Replicate=pd.Categorical(group.reset_index().index + 1)))
    )
    id_vars = ['Method', 'Solvent_Type', 'Extraction_Technique', 'Replicate']
    value_vars = [col for col in df1.columns if col.startswith('Measurement')]
    return pd.melt(df1, id_vars=id_vars, value_vars=value_vars, var_name='Measurement', value_name='carbs/mg')

def plot_gr_two(dataTall_fucoidan, dataTall_alginate, output_dir):
    """Функция для построения боксплотов с сравнением фукоидана и альгината."""
    plt.figure(figsize=(12, 10))
    method_order = sorted(dataTall_fucoidan['Method'].astype(int).unique())
    
    extraction_palette = {'W': 'deepskyblue', 'P': 'turquoise', 'M': 'gold'}
    solvent_palette = {'Water': 'darkblue', 'Acid': 'orange'}
    
    dataTall_fucoidan['Substrate'] = 'Fucoidan'
    dataTall_alginate['Substrate'] = 'Alginate'
    combined_data = pd.concat([dataTall_fucoidan, dataTall_alginate])
    combined_data['Method'] = combined_data['Method'].astype(int)
    
    ax = sns.boxplot(
        data=combined_data,
        x='Method',
        y='carbs/mg',
        hue='Substrate',
        dodge=True,
        width=0.3,  # Делаем боксплоты уже
        showfliers=False,  # Убираем выбросы (точки)
        palette={'Fucoidan': 'navy', 'Alginate': 'orange'}
    )
    
    for method in method_order:
        plt.axvline(x=method - 1, color='gray', linestyle='--', linewidth=0.5)
    
    plt.title('Comparison of Carbohydrates/mg between Fucoidan and Alginate')
    plt.xlabel('Extraction Method')
    plt.ylabel('Carbohydrates/mg')
    plt.xticks(ticks=range(len(method_order)), labels=[str(m) for m in method_order])
    plt.legend(title='Substrate', loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'Comparison_Fucoidan_Alginate.svg')
    plt.savefig(output_path, format='svg', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

# Использование
file_fucoidan = "G:\\My\\sov\\extract\\FL for permuations.xlsx"
file_alginate = "G:\\My\\sov\\extract\\Al for permuations.xlsx"
output_dir = os.path.join(os.path.dirname(__file__), 'Data')

data_fucoidan = process_data(file_fucoidan)
data_alginate = process_data(file_alginate)
plot_gr_two(data_fucoidan, data_alginate, output_dir)
