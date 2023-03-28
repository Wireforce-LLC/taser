from datetime import datetime
from elasticsearch import Elasticsearch
from pandas import Timestamp
from rich import inspect
from rich.console import Console

import cp
import pysolr
import pandas as pd
import plugins.prism_map_index
import plugins.general_score_by_prism

es = Elasticsearch("http://172.81.180.191:9241/")

console = Console()

# Create a client instance. The timeout and authentication options are not required.
# solr = pysolr.Solr('http://172.81.180.191:8983', always_commit=True)


def test(dir, meta):
  console.log(f"🤖 Autotest: {dir}")

  # solr.ping()

  # solr.add([
  #   {
  #     "id": "doc_1",
  #     "title": "A test document",
  #   }
  #   # {
  #   #   "id": "doc_2",
  #   #   "title": "The Banana: Tasty or Dangerous?",
  #   #   "_doc": [
  #   #     {"id": "child_doc_1", "title": "peel"},
  #   #     {"id": "child_doc_2", "title": "seed"},
  #   #   ]
  #   # },
  # ])

  cp.set_cp(dir)

  doc = plugins.prism_map_index.erase(plugins.prism_map_index.main())
  score = plugins.prism_map_index.erase(plugins.general_score_by_prism.main(doc))

  report = es.index(
    index='report',
    document={
      'created_at': Timestamp.now(),
      'score': score,
      'namespace_app': str(doc["namespace_app"]),
      'meta': meta
    }
  )

  # document = es.index(
  #   index='source_map',
  #   document={
  #     'created_at': Timestamp.now(),
  #     'source_map': doc,
  #     'meta': meta
  #   }
  # )

  inspect(score)


  console.log(f"ElasticSearch: report/{report['result']}")
  # console.log(f"ElasticSearch: doc/{False} and report/{report['result']}")
