import os
import math

def ltc_lnc(query, docs_path, k):

    # Step 1: Tokenize query terms and remove extera space and strip query
    query = str(query)
    query = query.replace("  ", " ")
    query = query.strip()
    query_terms = query.split(" ") # space is splitter

    # Step2: Read all docs and save all doc title in documents
    documents = [f for f in os.listdir(docs_path) if f.endswith('.txt')]

    # Step3: Create Postings list for query terms and calculate N: number of documents and create set of query terms
    Postings_list = {}
    N = len(documents)
    Postings_list["N"] = N
    set_of_query_term = []
    
    # Step3-A: Calculate [tf] for query term in [Query] 
    for term in query_terms:

        if Postings_list.get(term):
            Postings_list[term]["query"]["tf"] += 1
        else:
            Postings_list[term] = {}
            Postings_list[term]["query"] = {}
            Postings_list[term]["query"]["tf"] = 1
            set_of_query_term.append(term)
    
    # Step3-B: Calculate [tf] for query term in [all Documents]
    for term in query_terms:
        Postings_list[term]["document"] = {}
        for doc_title in documents:
            f = open(docs_path+doc_title, "r", encoding="UTF-8")
            document_terms = str(f.read()).split(" ")
            f.close()

            # befor anythings:
            Postings_list[term]["document"][doc_title] = {}
            Postings_list[term]["document"][doc_title]["tf"] = 0
            # after:
            for doc_term in document_terms:
                if term == doc_term:
                    try:
                        Postings_list[term]['document'][doc_title]["tf"] += 1
                    except:
                        try:
                            Postings_list[term]["document"][doc_title] = {}
                            Postings_list[term]["document"][doc_title]["tf"] = 1
                        except:
                            Postings_list[term]["document"][doc_title]["tf"] = 1


    # Step3-C: Calculate [tf_wt] for query term in [Query and all Documents]
    for term in query_terms:
        tf_query = Postings_list[term]["query"]["tf"]
        Postings_list[term]["query"]["tf_wt"] = 1 + math.log10(tf_query)

        try:
            for doc_title in Postings_list.get(term).get("document"):
                tf_document = Postings_list[term]["document"][doc_title]["tf"]
                if tf_document == 0:
                    Postings_list[term]["document"][doc_title]["tf_wt"] = 0
                else:
                    Postings_list[term]["document"][doc_title]["tf_wt"] = 1 + math.log10(tf_document)
        except: print("error")

    # Step3-D: Calculate [df, idf, wt] for query term in [Query] => idf = log10(N/df), wt = tf_wt * idf
    for term in query_terms:
        df = 0
        for docs in Postings_list[term]["document"]:
            if Postings_list[term]["document"][docs]["tf"] > 0:
                df += 1

        Postings_list[term]["query"]["df"] = df
        if df == 0:
            Postings_list[term]["query"]["idf"] = 0
        else:
            Postings_list[term]["query"]["idf"] = math.log10(N/df)
        
        Postings_list[term]["query"]["wt"] = Postings_list[term]["query"]["tf_wt"] * Postings_list[term]["query"]["idf"]

    # Step3-E: Calculate [wt] for query term in [all Documents] => idf = 1, wt = tf_wt * idf(==1)
    for term in query_terms:
        for doc_title in documents:
            Postings_list[term]["document"][doc_title]["wt"] = Postings_list[term]["document"][doc_title]["tf_wt"]

    # End of Calculate Postings_list
    print("------------------------------")    
    print("Postings_list: ", Postings_list)
    print("------------------------------")

    # Step4: Normalization of Query and goto vector space for [wt]:
    # Step4-A: calculate sum of wt for Query
    query_vector_normal = []
    sum = 0
    for term in set_of_query_term:
        sum += math.pow(Postings_list[term]["query"]["wt"], 2)
    sum = math.sqrt(sum)
    print("sum of wt for Query: ", sum)

    # Step4-B: calculate query_vector_normal with sum of wt 
    for term in set_of_query_term:
        wt = Postings_list[term]["query"]["wt"]
        if sum != 0:
            query_vector_normal.append(wt / sum)
        else:
            query_vector_normal.append(0)
    print("\n\nquery_vector_normal: ", query_vector_normal, "\n\n")

    # Step5: Normalization of all Documents and goto vector space for [wt] and save that in docs_vector_normal(as a dict)
    docs_vector_normal = {}
    for doc_title in documents:
        docs_vector_normal[doc_title] = []

        # Step5-A: calculate sum of wt for any Document
        sum = 0
        for term in set_of_query_term:
            sum += math.pow(Postings_list[term]["document"][doc_title]["wt"], 2)
        sum = math.sqrt(sum)
        print("sum_wt: ", sum, " doc title: ", doc_title)
        
        # Step5-B: calculate docs_vector_normal[doc_title] with sum of wt for any document
        for term in set_of_query_term:
            wt = Postings_list[term]["document"][doc_title]["wt"]
            if sum != 0:
                docs_vector_normal[doc_title].append(wt / sum)
            else:
                docs_vector_normal[doc_title].append(0)
    
    print("\n\ndocs_vector_normal: ", docs_vector_normal, "\n\n")

    # Step6: Cosine Similarity => Score list 
    # Spte6-A: Dot Product between Query vector normal and any Documents vector normal and save that in Score list[]
    Scores_list = []
    for doc_title in docs_vector_normal:
        doc_vector = docs_vector_normal[doc_title]
        score = 0
        for i in range(0, len(doc_vector)):
            score += doc_vector[i] * query_vector_normal[i]
        Scores_list.append([doc_title, score])
    print("Scores_list: ", Scores_list)

    # Step7: Sorting Scores_list and get top k doc (get rankings)
    min = 0
    for i in range(0, len(Scores_list)):
        for j in range(0, len(Scores_list)-i-1):
            if Scores_list[j][1] < Scores_list[j+1][1]:
                tmp_Scores_list = Scores_list[j]
                Scores_list[j] = Scores_list[j+1]
                Scores_list[j+1] = tmp_Scores_list
    print("\n\nSorted Scores_list: ", Scores_list, "\n\n")

    # Step8: TODO get k record from Sorted Score List 

    return Scores_list  


#####################################################
# Postings_list Structure:
# Postings_list = {
#         N : 100,
#         term1: {
#             query:{
#                 tf:1,
#                 tf_wt:1,
#                 df:1,
#                 idf:1,
#                 wt:1,
#                 normal:1
#             }
#             document:{
#                 doc_title1:{
#                     tf:1,
#                     tf_wt:1,
#                     wt:1,
#                     normal:1
#                 }
#                 doc_title2:{
#                     tf:1,
#                     tf_wt:1,
#                     wt:1,
#                     normal:1
#                 }
#                 .
#                 .
#                 .
#             }
#         }
#         term1: {
#             query:{
#                 tf:1,
#                 tf_wt:1,
#                 df:1,
#                 idf:1,
#                 wt:1,
#                 normal:1
#             }
#             document:{
#                 doc_title1:{
#                     tf:1,
#                     tf_wt:1,
#                     wt:1,
#                     normal:1
#                 }
#                 doc_title2:{
#                     tf:1,
#                     tf_wt:1,
#                     wt:1,
#                     normal:1
#                 }
#                 .
#                 .
#                 .
#             }
#         }
#         .
#         .
#         .
#     }

# Scores_list Structure:
# Scores_list = [
#     ["doc_title1", 1.00],
#     ["doc_title2", 0.50],
#     ["doc_title3", 0.25],
#     .
#     .
#     .
# ]