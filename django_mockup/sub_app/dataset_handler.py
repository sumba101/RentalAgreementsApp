import os
import json
import pandas as pd

editable_data_dir = os.path.join('sub_app', 'data', 'editable-data')
dataset_dir = os.path.join('sub_app', 'data', 'dataset')


def make_clauses_dict(input_dir=editable_data_dir, output_dir=dataset_dir):
    with open(os.path.join(input_dir, 'clause-list.txt'), 'r') as f:
        formal_list_content = f.read()

    clause_id_dict = dict()
    for split in formal_list_content.strip().split('\n\n'):
        clause_id, clause = split.strip().split('\n')
        clause_id = int(clause_id.strip())
        clause = clause.strip()
        clause_id_dict[clause_id] = clause

    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)

    with open(os.path.join(output_dir, 'clauses.json'), 'w') as f:
        json.dump(clause_id_dict, f)

    return clause_id_dict


def make_query_clause_dataset(clause_id_dict, input_dir=editable_data_dir, output_dir=dataset_dir):
    query_clause_dir = os.path.join(input_dir, 'query-clause')
    files = os.listdir(query_clause_dir)
    files.sort(key=lambda f: int(f[:-4]))
    query_clause_dicts = list()

    for file in files:
        with open(os.path.join(query_clause_dir, file), 'r') as f:
            query_clause_content = f.read().strip()

        valid_splits = list()
        for split in query_clause_content.split('\n'):
            split = split.strip()
            if split:
                valid_splits.append(split)

        clause_id = int(valid_splits[0])
        queries = valid_splits[2:]

        for i, query in enumerate(queries):
            query_clause_dict = dict()
            query_clause_dict['id'] = clause_id * 100 + i
            query_clause_dict['clause_id'] = clause_id
            query_clause_dict['query'] = query
            query_clause_dict['clause'] = clause_id_dict[clause_id]
            query_clause_dicts.append(query_clause_dict)

    with open(os.path.join(output_dir, 'query-to-clause.jsonl'), 'w') as f:
        for query_clause_dict in query_clause_dicts:
            query_clause_string = json.dumps(query_clause_dict)
            f.write(query_clause_string + '\n')

    return query_clause_dicts


def make_dataset(input_dir=editable_data_dir, output_dir=dataset_dir):
    clause_id_dict = make_clauses_dict(input_dir, output_dir)
    query_clause_dicts = make_query_clause_dataset(clause_id_dict, input_dir, output_dir)

    return clause_id_dict, query_clause_dicts


def load_clauses_dict(dataset_dir=dataset_dir):
    with open(os.path.join(dataset_dir, 'clauses.json'), 'r') as f:
        clauses_dict = json.load(f)

    return clauses_dict


def load_query_clause_dataset(dataset_dir=dataset_dir, as_pandas=True):
    with open(os.path.join(dataset_dir, 'query-to-clause.jsonl'), 'r') as f:
        query_clauses = pd.read_json(f, lines=True) if as_pandas else json.load(f)

    return query_clauses


def load_dataset(dataset_dir=dataset_dir, query_clause_as_pandas=True):
    clauses_dict = load_clauses_dict(dataset_dir)
    query_clauses = load_query_clause_dataset(dataset_dir, as_pandas=query_clause_as_pandas)

    return clauses_dict, query_clauses


if __name__ == '__main__':
    editable_data_dir = os.path.join('data', 'editable-data')
    dataset_dir = os.path.join('data', 'dataset')

    make_dataset(input_dir=editable_data_dir, output_dir=dataset_dir)
    clauses_dict, query_clauses = load_dataset(dataset_dir=dataset_dir, query_clause_as_pandas=True)
