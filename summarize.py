#!/usr/bin/env python3
#mbobak summarize a nq file, for quick queries, and quad now as subj to point to graph-url
 #this is almost like nq2ttl, but is sumarizing via the qry
import pandas as pd
import os
#context = "@prefix : <http://schema.org/> ." #might get larger, eg.incl dcat
context = "@prefix : <https://schema.org/> ." #https for now
#started by tweaking fnq of fn.nq then dump to fn.csv which could read here
# but can use ec.py utils, to just load summary.qry and get df right away
# then iterate over it  ;load ec like I do w/check.py and use
#could have summary in here, or give a get_summary_txt then get_summary(fnq)
#after this get max lat/lon and put as latitude/longnitude, then get centriod
 #consider a version of the query where the vars are already the so:keywords
 #but after changinge ResourceType to 'a', .. oh, this doesn't have : so special case anyway
#used this query on all of geodec using ec.py's get_summary and dumped to summary.csv
#Nov  5 17:24 get_summary.txt -> get_summary_good.txt
#still using txt file on my server right now instead
port=3030
ftsp=os.getenv('fuseki_tmp_summary_port')
if ftsp:
    print(f'changing port from {port} to {ftsp}')
    port=ftsp
qry="""
prefix schema: <https://schema.org/>
SELECT distinct ?subj ?g ?resourceType ?name ?description  ?pubname
        (GROUP_CONCAT(DISTINCT ?placename; SEPARATOR=", ") AS ?placenames)
        (GROUP_CONCAT(DISTINCT ?kwu; SEPARATOR=", ") AS ?kw) ?datep
        #(GROUP_CONCAT(DISTINCT ?url; SEPARATOR=", ") AS ?disurl)
        WHERE {
          graph ?g {
             ?subj schema:name ?name .
             ?subj schema:description ?description .
            Minus {?subj a schema:ResearchProject } .
            Minus {?subj a schema:Person } .
 BIND (IF (exists {?subj a schema:Dataset .} ||exists{?subj a schema:DataCatalog .} , "data", "tool")
   AS ?resourceType).
            optional {?subj schema:distribution/schema:url|schema:subjectOf/schema:url ?url .}
            OPTIONAL {?subj schema:datePublished ?date_p .}
            OPTIONAL {?subj schema:publisher/schema:name|schema:sdPublisher|schema:provider/schema:name ?pub_name .}
            #OPTIONAL {?subj schema:spatialCoverage/schema:name ?place_name .}
            OPTIONAL {?subj 
        schema:spatialCoverage/schema:name|schema:spatialCoverage/schema:additionalProperty/schema:name ?place_name .}
            OPTIONAL {?subj schema:keywords ?kwu .}
            BIND ( IF ( BOUND(?date_p), ?date_p, "No datePublished") as ?datep ) .
            BIND ( IF ( BOUND(?pub_name), ?pub_name, "No Publisher") as ?pubname ) .
            BIND ( IF ( BOUND(?place_name), ?place_name, "No spatialCoverage") as ?placename ) .
            BIND ( IF ( BOUND(?kw_u), ?kw_u, "") as ?kwu ) .
             }
        }
        #GROUP BY ?subj ?pubname ?placenames ?kw ?datep   ?name ?description  ?resourceType ?g
        GROUP BY ?subj ?g ?resourceType ?name ?description  ?pubname ?placenames ?kw ?datep
        """
        #using more constrained qry now in get_summary.txt * now above
         #want fuseki version to use above soon too
#tmp_endpoint=f'http://localhost:3030/{repo}/sparql' #fnq repo
#print(f'try:{tmp_endpoint}') #if >repo.ttl, till prints, will have to rm this line &next2:
#< not IN_COLAB
#< rdf_inited,rdflib_inited,sparql_inited=True,True,True
#import ec #will use dc.py going forward so:
import dc
#ec.dflt_endpoint = tmp_endpoint
#df=ec.get_summary("")
#all are tabbed after context
#a                       :Dataset ;
# then :so-keyword ;   last w/.
#column names:
# "subj" , "g" , "resourceType" , "name" , "description" , "pubname" , "placenames" , "kw" , "datep" ,
#next time just get a mapping file/have qry w/so keywords as much a possilbe
dbg=True
#dbg=False

def summaryDF2ttl(df):
    urns = {}
    import json
    def is_str(v):
        return type(v) is str
    print(f'{context}')
    for index, row in df.iterrows():
        if dbg:
            print(f'dbg:{row}')
        gu=df["g"][index]
        #skip the small %of dups, that even new get_summary.txt * has
        there = urns.get(gu)
        if not there:
            urns[gu]=1
        elif there: 
            #print(f'already:{there},so would break loop')
            continue #from loop
        rt=row['resourceType']
        name=json.dumps(row['name']) #check for NaN/fix
        if not name:
            name=f'""'
        if not is_str(name):
            name=f'"{name}"'
        if name=="NaN": #this works, but might use NA
            name=f'"{name}"'
        description=row['description']
        if is_str(description):
            sdes=json.dumps(description)
            #sdes=description.replace(' / ',' \/ ').replace('"','\"')
            #sdes=sdes.replace(' / ',' \/ ').replace('"','\"')
          # sdes=sdes.replace('"','\"')
        else:
            sdes=f'"{description}"'
        kw_=row['kw']
        if is_str(kw_):
            kw=json.dumps(kw_)
        else:
            kw=f'"{kw_}"'
        pubname=row['pubname']
        #if no publisher urn.split(':')
        #to use:repo in: ['urn', 'gleaner', 'summoned', 'opentopography', '58048498c7c26c7ab253519efc16df237866e8fe']
        #as of the last runs, this was being done per repo, which comes in on the CLI, so could just use that too*
        if pubname=="No Publisher":
            ul=gu.split(':')
            if len(ul)>4: #could check, for changing urn more, but for now:
                #pub_repo=ul[3]
                pub_repo=ul[4]
                if is_str(pub_repo):
                    pubname=pub_repo
                else: #could just use cli repo
                    global repo
                    pubname=repo
        datep=row['datep']
        placename=row['placenames']
        s=row['subj']
        print(" ")
        print(f'<{gu}>')
        #print(f'        a {rt} ;')
        if rt == "tool":
            print(f'        a :SoftwareApplication ;')
        else:
            print(f'        a :Dataset ;')
       #print(f'        :name "{name}" ;')
        print(f'        :name {name} ;')
       #print(f'        :description """{description}""" ;')
       #print(f'        :description """{sdes}""" ;')
        print(f'        :description ""{sdes}"" ;')
       #print(f'        :keyword "{kw}" ;')
       #print(f'        :keyword {kw} ;') #not what schema.org &the new query uses
        print(f'        :keywords {kw} ;')
        print(f'        :publisher "{pubname}" ;')
        print(f'        :place "{placename}" ;')
        print(f'        :date "{datep}" ;') #might be: "No datePublished" ;should change in qry, for dv's lack of checking
        print(f'        :subjectOf <{s}> .')
        #du= row.get("disurl") #not seeing yet
        du= row.get('url') # check now/not yet
        if is_str(du):
            print(f'        :distribution <{du}> .')
        mlat= row.get('maxlat') # check now/not yet
        if is_str(mlat):
            print(f'        :latitude {mlat} .')
        mlon= row.get('maxlon') # check now/not yet
        if is_str(mlon):
            print(f'        :longitude {mlon} .')
        encodingFormat= row.get('encodingFormat') # check now/not yet
        if is_str(encodingFormat):
            print(f'        :encodingFormat {encodingFormat} .')
    #see abt defaults from qry or here, think dv needs date as NA or blank/check
    #old:
    #got a bad:         :subjectOf <metadata-doi:10.17882/42182> .
    #incl original subj, just in case for now
    #lat/lon not in present ui, but in earlier version

def get_summary4repo_fuseki(repo):
    "so can call interactively to look at the df"
    #tmp_endpoint=f'http://localhost:3030/{repo}/sparql' #fnq repo
    tmp_endpoint=f'http://localhost:{port}/{repo}/sparql' #fnq repo
    print(f'try:{tmp_endpoint}') #if >repo.ttl, till prints, will have to rm this line &next2:
    dc.dflt_endpoint = tmp_endpoint
    df=dc.get_summary("")
    return df
#get_summary does v4qry 'summary' to get_summary_txt template, use v2iqt to instantiate it
 #then call iqt2df takes the InstantitedQueryTemplate and calls on endpoint
#or
#def summarize_repo(repo): #getting an error w/the qry above, so a little more debugging/to fix/to use this variant
def get_summary4repo_file(repo):
    "load .nq to rdflib and dump .ttl summary"
    #global qry
    #qry= "select ?s ?p ?o WHERE { ?s ?p ?o} limit 2" #to debug
    from os.path import exists
    fn=f'{repo}.nq'
    if not exists(fn):
        return f'no {fn} to run'
    else:
        print(f'qry={qry},on:{fn}')
    #results still need to go to a df, or similar iterable useable above
    #df=dc.query_fn(qry,fn) #prints rows, but in end: AttributeError: iterrows, so still needs tranlation to a df
    df=dc.kg_query_fn(qry,fn) #this works on simple qry from https://derwen.ai/docs/kgl/ex4_0/ ;but serde.py", line 197, in load_rdf 4wifire
    if dbg: #but still getting errors w/the bigger qry above on the nq file/more on this soon
        print(f'new df={df}')
    return df

if __name__ == '__main__':
    import sys
    if(len(sys.argv)>1):
        repo = sys.argv[1]
        ##tmp_endpoint=f'http://localhost:3030/{repo}/sparql' #fnq repo
        ##print(f'try:{tmp_endpoint}') #if >repo.ttl, till prints, will have to rm this line &next2:
        ##ec.dflt_endpoint = tmp_endpoint
        ##df=ec.get_summary("")
        #df=get_summary4repo_file(repo) #still needs dbg/finishing off
        df=get_summary4repo_fuseki(repo)
        summaryDF2ttl(df)
