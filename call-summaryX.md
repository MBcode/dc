## what you call to run summarization

#### from getting (gleaner) crawler's quad/repo  through making the summary triples, and loading them 
##### once we have a runX fix

```mermaid
flowchart TD;
R2S[repo_to_summary.sh]  -- calls --> G[1: get_runX.sh];
G -- produces --> nq(repo.nq) -- into --> SR;
R2S -- calls --> SR[2: summarize.py] -- produces --> RT(repo.ttl) -- ttl2blaze.sh --> B[blazegraph];
```

as soon as the [system](https://github.com/MBcode/ec/blob/master/system.md) is made more modular, the repo.nq can come from my [crawl](https://github.com/MBcode/ec/tree/master/crawl) as well
