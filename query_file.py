#from dc.py being tried in the dc/summarize.py version of tsum.py m_bobak

#another (but smaller) lib that could take qry results to a df
from gastrodon import *
from rdflib import *
#def gdf(qry,g):
def gdf(qry,fn):
    import sys
    #import gastrodon as gas
    #import rdflib as rdf
    import pandas as pd
    s=get_txtfile(fn)
    sl=len(s)
    print(f'got:fn={fn},sl={sl}')
    g=inline(s)
    print(f'g={g}')
    df=g.select(qry)
    print(f'df={df}')
    return df

#-
import os
#-
def add2log(cs):
    print(cs)
#-
def dfn(fn):
    "FileName or int:for:d#.nt"
    if isinstance(fn, int):
        fnt=f'd{fn}.nt'
    else:
        fnt=fn
    return fnt
#-
def file_ext(fn):
    """the ._part of the filename
    >>> file_ext("filename.txt")
    '.txt'
    """
    st=os.path.splitext(fn)
    add2log(f'fe:st={st}')
    return st[-1]
#-
def get_txtfile(fn):
    "ret str from file"
    with open(fn, "r") as f:
        return f.read()
#-

from gastrodon import *
def query_fn_g(qry,fn_): 
    "sparql qry on a filename of RDF data"
    fn=dfn(fn_) #maybe gen fn from int
    add2log(f'qry_fn:fn={fn},qry={qry}')
 #  from rdflib import ConjunctiveGraph #might just install rdflib right away
 #  g = ConjunctiveGraph(identifier=fn)
   #data = open(fn, "rb") #or get_textfile -no
    data = get_txtfile(fn)
    frmt="nquads"
    ext=file_ext(fn)
    if ext==".nt": 
        frmt="ntriples"
 #  g.parse(data, format=frmt)
    kb=inline(data)
    #ret= kb.query(qry) #AttributeError: 'LocalEndpoint' object has no attribute 'query'
    ret= kb.select(qry) 
    return ret

def t_g(fn="ihl-.nq"):
    df=query_fn_g("select ?s ?p ?o where {?s ?p ?o}",fn)
    return df

#both of these test files work now, on a good .nt file, producing a DF from the query over it

#now both test fncs have similar problems parsing the file, while rdflib can parse it
#Bad syntax (expected '.' or '}' or ']' at end of statement) at ^ in:
#"...b'1999/02/22-rdf-syntax-ns#type> <https://schema.org/Dataset> '^b'<http://ideational.ddns.net/ec/ld/iris.nq> .\n<https://ds.iri'..."

def query_fn(qry,fn_): 
    "sparql qry on a filename of RDF data"
    fn=dfn(fn_) #maybe gen fn from int
    add2log(f'qry_fn:fn={fn},qry={qry}')
    from rdflib import ConjunctiveGraph #might just install rdflib right away
    g = ConjunctiveGraph(identifier=fn)
    data = open(fn, "rb") #or get_textfile -no
    frmt="nquads"
    ext=file_ext(fn)
    if ext==".nt": 
        frmt="ntriples"
    g.parse(data, format=frmt)
    results = g.query(qry)
    #l= [str(result[0]) for result in results]  #worked more for set pp value results
    #print(f'l={l}')
    #if dbg:
    print(f'query_fn:g={g}')
    print(f'query_fn:bindings={results.bindings}')
    print(f'query_fn:results={results}')
    for r in results: 
        print(f'r={r}')
    add2log(results) #
    #if don't want to go for kglab just yet, find a way to convert this output to a format(df)that summarization can use
    #return results
    #df=gdf(qry,g)
    #df=gdf(qry,fn)
    #df=map(asdict,results)
    #df=map(to_dict,results)
    return df

#def kg_query_fn(qry,fn): #needs fix/testing 
def kg_query_fn(qry,fn, format="nquads"):
    "kglab:sparql qry on a filename of RDF data"
    import kglab
    namespaces = { "so": "https://schema.org" }
    kg = kglab.KnowledgeGraph(name = fn, base_uri = "http://geocodes.ddns.net/ld/", namespaces = namespaces,)
    kg.load_rdf(fn)
    #could viz as well, see: https://derwen.ai/docs/kgl/ex4_0/ 
    #df = kg.query_as_df(qry)
    #df = kg.query_as_df(qry, format=format) #got an unexpected keyword argument 'format'
    df = kg.query_as_df(qry)
    return df

def t_kg(fn="ihl-.nq"):
    df=kg_query_fn("select ?s ?p ?o where {?s ?p ?o}",fn)
    return df
