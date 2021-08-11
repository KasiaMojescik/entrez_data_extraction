from Bio import Entrez, Medline




class EntrezSearchService:

    def __init__(self, db):
        self.db = db

    def append_data(self, search, retstart, retmax, final):
        handle = Entrez.read(search)
        web_env = handle['WebEnv']
        print("WebEnv: ", web_env)
        retstart += retmax
        try:
            final.append(handle['IdList'])
        except Exception as e:
            raise IOError(str(e))
        finally:
            search.close()
        return final, web_env, retstart

    def perform_esearch(self, retstart, retmax, totalRecords, query, email):
        Entrez.email = email
        final = []
        search = Entrez.esearch(db=self.db, retstart=retstart, retmax=retmax, term=query, usehistory='y')
        first_search = self.append_data(search, retstart, retmax, final)
        final = first_search[0]
        web_env = first_search[1]
        retstart = first_search[2]
        while retstart < totalRecords:
            search = Entrez.esearch(db=self.db, retstart=retstart, retmax=retmax, term=query, web_env=web_env,
                                    usehistory='y')
            data = self.append_data(search, retstart, retmax, final)
            final = data[0]
            retstart = data[2]

        print("Finished searching. Roughly the number of ids extracted : ", len(final)*len(final[0]))
        return final

    def fetch_rec(self, rec_id):
        fetch_handle = Entrez.efetch(db=self.db, id=rec_id,
                                     rettype='Medline', retmode='json')
        rec = fetch_handle
        return rec

