import matplotlib.pyplot as plt
import numpy as np
# Data for GPT-4o
gpt4o_datasets = ["civic", "paper", "notice"]
gpt4o_compression_rates = [0.2015635114275756, 0.12609731992326026, 0.1087875542528606]

# Data for GPT-4turbo
gpt4turbo_compression_rates = [0.24289199820743915, 0.08766932155107261, 0.07136012626120286]
gpt4turbo_jaccard_similarity = [0.7640746928396542, 0.7440609098503835, 0.825]

# Creating two plots: Compression Rate and Average Jaccard Similarity

fig, axs = plt.subplots(2, 1, figsize=(8, 12))

# Compression Rate Comparison
bar_width = 0.35
x = np.arange(len(gpt4o_datasets))

# Bar chart for compression rates
bars_gpt4o = axs[0].bar(x - bar_width/2, gpt4o_compression_rates, bar_width, label='GPT-4o', color='blue')
bars_gpt4turbo = axs[0].bar(x + bar_width/2, gpt4turbo_compression_rates, bar_width, label='GPT-4turbo', color='green')

# Adding labels to each bar for compression rates
for bar in bars_gpt4o:
    yval = bar.get_height()
    axs[0].text(bar.get_x() + bar.get_width()/2, yval + 0.01, round(yval, 3), ha='center', va='bottom')
for bar in bars_gpt4turbo:
    yval = bar.get_height()
    axs[0].text(bar.get_x() + bar.get_width()/2, yval + 0.01, round(yval, 3), ha='center', va='bottom')

# Labels and title for Compression Rate
axs[0].set_xlabel('Dataset')
axs[0].set_ylabel('Compression Rate')
axs[0].set_title('Baseline1 Compression Rate Comparison: GPT-4o vs GPT-4turbo')
axs[0].set_xticks(x)
axs[0].set_xticklabels(gpt4o_datasets)
axs[0].legend()

# Jaccard Similarity Comparison for GPT-4turbo
bars_jaccard = axs[1].bar(x, gpt4turbo_jaccard_similarity, bar_width, label='Jaccard Similarity (GPT-4turbo)', color='orange')

# Adding labels to each bar for Jaccard similarity
for bar in bars_jaccard:
    yval = bar.get_height()
    axs[1].text(bar.get_x() + bar.get_width()/2, yval + 0.01, round(yval, 3), ha='center', va='bottom')

# Labels and title for Jaccard Similarity
axs[1].set_xlabel('Dataset')
axs[1].set_ylabel('Jaccard Similarity')
axs[1].set_title('Average Jaccard Similarity Comparison (GPT-4turbo)')
axs[1].set_xticks(x)
axs[1].set_xticklabels(gpt4o_datasets)

# Display the plots
plt.tight_layout()
plt.show()
