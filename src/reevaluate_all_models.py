import spacy
import json
# __sresch__ these imports need to be done, because otherwise the unpickling of metadata would crash
# in the function NERer.load_metadata . No idea why.
from ner.model_ner import ModelType, TrainingStyle
import ner.model_ner


print("starting evaluations")
# this is necessary to avoid this strange E050
# related: https://github.com/explosion/spaCy/issues/3552
nlp = spacy.load('de_core_news_md')
del nlp





def evaluate_model_2019_12_03():
    def read_data_from_txt(mypath):
        """
        __sresch__: this function is copied without modifications from https://gitlab.oeaw.ac.at/acdh-ch/apis/spacy-ner/-/blob/8e75d3561e617f1bd135d4c06fbb982285f6f544/notebooks/NER%20Place%20Institution.ipynb 
        because since it's in a jupyter notebook, it couldn't be easily imported without third 
        party tooling. And if it the import was made possible, it executed the whole other 
        notebook. And I didn't want to interfer in the original code just to make that function 
        importable here. So I just copied it as a whole here.
        """
        mydata = []
        with open(mypath, "r") as f:
            lines = f.readlines()
            i = 0
            while i < len(lines):
                while lines[i].isspace():
                    i += 1
                # we found a non-empty line to use for t
                t = lines[i].strip()
                i += 1
                while lines[i].isspace():
                    i += 1
                # we found a non-empty line to use for e if possible, else for t
                e = None
                while e == None:
                    try:
                        e = eval(lines[i])
                    except SyntaxError:
                        t += lines[i].strip()
                        i += 1
                        while lines[i].isspace():
                            i += 1
                        # we found a non-empty line to try to use for e again
                i += 1
                mydata.append( (t, e, None, None) )
        return mydata

    # __sresch__ custom code, using the given txt reader function above made for that data shape
    print("running 'evaluate_model_2019_12_03'")
    model_dir = "/veld/input/ner_apis_2019-12-03_23:32:24"
    nlp = spacy.load(f"{model_dir}/nlp")
    print(f"NER tags: {nlp.get_pipe('ner').labels}")
    eval_data = read_data_from_txt(f"{model_dir}/corpus/evalset.txt")
    print(f"number of tags in evaluation data: {sum([len(e[1]['entities']) for e in eval_data])}")
    print(f"number of sentences in evaluation data: {len(eval_data)}")
    eval_data_spacy = [(s,e) for s, e, _, _ in eval_data]
    scorer = nlp.evaluate(eval_data_spacy, verbose=False)
    print(f"p: {scorer.ents_p}, r: {scorer.ents_r}")


if __name__ == "__main__":
    evaluate_model_2019_12_03()

