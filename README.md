# apisix-logger

1. Clone APISIX docker

```bash
git clone https://github.com/apache/apisix-docker
```

2. Add plugin to config.yaml

Go to /example/apisix_conf/config.yaml and add the following lines to the file:

```yaml
plugins:                           # plugin list (sorted by priority)
  - proxy-rewrite                  # priority: 1008
  - http-logger                    # priority: 410
```

3. Start APISIX docker

Go to /example

```bash
docker compose up -d
```

4. Check if the plugin is loaded

```bash
curl --location --request GET 'http://127.0.0.1:9180/apisix/admin/plugins/list'
```
5. Start the logger

Go to /logger in this repo

```bash
docker compose up -d
```

6. Add a route

```bash
curl --location --request PUT 'http://127.0.0.1:9180/apisix/admin/routes' \
--header 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' \
--header 'Content-Type: application/json' \
--data '{
  "id": "test",
  "uri": "/test",
  "methods": ["POST"],  
  "upstream": {
    "type": "roundrobin",
    "nodes": {
      "host.docker.internal:3000": 1
    }
  },
    "plugins": {  
        "proxy-rewrite": {  
            "regex_uri": ["^/chat(.*)", "/api/v1/process/7a0cd6ca-454c-4cf2-b6c3-daf712eded50$1"]  
        },
        "http-logger": {
            "uri": "http://host.docker.internal:8080/logs",
            "include_req_body": true,
            "include_resp_body": true
        },
        "total_tokens_counter": {}
    }  
}'
```

7. Test the route

```bash
curl --location 'http://localhost:9080/chat' \
--header 'x-api-key: sk-SWkSvU6jTkOXzA5filIbYy0Qk7IsbJhc2jFbFRsGSPI' \
--header 'Content-Type: application/json' \
--data '{"inputs": {"input":"Hi"}}'
```

8. Check the logs

```bash
docker logs apisix-logger_logger_1
```