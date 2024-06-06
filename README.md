# WhatsApp Transcribe

A simple project that create a Twilio Whatsapp Bot to transcribe voice messages.


## Setup
Dependencies are organized using PDM and a PyProject.toml


## Technologies
* Twilio API Whatsap Handling
* CloudFlare Tunnel for Serving


## Deployment
Fill out the environment template:

``` sh
TWILIO_ACCOUNT_SID=<Account Sid>
TWILIO_AUTH_TOKEN=<Auth Token>
TWILIO_PHONE_NUMBER=whatsapp:<twilio phone number>
TUNNEL_TOKEN=<Cloud Flare Tunnel Token>
API_KEY=<Random API key e.g. (openssl rand -hex 32)>
```


then run 

``` sh
docker-compose --env-file <env-file> up -d
```

to start the deployment. You probably need to configure the tunnel to correctly route traffic to `http://whatsapp-transcribe`
