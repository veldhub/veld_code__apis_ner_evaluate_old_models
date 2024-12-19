# APIS NER evaluate

This is a code veld being used for a real task in the intavia project. It reevaluates models 
trained using spacy2 here: https://gitlab.oeaw.ac.at/acdh-ch/apis/spacy-ner .

This repo is a VELD executable, meaning it is not supposed to run on its own. It is wired into a
VELD chain here: https://gitlab.oeaw.ac.at/acdh-ch/nlp/veld_chain_5_apis_ner_evaluate_old_models
which is the main execution focus. 

## Evaluation details of spacy 2.2.4 models

The main code for evaluation lies in
[./src/reevaluate_all_models.py](./src/reevaluate_all_models.py). There some pre-existing code from
Sabine's repo is reused (by simply copying it) as it was tailored to the data shape.

There are 7 trained models in https://gitlab.oeaw.ac.at/acdh-ch/apis/spacy-ner .

6 of those have evaluation data in their folder, so that is used to validate the models.

This evaluation data exists in these formats:
- txt (1x: 2019-12-03)
- pickle (4x: 2020-01-02 - 2020-04-16)
- json (1x: 2020-04-30)

For the `txt` and `pickle` files there are parsing functions scattered around in the original repo.
Importing them from their modules however causes execution of the modules which leads to crashes as
a lot of context is missing. In order to avoid changes to an undocumented and sprawled codebase, but
still to reuse code and its context, relevant code was copied / imported here. For the `json` file,
no existing parsing function was found, so one was implemented.

There were also existing evaluation functions compatible with the pickle files of the models
2020-01-02 - 2020-04-16, so that was copied here and reused. For the others, custom evaluation logic
was implemented, using spaCy's function on the `txt` and a custom one on the `json` file as that
data was a in shape incompatible with spaCy's function.

The commit of the remaining code base which was copied or imported from is
https://gitlab.oeaw.ac.at/acdh-ch/apis/spacy-ner/-/tree/8e75d3561e617f1bd135d4c06fbb982285f6f544


