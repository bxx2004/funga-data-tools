import json
import os
import random

a = []
for e in os.listdir("SGD/sgd/gene/1.json"):
    with open(os.path.join("SGD/gene", e)) as f:
        arr = json.loads(f.read())
        for gene in arr:
            ca = [gene['symbol'],round(random.random(),2)]
            if ca[0]:
                a.append(ca)
            if len(a) >=30:
                break
print(json.dumps(a))