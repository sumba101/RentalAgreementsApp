import torch
from transformers import AutoTokenizer, AutoModel


def combine_embeddings_by_mean(model_output, attention_mask):
    last_state = model_output[0]
    expanded_mask = attention_mask.unsqueeze(-1).expand(last_state.size()).float()
    sum_mask = torch.clamp(torch.sum(expanded_mask, 1), min=1e-9)
    embeddings = torch.sum(last_state * expanded_mask, 1) / sum_mask

    return embeddings


tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/roberta-base-nli-stsb-mean-tokens')
model = AutoModel.from_pretrained('sentence-transformers/roberta-base-nli-stsb-mean-tokens')

clauses_file = 'uncommon-clauses.txt'
clauses = list()

with open(clauses_file, 'r') as f:
    for line in f.readlines():
        if not line.strip() == '':
            clauses.append(line.strip())

if __name__ == '__main__':
    print(clauses)
    print(len(clauses))

    encoded_input = tokenizer(clauses, max_length=64, padding='max_length', truncation=True, return_tensors='pt')
    model_output = model(**encoded_input)
    embeddings = combine_embeddings_by_mean(model_output, attention_mask=encoded_input['attention_mask'])

    print(embeddings)
    print(embeddings.shape)
