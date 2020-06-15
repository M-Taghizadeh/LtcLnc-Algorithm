import os
from flask import flash, redirect, render_template, request, url_for
from . import app
from .search_engine_core import ltc_lnc

@app.route("/", methods=["GET"])
def index():
    # Loading all documents
    path = "database/"
    documents = [f for f in os.listdir(path) if f.endswith('.txt')]
    
    query = request.args.get("query")
    if query:
        # Core of Search Engine:
        top_k_docs = ltc_lnc(query, path, 5)
        return render_template("index.html", top_k_docs=top_k_docs, documents=documents)

    return render_template("index.html", documents=documents)


@app.route("/add_document/", methods=["GET", "POST"])
def add_doc():
    if request.method == "POST":
        # saving document in database as txt file:
        doc_title = request.form.get("doc_title") + ".txt"
        document = request.form.get("document")

        if document != "":
            f = open(f'database/{doc_title}', "w", encoding="utf-8")
            f.write(document)
            f.close()
        else:
            flash("متن داکیومنت را بنویسید")
            return render_template("add_doc.html")
            
        return redirect(url_for("index"))
    else:
        return render_template("add_doc.html")


@app.route("/edit_document/<string:doc_title>/")
def edit_doc(doc_title):
    f = open(f'database/{doc_title}', "r", encoding="utf-8")
    document = str(f.read())
    f.close()
    doc_title = doc_title[:-4]
    return render_template("add_doc.html", document=document, doc_title=doc_title)


@app.route("/delete_document/<string:doc_title>/")
def delete_doc(doc_title):
    # delete file with os lib
    os.remove(f'database/{doc_title}')
    # reload home page
    return redirect(url_for("index"))
