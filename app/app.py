from flask import Flask, render_template
# from .utils.absolute_paths import AbsPaths


app = Flask(__name__)
app.config["SECRET_KEY"] = "you-will-never-guess"

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
    app.run(debug=True, port=5006, host="0.0.0.0")