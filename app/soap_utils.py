import sys
from suds.client import Client
from config import PROXY
from app import db
from .models import Wsdl


class SoapManager():

    def __init__(self):
        self.client = None
        self.connection_info = 'Not connected'

    # connect to WS and get WSDL definition
    def connect(self, url, use_proxy = False):

        #check proxy usage
        if use_proxy:
            p = PROXY
        else:
            p = None

        # get wsdl
        try:
            self.client = Client(url, proxy=p, timeout=10)  # sacar timeout y proxy settings a config
            self.connection_info = 'Successfully connected to ' + self.client.wsdl.url
        except:
            self.connection_info = sys.exc_info()[0]
            self.client = None
            return False

        return True


    def get_connnection_info(self):

        return self.connection_info


    # get methods as a dictionary {'service','port','methods'}
    def get_methods(self):

        l = []
        if self.client is None:
            return l

        for s in self.client.wsdl.services:
            for p in s.ports:
                lm = []
                for m in p.methods:
                    lm.append(m)
                d = {'service': s.name, 'port': p.name, 'methods': sorted(lm)}
                l.append(d)
        return l

    def get_wsdl_summary(self):

        if self.client is not None:
            return str(self.client)
        else:
            return ''

    def get_method_detail(self, m):

        if self.client is not None:
            s = self.client.factory.create(m)
        else:
            s = 'not found'
        return s


def get_wsdl_list():

    wsdls = Wsdl.query.all()
    return wsdls


def get_ws(id):

    wsdl = Wsdl.query.filter_by(id=id).first()
    return wsdl


def save_wsdl(wsdl):

    # check if wsdl name already exists
    w = Wsdl.query.filter_by(name=wsdl.name).first()
    if w is None:
        db.session.add(wsdl)
        db.session.commit()
        return True
    else:
        return False


