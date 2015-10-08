#Agora-Examples

A set of Python examples showing how to use Agora to retrieve fragments of data into a Linked Data context.

##Examples

#####Consuming DBPedia Films using an ad-hoc service of Agora seeds
* Folder: ld-movies-service

#####Consuming DBPedia Films using their URIs as Agora seeds 
* Folder: ld-movies-seeds

#Structure
Each example contains:

* A `README.md` file explaining its purpose and process.
* A `requirements.txt` file that specifies the package dependencies that must be install in order to succesfully run the example.
* A `*.ttl` file that contains a turtle-based representation of the specific ontology.
* A `main.py` python script that does the job.

#Usage
1. Create a Python virtualenv (recommended)
2. Change to the specific folder of the example you want to run.
3. Install dependencies: `pip install -r requirements.txt`
4. Run the example: `python main.py`
5. Open a browser (preferably Chrome) and try some queries!

##License
Agora-Examples is distributed under the Apache License, version 2.0.


