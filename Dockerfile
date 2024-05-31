FROM python:3.7.6
RUN pip install \
    spacy==2.2.4 \
    de-core-news-md@https://github.com/explosion/spacy-models/releases/download/de_core_news_md-2.2.5/de_core_news_md-2.2.5.tar.gz#sha256:f325eebb70e0c4fe280deb605004667a65bb3457dcde7a719926a4e040266cca
#CMD ["python", "/veld/executable/src/reevaluate_all_models.py"]

