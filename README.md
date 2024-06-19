<img src="/logo.png" alt="image" width="300" height="auto">

# VoiceGist - A WhatsApp Transcription Service

A simple project that creates a Twilio Whatsapp Bot to transcribe voice messages.


## Setup
Dependencies are organized using PDM and a PyProject.toml


## Technologies
* [Twilio API](https://www.twilio.com/de-de/messaging/channels/whatsapp) for Whatsapp Handling
* [CloudFlare Tunnel](https://www.cloudflare.com/products/tunnel/) for Serving
* [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper) for efficient transcriptions
* [Ollama](https://ollama.com/) for LLM Serving



## Deployment
Setup a Twilio account and configure a Whatsapp Sandbox. This will give you all the Twilio settings.
Next, setup a Cloudflare Account and create a Zero Trust tunnel for the URL where you set Twilio endpoint. If using the docker-copmose, you can point the tunnel locally to `` http://whatsapp-transcribe`` to connect the docker containers.
Last create a random API key to protect your transcription endpoint from misuse.

Fill out the environment template using this information in a ``.env`` file:

``` sh
TWILIO_ACCOUNT_SID=<Account Sid>
TWILIO_AUTH_TOKEN=<Auth Token>
TWILIO_PHONE_NUMBER=whatsapp:<twilio phone number>
TWILIO_WEBHOOK_URL=<Url confgiured in Twilio>
TUNNEL_TOKEN=<Cloud Flare Tunnel Token>
API_KEY=<Random API key e.g. (openssl rand -hex 32)>

TRANSCRIBE_MODEL=large # Whisper Model Size
SUMMARIZE_MODEL=qwen2:7b-instruct
OLLAMA_HOST=http://host.docker.internal:11434 # If running Ollama on Host
```


then run 

``` sh
docker-compose up -d
```

to start the deployment. 


## Twilio Limits
Limits for message sizes can be found [here](https://www.twilio.com/docs/conversations/conversations-limits)


## Development
To start developing simply install the dependencies using [PDM](https://github.com/pdm-project/pdm). For install PDM according to your operating system and then run

``` sh
pdm install
```
which automatically installs package and development dependencies.

Then you can run the tests and create the docs with

``` sh
make docs test
```

### Tests
Currently, the tests require a working Ollama setup. If you don't have Ollama running please install it directly or using docker and adjust ``conftest.py`` to your environment.
