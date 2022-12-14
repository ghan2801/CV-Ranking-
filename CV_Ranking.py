# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pickle

import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
import json
import sys, fitz, pandas as pd

from spacy.matcher import Matcher

from nltk.corpus import stopwords
import nltk

import re

from ast import JoinedStr

import streamlit as st

nltk.download('stopwords')



nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)





def extract_name(resume_text):
  nlp = spacy.load("en_core_web_sm")
  nlp_text = nlp(resume_text)
    
  # First name and Last name are always Proper Nouns
  pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    
  matcher.add('NAME', [pattern], on_match=None)
    
  matches = matcher(nlp_text)
    
  for match_id, start, end in matches:
    span = nlp_text[start:end]
    print(span.text)
    return span.text



# Grad all general stop words
STOPWORDS = set(stopwords.words('english'))

# Education Degrees
Degree = [
            'BE','B.E.', 'B.E', 'BS', 'B.S','C.A.','c.a.','B.Com','B. Com',
            'M. Com', 'M.Com','M. Com .',
            'ME', 'M.E', 'M.E.', 'MS', 'M.S',
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH',
            'PHD', 'phd', 'ph.d', 'Ph.D.','MBA','mba',
            'graduate', 'post-graduate','5 year integrated masters','masters',
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII','BACHELOR'
        ]

def extract_degree(resume_text):
    nlp_text = nlp(resume_text)

    # Sentence Tokenizer
    nlp_text = [sent.text.strip() for sent in nlp_text.sents]

    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            try:
                if tex.upper() in Degree and tex not in STOPWORDS:
                    edu[tex] = text + nlp_text[index + 1]
    
            except IndexError:
                pass
            continue
                

    # Extract year
    education = []
    for key in edu.keys():
        year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
        if year:
            education.append((key, ''.join(year[0])))
        else:
            education.append(key)
    return education

def extract_skills(resume_text):
    nlp_text = nlp(resume_text)

    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]
    
    skills = ["machine learning",
             "deep learning",
             "nlp",
             "natural language processing",
             "mysql",
             "sql",
             "django",
             "computer vision",
             "opencv",
             "mongodb",
             "artificial intelligence",
             "ai",
             "flask",
             "robotics",
             "data structures",
             "python",
             "c",
             "matlab",
             'NumPy','CSS', 'HTML', 'Javascipt',
             'Pandas', 'Tensor???ow', 'Scikit-Learn', 'OpenCV','tableau',
              'Sentiment Analysis', 'NLTK','BeRT','XLNet', 'Data Science','MATLAB','Project Management','Chain Management',
              'MySQL','AWS','Data Analysis','Software Development','java',
              'ajenti','django-suit','django-xadmin','flask-admin','flower','grappelli','wooey','algorithms','pypattyrn',
              'python-patterns','sortedcontainers','django-simple-captcha','django-simple-spam-blocker','django-compressor',
              'django-pipeline','django-storages','fanstatic','fileconveyor','flask-assets','jinja-assets-compressor','webassets',
              'audiolazy','audioread','beets','dejavu','django-elastic-transcoder','eyed3','id3reader','m3u8','mingus','pyaudioanalysis',
              'pydub','pyechonest','talkbox','timeside','tinytag','authomatic','django-allauth','django-oauth-toolkit','flask-oauthlib',
              'oauthlib','python-oauth2','python-social-auth','rauth','sanction','jose','pyjwt','python-jws','python-jwt','bitbake',
              'buildout','platformio','pybuilder','scons','django-cms','djedi-cms','feincms','kotti','mezzanine','opps','plone',
              'quokka','wagtail','widgy','beaker','diskcache','django-cache-machine','django-cacheops','django-viewlet',
              'dogpile.cache','hermescache','johnny-cache','pylibmc','errbot','coala','code2flow','pycallgraph','flake8','pylama',
              'pylint','mypy','asciimatics','cement','click','cliff','clint','colorama','docopt','gooey','python-fire','python-prompt-toolkit','aws-cli','bashplotlib','caniusepython3','cookiecutter','doitlive','howdoi','httpie','mycli','pathpicker','percol','pgcli','saws','thefuck','try','python-future','python-modernize','six','opencv','pyocr','pytesseract','simplecv','eventlet','gevent','multiprocessing','threading','tomorrow','uvloop','config','configobj','configparser','profig','python-decouple','cryptography','hashids','paramiko','passlib','pynacl','blaze','orange','pandas','cerberus','colander','jsonschema','schematics','valideer','voluptuous','altair','bokeh','ggplot','matplotlib','pygal','pygraphviz','pyqtgraph','seaborn','vispy','pickledb','pipelinedb','tinydb','zodb','mysql','mysql-python','mysqlclient','oursql','pymysql','postgresql','psycopg2','queries','txpostgres','apsw','pymssql','nosql','cassandra-python-driver','happybase','plyvel','py2neo','pycassa','pymongo','redis-py','telephus','txredis','arrow','chronyk','dateutil','delorean','moment','pendulum','pytime','pytz','when.py','ipdb','pdb++','pudb','remote-pdb','wdb','line_profiler','memory_profiler','profiling','vprof','caffe','keras','mxnet','neupy','pytorch','tensorflow','theano','ansible','cloud-init','cuisine','docker','fabric','fabtools','honcho','openstack','pexpect','psutil','saltstack','supervisor','dh-virtualenv','nuitka','py2app','py2exe','pyinstaller','pynsist','sphinx','awesome-sphinxdoc','mkdocs','pdoc','pycco','s3cmd','s4cmd','you-get','youtube-dl','alipay','cartridge','django-oscar','django-shop','merchant','money','python-currencies','forex-python','shoop','emacs','elpy','sublime','anaconda','sublimejedi','vim','jedi-vim','python-mode','youcompleteme','ptvs','visual','python','magic','liclipse','pycharm','spyder','envelopes','flanker','imbox','inbox.py','lamson','marrow','modoboa','nylas','yagmail','pipenv','p','pyenv','venv','virtualenv','virtualenvwrapper','imghdr','mimetypes','path.py','pathlib','python-magic','unipath','watchdog','cffi','ctypes','pycuda','swig','deform','django-bootstrap3','django-crispy-forms','django-remote-forms','wtforms','cytoolz','fn.py','funcy','toolz','curses','enaml','flexx','kivy','pyglet','pygobject','pyqt','pyside','pywebview','tkinter','toga','urwid','wxpython','cocos2d','panda3d','pygame','pyogre','pyopengl','pysdl2','renpy','django-countries','geodjango','geoip','geojson','geopy','pygeoip','beautifulsoup','bleach','cssutils','html5lib','lxml','markupsafe','pyquery','untangle','weasyprint','xmldataset','xmltodict','grequests','httplib2','requests','treq','urllib3','ino','keyboard','mouse','pingo','pyro','pyuserinput','scapy','wifi','hmap','imgseek','nude.py','pagan','pillow','pybarcode','pygram','python-qrcode','quads','scikit-image','thumbor','wand','clpython','cpython','cython','grumpy','ironpython','jython','micropython','numba','peachpy','pyjion','pypy','pysec','pyston','stackless','interactive','bpython','jupyter','ptpython','babel','pyicu','apscheduler','django-schedule','doit','gunnery','joblib','plan','schedule','spiff','taskflow','eliot','logbook','logging','sentry','metrics','nupic','scikit-learn','spark','vowpal_porpoise','xgboost','pyspark','luigi','mrjob','streamparse','dask','python(x','y)','pythonlibs','pythonnet','pywin32','winpython','gensim','jieba','langid.py','nltk','pattern','polyglot','snownlp','spacy','textblob','mininet','pox','pyretic','sdx','asyncio','diesel','pulsar','pyzmq','twisted','txzmq','napalm','django-activity-stream','stream-framework','django','sqlalchemy','awesome-sqlalchemy','orator','peewee','ponyorm','pydal','python-sql','pip','conda','curdling','pip-tools','wheel','warehouse','bandersnatch','devpi','localshop','carteblanche','django-guardian','django-rules','delegator.py subprocesses for','sarge','sh','celery','huey','mrq','rq','simpleq','annoy','fastfm','implicit','libffm','lightfm','surprise','tensorrec','django-rest-framework','django-tastypie','flask','eve','flask-api-utils','flask-api','flask-restful','flask-restless','pyramid','cornice','falcon','hug','restless','ripozo','sandman','apistar','simplejsonrpcserver','simplexmlrpcserver','zerorpc','astropy','bcbio-nextgen','bccb','biopython','cclib','networkx','nipy','numpy','obspy','pydy','pymc','rdkit','scipy','statsmodels','sympy','zipline','simpy','django-haystack','elasticsearch-dsl-py','elasticsearch-py','esengine','pysolr','solrpy','whoosh','marshmallow','apex','python-lambda','zappa','tablib','marmir','openpyxl','pyexcel','python-docx','relatorio','unoconv','xlsxwriter','xlwings','xlwt / xlrd','pdf','pdfminer','pypdf2','reportlab','markdown','mistune','python-markdown','yaml','pyyaml','csvkit','unp','cactus','hyde','lektor','nikola','pelican','tinkerer','django-taggit','genshi','jinja2','mako','hypothesis','mamba','nose','nose2','pytest','robot','unittest','green','tox','locust','pyautogui','selenium','sixpack','splinter','doublex','freezegun','httmock','httpretty','mock','responses','vcr.py','factory_boy','mixer','model_mommy','mimesis','fake2db','faker','radar','chardet','difflib','ftfy','fuzzywuzzy','levenshtein','pangu.py','pyfiglet','pypinyin','shortuuid','unidecode','uniout','xpinyin','slugify','awesome-slugify','python-slugify','unicode-slugify','parser','phonenumbers','ply','pygments','pyparsing','python-nameparser','python-user-agents','sqlparse','apache-libcloud','boto3','django-wordpress','facebook-sdk','facepy','gmail','google-api-python-client','gspread','twython','furl','purl','pyshorteners','short_url','webargs','moviepy','scikit-video','wsgi-compatible','bjoern','fapws3','gunicorn','meinheld','netius','paste','rocket','uwsgi','waitress','werkzeug','haul','html2text','lassie','micawber','newspaper','opengraph','python-goose','python-readability','sanitize','sumy','textract','cola','demiurge','feedparser','grab','mechanicalsoup','portia','pyspider','robobrowser','scrapy','bottle','cherrypy','awesome-django','awesome-flask','awesome-pyramid','sanic','tornado','turbogears','web2py','github','autobahnpython','crossbar','django-socketio','websocket-for-python','javascript','php','c#','c++','ruby','css','c','objective-c','shell','scala','swift','matlab','clojure','octave','machine learning','data analytics','predictive analytics','html','js','accounts payable','receivables','inventory controls','payroll','deposits','bank reconciliation','planning and enacting cash-flows','report preparation','financial models','financial controls','documentation','time management','schedules','benchmarking','future state assessment','business process re-engineering','as-is analysis','defining solutions and scope','gap analysis','role change','wireframing','prototyping','user stories','financial analysis/modeling','swot analysis','quickbooks','quicken','erp','enterprise resource planning','spanish','german','rest','soap','json','website','ui','ux','design','crm','cms','communication','coding','windows','servers','unix','linux','redhat','solaris','java','perl','vb script','xml','database','oracle','microsoft sql','sql','microsoft word','microsoft powerpoint','powerpoint','word','excel','visio','microsoft visio','microsoft excel','adobe','photoshop','hadoop','hbase','hive','zookeeper','openserver','auto cad','pl/sql','ruby on rails','asp','jsp','operations','technical','training','sales','marketing','reporting','compliance','strategy','research','analytical','engineering','policies','budget','finance','project management','health','customer service','content','presentation','brand','presentations','safety','certification','seo','digital marketing','accounting','regulations','legal','engagement','analytics','distribution','coaching','testing','vendors','consulting','writing','contracts','inventory','retail','healthcare','regulatory','scheduling','construction','logistics','mobile','c???(programming language)','correspondence','controls','human resources','specifications','recruitment','procurement','partnership','partnerships','management experience','negotiation','hardware','programming','agile','forecasting','advertising','business development','audit','architecture','supply chain','governance','staffing','continuous improvement','product development','networking','recruiting','product management','sap','troubleshooting','computer science','budgeting','electrical','customer experience','economics','information technology','transportation','social media','automation','lifecycle','filing','modeling','investigation','editing','purchasing','kpis','hospital','forecasts','acquisition','expenses','billing','workflow','product owner','analyze','cross functional','business process','process','improvement','pivot tables','pivot','vlookups','sharepoint','microsoft sharepoint','access database','access','test case','jira','tfs','hp alm','tableau','business object','business intelligence','jad','solicitation','kaban','vue.js',
              'sketch','indesign','illustrator','english','french','active directory','data center',
              'solution architecture','dns','network design','open source','desktop support','application support','administration',
              'change management','video','invoices','administrative support','payments','lean','process improvement','installation',
              'risk management','transactions','investigations','r (programming language)','data analysis','statistics','protocols',
              'program management','quality assurance','banking','outreach','sourcing','microsoft office','merchandising','r',
              'teaching','pharmaceutical','fulfillment','positioning','tax','service delivery','investigate','editorial',
              'account management','valid drivers license','electronics','pr','public relations','assembly','facebook',
              'spreadsheets','recruit','proposal','data entry','hotel','ordering','branding','life cycle','real estate',
              'relationship management','researching','process improvements','chemistry','saas','cad','sales experience',
              'mathematics','customer-facing','audio','project management skills','six sigma','hospitality','mechanical engineering',
              'auditing','employee relations','android','security clearance','licensing','fundraising','repairs','iso','market research',
              'business strategy','pmp','data management','quality control','reconciliation','conversion','business analysis',
              'financial analysis','ecommerce','client service','publishing','supervising','complex projects','key performance indicators',
              'scrum','sports','e-commerce','journalism','d (programming language)','data collection','higher education',
              'marketing programs','financial management','business plans','user experience','client relationships','cloud',
              'analytical skills','cisco','internal stakeholders','product marketing','regulatory requirements','itil','information security','aviation','supply chain management','industry experience','autocad','purchase orders','acquisitions','tv','instrumentation','strategic direction','law enforcement','call center','experiments','technical skills','human resource','business cases','build relationships','invoicing','support services','marketing strategy','operating systems','biology','start-up','electrical engineering','workflows','routing','non-profit','marketing plans','due diligence','business management','iphone','architectures','reconcile','dynamic environment','external partners','asset management','emea','intranet','sops','sas','digital media','prospecting','financial reporting','project delivery','operational excellence','standard operating procedures','technical knowledge','on-call','talent management','stakeholder management','tablets','analyze data','financial statements','microsoft office suite','fitness','case management','value proposition','industry trends','rfp','broadcast','portfolio management','fabrication','financial performance','customer requirements','psychology','marketing materials','resource management','physics','mortgage','development activities','end user','business planning','root cause','analysis','leadership development','relationship building','sdlc','on-boarding','quality standards','regulatory compliance','aws','kpi','status reports','product line','drafting','phone calls','product knowledge','business stakeholders','technical issues','admissions','supervisory experience','usability','pharmacy','commissioning','project plan','ms excel','fda','test plans','variances','financing','travel arrangements','internal customers','medical device','counsel','inventory management','performance metrics','lighting','outsourcing','performance improvement','management consulting','graphic design','transport','information management','.net','wpf','startup','matrix','front-end','project planning','business systems','accounts receivable','public health','hris','instructional design','in-store','employee engagement','cost effective','sales management','api','adobe creative suite','twitter','program development','event planning','cash flow','strategic plans','vendor management','trade shows','hotels','segmentation','contract management','gis','talent acquisition','photography','internal communications','client services','ibm','financial reports','product quality','beverage','strong analytical skills','underwriting','cpr','mining','sales goals','chemicals','scripting','migration','software engineering','mis','therapeutic','general ledger','ms project','standardization','retention','spelling','media relations','os','daily operations','immigration','product design','etl','field sales','driving record','peoplesoft','benchmark','quality management','apis','test cases','internal controls','telecom','business issues','research projects','data quality','strategic initiatives','office software','cfa','co-op','big data','journal entries','vmware','help desk','statistical analysis','datasets','alliances','solidworks','prototype','lan','sci','budget management','rfps','flex','gaap','experimental','cpg','information system','customer facing','process development','web services','international','travel','revenue growth','software development life cycle','operations management','computer applications','risk assessments','sales operations','raw materials','internal audit','physical security','sql server','affiliate','computer software','manage projects','business continuity','litigation','it infrastructure','cost reduction','small business','annual budget','ios','html5','real-time','consulting experience','circuits','risk assessment','cross-functional team','public policy','analyzing data','consulting services','google drive','ad words','pay per click','email','db2','expense tracking','reports','wordpress','yoast','ghostwriting','corel draw','automated billing','system','customer management','debugging','system administration','network configuration','software installation','security','tech support','updates','tci/ip','dhcp','wan/lan','ubuntu','virtualized networks','network automation','cloud management','ai','salesforce','mango db','math','calculus','product launch','mvp'


             ]
    
    skillset = []
    
    # check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    
    # check for bi-grams and tri-grams (example: machine learning)
    for token in nlp_text.noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    
    return [i.capitalize() for i in set([i.lower() for i in skillset])]




loaded_model = pickle.load(open('C:/Users/ghanshyam.rajput/Desktop/DIPMLAI/trained_model.sav', 'rb'))
# creating a function for Prediction

def ranking (input_data):
    
    prediction = loaded_model(input_data)
    return prediction

def printtable (txt):

    print(txt)

def main():
    
    n = pd.DataFrame(columns=['Name','Skills','College Name','Graduation Year','Degree','Designation','Graduation Year','Years of Experience','Companies worked at'])
    jd = pd.DataFrame(columns=['Skills','Degree','Designation','Years of Experience'])
    # giving a title
    st.title('CV Ranking based on JDs')
    
    
    # getting the input data from the user
    
    res = {}
    position = st.text_input('Please select the position:')
    nor = st.text_input('Please enter how many resumes want to scan: ')
    
    for i in range(1,nor+1):
        print('Resume - ',i)
        rpath = st.text_input('Path of resume: ')
        doc = fitz.open(rpath)
        text = " "
        for page in doc:
            text = text + str(page.get_text())
            text = text.strip()
            text = ' '.join(text.split())
            res[i]=text
            doc = ranking(res[i])
            d ={}
            for ent in doc.ents:
                d[ent.label_] = ent.text
            df=pd.DataFrame(d,columns=['Name','Skills','College Name','Graduation Year','Degree','Designation','Graduation Year','Years of Experience','Companies worked at'],index=['Name']).reset_index(drop=True)
            df.loc[df['Skills'].isnull(), 'Skills'] = str(extract_skills(res[i]))
            df.loc[df['Name'].isnull(), 'Name'] = extract_name(res[i])
            if len(extract_degree(res[i])) != 0:
                df.loc[df['Degree'].isnull(), 'Degree'] = extract_degree(res[i])
            n = pd.concat([n, df], ignore_index = True)




    
    # code for Prediction
    diagnosis = ''
    
    # creating a button for Prediction
    
    if st.button('Check Result'):
        diagnosis = printtable(n)
        
        
    st.success(diagnosis)
    
if __name__ == '__main__':
    main() 
    
    
    

# loading the saved model
