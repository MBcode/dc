## what you call to run summarization

#### from getting (gleaner) crawler's quad/repo  through making the summary triples, and loading them

```mermaid
flowchart TD;
R2S[repo_to_summary.sh]  -- calls --> G[1: fix_runX.sh];
G -- calls --> gr[1:get_repo.py]
G -- calls --> r2n[2:run2nq.py] -- loads --> rdf2[rdf2nq.py];
R2S -- calls --> SR[2: summarize.py] -- produces --> RT(repo.ttl) -- ttl2blaze.sh --> B[blazegraph];
r2n -- produces --> nq(repo.nq) -- into --> SR;
```
#### with [runX fix](https://github.com/gleanerio/gleaner/issues/126) the process becomes [even easier](call-summaryX.md)

as soon as the [system](https://github.com/MBcode/ec/blob/master/system.md) is made more modular, the repo.nq can come from my [crawl](https://github.com/MBcode/ec/tree/master/crawl) as well
