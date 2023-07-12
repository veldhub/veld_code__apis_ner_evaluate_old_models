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

eval_data_dict = {}


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
    model_dir = "ner_apis_2019-12-03_23:32:24"
    nlp = spacy.load(f"/veld/input/{model_dir}/nlp")
    ner_tags = nlp.get_pipe('ner').labels
    print(f"NER tags: {ner_tags}")
    evaluation_file = f"{model_dir}/corpus/evalset.txt"
    eval_data = read_data_from_txt(f"/veld/input/{evaluation_file}")
    evaluation_count_sentences = len(eval_data)
    print(f"number of sentences in evaluation data: {evaluation_count_sentences}")
    evaluation_count_tags = sum([len(e[1]['entities']) for e in eval_data])
    print(f"number of tags in evaluation data: {evaluation_count_tags}")
    eval_data_spacy = [(s,e) for s, e, _, _ in eval_data]
    scorer = nlp.evaluate(eval_data_spacy, verbose=False)
    print(f"p: {scorer.ents_p}, r: {scorer.ents_r}")
    eval_data_dict[model_dir] = {}
    eval_data_dict[model_dir]["eval_data_description"] = {
        "evaluation_file": evaluation_file, 
        "evaluation_count_sentences": evaluation_count_sentences,
        "evaluation_count_tags": evaluation_count_tags,
        "ner_tags": ner_tags,
    }
    eval_data_dict[model_dir]["evaluations"] = [
        {
            "evaluation": "spacy's evaluation",
            "p": scorer.ents_p,
            "r": scorer.ents_r,
        }
    ]


def evaluate_models_2020_01_02_until_2020_04_16():
    """
    __sresch__: copied into here from
    https://gitlab.oeaw.ac.at/acdh-ch/apis/spacy-ner/-/blob/8e75d3561e617f1bd135d4c06fbb982285f6f544/notebooks/evaluate_model.py
    as it could not be imported without causing execution of the imported modules, and I didn't
    want to refactor undocumented code. A few things were adapted such as model paths and minor 
    execution flows.
    """
    def evaluate_without_tokenization_mismatches(nerer, pipes_to_disable):
        print("The abbreviations files during data extraction and model training did not match. " +
            "I will now remove the datapoints from the evaluation set whose tokenization differs.")
        with nerer.nlp.disable_pipes(*pipes_to_disable):
            sent_doc_gp = [ (d.sentence, nerer.nlp(d.sentence), d.goldparse) for d in nerer.evaluation_data ]
        num_prob = 0
        ok = []
        for s,d,g in sent_doc_gp:
            if len(d) != len(g):
                num_prob += 1
            else:
                ok.append( (s,g) )
        print(f"I remove {num_prob} datapoints from the evaluation data.")
        print(f"Trying the evaluation again ...")
        # copy here what nerer.evaluate() does:
        with nerer.nlp.disable_pipes(*pipes_to_disable):
            scorer = nerer.nlp.evaluate(ok, verbose=False)
            nerer.scorer = scorer
            nerer.scores = scorer.scores

    # __sresch__ custom data structure to avoid the hardwired on in evaluate_models.py
    evaluations = [
        {
            "model_dir": "ner_apis_2020-01-02_12:34:48",
            "run_eval_manual": True,
            "run_eval_0": True,
             # run_eval_1 would crash because tagger pipeline is missing in model, so it's disabled
            "run_eval_1": False,
        },
        {
            "model_dir": "ner_apis_2020-01-29_13:19:53",
            "run_eval_manual": True,
            "run_eval_0": True,
             # run_eval_1 would crash because tagger pipeline is missing in model, so it's disabled
            "run_eval_1": False,
        },
        {
            "model_dir": "ner_apis_2020-04-07_15:00:35",
            "run_eval_manual": True,
            "run_eval_0": True,
            "run_eval_1": True,
        },
        {
            "model_dir": "ner_apis_2020-04-16_14:21:46",
            "run_eval_manual": True,
            "run_eval_0": True,
            "run_eval_1": True,
        },
    ]
    # __sresch__ taken from evaluate_model.py, adapted only in minor parts
    for e in evaluations:
        # ============= LOAD MODEL

        print(f"Loading model at /veld/input/{e['model_dir']} ...")
        nerer = ner.model_ner.NERer.from_saved(
            f"/veld/input/{e['model_dir']}", 
            load_training_data=False
        )
        print("Finished loading model.")
        evaluation_count_sentences = len(nerer.evaluation_data)
        print(f"number of sentences in evaluation data: {evaluation_count_sentences}")
        evaluation_count_tags = sum(len(e.entities) for e in nerer.evaluation_data)
        print(f"number of tags in evaluation data: {evaluation_count_tags}")
        ner_tags = nerer.nlp.get_pipe('ner').labels
        print(f"NER tags: {ner_tags}")
        eval_data_dict[e["model_dir"]] = {}
        eval_data_dict[e["model_dir"]]["eval_data_description"] = {
            "evaluation_file": f"{e['model_dir']}/corpus/evalset.pickle",
            "evaluation_count_sentences": evaluation_count_sentences,
            "evaluation_count_tags": evaluation_count_tags,
            "ner_tags": ner_tags,
        }

        # ================= MANUAL EVALUATION

        if e["run_eval_manual"]:
            print("Starting EM (manual evaluation) ...")
            nerer.evaluate_manually()
            e['EM'] = nerer.scores_manual
            print(f"EM: ents_p={nerer.scores_manual.p()}, ents_r={nerer.scores_manual.r()}")
            eval_data_dict[e["model_dir"]]["evaluations"] = [
                {
                    "evaluation": "manual evaluation",
                    "p": nerer.scores_manual.p(),
                    "r": nerer.scores_manual.r(),
                }
            ]

        # ================= SPACY'S EVALUATION

        if e["run_eval_0"]:
            print("Running spacy's evaluation (E0) with (string, GoldParse) as input over only the 'ner' pipe ...")
            assert nerer.nlp.has_pipe('ner')
            pipes_to_disable = []
            if nerer.nlp.has_pipe('tagger'):
                pipes_to_disable.append('tagger')
            if nerer.nlp.has_pipe('parser'):
                pipes_to_disable.append('parser')
            try:
                nerer.evaluate(pipes_to_disable=pipes_to_disable)
            except ValueError:
                evaluate_without_tokenization_mismatches(nerer, pipes_to_disable)
            scorer0 = nerer.scorer
            e['E0'] = scorer0
            print(f"E0: ents_p={scorer0.ents_p}, ents_r={scorer0.ents_r}")
            eval_data_dict[e["model_dir"]]["evaluations"].append(
                {
                    "evaluation": "spacy's evaluation (E0) with 'ner' pipe",
                    "p": scorer0.ents_p,
                    "r": scorer0.ents_r,
                }
            )

        if e["run_eval_1"]:
            print("Running spacy's evaluation (E1) with (string, GoldParse) as input over the pipes 'tagger', 'parser', and 'ner' ...")
            assert nerer.nlp.has_pipe('tagger')
            assert nerer.nlp.has_pipe('parser')
            assert nerer.nlp.has_pipe('ner')
            pipes_to_disable = []
            try:
                nerer.evaluate(pipes_to_disable=pipes_to_disable)
            except ValueError:
                evaluate_without_tokenization_mismatches(nerer, pipes_to_disable)
            scorer1 = nerer.scorer
            e['E1'] = scorer1
            print(f"E1: ents_p={scorer1.ents_p}, ents_r={scorer1.ents_r}")
            eval_data_dict[e["model_dir"]]["evaluations"].append(
                {
                    "evaluation": "spacy's evaluation (E1) with 'tagger', 'parser', 'ner' pipes",
                    "p": scorer1.ents_p,
                    "r": scorer1.ents_r,
                }
            )


def evaluate_model_2020_04_30():
    """
    __srech__: custom function so that the evaluation data's shape is handled. The data and its 
    tags is persisted as list of tokens, making it necessary to compare them against predicted 
    tokens, which hinders the usage of spaCy's evaluate function (to my knowledge). Meaning that 
    precision and recall are manually calculated.
    """
    model_dir = "ner_apis_2020-04-30_11:24:09"
    nlp = spacy.load(f"/veld/input/{model_dir}/nlp")
    ner_valid_list = nlp.get_pipe("ner").labels
    print(f"NER tags: {ner_valid_list}")
    count_tp = 0
    count_fp = 0
    count_fn = 0
    count_total = 0
    count_sentences = 0
    count_tags = 0
    evaluation_file = f"{model_dir}/corpus/evalset.json" 
    with open(f"/veld/input/{evaluation_file}", "r", encoding="utf-8") as f:
        eval_data = json.load(f)["paragraphs"]
        for p in eval_data:
            token_pred_list = nlp(p["raw"])
            token_real_list = []
            for s in p["sentences"]:
                for t in s["tokens"]:
                    token_real_list.append(t)
                    if t["ner"] != "O":
                        count_tags += 1
                count_sentences += 1
            for token_pred, token_real in zip(token_pred_list, token_real_list):
                if token_pred.orth_ == token_real["orth"]:
                    ner_pred = token_pred.ent_type_
                    ner_real = token_real["ner"]
                    if ner_pred != "" or ner_real != "O":
                        count_total += 1
                        pred_is_correct = False
                        for ner_valid in ner_valid_list:
                            if ner_valid in ner_pred and ner_valid in ner_real:
                                pred_is_correct = True
                                count_tp += 1
                                break
                        if not pred_is_correct:
                            if ner_pred != "":
                                count_fp += 1
                            elif ner_pred == "" and ner_real != "O" :
                                count_fn += 1

    print(f"number of tags in evaluation data: {count_tags}")
    print(f"number of sentences in evaluation data: {count_sentences}")
    if count_tp + count_fp + count_fn != count_total:
        raise Exception()

    p = count_tp / (count_tp + count_fp)
    r = count_tp / (count_tp + count_fn)
    print(f"p: {p}, r: {r}")
    eval_data_dict[model_dir] = {}
    eval_data_dict[model_dir]["eval_data_description"] = {
        "evaluation_file": evaluation_file, 
        "evaluation_count_sentences": count_sentences,
        "evaluation_count_tags": f"{count_tags} (BILOU tags, so plenty of redundancies)",
        "ner_tags": ner_valid_list,
    }
    eval_data_dict[model_dir]["evaluations"] = [
        {
            "evaluation": "manual evaluation",
            "p": p * 100,
            "r": r * 100,
        }
    ]


def write_eval_to_file(eval_file_path, eval_data):
    with open(eval_file_path, "w") as f:
        for m, e in eval_data.items():
            eval_data_description = e["eval_data_description"]
            f.write("- model: **" + m + "**\n")
            f.write("  - evaluation data description:\n")
            f.write(f"    - evaluation file: {eval_data_description['evaluation_file']}\n")
            f.write(
                "    - evaluation data size: " 
                + f"count sentences: {eval_data_description['evaluation_count_sentences']}"
                + f", count NER tags: {eval_data_description['evaluation_count_tags']}\n"
            )
            f.write(f"    - NER tags: {eval_data_description['ner_tags']}\n")
            f.write("  - evaluations:\n")
            for e_instance in e["evaluations"]:
                f.write(
                    f"    - {e_instance['evaluation']}: "
                    + f"**p: {round(e_instance['p'], 2)}, "
                    + f"r: {round(e_instance['r'], 2)}**\n"
                )


if __name__ == "__main__":
    evaluate_model_2019_12_03()
    evaluate_models_2020_01_02_until_2020_04_16()
    evaluate_model_2020_04_30()
    write_eval_to_file("/veld/output/reevaluations_all.md", eval_data_dict)

