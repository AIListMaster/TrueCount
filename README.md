# TrueCount - Sentiment Analysis using BERT

A demo project to train a BERT model for sentiment analysis of restaurants. We are using [Flask-Admin](https://github.com/app-generator/flask-adminlte) for this project.

<br />

## ✅ Includes

- Web interface form restaurant reviews
- Sample code to train BERT
- Sample code to scrap reviews.

![TrueCount - Sentiment Analysis using BERT.](https://github.com/AIListMaster/TrueCount/blob/master/screenshot.png?raw=true)

<br />

## ✅ Manual Build

> Download the code 

```bash
$ git clone git@github.com:AIListMaster/TrueCount.git
$ cd TrueCount
```

<br />

### 👉 Set Up for `Unix`, `MacOS` 

> Install modules via `VENV`  

```bash
$ virtualenv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```

<br />

> Set Up Flask Environment

```bash
$ export FLASK_APP=run.py
$ export FLASK_ENV=development
```

<br />

> Start the app

```bash
$ flask run
```

At this point, the app runs at `http://127.0.0.1:5000/`.