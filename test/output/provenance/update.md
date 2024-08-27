Two versions of embedding for global baseline
legacy: ada_embedding
new: 3-small

Two versions of search strategies for baseline1
legacy: dfs: may miss some search pool element
new: bfs

Two versions of evidence length for baseline1
legacy: 0.1. meaning 0.1 * token_num(raw_provenance)
new: 0.2. because average of baseline0 is 0.2.

Two versions of evidence delimiter for global baseline
legacy: '\n\n', may conflict with that in sentences. 
new: '||', also specify that in the prompt of generate_from_evidence

