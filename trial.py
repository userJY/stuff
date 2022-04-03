import base64
import codecs
import json
import sys
import pandas as pd

presentraw = None
present = None
past = None
presentraw = sys.stdin.read()


# IMPORTANT, our repo contains a cleaned model that removes candles and parses datetime
# but input data uses unix ms datetime enclosed in a candles json obj.

# input model from curl has candle which we remove

def InputModelextract(filein):
    tempdf = pd.read_json(filein)
    newdf = tempdf["candles"]
    newdf2 = pd.DataFrame(list(newdf))
    newdf2['datetime'] = pd.to_datetime(newdf2['datetime'],origin='unix',unit='ms')
    return newdf2

present = InputModelextract(presentraw)
print(present.shape())

# repo model, does not have candle

with codecs.open('ooout','r',encoding="base64") as f:
    past = pd.read_json(f)

print(past.shape())
presentrepo = pd.merge(past,present,how='outer')

print(presentrepo.shape())
result = presentrepo.to_json()
with open('ooout','wb') as f:
    newresult = base64.b64encode(result.encode('utf-8'))
    f.write(newresult)
