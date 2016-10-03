from flask import render_template, flash, redirect, url_for, g, session, request
from app import app, db, babel
from .soap_forms import NewWsdlForm, RetrieveWsdlInfo
from config import LANGUAGES
from .soap_utils import *
from .models import Wsdl

# global vars
sm = SoapManager()

# root & default path
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    return render_template('index.html', title='SOAP')


# default soap_index path
@app.route('/soap', methods=['GET', 'POST'])
@app.route('/soap/index', methods=['GET', 'POST'])
def soap_index():

    return render_template('soap/index.html', title='SOAP')


############################### WSDL VIEWS ###############################
# wsdl retrieve
@app.route('/soap/wsdl', methods=['GET', 'POST'])
def soap_wsdl():

    # salvar wsld
    new_wsdl_form = NewWsdlForm()
    if new_wsdl_form.validate_on_submit():
        print('entro en el validate que no debo')
        name = new_wsdl_form.name.data
        url = new_wsdl_form.url.data
        w = Wsdl(name=name, url=url)
        if not save_wsdl(w):
            return render_template('soap/error.html', error='Ya existe un WSDL con ese nombre')

    # conectar con wsdl
    get_wsdl_form = RetrieveWsdlInfo()
    wl = get_wsdl_list()
    get_wsdl_form.id.choices = [(w.id, w.name + ' - ' + w.url) for w in wl]
    if get_wsdl_form.validate_on_submit():
        use_proxy = get_wsdl_form.use_proxy.data
        wsdl = get_ws(get_wsdl_form.id.data)
        if sm.connect(wsdl.url,use_proxy=use_proxy):
            ms = sm.get_methods()
            return render_template('soap/client.html', title='WS Client', methods=ms)
        else:
            return render_template('soap/error.html', error=sm.get_connnection_info())

    #print(get_wsdl_form.errors)
    #print(get_wsdl_form.id.data)
    return render_template('soap/wsdl.html', get_wsdl_form=get_wsdl_form, new_wsdl_form=new_wsdl_form, wsdls=wl, title='Explore WSDL - Retry')


# change proxy settings
@app.route('/soap/proxy', methods=['GET', 'POST'])
def soap_proxy():

    #wsdl_form = WsdlForm()
    #crear proxy form
    #return render_template('soap/proxy.html', wsdl_form=wsdl_form, title='WSDL')
    return render_template('soap/index.html', title='TODO')


# wsdl summary
@app.route('/soap/wsdl_sum')
def soap_wsdl_sum():

    wsdl = sm.get_wsdl_summary()
    return render_template('soap/wsdl_sum.html', wsdl_sum=wsdl)


# method summary
@app.route('/soap/method/<method>')
def soap_method(method):

    m = sm.get_method_detail(method)
    return render_template('soap/method.html', title=method, method_sum=m)


############################### PIONLINE VIEWS ###############################