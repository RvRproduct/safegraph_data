# %%
# https://towardsdatascience.com/connecting-to-a-graphql-api-using-python-246dda927840
import requests
import json
import jsonlines
import pandas as pd
# %%
query = """
query {
    characters {
    results {
      name
      status
      species
      type
      gender
    }
  }
}
"""

query = """
query {
    characters {
    results {
      name
      status
      species
      type
      gender
      image
      episode{
        episode
        name
        air_date
      }
    }
  }
}
"""
# %%
url = 'https://rickandmortyapi.com/graphql/'
r = requests.post(url, json={'query': query})
print(r.status_code)
print(r.text)
# %%
json_data = json.loads(r.text)
# %%
df_data = json_data['data']['characters']['results']
df = pd.json_normalize(df_data)
# %%

# %%

for i, value in enumerate(df_data):
  print(i)
  idat = df_data[i].copy()
  number = list()
  name = list()
  airdate = list()
  for j, jvalue in enumerate(idat['episode']):
    iseason = idat['episode'][j]
    number.append(iseason['episode'])
    name.append(iseason['name'])
    airdate.append(iseason['air_date'])
  df_data[i]['episode'] = {
    'number':number,
    "name":name,
    "air_date":airdate}

# %%  
# https://blog.softhints.com/python-convert-json-to-json-lines/  
with jsonlines.open('output.jsonl', mode='w') as writer:
    writer.write_all(df_data)

# %%
pd.read_json("output.jsonl", lines=True)
# %%
