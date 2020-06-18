import os
import json
import pickle

def create_postings_list_on_all_docs(postings_path, docs_path):
    documents = [f for f in os.listdir(docs_path) if f.endswith('.txt')]
    POSTINGS_LIST = {}

    for doc_title in documents:
        f = open(docs_path+doc_title, "r", encoding="UTF-8")
        document_terms = str(f.read()).split(" ")
        f.close()

        for doc_term in document_terms:
            if not POSTINGS_LIST.get(doc_term):
                POSTINGS_LIST[doc_term] = {}
            if not POSTINGS_LIST.get(doc_term).get(doc_title):
                POSTINGS_LIST[doc_term][doc_title] = 1
            else:
                POSTINGS_LIST[doc_term][doc_title] += 1
    
    # Write POSTINGS_LIST into database:
    with open(f'{postings_path}/POSTINGS_LIST.txt', "w", encoding="UTF-8") as f:
        json.dump(POSTINGS_LIST, f)
    
    with open(f'{postings_path}/POSTINGS_LIST.dat', "wb") as f:
        pickle.dump(POSTINGS_LIST, f)


def update_postings_list_on_this_doc(postings_path, docs_path, doc_title):
    f = open(docs_path + doc_title, "r", encoding="UTF-8")
    document_terms = str(f.read()).split(" ")
    f.close()

    with open(f'{postings_path}/POSTINGS_LIST.dat', "rb") as f:
        POSTINGS_LIST = pickle.load(f)

    repetition_in_this_doc = 0
    for doc_term in document_terms:
        if not POSTINGS_LIST.get(doc_term):
            POSTINGS_LIST[doc_term] = {}
        else:
            POSTINGS_LIST[doc_term] = 0

        if not POSTINGS_LIST.get(doc_term).get(doc_title):
            POSTINGS_LIST[doc_term][doc_title] = 1
        else:
            POSTINGS_LIST[doc_term][doc_title] += 1
    
    # Write POSTINGS_LIST into database:
    with open(f'{postings_path}/POSTINGS_LIST.txt', "w", encoding="UTF-8") as f:
        json.dump(POSTINGS_LIST, f)
    
    with open(f'{postings_path}/POSTINGS_LIST.dat', "wb") as f:
        pickle.dump(POSTINGS_LIST, f)