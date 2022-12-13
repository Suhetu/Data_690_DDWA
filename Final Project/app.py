from flask import Flask
from flask import abort, request
import numpy as np
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import GridSearchCV

app = Flask(__name__)

data = pd.read_csv('diagnostics.csv', header=None)
data.columns =['Temperature of patient', 'Occurrence of nausea', 'Lumbar pain', 'Urine pushing', 'Micturition pains', 'Burning of urethra, itch, swelling of urethra outlet', 'decision: Inflammation of urinary bladder', 'decision: Nephritis of renal pelvis origin']
data.columns = [i.replace(',', '').replace(' ', '_').replace(':', '') for i in data.columns]
data.Temperature_of_patient = data.Temperature_of_patient.apply(lambda x: x.replace(',', '.'))
data.Occurrence_of_nausea = [i.replace('no', '0').replace('yes', '1') for i in data.Occurrence_of_nausea]
data.Lumbar_pain = [i.replace('no', '0').replace('yes', '1') for i in data.Lumbar_pain]
data.Urine_pushing = [i.replace('no', '0').replace('yes', '1') for i in data.Urine_pushing]
data.Micturition_pains = [i.replace('no', '0').replace('yes', '1') for i in data.Micturition_pains]
data.Burning_of_urethra_itch_swelling_of_urethra_outlet = [i.replace('no', '0').replace('yes', '1') for i in data.Burning_of_urethra_itch_swelling_of_urethra_outlet]
data.decision_Inflammation_of_urinary_bladder = [i.replace('no', '0').replace('yes', '1') for i in data.decision_Inflammation_of_urinary_bladder]
data.decision_Nephritis_of_renal_pelvis_origin = [i.replace('no', '0').replace('yes', '1') for i in data.decision_Nephritis_of_renal_pelvis_origin]

X = data.iloc[:,:6]
y = data.iloc[:,6:7]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

clf1 = LogisticRegression(penalty='l2', C=0.001, solver='lbfgs', random_state=2)
clf2 = DecisionTreeClassifier(max_depth=1, criterion='entropy', random_state=3)
clf3 = KNeighborsClassifier(n_neighbors=1, p=2, metric='minkowski')

pipe1 = Pipeline([('scaler', StandardScaler()),('logreg', clf1)])
pipe2 = Pipeline([('scaler', StandardScaler()),('tree', clf2)])
pipe3 = Pipeline([('scaler', StandardScaler()),('knn', clf3)])

labs = ['Logistic Regression', 'Decision Tree', 'k-Nearest Neighbors']
clfs = [pipe1, pipe2, pipe3]
clfs = zip(labs, clfs)

ems = [('lr', pipe1),('dt', pipe2),('knn', pipe3)]
clf4 = VotingClassifier(estimators= ems, weights=None, voting='soft')

scores = cross_val_score(estimator=clf4, X=X_train, y=y_train, cv=10, scoring='roc_auc')

params = {'lr__logreg__C':[0.001, 0.1, 1, 10], 
          'dt__tree__max_depth': [1,2,3], 
          'knn__knn__n_neighbors': [1,2,3]
         }

vc_gs_1 = GridSearchCV(estimator=clf4, param_grid=params, scoring='roc_auc', refit=True)
vc_gs_1 = vc_gs_1.fit(X_train, y_train)
vc_gs_1_score = vc_gs_1.score(X_test, y_test)

y = data.iloc[:,7:8]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

clf1 = LogisticRegression(penalty='l2', C=0.001, solver='lbfgs', random_state=2)
clf2 = DecisionTreeClassifier(max_depth=1, criterion='entropy', random_state=3)
clf3 = KNeighborsClassifier(n_neighbors=1, p=2, metric='minkowski')

pipe1 = Pipeline([('scaler', StandardScaler()),('logreg', clf1)])
pipe2 = Pipeline([('scaler', StandardScaler()),('tree', clf2)])
pipe3 = Pipeline([('scaler', StandardScaler()),('knn', clf3)])

labs = ['Logistic Regression', 'Decision Tree', 'k-Nearest Neighbors']
clfs = [pipe1, pipe2, pipe3]
clfs = zip(labs, clfs)

ems = [('lr', pipe1),('dt', pipe2),('knn', pipe3)]
clf4 = VotingClassifier(estimators= ems, weights=None, voting='soft')

scores = cross_val_score(estimator=clf4, X=X_train, y=y_train, cv=10, scoring='roc_auc')

params = {'lr__logreg__C':[0.001, 0.1, 1, 10], 
          'dt__tree__max_depth': [1,2,3], 
          'knn__knn__n_neighbors': [1,2,3]
         }

vc_gs_2 = GridSearchCV(estimator=clf4, param_grid=params, scoring='roc_auc', refit=True)
vc_gs_2 = vc_gs_2.fit(X_train, y_train)
vc_gs_2_score = vc_gs_2.score(X_test, y_test)



@app.route('/predict', methods=['POST', 'GET'])
def predict_disease():
    if request.method == "POST":
        if request.json and 'data' in request.json:
            print(request.json)

            patient_info = request.json['data']
            arr_patient_info = np.array(patient_info).reshape(1,-1)

            if arr_patient_info[0][0] == 'IUB':
                pred = vc_gs_1.predict_proba(np.array(arr_patient_info[0][1:]).reshape(1,-1))
                return {"prediction": pred[0][1]}
            
            if arr_patient_info[0][0] == 'NRP':
                pred = vc_gs_2.predict_proba(np.array(arr_patient_info[0][1:]).reshape(1,-1))
                return {"prediction": pred[0][1]}

        else: abort(405)
    else: abort(405)