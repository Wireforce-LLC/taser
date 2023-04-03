import sys
import warnings

import executor

warnings.simplefilter('ignore')

if 'exec' in sys.argv:
  file_src = sys.argv[sys.argv.index('exec') + 1]

  with open(file_src, 'r') as file:
    term = file.read()
    file.close()

    print(executor.input_execute(term))

  exit(0)