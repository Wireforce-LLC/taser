from datetime import datetime
from elasticsearch import Elasticsearch
from pandas import Timestamp
from pydash import uniq
from rich import inspect
from rich.console import Console
from pymongo import MongoClient

import cp
import plugins.prism_map_index
import plugins.general_score_by_prism

es = Elasticsearch("http://172.81.180.191:9241/")
mongo = MongoClient('mongodb://172.81.180.191:27017/')

console = Console()

mongo_docs = mongo.taser_docs

def test(dir, meta):
  vpath = f'{meta.get("sender_id", "")}/{meta.get("filename", "")}'

  console.log(f"🤖 Autotest: {dir}; vpath: {vpath}")

  if not cp.set_cp(dir):
    console.log(f"Failed to go to the source code directory")

  doc = plugins.prism_map_index.erase(plugins.prism_map_index.main(dir))
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

  net = es.index(
    index='net',
    document={
      'created_at': Timestamp.now(),
      'namespace_app': str(doc["namespace_app"]),
      'sender_id': meta.get('sender_id'),
    }
  )

  revisoro_warn_files = []

  if doc.get('revesiro', None):
    revisoro_warn_files = list(
      map(
        lambda x: x.get('package_name'),
        doc.get('revesiro', {}).get('warn_files')
      )
    )

  revisoro = es.index(
    index='revisoro',
    document={
      'created_at': Timestamp.now(),
      'namespace_app': str(doc["namespace_app"]),
      'sender_id': meta.get('sender_id'),
      'revisoro_percent': doc.get('revisoro_percent', -1),
      'revisoro_used_apps': uniq(revisoro_warn_files),
    }
  )

  count_docs = mongo_docs.docs.count_documents({
    'vpath': vpath,
  })


  if count_docs == 0:
    inserted_doc = mongo_docs.docs.insert_one({
      'vpath': vpath,
      'created_at': datetime.utcnow(),
      'source_map': doc,
      'meta': meta
    })

  else:
    inserted_doc = None

  inspect(score)

  # console.log(f"ElasticSearch: report/{report['result']} inserted_doc/{inserted_doc} net/{net['result']}")
  # console.log(f"ElasticSearch: doc/{False} and report/{report['result']}")
