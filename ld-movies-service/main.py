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
from rdflib import Graph, URIRef, RDF
from rdflib.namespace import Namespace
from flask import Flask, url_for, make_response
import requests
import netifaces as ni
import sys
from urlparse import urljoin

__author__ = 'Fernando Serena'


PORT = 5005
DEBUG = False
films = set([])
AGORA_HOST = 'http://localhost:9002'

app = Flask(__name__)
AMOVIES = Namespace('http://agora.org/amovies#')


@app.route('/')
def get_service():
    root_g = Graph()
    me = URIRef(url_for('get_service', _external=True))
    root_g.add((me, RDF.type, AMOVIES.Service))
    for film in films:
        root_g.add((me, AMOVIES.hasFilm, film))

    response = make_response(root_g.serialize(format='turtle'))
    response.headers['Content-Type'] = 'text/turtle'

    return response


if __name__ == '__main__':
    # Get all dbpedia known films
    sparql = SPARQLWrapper("http://es.dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    sparql.setQuery("""
        SELECT distinct ?film
        WHERE {?film a dbpedia-owl:Film}
    """)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        films.add(URIRef(result["film"]["value"]))

    if len(sys.argv) > 1:
        AGORA_HOST = sys.argv[1]

    # POST movies vocabulary
    with open('movies-service.ttl') as f:
        ttl = f.read()
        requests.post(urljoin(AGORA_HOST, 'vocabs'), data=ttl, headers={'Content-Type': 'text/turtle'})

    # Get local IP address of eth0 (needed when using a virtualized Agora (Vagrant, Docker))
    ni.ifaddresses('eth0')
    ip = ni.ifaddresses('eth0')[2][0]['addr']

    # Clear existing amovies:Service and dbpedia-owl:Film seeds and self-register
    response = requests.get(urljoin(AGORA_HOST, 'seeds'))
    seeds = response.json()['seeds']
    if 'amovies:Service' in seeds.keys():
        for seed in seeds['amovies:Service']:
            requests.delete(urljoin(AGORA_HOST, 'seeds/id/{}'.format(seed['id'])))
    if 'dbpedia-owl:Film' in seeds.keys():
        for seed in seeds['dbpedia-owl:Film']:
            print u'Deleting {}'.format(seed['uri'])
            requests.delete(urljoin(AGORA_HOST, 'seeds/id/{}'.format(seed['id'])))

    requests.post(urljoin(AGORA_HOST, 'seeds'),
                  data=json.dumps({'type': 'amovies:Service', 'uri': 'http://{}:{}/'.format(ip, PORT)}),
                  headers={'Content-Type': 'application/json'})

    # Start the service
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
