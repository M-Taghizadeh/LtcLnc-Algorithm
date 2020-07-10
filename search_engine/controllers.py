import os
from flask import flash, redirect, render_template, request, url_for
from . import app
from .create_postings_list import create_postings_list_on_all_docs, update_postings_list_on_this_doc, delete_postings_list_on_this_doc
from .search_engine_core import ltc_lnc

# database directories:
postings_path = "Postings_lists/"
docs_path = "database/"

@app.route("/", methods=["GET"])
def index():
    # Loading all documents
    documents = [f for f in os.listdir(docs_path) if f.endswith('.txt')]
    
    # get user query
    query = request.args.get("q")
    if query:
        # Core of Search Engine:
        top_k_docs = ltc_lnc(query, postings_path, docs_path, 10) # you can set k (top k documents)
        return render_template("index.html", top_k_docs=top_k_docs, documents=documents)

    return render_template("index.html", documents=documents)


@app.route("/add_document/", methods=["GET", "POST"])
def add_doc():
    if request.method == "POST":
        # saving document in database as txt file:
        doc_title = request.form.get("doc_title") + ".txt"
        document = request.form.get("document")

        if document != "":
            f = open(f'{docs_path}{doc_title}', "w", encoding="utf-8")
            f.write(document)
            f.close()

            # Create postings_list for all documents
            if os.path.exists(f'{postings_path}POSTINGS_LIST.dat'):
                update_postings_list_on_this_doc(postings_path, docs_path, doc_title)
            else:
                create_postings_list_on_all_docs(postings_path, docs_path)

        else:
            flash("متن داکیومنت را بنویسید")
            return render_template("add_doc.html")
            
        return redirect(url_for("index"))
    else:
        return render_template("add_doc.html")


@app.route("/edit_document/<string:doc_title>/")
def edit_doc(doc_title):
    f = open(f'{docs_path}{doc_title}', "r", encoding="utf-8")
    document = str(f.read())
    f.close()
    doc_title = doc_title[:-4]
    return render_template("add_doc.html", document=document, doc_title=doc_title)


@app.route("/delete_document/<string:doc_title>/")
def delete_doc(doc_title):
    
    # update POSTINGS_LIST
    delete_postings_list_on_this_doc(postings_path, doc_title)

    # delete file with os lib
    os.remove(f'{docs_path}{doc_title}')

    # reload home page
    return redirect(url_for("index"))


@app.route("/create_postings_list/")
def create_postings_list_route():
    # Create postings_list for all documents
    create_postings_list_on_all_docs(postings_path, docs_path)
    return redirect(url_for("index"))