from semantic_search import *

tokenizer, model = load_models()
print('Tokenizer & model loaded.')

clauses = load_clauses()
print('clauses', clauses)
print(len(clauses))


embeddings = get_embeddings(clauses, tokenizer, model)
print('embeddings', embeddings)
print(embeddings.shape)

create_and_store_index(embeddings, name='sub_app/dense_index_nonoptim.bin')
