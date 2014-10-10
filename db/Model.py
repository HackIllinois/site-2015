from google.appengine.ext import ndb
from Event import Event
# import logging

class Model(ndb.Model):

    '''
    Sets even 'HackIllinois' as ancestor
    Strongly consistent, but only around one write per second

    TODO: for future models modify ancestral inheritance
    https://cloud.google.com/appengine/docs/python/ndb/queries#ancestor
    '''
    _automaticallyAddEventAsAncestor = False

    @classmethod
    def _automatically_add_event_as_ancestor(cls):
        cls._automaticallyAddEventAsAncestor = True

    @staticmethod
    def get_default_event_parent_key():
        '''
        Fetches or creates and return Hackillinois Event
        This is the workaround for the strong consistency
        '''
        q = Event.query()
        if q.count() < 1:
            event = Event(name='HackIllinois')
            return event.put()
        else:
            return q.fetch()[0].key

    def _get_required(cls):
        '''
        private method for getting a list of all required properties of a class
        
        @param cls - Model: the class model to use
        @return - List: a list of all required properties of a class
        '''
        properties = cls._properties
        required = []
        for p in properties:
            if properties[p]._required:
                required.append(p)
        return required

    @classmethod
    @ndb.transactional
    def f_add(cls, data, parent=None):
        '''
        Creates a new model and adds it to the database
        WILL NOT override data if already there
        Helper function for 'add'

        @param cls - Model: the class model to use
        @param data - Dictionary: the data to add in the datastore
        @return - Key: Key of datastore entry (can be used as a boolean to check whether or not the data was added to the database)

        ex: Attendee.f_add({'nameFirst':'John', 'nameLast':'Doe', 'email':'doe1@illinois.edu', 'year':3})
        '''

        o = cls(parent=parent)
        # logging.info("Model: f_add object is none: " + str(o == None))
        for prop in data:
            setattr(o, prop, data[prop])

        ret = o.put() #TODO: Catch possible bad value error
        # logging.info("Model: f_add put returned " + str(ret))

        return ret

    @classmethod
    def add(cls, data, search=None, parent=None):
        '''
        Creates a model and adds it to the datastore
        WILL NOT override data if already there
        WILL NOT add data if similar data is already there, determined by "search" xor model's unique_properties() attribute
        Calls upon f_add as a Helper function

        @param cls - Model: the class model to use
        @param data - Dictionary: the data to add in the datastore
        @param search - Dictionary: properties to search the datastore
        @return - Key: Key of datastore entry (can be used as a boolean to check whether or not the data was added to the database)

        Assume Attendee has a unique_property 'email'
        ex: Attendee.add({'nameFirst':'John', 'nameLast':'Doe', 'email':'doe1@illinois.edu', 'year':3})
        Returns True if "doe1@illinois.edu" is not already in the database and data is successfully added
        Returns False otherwise
        OR
        Assume Attendee does not have any unique_properties
        Attendee.add({'nameFirst':'John', 'nameLast':'Doe', 'email':'doe1@illinois.edu', 'year':3}, {'email':'doe1@illinois.edu'})
        Same result
        '''

        '''
        TODO: Rework with new parent protocol
        '''

        # logging.info("Model: Begining")
        # logging.info("Model: cls=" + str(cls))
        # logging.info("Model: data=" + str(data))
        # logging.info("Model: search=" + str(search))
        # logging.info("Model: parent=" + str(parent))


        if cls._automaticallyAddEventAsAncestor:
            parent = cls.get_default_event_parent_key()

        # logging.info("Model: before search")

        if not search:
            search = {}
            try:
                properties = cls.unique_properties()
                for p in properties:
                    search[p] = data[p]
            except AttributeError:
                # logging.info("Model: AttributeError")
                #class does not have attribute unique_properties()
                return cls.f_add(data, parent=parent)
            except LookupError:
                #data does not key "p"
                # logging.info("Model: LookupError")
                return False
        # logging.info("Model: before in database")
        if not cls.in_database(search):
            # logging.info("Model: not in database")
            return cls.f_add(data, parent=parent)
        return False

    @classmethod
    @ndb.transactional
    def update(cls, data, key):
        '''
        Updates a model in the datastore
        WILL override data if already there

        @param cls - Model: the class model to use
        @param data - Dictionary: the data to change in the database
        @param key - Key: key of model
        @return - Key: Key of datastore entry (can be used as a boolean to check whether or not the data was updated)

        ex: Attendee.update({'nameFirst':'John', 'nameLast':'Doe'}, key)
        '''
        u = key.get()
        for p in data:
            setattr(u, p, data[p])
        ret = u.put() #TODO: Catch possible errors
        return ret

    @classmethod
    def update_search(cls, data, search=None):
        '''
        Updates a model in the database
        WILL override data if already there, determined by "search" xor model's unique_properties() attribute

        @param cls - Model: the class model to use
        @param data - Dictionary: the data to change in the database
        @param search - Dictionary: the parameters to search with
        @return - Key: Key of datastore entry (can be used as a boolean to check whether or not the data was updated)

        ex: Attendee.update_search({'nameFirst':'John', 'nameLast':'Doe'}, {'email':'doe1@illinois.edu', 'year':3})
        '''
        if not search:
            search = {}
            try:
                properties = cls.unique_properties()
                for p in properties:
                    search[p] = data[p]
            except AttributeError:
                #class does not have attribute unique_properties()
                return False
            except LookupError:
                #data does not key "p"
                return False
        m = cls.search_database(search).get()
        if m != None:
            return cls.update(data, m.key)
        return False

    @classmethod
    def add_or_update(cls, data, search=None):
        '''
        Adds or updates a model in the database
        WILL override data if already there

        @param cls - Model: the class model to use
        @param data - Dictionary: the data to change in the database
        @param search - Dictionary: the parameters to search with
        @return: nothing

        ex: Attendee.update_model({'nameFirst':'John', 'nameLast':'Doe'}, {'email':'doe1@illinois.edu', 'year':3})
        '''

        if not search:
            search = {}
            try:
                properties = cls.unique_properties()
                for p in properties:
                    search[p] = data[p]
            except AttributeError:
                #class does not have attribute unique_properties()
                return False
            except LookupError:
                #data does not key "p"
                return False

        #print 'search: %s' % search

        if not cls.add(data, search):
            cls.update_search(data, search)

    @classmethod
    def delete_search(cls, search):
        '''
        deletes a model in the database

        @param cls - Model: the class model to use
        @param search - Dictionary: the parameters to search with
        @return: nothing

        ex: Attendee.delete_search({'email':'doe1@illinois.edu', 'year':3})
        '''
        #These functions need to be changed to delete all references a model ex. an Attendee in a Team
        m = cls.search_database(search).get()
        if m != None:
            cls.delete(m.key)

    @classmethod
    @ndb.transactional
    def delete(cls, key):
        '''
        deletes a model in the database

        @param cls - Model: the class model to use
        @param key - Key: key to delete
        @return: nothing

        ex: Attendee.update_model(key)
        '''
        #If the key is stored in multiple places this function need to be changed to delete all references a model ex. an Attendee in a Team
        key.delete()

    @classmethod
    def in_database(cls, search):
        '''
        Determines if the data already in the database, determined by "search"
        DOES NOT effect the database

        @param cls - Model: the class model to use
        @param search - Dictionary: the data used to search the database
        @return - Boolean: True if the data is in the database, False otherwise

        ex: Attendee.in_database({'email':'doe1@illinois.edu'})
        Returns True if "doe1@illinois.edu" is already in the database
        Returns False otherwise
        '''
        return cls.search_database(search).count(limit = 1) > 0

    @classmethod
    def search_database(cls, search=None, perfect_match=True):
        '''
        Searches the database for models matching "search"
        DOES NOT effect the database

        @param cls - Model: the class model to use
        @param search - Dictionary: the data used to search the database
        @perfect_match - Boolean: True = every argument matches : False = at least one argument matches
        #TODO: impliment perfect_match
        @return - Query: iterator of models

        ex: Attendee.search_database({'email':'doe1@illinois.edu'})
        '''
        if search is None: search = {}

        q = cls.query(ancestor=cls.get_default_event_parent_key()) #TODO: Rework this for new parent protocol
        for k in search:
            q = q.filter(getattr(cls, k) == search[k])
        return q
