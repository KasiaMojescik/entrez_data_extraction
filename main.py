import pandas as pd
import os.path
from entrezService import EntrezSearchService
from Bio import Medline
from datetime import datetime


def main(db, retstart, retmax, totalRecords, query, email, fileName):
    print("Start time: ", datetime.now())
    entrez_service = EntrezSearchService(db)
    rec_id_list = entrez_service.perform_esearch(retstart, retmax, totalRecords, query, email)
    records = []
    cleaned_records = []
    missing_abstracts = 0
    for search in rec_id_list:
        rec = entrez_service.fetch_rec(search)
        records.extend(list(Medline.parse(rec)))
    for article in records:
        if 'AB' in article:
            keys_values = article.items()
            casted_article = {str(key): str(value) for key, value in keys_values}
            cleaned_records.append(casted_article)
        else:
            missing_abstracts += 1

    print("Extraction end time: ", datetime.now())
    print("missing abstracts: ", missing_abstracts)
    print("Creating dataframe start: ", datetime.now())
    df = pd.DataFrame(cleaned_records)
    print("DF creation end time: ", datetime.now())
    my_path = os.path.abspath(os.path.dirname(__file__))
    print("Extracting to csv")
    path = os.path.join(my_path, "data\\" + fileName + ".csv")
    df.to_csv(path)
    print("Extraction to csv time: ", datetime.now())

if __name__ == '__main__':
    main("pubmed", 0, 10, 100, "neuroscience", "your_email", "dataNLP")
    # globals()[sys.argv[1]](sys.argv[2])(sys.argv[3])(sys.argv[4])(sys.argv[5])(sys.argv[6])(sys.argv[7])