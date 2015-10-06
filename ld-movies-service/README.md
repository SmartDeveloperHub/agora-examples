#Agora-Examples
##Consuming DBPedia Films using an ad-hoc service of Agora seeds 

This example publishes a local URI that represents a virtual concept called `amovies:Service`, which establishes a containment relationship with `dbpedia-owl:Film`
resources by means of an ad-hoc property called `amovies:hasFilm`.

###How it works?
1. Run a SPARQL query to the DBPedia to get all known films:
  `SELECT distinct ?film WHERE {?film a dbpedia-owl:Film}`
2. Teach Agora the specific vocabulary that will be used to consume existing data on films and other related concepts.
3. Build and expose the ad-hoc service and register it as a seed that contains `dbpedia-owl:Film` resources.

### Agora fragment queries
* Get all relations between the films and the actors who star: `http://AGORA_HOST/fragment?gp={?f dpedia-owl:starring ?a}`
* Same as previous query, but also getting the birth name of these actors: `http://AGORA_HOST/fragment?gp={?f dpedia-owl:starring ?a. ?a dbp:birthName ?n}`
* Get all films, their distributors and known locations of each them: `http://AGORA_HOST/fragment?gp={?f dbpedia-owl:distributor ?d. ?d dbpedia-owl:location ?l}`

##License
Agora-Examples is distributed under the Apache License, version 2.0.


