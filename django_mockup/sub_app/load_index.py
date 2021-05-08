import nmslib
from semantic_search import combine_embeddings_by_mean, tokenizer, model, clauses

queries = list()

with open('queries.txt', 'r') as f:
    for line in f.readlines():
        if not line == '\n':
            queries.append(line.strip())

query_input = tokenizer(queries, max_length=64, padding='max_length', truncation=True, return_tensors='pt')
query_output = model(**query_input)
query_embeddings = combine_embeddings_by_mean(query_output, query_input['attention_mask'])
query_embeddings = query_embeddings.detach().numpy()

print('query_embeddings', query_embeddings)

space_name = 'cosinesimil'
space_params = {'p': 3}
data = nmslib.DataType.DENSE_VECTOR

index = nmslib.init(method='hnsw', space=space_name)
index.loadIndex('dense_index_nonoptim.bin', load_data=True)

neighbors = index.knnQueryBatch(query_embeddings, k=1, num_threads=2)
print(neighbors)

for result in neighbors:
    index = result[0][0]
    print(clauses[index])
