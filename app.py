from flask import Flask,render_template,request
import os
from utils import pipeline_model

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("main.html")


@app.route('/about')
def about():
    return render_template("about.html")
@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        print("Request files keys:", request.files.keys())  
        print("Request form keys:", request.form.keys())  

        img = request.files.get('image')
        if img is None or img.filename == '':
            return "No image uploaded. Please select a file.", 400

        filename = img.filename
        path = os.path.join('static/uploads', filename)
        os.makedirs(os.path.dirname(path), exist_ok=True) 
        img.save(path)

        print("Uploaded file:", filename)

        predictions = pipeline_model(path)
        print("Predictions:", predictions) 

        return render_template("predict.html", p="uploads/{}".format(filename), pred=predictions)

    return render_template("predict.html",  pred="")


if __name__ == '__main__':
    app.run(port=5000,debug=True)



