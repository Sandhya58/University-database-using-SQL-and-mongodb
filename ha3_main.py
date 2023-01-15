import json
import ha3lib as ha

f = open("sampleUnivDB.json", "r")
input = json.loads(f.read())

output = ha.ha3(input)

print(json.dumps(output))
