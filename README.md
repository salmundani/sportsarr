# Sportsarr

## Overview

Computer Use agent that given a sport and two teams playing a live match:

1. Scrapes FMHY[https://fmhy.net/] live sports section
1. Tries one of the FMHY's starred URLs at a time until it finds a valid stream
1. Once found, opens the stream, plays it and sets it to fullscreen mode

It uses OpenAGI's Lux as the Computer Use model.

Built for "OpenAGI Computer Use: Launch & Hack Night" Hackathon at GitHub HQ, San Francisco

## Pre-requesites

- Install uv
- Get OpenAGI API key: https://developer.agiopen.org/api-keys/
- Run `uv sync`
- Source .venv and run `oagi agent permission` until it doesn't complain about missing permissions
- Install ublock origin lite for Chrome
- Setup .env with 

```sh
OAGI_API_KEY=sk-...
OAGI_BASE_URL=https://api.agiopen.org
```

Run with `uv run main.py "<team1>" "<team2>" "<sport_name>"`

## Motivation

I built this tool as I wanted to watch an Argentinean footbal match from the US, and there was no legal way to view it. I had to explore these shady sites, full of broken links and streams which took me like 15 minutes to find one that works. This project automates this cumbersome task away. Don't use it for pirating. You wouldn't steal a car.
