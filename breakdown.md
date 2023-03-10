### earthcube_utliites [wiki](https://github.com/earthcube/earthcube_utilities/wiki)

#### originally used for notebooks only, but getting more reuse in the rest of the workflow

##### this has caused a natural breakdown of Sub-Modules, that can be used as needed

```mermaid
flowchart TD;
EC[ec.py] -- broke_out --> T[testing:1475];
EC -- leaving --> ec2[ec main:2248];
ec2 -- back2early --> U[earthcube_utilities:518]  -- has --> R[a bit for opening data in notebooks];
U -- loads --> TR[the rest]
TR -- import --> MB[min-base:690];
TR -- import --> query[SPARQL queries from git:175];
TR -- import --> R2[rdf2nq:146];
U -- could_load --> TR2[more];
TR2 ----> RD[related datasets:145];
TR2 ----> RC[RO-CRATE creation:107];
TR2 -- leaving --> o[other:718]
``` 

### <ins>**earthcube_utilities** [breakdown](https://github.com/earthcube/earthcube_utilities/blob/dcm/earthcube_utilities/docs/breakdown.md)</ins>


#### <ins>[earthcube_utilities.py](earthcube_utilities.py)</ins> has early <ins>notebook specific code that can go into a notebook/data_download sub module<ins>



#### <ins>[mb.py](mb.py) mini-base small util functions</ins> that sometimes end up getting copied into the other places they are needed now



#### <ins>[query.py](query.py) is can do all the SPARQL queries the UI can do</ins>
##### it is setup to add one get_{qry_name}\_txt  function to get the txt of the query, usually from raw git
##### then a function: {qry_name} that calls one fuction with {qry_name} as the arg, and maybe a variable
###### it will get the txt from the 1st function, and replace the var w/in the template txt, run the query and return a DF


#### <ins>[rdf2nq.py](rdf2nq.py) takes one form of rdf triples, and adds the filename of the file as the last column in its nquads</ins> output

##### if it is .ntriples, then you just add a column
##### if it is another format like jsonld, then it runs jena's riot RDF I/O technology (RIOT) on it first right now, but could use rdflib


### There is more that I'm working on the grouping [now](https://mbobak.ncsa.illinois.edu/ec/utils/?C=M;O=D)
#### to include some high level descriptions of possible groupings/(of)functionality, 
##### and places to make more use of other libs, e.g.  [pydash](https://github.com/dgilland/pydash) and [kglab](https://derwen.ai/docs/kgl/ex4_0/) 
#### and there is the original third sectioned off for the [old](https://github.com/earthcube/ec/blob/master/ect.py) <ins>testing</ins>, that parts of 
##### could be integrated with the new [gleaner-logging](https://github.com/search?q=org%3Agleanerio+logging&type=code).worklfow.

### <ins>Could</ins> be <ins>load</ins>ing:
##### <ins>related-data</ins> using sklearn [here](https://github.com/MBcode/ec/blob/master/qry/rec.py)
##### <ins>RO-CRATE metadata creation</ins>, that dv asked for

