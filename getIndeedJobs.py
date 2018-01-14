from indeed import IndeedClient
import pandas as pd

class indeed:   
    
    #jobDataFrame 
    
    def __init__(self):
#        self.jobDataFrame= pd.DataFrame();
        self.client = IndeedClient(8836246992678581);
        
    def skill(self,l,city,jobtype):
        #print l
        #print " AND ".join(l)
        print (jobtype)
        if jobtype in ['intern','internship','Internship']:
            jobtype = 'internship'
        else:
            jobtype = 'fulltime'
        params = {
            'q' : " AND ".join(l),
            'l' : city,
            'jt' : jobtype,
            'userip' : "1.2.3.4",
            'useragent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)",
            'limit' : "25",
            'start' : 0,
            'highlight' : 1
          
        }
        i = 25
        search_response = self.client.search(**params)
        results = []
        if (len(search_response['results']) <= 0):
            return results
            
        
        while(i<100 and i<search_response['totalResults']):        
            results += search_response['results']
            params['start'] += 25
            search_response = self.client.search(**params)
            results += search_response['results']
            i+=25
            print (params['start'])
        
        self.jobDataFrame = pd.DataFrame(results).drop_duplicates('jobkey')
        self.jobDataFrame.to_csv("sample.csv",encoding='UTF-8')
        return results    

    def skillOR(self,l,city,jobtype):
        #print l
        #print " AND ".join(l)
        print (jobtype)
        if jobtype in ['intern','internship','Internship']:
            jobtype = 'internship'
        else:
            jobtype = 'fulltime'
        params = {
            'q' : " OR ".join(l),
            'l' : city,
            'jt' : jobtype,
            'userip' : "1.2.3.4",
            'useragent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)",
            'limit' : "50"
        }
        i = 25
        search_response = self.client.search(**params)
        results = []
        if (len(search_response['results']) <= 0):
            return results
            
        
        while(i<100 and i<search_response['totalResults']):        
            results += search_response['results']
            params['start'] += 25
            search_response = self.client.search(**params)
            results += search_response['results']
            i+=25
            print (params['start'])
        
        self.jobDataFrame = pd.DataFrame(results).drop_duplicates('jobkey')
        self.jobDataFrame.to_csv("sample.csv",encoding='UTF-8')
        return results