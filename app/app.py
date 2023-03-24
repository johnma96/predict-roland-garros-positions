from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/other')
def other():
    return render_template('other.html')

@app.route('/select_option', methods=['POST'])
def select_option():
    option = request.form['option']
    if option == 'option1':
        return redirect(url_for('option1'))
    elif option == 'option2':
        return redirect(url_for('option2'))
    elif option == 'option3':
        return redirect(url_for('option3'))

@app.route('/option1')
def option1():
    return render_template('option1.html')

@app.route('/option2')
def option2():
    return render_template('option2.html')

@app.route('/option3')
def option3():
    return render_template('option3.html')


if __name__ == '__main__':
    app.run(debug=True, port=5004)


"""
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/other')
def other():
    return render_template('other.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
"""
"""

from flask import Flask, render_template
# from .utils.absolute_paths import AbsPaths


app = Flask(__name__)
app.config["SECRET_KEY"] = "you-will-never-guess"


@app.route("/", methods=["GET", "POST"])
def home():
    # index_file = AbsPaths().get_abs_path_file(file_name='index.html')
    index_file = 'inihome.html'
    return render_template(index_file)

@app.route("/", methods=["GET", "POST"])
def index():
    # index_file = AbsPaths().get_abs_path_file(file_name='index.html')
    index_file = 'index.html'
    return render_template(index_file)

# @app.route("/classification_report", methods=["GET", "POST"])
# def index():
#     index_file = 'index.html'
#     with open('C:\\Users\\johnm\\Desktop\\predict-roland-garros-positions\\reports\\plain-text\\evaluation.txt', 'r') as fp:
#         return render_template(index_file, text=fp.read())

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
    
"""