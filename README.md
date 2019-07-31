# StackPros

# Technical Task: A Presidential assignment

### Assumptions:
- User will ping the listener API with a JSON payload (POST)
- The JSON is validated and formatted to match the RFP
- The requirement "Presidents should be divided up by century the year they were in power" will need more clarification, and is deferred for now.
- The output CSV is first ordered alphabetically by first name, and then last name. 
- Assuming inauguration happens on January 20 by the constitution the term date is marked as (01-20-yyyy) 

### Descriptions:
- Two Flask APIs (listener and processor)
- Each is containerized using docker
- docker-compose is then used to host the apis

To test the APIs run the following:

```.env
    docker-compose up
```

And when the two API's are built and running, from another window:

```.env
    curl -H Content-Type:application/json \
      -o \
      --request POST \
      --data '[
      {
        "id": 1,
        "president": 1,
        "nm": "George Washington",
        "pp": "None, Federalist",
        "tm": "1789-1797"
      }
      ...
      ]' \
      http://localhost:8001/
```






