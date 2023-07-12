# experimental VELD executable

This is a prototype being used for a real task in the intavia project. It re-evaluates models 
trained using spacy2 here: https://gitlab.oeaw.ac.at/acdh-ch/apis/spacy-ner .

The main code for evaluation lies in
[./src/reevaluate_all_models.py](./src/reevaluate_all_models.py). There some pre-existing code from
Sabine's repo is reused (by simply copying it) as it was tailored to the data shape.

This repo is a VELD executable, meaning it is not supposed to run on its own. It is wired into a
VELD chain here: https://gitlab.oeaw.ac.at/acdh-ch/nlp/veld_chain_5_apis_ner_evaluate_old_models
which is the main execution focus. 
