These inputs:
```
$ curl -X 'POST'   'http://127.0.0.1:8000/message'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '{
  "message": "tell me a better joke"
}'
{"status":"ok"}

$ curl -X 'POST'   'http://127.0.0.1:8000/message'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '{
  "message": "tell me a better joke about planets"
}'
{"status":"ok"}

$ curl -X 'POST'   'http://127.0.0.1:8000/message'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '{
  "message": "Give me names of 3 beers"
}'
{"status":"ok"}
```

Produced these outputs:
```
$ cat output.txt 
{"input": "tell me a better joke", "result": "Why don't scientists trust atoms?\n\nBecause they make up everything!"}
{"input": "tell me a better joke about planets", "result": "Why did Mars go to the party?\n\nBecause it was a \"gas\"! (get it?)"}
{"input": "Give me names of 3 beers", "result": "Here are three beer names:\n\n1. Guinness\n2. Lagunitas IPA\n3. Corona"}
```

