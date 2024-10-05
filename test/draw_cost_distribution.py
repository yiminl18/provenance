import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

baselines = ['baseline3_reverse', 'baseline2_binary', 'baseline2_greedy']
datasets = ['civic', 'notice', 'paper']
models = ['gpt4o']

def draw_index_and_cost_distribution(baseline:str, dataset:str, model:str):

    # Define the folder path
    folder_path = f'test/output/provenance/{baseline}/{dataset}/{model}'

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
                    answer = entry.get("raw_answer", None)

                    # Check if the answer is None and set a flag
                    is_non_answer = True if answer=="None" else False

                    call_count = entry.get("gpt35_call_count", 0) + entry.get("gpt4o_call_count", 0) + entry.get("gpt4o_mini_call_count", 0) + entry.get("gpt4_turbo_call_count", 0)
                    compression_rate = entry.get("compression_rate", None)
                    cost = entry.get("cost", None)
                    total_indices = len(entry.get("sentences", []))
                    
                    data.append({"question_id": question_id, "document_id": document_id, "call_count": call_count, 
                                "compression_rate": compression_rate, "cost": cost, "total_indices": total_indices, "is_non_answer": is_non_answer})
                    
                    index_to_delete = entry.get("index_to_delete", [])
                    if not index_to_delete:
                        index_to_delete = [-1]
                    index_data_qd.append({"question_id": question_id, "document_id": document_id, "index_to_delete": index_to_delete})

    # Convert to DataFrame
    df = pd.DataFrame(data)
    index_df_qd = pd.DataFrame(index_data_qd)

    # Explode the 'index_to_delete' into individual rows for analysis
    index_exploded_df_qd = index_df_qd.explode("index_to_delete").reset_index(drop=True)
    index_exploded_df_qd['index_to_delete'] = index_exploded_df_qd['index_to_delete'].astype(int)

    # Merge index data with call_count, compression_rate, cost, total_indices, and non-answer flag
    merged_df = pd.merge(index_exploded_df_qd, df[['question_id', 'document_id', 'compression_rate', 'call_count', 'cost', 'total_indices', 'is_non_answer']], 
                        on=['question_id', 'document_id'], how='left')

    # Create the list of unique (question, document) pairs from the merged data
    pairs = sorted(merged_df.drop_duplicates(subset=['question_id', 'document_id'])
                .apply(lambda row: f"Q{row['question_id']}, D{row['document_id']}", axis=1).tolist())

    df['pair_label'] = df.apply(lambda row: f"Q{row['question_id']}, D{row['document_id']}", axis=1)
    df = df.set_index('pair_label').reindex(pairs)

    # Set up the figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 8), gridspec_kw={'width_ratios': [2, 1]})

    # Scatter Plot with Annotations (Left Plot)
    for (question_id, document_id), group in merged_df.groupby(['question_id', 'document_id']):
        label = f'Q{question_id}, D{document_id}'
        ax1.scatter([f'Q{question_id}, D{document_id}'] * len(group), group['index_to_delete'], label=label, alpha=0.6)
        
        top_y_position = group['index_to_delete'].max() + 1
        compression_rate = f"{group['compression_rate'].iloc[0]:.3f}" if pd.notna(group['compression_rate'].iloc[0]) else "N/A"
        call_count = f"{group['call_count'].iloc[0]:.3f}" if pd.notna(group['call_count'].iloc[0]) else "N/A"
        cost = f"{group['cost'].iloc[0]:.3f}" if pd.notna(group['cost'].iloc[0]) else "N/A"
        
        annotation = f"CR: {compression_rate}\nCC: {call_count}\nCost: {cost}"
        ax1.text(f'Q{question_id}, D{document_id}', top_y_position, annotation, fontsize=8, ha='center')

        total_indices = group['total_indices'].iloc[0]
        ax1.plot([f'Q{question_id}, D{document_id}', f'Q{question_id}, D{document_id}'], [0, total_indices - 1], color='grey', linestyle='-', linewidth=1)

    ax1.axhline(y=-1, color='grey', linestyle='--')
    ax1.set_xlabel('(Question, Document) Pair')
    ax1.set_ylabel('Index to Delete')
    ax1.set_title(f'Dispersion of Indices to Delete, baseline{baseline}/{dataset}/{model}')
    ax1.set_xticks(range(len(pairs)))

    # Set x-tick labels without color yet
    xticks = ax1.set_xticklabels(pairs, rotation=90)

    # Determine the colors for x-axis labels based on whether it's a non-answer
    xtick_colors = ['red' if df.loc[pair, 'is_non_answer'] else 'black' for pair in pairs]

    # Set the color for each x-tick label individually
    for tick, color in zip(xticks, xtick_colors):
        tick.set_color(color)

    # Bar Plot of Costs (Right Plot)
    bar_positions = np.arange(len(pairs))
    bar_width = 0.4
    ax2.bar(bar_positions, df['cost'], width=bar_width, color='lightgray', alpha=0.5, label='Cost', zorder=0)

    ax2.set_xlabel('(Question, Document) Pair')
    ax2.set_ylabel('Cost')
    ax2.set_title('Cost by (Question, Document) Pair')
    ax2.set_xticks(bar_positions)

    # Set x-tick labels without color yet
    xticks_bar = ax2.set_xticklabels(pairs, rotation=90)

    # Set the color for each x-tick label in the bar plot individually
    for tick, color in zip(xticks_bar, xtick_colors):
        tick.set_color(color)

    plt.tight_layout()
    plt.savefig(f'test/output/provenance/{baseline}/{baseline}_{dataset}_{model}_combined_plot.png')

for baseline in baselines:
    for dataset in datasets:
        for model in models:
            draw_index_and_cost_distribution(baseline, dataset, model) 