# Managing Dataset

## Manually adding/editing data
* Use __editable_data__ folder for manually adding entries in the dataset.
* If a new clause is to be added, add it in the right format in __clause-list.txt__ file first
* Corresponsing to the __id__ of this new clause (i.e. the number above this clause in clause-list.txt file), create a __.txt__ file in __query-clause__ folder
* Add one or more queries in the new notepad file. The first line is _clause id_, second line is the actual _clause_, all the succeeding lines are different 
_queries_ that should retrieve this clause. Ensure the _format_ as other files (spacing, line gaps, ..).
* Similar procedure as above point if new queries are to be added to an existing clause.

## Creating & using dataset

* `make_dataset()` function of `dataset_handler.py` automatically builds the dataset from the latest version of editable_data.
* A _json_ file: __clauses.json__ containing clauses mapped to their ids and a _jsonl_ file: __query-to-clause.jsonl__ with each line containing a json object 
for _query_, _clause id_, _object id_ & _clause_ is available as part of the workable dataset.
* `load_dataset()` function from same module loads the dataset as _dictionary_ and pandas _DataFrame_ respectively by default.

Using codebase developed for the application, studies can be performed by using this dataset to find out the best accuracy method, as a demo in 
the notebook `test_semantic_search.ipynb`.
