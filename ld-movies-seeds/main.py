"""
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  This file is part of the Smart Developer Hub Project:
    http://www.smartdeveloperhub.org

  Center for Open Middleware
        http://www.centeropenmiddleware.com/
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  Copyright (C) 2015 Center for Open Middleware.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at 

            http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
"""
import json
from SPARQLWrapper import SPARQLWrapper, JSON
import requests
import sys
from urlparse import urljoin

__author__ = 'Fernando Serena'


PORT = 5005
DEBUG = False
films = set([])
AGORA_HOST = 'http://localhost:9002'


if __name__ == '__main__':
    # Get all dbpedia known films
    sparql = SPARQLWrapper("http://es.dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    sparql.setQuery("""
        SELECT distinct ?film
        WHERE {?film a dbpedia-owl:Film} LIMIT 100
    """)
    results = sparql.query().convert()

    if len(sys.argv) > 1:
        AGORA_HOST = sys.argv[1]

    # POST movies vocabulary
    with open('movies-model.ttl') as f:
        ttl = f.read()
        requests.post(urljoin(AGORA_HOST, 'vocabs'), data=ttl, headers={'Content-Type': 'text/turtle'})

    # Clear existing dbpedia-owl:Film seeds
    response = requests.get(urljoin(AGORA_HOST, 'seeds'))
    seeds = response.json()['seeds']
    if 'amovies:Service' in seeds.keys():   # Clear service seeds (if present)
        for seed in seeds['amovies:Service']:
            requests.delete(urljoin(AGORA_HOST, 'seeds/id/{}'.format(seed['id'])))
    if 'dbpedia-owl:Film' in seeds.keys():
        for seed in seeds['dbpedia-owl:Film']:
            print u'Deleting {}'.format(seed['uri'])
            requests.delete(urljoin(AGORA_HOST, 'seeds/id/{}'.format(seed['id'])))

    # Register all obtained dbpedia-owl:Film resources
    for result in results["results"]["bindings"]:
        f = result["film"]["value"]
        print u'Registering {}'.format(f)
        requests.post(urljoin(AGORA_HOST, 'seeds'),
                      data=json.dumps({'type': 'dbpedia-owl:Film', 'uri': f}),
                      headers={'Content-Type': 'application/json'})

