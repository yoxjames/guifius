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

class NET_TYPE(CODE_DB):
    def __init__(self):
        self.CLASS = 4

        self.FREE = self.get_id_val("FREE")
        self.CORPORATE = self.get_id_val("CORPORATE")
        self.UNKNOWN = self.get_id_val("UNKNOWN")

    def get_id_val(self,name):
        return super(NET_TYPE, self).get_id_val(self.CLASS, name)
        


class NET_PHASE_TYPE(CODE_DB):
    def __init__(self):
        self.CLASS = 1

        self.FUN = self.get_id_val("FUN")
        self.PLANNED = self.get_id_val("PLANNED")
        self.IN_PROGRESS = self.get_id_val("IN_PROGRESS")
        self.ONLINE = self.get_id_val("ONLINE")

    def get_id_val(self,name):
        return super(NET_PHASE_TYPE,self).get_id_val(self.CLASS,name)
    
class RELATION(CODE_DB):
    def __init__(self):
        self.CLASS = 2

        self.A_NETWORK_B_PERSON = self.get_id_val("A_NETWORK_B_PERSON")
        self.A_NETWORK_B_DEVICE = self.get_id_val("A_NETWORK_B_DEVICE")

    def get_id_val(self,name):
        return super(RELATION,self).get_id_val(self.CLASS,name)

class OBJECT_TYPE(CODE_DB):
    def __init__(self):
        self.CLASS = 3

        self.POLYGON = self.get_id_val("POLYGON")

    def get_id_val(self,name):
        return super(OBJECT_TYPE,self).get_id_val(self.CLASS,name)


class CODE_CLASS:
    def __init__(self):
        self.NET_PHASE_TYPE = NET_PHASE_TYPE()
        self.NET_TYPE = NET_TYPE()
        self.RELATION = RELATION()
        self.OBJECT_TYPE = OBJECT_TYPE()

        self.FUNC = CODE_DB()

