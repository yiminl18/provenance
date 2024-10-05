import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

baseline = 'baseline2_binary'
dataset = 'civic'
model = 'gpt4o'

# Define the folder path
folder_path = f'test/output/provenance/{baseline}/{dataset}/{model}'  # Replace with the actual folder path

# Read all JSON files in the folder
data = []
index_data_qd = []
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        with open(os.path.join(folder_path, filename), 'r') as file:
            content = json.load(file)
            for entry in content:
                question_id = entry.get("question_id", None)
                document_id = entry.get("document_id", None)
                call_count = entry.get("gpt35_call_count", 0) + entry.get("gpt4o_call_count", 0) + entry.get("gpt4o_mini_call_count", 0) + entry.get("gpt4_turbo_call_count", 0)
                compression_rate = entry.get("compression_rate", None)
                cost = entry.get("cost", None)  # Assuming 'cost' is a field in your JSON
                total_indices = len(entry.get("sentences", []))  # Get the total number of original indices
                data.append({"question_id": question_id, "document_id": document_id, "call_count": call_count, 
                             "compression_rate": compression_rate, "cost": cost, "total_indices": total_indices})
                
                # Handle index_to_delete, ensuring we handle empty lists
                index_to_delete = entry.get("index_to_delete", [])
                if not index_to_delete:
                    index_to_delete = [-1]  # Assign a placeholder value if the list is empty
                index_data_qd.append({"question_id": question_id, "document_id": document_id, "index_to_delete": index_to_delete})

# Convert to DataFrame
df = pd.DataFrame(data)

# Convert to DataFrame
index_df_qd = pd.DataFrame(index_data_qd)

# Explode the 'index_to_delete' into individual rows for analysis
index_exploded_df_qd = index_df_qd.explode("index_to_delete").reset_index(drop=True)
index_exploded_df_qd['index_to_delete'] = index_exploded_df_qd['index_to_delete'].astype(int)

# Merge index data with call_count, compression_rate, cost, and total_indices
merged_df = pd.merge(index_exploded_df_qd, df[['question_id', 'document_id', 'compression_rate', 'call_count', 'cost', 'total_indices']], 
                     on=['question_id', 'document_id'], how='left')

# Visualize the distribution of indices for each (question, document) pair, with annotations
plt.figure(figsize=(16, 8))

# Adjust the top margin to accommodate more space for annotations
plt.subplots_adjust(top=0.85)

# Plot a scatter plot to visualize the dispersion
for (question_id, document_id), group in merged_df.groupby(['question_id', 'document_id']):
    label = f'Q{question_id}, D{document_id}'
    plt.scatter([f'Q{question_id}, D{document_id}'] * len(group), group['index_to_delete'], label=label, alpha=0.6)
    
    # Annotate only once at the top position for each column
    top_y_position = group['index_to_delete'].max() + 1  # Place the annotation just above the highest point
    compression_rate = f"{group['compression_rate'].iloc[0]:.3f}" if pd.notna(group['compression_rate'].iloc[0]) else "N/A"
    call_count = f"{group['call_count'].iloc[0]:.3f}" if pd.notna(group['call_count'].iloc[0]) else "N/A"
    cost = f"{group['cost'].iloc[0]:.3f}" if pd.notna(group['cost'].iloc[0]) else "N/A"
    
    annotation = f"CR: {compression_rate}\nCC: {call_count}\nCost: {cost}"
    
    plt.text(f'Q{question_id}, D{document_id}', top_y_position, annotation, fontsize=8, ha='center')

    # Add a horizontal line at the total index count for this (question_id, document_id) pair
    total_indices = group['total_indices'].iloc[0]
    plt.plot([f'Q{question_id}, D{document_id}', f'Q{question_id}, D{document_id}'], [0, total_indices-1], color='grey', linestyle='-', linewidth=1)

# Customize y-axis to indicate the placeholder for empty entries
plt.axhline(y=-1, color='grey', linestyle='--')  # Optional: add a line for clarity
plt.xlabel('(Question, Document) Pair')
plt.ylabel('Index to Delete')
plt.title('Dispersion of Indices to Delete by (Question, Document) Pair with Annotations (including empty)')
plt.xticks(rotation=90)

# Remove the legend
# plt.legend(title='Question ID', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.savefig(f'test/output/provenance/{baseline}/{dataset}_{model}_index_dispersion_qd_annotated.png')