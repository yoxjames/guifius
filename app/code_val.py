from db import Database

class CODE_DB(Database):
    def get_id_val(self, class_val, name):
        raw =  self.query_db('select * from type_val where class = ? and name = ?',
                  [class_val,name],one=True)
        return raw['id_val']

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
            
        results = self.query_db('select name from type_val where class = ?',
                [class_val], one=False)
        for r in results:
            resultant[r['name']] = 'desc' #Placeholder for query

        return resultant



    def cache_class(self, class_val, name):
        return self.query_class_full(class_val)

    def cache_class_client(self, class_val, name):
        return \
        {
            name : self.query_class_client(class_val)
        }
        
        

class NET_TYPE(CODE_DB):
    def __init__(self):
        self.CLASS = 4
        self.NAME = "NET_TYPE"

        self.FREE = self.get_id_val("FREE")
        self.CORPORATE = self.get_id_val("CORPORATE")
        self.UNKNOWN = self.get_id_val("UNKNOWN")


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

        self.FUN = self.get_id_val("FUN")
        self.PLANNED = self.get_id_val("PLANNED")
        self.IN_PROGRESS = self.get_id_val("IN_PROGRESS")
        self.ONLINE = self.get_id_val("ONLINE")

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

        self.HORIZONTAL = self.get_id_val("HORIZONTAL")
        self.VERTICAL = self.get_id_val("VERTICAL")
        self.UNKNOWN = self.get_id_val("UNKNOWN")

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

        self.UNKNOWN = self.get_id_val("UNKNOWN")

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

        self.A_NETWORK_B_PERSON = self.get_id_val("A_NETWORK_B_PERSON")
        self.A_NETWORK_B_DEVICE = self.get_id_val("A_NETWORK_B_DEVICE")

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

        self.POLYGON = self.get_id_val("POLYGON")

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

        self.UNKNOWN = self.get_id_val("UNKNOWN")

    def get_id_val(self,name):
        return super(CONNECTION_TYPE,self).get_id_val(self.CLASS,name)

    def query_class(self):
        return super(CONNECTION_TYPE,self).query_class_client(self.CLASS)

    def cache_class(self):
        return super(CONNECTION_TYPE, self).cache_class(self.CLASS,self.NAME)


                



class CODE_CLASS:
    def __init__(self):
        self.NET_PHASE_TYPE = NET_PHASE_TYPE()
        self.NET_TYPE = NET_TYPE()
        self.RELATION = RELATION()
        self.OBJECT_TYPE = OBJECT_TYPE()
        self.NODE_TYPE = NODE_TYPE()
        self.POLARIZATION_TYPE = POLARIZATION_TYPE()
        self.CONNECTION_TYPE = CONNECTION_TYPE()

        self.INTERNAL_CACHE = self.recache_all()
        self.EXTERNAL_CACHE = self.recache_all_client()

        self.FUNC = CODE_DB()


    def recache_all_client(self):
        return \
        {
            self.NET_PHASE_TYPE.NAME : self.NET_PHASE_TYPE.query_class(),
            self.NET_TYPE.NAME : self.NET_TYPE.query_class(),
            self.RELATION.NAME : self.RELATION.query_class(),
            self.OBJECT_TYPE.NAME : self.OBJECT_TYPE.query_class(),
            self.NODE_TYPE.NAME : self.NODE_TYPE.query_class(),
            self.POLARIZATION_TYPE.NAME : self.POLARIZATION_TYPE.query_class(),
            self.CONNECTION_TYPE.NAME : self.CONNECTION_TYPE.query_class()
        }

    def recache_all(self):
        return \
        {
            self.NET_PHASE_TYPE.NAME : self.NET_PHASE_TYPE.cache_class(),
            self.NET_TYPE.NAME : self.NET_TYPE.cache_class(),
            self.RELATION.NAME : self.RELATION.cache_class(),
            self.OBJECT_TYPE.NAME : self.OBJECT_TYPE.cache_class(),
            self.NODE_TYPE.NAME : self.NODE_TYPE.cache_class(),
            self.POLARIZATION_TYPE.NAME : self.POLARIZATION_TYPE.cache_class(),
            self.CONNECTION_TYPE.NAME : self.CONNECTION_TYPE.cache_class()
        }
