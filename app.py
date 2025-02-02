from flask import Flask, request, redirect, url_for

from flask import render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        age = request.form['age']
        experience = request.form['experience']
        credit_score = request.form['creditScore']
        income = request.form['income']
        marital_status = request.form['maritalStatus']

        # Redirect to the result page with the form data
        return redirect(url_for('result', name=name, age=age, experience=experience, credit_score=credit_score, income=income, marital_status=marital_status))

    # Render the form page for GET requests
    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html')
@app.route('/results')
def results():
    return render_template('results.html')


if __name__ == '__main__':
    app.run(debug=True)
