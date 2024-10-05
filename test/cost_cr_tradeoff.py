# Re-import necessary libraries and reset plot settings after environment reset
import matplotlib.pyplot as plt

# Re-define the updated data
data_updated = [
    {
        "baseline_name": "baseline3_reverse",
        "model_name": "gpt4o",
        "dataset_name": "civic",
        "cost": 2.45169,
        "compression_rate": 0.666866094832716,
        "average_sentence_number": 16.266666666666666,
    },
    {
        "baseline_name": "baseline3_reverse",
        "model_name": "gpt4o",
        "dataset_name": "paper",
        "cost": 2.4607400000000004,
        "compression_rate": 0.5345860899850884,
        "average_sentence_number": 17.033333333333335,
    },
    {
        "baseline_name": "baseline3_reverse",
        "model_name": "gpt4o",
        "dataset_name": "notice",
        "cost": 1.8237400000000001,
        "compression_rate": 0.20853910139739254,
        "average_sentence_number": 3.1333333333333333,
    },
    {
        "baseline_name": "baseline2_greedy",
        "model_name": "gpt4o",
        "dataset_name": "civic",
        "cost": 4.2699050000000005,
        "compression_rate": 0.6675080653045117,
        "average_sentence_number": 16.033333333333335,
    },
    {
        "baseline_name": "baseline2_greedy",
        "model_name": "gpt4o",
        "dataset_name": "paper",
        "cost": 4.884745000000001,
        "compression_rate": 0.47170315384998446,
        "average_sentence_number": 15.666666666666666,
    },
    {
        "baseline_name": "baseline2_greedy",
        "model_name": "gpt4o",
        "dataset_name": "notice",
        "cost": 1.8942550000000002,
        "compression_rate": 0.16819134717356243,
        "average_sentence_number": 2.8666666666666667,
    },
    {
        "baseline_name": "baseline2_binary",
        "model_name": "gpt4o",
        "dataset_name": "civic",
        "average_sentence_number": 6.566666666666666,
        "compression_rate": 0.5087157337771768,
        "cost": 5.465605,
    },
    {
        "baseline_name": "baseline2_binary",
        "model_name": "gpt4o",
        "dataset_name": "paper",
        "cost": 6.45652,
        "average_sentence_number": 3.7333333333333334,
        "compression_rate": 0.34920174942099397
    },
    {
        "baseline_name": "baseline2_binary",
        "model_name": "gpt4o",
        "dataset_name": "notice",
        "average_sentence_number": 1.1666666666666667,
        "compression_rate": 0.13431160300235606,
        "cost": 0.872025,
    },
        {
        "baseline_name": "baseline2_greedy_refine",
        "model_name": "gpt4o",
        "dataset_name": "civic",
        "average_jaccard_similarity": 1.0,
        "average_token_number_of_evidence": 355.3333333333333,
        "average_token_number_of_provenance": 669.4333333333333,
        "average_sentence_number": 12.266666666666667,
        "compression_rate": 0.5254444350934737,
        "cost": 5.7528950000000005,
    },
    {
        "baseline_name": "baseline2_greedy_refine",
        "model_name": "gpt4o",
        "dataset_name": "paper",
        "average_jaccard_similarity": 1.0,
        "average_token_number_of_evidence": 205.53333333333333,
        "average_token_number_of_provenance": 573.3666666666667,
        "average_sentence_number": 11.466666666666667,
        "compression_rate": 0.34946493997924544,
        "cost": 5.9595400000000005,
    },
    {
        "baseline_name": "baseline2_greedy_refine",
        "model_name": "gpt4o",
        "dataset_name": "notice",
        "average_jaccard_similarity": 1.0,
        "average_token_number_of_evidence": 83.36666666666666,
        "average_token_number_of_provenance": 591.3666666666667,
        "average_sentence_number": 2.2666666666666666,
        "compression_rate": 0.13835195554512542,
        "cost": 1.9570200000000002,
    }
]
# data_updated = [
#     {
#         "baseline_name": "baseline0",
#         "model_name": "gpt4o",
#         "dataset_name": "civic",
#         "average_jaccard_similarity": 0.8209471470341037,
#         "average_sentence_number": 8.0,
#         "average_compression_rate": 0.1755519092733854,
#         "cost": 0.39454500000000003,
#     },
#     {
#         "baseline_name": "baseline0",
#         "model_name": "gpt4o",
#         "dataset_name": "paper",
#         "average_jaccard_similarity": 0.7914194577352471,
#         "average_sentence_number": 5.4,
#         "average_compression_rate": 0.1378284039541474,
#         "cost": 0.291205,
#     },
#     {
#         "baseline_name": "baseline0",
#         "model_name": "gpt4o",
#         "dataset_name": "notice",
#         "average_jaccard_similarity": 0.9047619047619048,
#         "average_sentence_number": 2.6,
#         "average_compression_rate": 0.10806800320127853,
#         "cost": 0.34740000000000004,
#     },
#     {
#         "baseline_name": "baseline1",
#         "model_name": "gpt4o",
#         "dataset_name": "civic",
#         "average_jaccard_similarity": 0.7831506466809427,
#         "average_sentence_number": 8.233333333333333,
#         "average_compression_rate": 0.4076265706870266,
#         "cost": 0.14276,
#     },
#     {
#         "baseline_name": "baseline1",
#         "model_name": "gpt4o",
#         "dataset_name": "paper",
#         "average_jaccard_similarity": 0.5903914141414142,
#         "average_sentence_number": 7.366666666666666,
#         "average_compression_rate": 0.24135507926532984,
#         "cost": 0.07992,
#     },
#     {
#         "baseline_name": "baseline1",
#         "model_name": "gpt4o",
#         "dataset_name": "notice",
#         "average_jaccard_similarity": 0.9194444444444444,
#         "average_sentence_number": 3.8333333333333335,
#         "average_compression_rate": 0.2525615629293758,
#         "cost": 0.091155,
#     }
# ]

# Define unique colors and markers for each baseline
baselines = list(set(d['baseline_name'] for d in data_updated))
colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
markers = ['o', 's', '^', 'D', 'v', 'p', 'P', '*', 'X', 'H']
baseline_styles = dict(zip(baselines, zip(colors, markers)))

# Plotting
plt.figure(figsize=(10, 6))
seen_labels = set()

for entry in data_updated:
    baseline = entry['baseline_name']
    dataset = entry['dataset_name']
    cost = entry['cost']
    compression_rate = entry['compression_rate']
    # compression_rate = entry['average_jaccard_similarity']
    average_sentence_number = entry['average_sentence_number']
    
    # Calculate remaining index count
    remaining_index = average_sentence_number
    
    color, marker = baseline_styles[baseline]
    label = f"{baseline}"
    if label not in seen_labels:
        plt.scatter(cost, compression_rate, color=color, marker=marker, label=label, s=80, edgecolors='black')
        seen_labels.add(label)  # Add to the set to prevent duplication
    else:
        plt.scatter(cost, compression_rate, color=color, marker=marker, s=80, edgecolors='black')
    
    # plt.scatter(cost, compression_rate, color=color, marker=marker, label=f"{baseline}", s=80, edgecolors='black')
    
    # Annotate the points with dataset name and coordinates
    plt.text(cost, compression_rate, f"({cost:.2f}, {compression_rate:.2f}) {dataset}, {remaining_index:.2f}", fontsize=8, ha='right')

# Set plot titles and labels
plt.title("CR vs Cost by Dataset and Baseline (Updated)")
plt.xlabel("Cost")
plt.ylabel("Compression Rate")
# plt.ylabel("Jaccard Similarity")

# Set legend
plt.legend(loc='best', fontsize=8, title='Baseline (Dataset)', title_fontsize='10')

# Show plot
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('test/output/provenance/cost_cr_tradeoff_with_refine.png')