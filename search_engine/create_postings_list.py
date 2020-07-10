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

    # delete this document from postings list:
    terms_that_must_be_pop_from_postings = []
    for t in POSTINGS_LIST.keys():
        if POSTINGS_LIST[t].get(doc_title):
            POSTINGS_LIST[t].pop(doc_title)

            if POSTINGS_LIST[t] == {}:
                terms_that_must_be_pop_from_postings.append(t)

    for t in terms_that_must_be_pop_from_postings:
        POSTINGS_LIST.pop(t)

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

def delete_postings_list_on_this_doc(postings_path, doc_title):
    with open(f'{postings_path}/POSTINGS_LIST.dat', "rb") as f:
        POSTINGS_LIST = pickle.load(f)
    
    # delete this document from postings list:
    terms_that_must_be_pop_from_postings = []
    for t in POSTINGS_LIST.keys():
        if POSTINGS_LIST[t].get(doc_title):
            POSTINGS_LIST[t].pop(doc_title)

            if POSTINGS_LIST[t] == {}:
                terms_that_must_be_pop_from_postings.append(t) 

    for t in terms_that_must_be_pop_from_postings:
        POSTINGS_LIST.pop(t)
    
    # Write POSTINGS_LIST into database:
    with open(f'{postings_path}/POSTINGS_LIST.txt', "w", encoding="UTF-8") as f:
        json.dump(POSTINGS_LIST, f)
    
    with open(f'{postings_path}/POSTINGS_LIST.dat', "wb") as f:
        pickle.dump(POSTINGS_LIST, f)