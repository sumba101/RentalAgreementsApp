from transformers import AutoTokenizer, AutoModel
import nmslib
import torch


def get_query_list(freeform, delimiter='*'):
    splits = freeform.split(delimiter)
    queries = list()

    for split in splits:
        if not split.strip() == '':
            queries.append(split.strip())

    return queries


def load_uncommon_clauses(filename='sub_app/uncommon-clauses.txt'):
    clauses = list()

    with open(filename, 'r') as f:
        for line in f.readlines():
            if not line.strip() == '':
                clauses.append(line.strip())

    return clauses


def load_models(model_name='sentence-transformers/roberta-base-nli-stsb-mean-tokens'):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    return tokenizer, model


def get_embeddings(sentences, tokenizer, model):
    encoded_input = tokenizer(sentences, max_length=64, padding='max_length', truncation=True, return_tensors='pt')
    model_output = model(**encoded_input)
    embeddings = combine_embeddings_by_mean(model_output, attention_mask=encoded_input['attention_mask'])
    embeddings = embeddings.detach()

    return embeddings


def combine_embeddings_by_mean(model_output, attention_mask):
    last_state = model_output[0]
    expanded_mask = attention_mask.unsqueeze(-1).expand(last_state.size()).float()
    sum_mask = torch.clamp(torch.sum(expanded_mask, 1), min=1e-9)
    embeddings = torch.sum(last_state * expanded_mask, 1) / sum_mask

    return embeddings


def create_and_store_index(embeddings, name):
    index = nmslib.init(method='hnsw', space='cosinesimil', data_type=nmslib.DataType.DENSE_VECTOR)
    index.addDataPointBatch(embeddings)
    index.createIndex({'post': 2}, print_progress=True)
    index.saveIndex(name, save_data=True)


def load_index(name):
    index = nmslib.init(method='hnsw', space='cosinesimil', data_type=nmslib.DataType.DENSE_VECTOR)
    index.loadIndex(name, load_data=True)

    return index


def search_clauses_for_queries(query_embeddings, index):
    clauses = load_uncommon_clauses()
    neighbors = index.knnQueryBatch(query_embeddings, k=1, num_threads=2)
    searched_clauses = [clauses[result[0][0]] for result in neighbors]

    return searched_clauses

