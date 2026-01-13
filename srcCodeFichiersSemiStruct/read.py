import json

with open('BDD101\data.json', 'r') as f:
    data = json.load(f)
print(json.dumps(data["features"], sort_keys=True, indent=4))

data["features"][0]["geometry"]["coordinates"] = [78.0, 45.0]
data["features"][0]["properties"]["prop1"] = "value1"

with open('BDD101\data.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

f.close()

print(json.dumps(data["features"], sort_keys=True, indent=4))