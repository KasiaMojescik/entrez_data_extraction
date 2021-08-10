from Bio import Entrez




class EntrezSearchService:

    def __init__(self, db):
        self.db = db

    def search_medline(self, retstart, retmax, totalRecords, query, email):
        Entrez.email = email
        final = []
        while (retstart < totalRecords):
            search = Entrez.esearch(db=self.db, retstart=retstart, retmax=retmax, term=query, usehistory='y')
            handle = Entrez.read(search)
            retstart += retmax
            try:
                final += handle['IdList']
            except Exception as e:
                raise IOError(str(e))
            finally:
                search.close()
        print("Finished searching " + self.db + " for all ids. Number of ids retrieved: ", len(final))
        return final

    def fetch_rec(self, rec_id):
        fetch_handle = Entrez.efetch(db=self.db, id=rec_id,
                                     rettype='Medline', retmode='json')
        rec = fetch_handle.read()
        return rec

