FROM python:3.6.15
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt
#CMD ["jupyter", "notebook", "--allow-root", "/veld/exec/notebooks"]
CMD ["python", "/veld/exec/src/reevaluate_all_models.py"]

