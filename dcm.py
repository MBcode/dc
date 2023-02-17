#Mbobak
#=starting a version of dc.py   
#that has mb.py and these 2 other files taken out, where it recomposes them
#in this staging ground, I'll call it: dcm.py, For: DeCoder-Module version
#-
#in a way, this is an example of how any file might just include what is necessary
# the summarize files, that use the last 2 imports, could then import mb
# as they do in this collection of files, and they should work the same way
#-
#as more a clean-room way of doing it, it could just start with
#import mb
from mb import *  #do this too, if you want this to approach be a replacement for: earthcube_utillities, that I can put in a new branch
#presently the files below have some fncs from the one above
  #was called qry.py in summarize
#import query 
#import rdf2nq 
#could try this, to avoid longer prefix, but will probably just import the parts you want and call directly
from query import * 
from rdf2nq import *
#so now to remove them, from those files, and make refs to mb ;done
#once again, this might just be an example, but could let you load all the utils
