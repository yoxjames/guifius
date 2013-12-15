from db import Database
class CODE_DB(Database):
    ## DEPRICATED
    # There should be no reason to use this function
    # when the cache can be used.
    def get_id_val(self, class_val, name):
        raw =  self.query_db('select * from type_val where class = ? and name = ?',
                  [class_val,name],one=True)
        return raw['id_val']

    ## DEPRICATED
    # There should be no reason to use this function
    # when the cache can be used.
    def get_name_val(self, id_val):
        raw = self.query_db('select * from type_val where id_val = ?',
                [id_val],one=True)
        return raw['name']

    def query_class_full(self, class_val):
        resultant = {}
        results = self.query_db('select name,id_val from type_val where class = ?',
                [class_val], one=False)
        for r in results:
            resultant[r['name']] = r['id_val']
        return resultant
    
    def query_class_client(self, class_val):
        resultant = {}
            
        results = self.query_db('select name,description from type_val where class = ?',
                [class_val], one=False)
        for r in results:
            resultant[r['name']] = r['description'] 

        return resultant

    def cache_vals(self):
        vals = []
        results = self.query_db('select id_val,name from type_val order by id_val',[],one=False)

        for r in results:
            vals.append(r['name'])

        return vals
            



    def cache_class(self, class_val, name):
        return self.query_class_full(class_val)

    def cache_class_client(self, class_val, name):
        return \
        {
            name : self.query_class_client(class_val)
        }
        
        
'''
class NET_TYPE(CODE_DB):
    def __init__(self):
        self.CLASS = 4
        self.NAME = "NET_TYPE"

    def get_id_val(self,name):
        return super(NET_TYPE, self).get_id_val(self.CLASS, name)

    def query_class(self):
        return super(NET_TYPE, self).query_class_client(self.CLASS)

    def cache_class(self):
        return super(NET_TYPE, self).cache_class(self.CLASS,self.NAME)
        


class NET_PHASE_TYPE(CODE_DB):
    def __init__(self):
        self.CLASS = 1
        self.NAME = "NET_PHASE_TYPE"

    def get_id_val(self,name):
        return super(NET_PHASE_TYPE,self).get_id_val(self.CLASS,name)

    def query_class(self):
        return super(NET_PHASE_TYPE, self).query_class_client(self.CLASS)

    def cache_class(self):
        return super(NET_PHASE_TYPE, self).cache_class(self.CLASS,self.NAME)

class POLARIZATION_TYPE(CODE_DB):
    def __init__(self):
        self.CLASS = 5
        self.NAME = "POLARIZATION_TYPE"

    def get_id_val(self,name):
        return super(POLARIZATION_TYPE,self).get_id_val(self.CLASS,name)

    def query_class(self):
        return super(POLARIZATION_TYPE,self).query_class_client(self.CLASS)

    def cache_class(self):
        return super(POLARIZATION_TYPE, self).cache_class(self.CLASS,self.NAME)

class NODE_TYPE(CODE_DB):
    def __init__(self):
        self.CLASS = 6
        self.NAME = "NODE_TYPE"

    def get_id_val(self,name):
        return super(NODE_TYPE,self).get_id_val(self.CLASS,name)

    def query_class(self):
        return super(NODE_TYPE,self).query_class_client(self.CLASS)

    def cache_class(self):
        return super(NODE_TYPE, self).cache_class(self.CLASS,self.NAME)

    
class RELATION(CODE_DB):
    def __init__(self):
        self.CLASS = 2
        self.NAME = "RELATION"

    def get_id_val(self,name):
        return super(RELATION,self).get_id_val(self.CLASS,name)


    def query_class(self):
        return super(RELATION, self).query_class_client(self.CLASS)
    
    def cache_class(self):
        return super(RELATION, self).cache_class(self.CLASS,self.NAME)


class OBJECT_TYPE(CODE_DB):
    def __init__(self):
        self.CLASS = 3
        self.NAME = "OBJECT_TYPE"

    def get_id_val(self,name):
        return super(OBJECT_TYPE,self).get_id_val(self.CLASS,name)

    def query_class(self):
        return super(OBJECT_TYPE, self).query_class_client(self.CLASS)

    def cache_class(self):
        return super(OBJECT_TYPE, self).cache_class(self.CLASS,self.NAME)


class CONNECTION_TYPE(CODE_DB):
    def __init__(self):
        self.CLASS = 7
        self.NAME = "CONNECTION_TYPE"

    def get_id_val(self,name):
        return super(CONNECTION_TYPE,self).get_id_val(self.CLASS,name)

    def query_class(self):
        return super(CONNECTION_TYPE,self).query_class_client(self.CLASS)

    def cache_class(self):
        return super(CONNECTION_TYPE, self).cache_class(self.CLASS,self.NAME)
'''
class CODE_DB(Database):

    ## DEPRICATED
    # There should be no reason to use this function
    # when the cache can be used.
    def get_id_val(self, class_name, name):
        raw =  self.query_db('select * from type_val where class = ? and name = ?',
                  [class_name,name],one=True)
        return raw['id_val']

    ## DEPRICATED
    # There should be no reason to use this function
    # when the cache can be used.
    def get_name_val(self, id_val):
        raw = self.query_db('select * from type_val where id_val = ?',
                [id_val],one=True)
        return raw['name']

    def query_class_full(self):
        resultant = {}
        results = self.query_db('select distinct class_name from type_val',[],one=False)
        
        for r in results:
            resultant[r['class_name']] = self.query_class_full_r(r['class_name'])
        return resultant
    
    def query_class_full_r(self, class_name):
        resultant = {}
        results = self.query_db('select name,id_val from type_val where class_name = ?',
                [class_name], one=False)
        for r in results:
            resultant[r['name']] = r['id_val']
        return resultant
    
    def query_class_client(self):
        resultant = {}
        results = self.query_db(
                'select distinct class_name from type_val',
                [],
                one=False)
        for r in results:
            resultant[r['class_name']] = self.query_class_client_r(r['class_name'])

        return resultant

    def query_class_client_r(self, class_name):
        resultant = {}
            
        results = self.query_db('select name,description from type_val where class_name = ?',
                [class_name], one=False)
        for r in results:
            resultant[r['name']] = r['description'] 

        return resultant

    def cache_vals(self):
        vals = {}
        results = self.query_db('select id_val,name from type_val order by id_val',[],one=False)

        for r in results:
            vals[r['id_val']] = r['name']

        return vals
            



    def cache_class(self, class_val, name):
        return self.query_class_full(class_val)

    def cache_class_client(self, class_val, name):
        return \
        {
            name : self.query_class_client(class_val)
        }
        
        


class CODE_CLASS(CODE_DB):

    def __init__(self):

        print "Initting"

        self.I = self.query_class_full()
        self.E = self.query_class_client()
        self.VAL = self.cache_vals()

        print self.query_class_full()

    def get_id_val(self, class_name, value):
        return self.I[class_name][value]

    def get_name_val(self, id_val):
        return self.VAL[id_val]




