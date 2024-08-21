# A2SV AI for Impact Hackathon voting bot
This is a repository for telegram bot that collects voting data for hackathon projects.

## Getting Started
### Method One : Manual
> Install the requirements.
```bash
pip install -r requirements.txt
```

> Setup your environmental variables
- Add a .env file in the project root directory with the following in it.

```.env
BOT_TOKEN=<Your Bot Token>
MONGO_DB_CONNECTION_STRING=<Your Mongodb Connection String>
ADMIN_IDS=<Comma separated list of admin ids>
PORT=<Port to run the bot on>
WEBHOOK_URL=<Webhook url>
```

> Run the project
```bash
python3 main.py
```

### Method Two : Docker (Recommended)
> Build the docker image
```bash
docker build -t a2sv-ai-for-impact-hackathon-voting-bot .
```

> Run the docker container
```bash
docker run -d <choose your image name>
```