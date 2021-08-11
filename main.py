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
    print("Fetching start time: ", datetime.now())
    for search in rec_id_list:
        rec = entrez_service.fetch_rec(search)
        try:
            records.extend(list(Medline.parse(rec)))
        except:
            print("Exception thrown at medline parsing")

    print("Fetching end time: ", datetime.now())
    print("Article appending start time: ", datetime.now())
    for article in records:
        # decode("utf-8")
        if 'AB' in article:
            keys_values = article.items()
            casted_article = {str(key): str(value) for key, value in keys_values}
            cleaned_records.append(casted_article)
        elif 'AB'.encode('utf-8') in article:
            keys_values = article.items()
            casted_article = {}
            for key, value in keys_values:
                if isinstance(value, list):
                    casted_article.update({key.decode("utf-8"): [x.decode('utf-8') for x in value]})
                else:
                    casted_article.update({key.decode("utf-8"): value.decode("utf-8")})
            cleaned_records.append(casted_article)
        else:
            missing_abstracts += 1
    print("Article appending end time: ", datetime.now())

    print("Extraction end time: ", datetime.now())
    print("missing abstracts: ", missing_abstracts)
    print("Creating dataframe start: ", datetime.now())
    df = pd.DataFrame(cleaned_records)
    print("DF creation end time: ", datetime.now())
    my_path = os.path.abspath(os.path.dirname(__file__))
    print("Extracting to csv start: ", datetime.now())
    path = os.path.join(my_path, "data\\" + fileName + ".csv")
    df.to_csv(path)
    print("Extraction to csv time: ", datetime.now())

if __name__ == '__main__':
    main("pmc", 0, 10000, 100000, "neuroscience", "your_email", "dataNLP")
    # globals()[sys.argv[1]](sys.argv[2])(sys.argv[3])(sys.argv[4])(sys.argv[5])(sys.argv[6])(sys.argv[7])