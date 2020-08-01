# fast-api-serving

A docker image serving a ML model built in sklearn.

Train the model:
* Run logistic-1.ipynb 

Build the docker image:
* docker build -t app-iris .

Run:
* docker run -d --name app-iris-container -p 80:80 app-iris

Cleanup: 
* docker container stop app-iris-container
* docker container rm app-iris-container
* docker image rm app-iris

Run without docker:
* uvicorn main:app --reload
