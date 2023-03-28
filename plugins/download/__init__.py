from cp import set_cp
from download import download
PROMPT_TOOLKIT_ARGS = ""

def main(url, file_path, progressbar=True):
  path = download(
    url,
    f"./mount/downloads/{file_path}",
    progressbar=progressbar,
    timeout=30,

  )

  return path
