import torch
import nmslib

embeddings = torch.load('embeddings.pt').detach().numpy()

print(embeddings.shape)

index = nmslib.init(method='hnsw', space='cosinesimil')
index.addDataPointBatch(embeddings)
index.createIndex({'post': 2}, print_progress=True)
index.saveIndex('dense_index_nonoptim.bin', save_data=True)

print(index)
