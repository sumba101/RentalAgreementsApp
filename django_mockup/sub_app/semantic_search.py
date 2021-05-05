import torch
from transformers import AutoTokenizer, AutoModel

clauses_file = 'uncommon-clauses.txt'
clauses = list()

with open(clauses_file, 'r') as f:
    for line in f.readlines():
        if not line.strip() == '':
            clauses.append(line.strip())

print(clauses)
print(len(clauses))

tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/roberta-base-nli-stsb-mean-tokens')
model = AutoModel.from_pretrained('sentence-transformers/roberta-base-nli-stsb-mean-tokens')

# max_length = 0
# for clause in clauses:
#     tokenized_length = len(tokenizer.tokenize(clause))
#     print(tokenized_length)
#     if tokenized_length > max_length:
#         max_length = tokenized_length
#
# print(max_length)

# sentence = clauses[0]
# encoded_input = tokenizer(sentence, max_length=64, padding='max_length', truncation=True, return_tensors='pt')
# print(encoded_input)
# embedding = model(**encoded_input)[0]
# print(embedding)
#
# attention_mask = encoded_input['attention_mask']
# print(attention_mask)
# print(attention_mask.unsqueeze(-1))
# print(attention_mask.unsqueeze(-1).expand(embedding.size()))
# print(attention_mask.unsqueeze(-1).expand(embedding.size()).float())
#
# input_mask_expanded = attention_mask.unsqueeze(-1).expand(embedding.size()).float()
# print(torch.clamp(input_mask_expanded.sum(2), min=1e-9))


def combine_embeddings_by_mean(model_output, attention_mask):
    last_state = model_output[0]
    expanded_mask = attention_mask.unsqueeze(-1).expand(last_state.size()).float()
    sum_mask = torch.clamp(torch.sum(expanded_mask, 1), min=1e-9)
    embeddings = torch.sum(last_state * expanded_mask, 1) / sum_mask

    return embeddings


encoded_input = tokenizer(clauses, max_length=64, padding='max_length', truncation=True, return_tensors='pt')
model_output = model(**encoded_input)
embeddings = combine_embeddings_by_mean(model_output, attention_mask=encoded_input['attention_mask'])

print(embeddings)
print(embeddings.shape)
