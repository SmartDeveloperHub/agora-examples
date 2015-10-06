#Agora-Examples
## Consuming DBPedia Films using their URIs as Agora seeds 

This example demonstrates how we can use Agora without the need of creating any virtual containment relationship for the DBPedia resources.

###How it works?
1. Run a SPARQL query to the DBPedia to get all known films:
  `SELECT distinct ?film WHERE {?film a dbpedia-owl:Film} LIMIT 100`
2. Teach Agora the specific vocabulary that will be used to consume existing data on films and other related concepts.
3. Register all o`dbpedia-owl:Film` obtained URIs as seeds.

### Agora fragment queries
* Get all relations between the films and the actors who star: `http://AGORA_HOST/fragment?gp={?f dpedia-owl:starring ?a}`
* Same as previous query, but also getting the birth name of these actors: `http://AGORA_HOST/fragment?gp={?f dpedia-owl:starring ?a. ?a dbp:birthName ?n}`
* Get all films, their distributors and known locations of each them: `http://AGORA_HOST/fragment?gp={?f dbpedia-owl:distributor ?d. ?d dbpedia-owl:location ?l}`

##License
Agora-Examples is distributed under the Apache License, version 2.0.


