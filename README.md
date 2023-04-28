# startgpt

1. Add Environment variables
`cp .env.example .env` & add values

2. Run motorhead server
```
docker run --name motorhead -p 8080:8080 -e MOTORHEAD_PORT=8080 -e REDIS_URL='<redis>' -e MOTORHEAD_LONG_TERM_MEMORY=true -e MOTORHEAD_MAX_WINDOW_SIZE=4 -e OPENAI_API_KEY='sk-<>' ghcr.io/getmetal/motorhead:latest
```

3. Run startgpt server
```
flask run
```