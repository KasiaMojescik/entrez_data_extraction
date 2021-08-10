import sys
from io import StringIO
import pandas as pd
import os.path
from entrezService import EntrezSearchService
from Bio import Medline


def main(db, retstart, retmax, totalRecords, query, email, fileName):
    entrez_service = EntrezSearchService(db)
    rec_id_list = entrez_service.search_medline(retstart, retmax, totalRecords, query, email)
    final_rec_list = {}
    i = 0
    for rec_id in rec_id_list:
        rec = entrez_service.fetch_rec(rec_id)
        rec_file = StringIO(rec.decode("utf-8"))
        medline_rec = Medline.read(rec_file)
        if 'AB' in medline_rec:
            print(i, rec_id)
            keys_values = medline_rec.items()
            medline_rec = {str(key): str(value) for key, value in keys_values}
            final_rec_list[i] = medline_rec
            i = i + 1
        else:
            print(i + " doesn't have abstract")

    print("Creating dataframe")
    df = pd.DataFrame.from_dict(final_rec_list, orient='index')
    my_path = os.path.abspath(os.path.dirname(__file__))
    print("Extracting to csv")
    path = os.path.join(my_path, "data\\" + fileName + ".csv")
    df.to_csv(path)


if __name__ == '__main__':
    # main("pmc", 0, 10, 10, "neuroscience", "your_email", "dataNLP")
    globals()[sys.argv[1]](sys.argv[2])(sys.argv[3])(sys.argv[4])(sys.argv[5])(sys.argv[6])(sys.argv[7])