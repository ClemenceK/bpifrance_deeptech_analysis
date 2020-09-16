import json
import joblib
# to launch api server:
# python app.py
from flask import Flask
from flask import request
from bpideep.getpatent import Patent
from bpideep.getdata import company_search
from bpideep.feateng import feat_eng_new_entry

app = Flask(__name__)

@app.route('/')
def index():
     return 'OK'

@app.route('/predict', methods=['GET'])
def predict():
    name = request.args['name']

    # get nb of patents with Big Query
    patent = Patent()
    nb_patents = patent.get_nb_patents(name)

    # get DealRoom datas
    X = company_search(name)
    if X.empty:
        return 'Company name not found on DealRoom'
    X['nb_patents'] = nb_patents
    X = feat_eng_new_entry(X)

    pipeline = joblib.load('bpideepmodel.joblib')
    results = pipeline.predict(X)
    return {"predictions": str(results[0])}

    # TODO
    # create an X_pred dataframe from request.args
    # enrich with dealroom et google patent
    # load model.joblib
    # make a prediction
    # return result
    # y_pred = 3
    # prediction_dict = { 'pred' : y_pred}
    # return prediction_dict
    # return json.dumps({'coucou' : 'yes'})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
