# BN Adjustable Bed Mock API and Socket Interface

_**This project is not an official project of, and is in no way affiliated with, Blissful Nights or the Ronin Wifi mobile app**_

[![codecov](https://codecov.io/gh/trevorlauder/bn-adjustable-bed/branch/main/graph/badge.svg?token=DHZC7X92PP)](https://codecov.io/gh/trevorlauder/bn-adjustable-bed)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/trevorlauder/bn-adjustable-bed/main.svg)](https://results.pre-commit.ci/latest/github/trevorlauder/bn-adjustable-bed/main)
[![CI](https://github.com/trevorlauder/bn-adjustable-bed/actions/workflows/ci.yml/badge.svg)](https://github.com/trevorlauder/bn-adjustable-bed/actions/workflows/ci.yml)
[![Release](https://github.com/trevorlauder/bn-adjustable-bed/actions/workflows/release.yml/badge.svg)](https://github.com/trevorlauder/bn-adjustable-bed/actions/workflows/release.yml)
[![PyPI version](https://badge.fury.io/py/bn-adjustable-bed.svg)](https://badge.fury.io/py/bn-adjustable-bed)

![image](https://user-images.githubusercontent.com/2594126/141405656-401480c5-f23f-4846-a241-405e7ca7c813.png)
![image](https://user-images.githubusercontent.com/2594126/141405860-21e5c871-292e-42c5-a5ab-f0efaf072c0f.png)


This project sets up an HTTP API and Socket Interface for the [Blissful Nights Wall Hugger Adjustable Bed with Massage and Alexa Voice Command](https://www.blissfulnights.com/collections/adjustable-bed-bases/products/wall-glide-adjustable-bed-with-massage-and-voice-command).

I can control the bed using the HTTP API or the mobile app without having anything connected to the official servers hosted in AWS.

I have the HTTP API hooked up to my iOS Shortcuts which allows me to use it in my automation.

Not all of the socket communication protocol is understood, but enough of it has been reverse engineered to provide this functionality.

## Docker Hub Links

* [bn-adjustable-bed](https://hub.docker.com/r/trevorlauder/bn-adjustable-bed)

## How to Use

To use it, you must hijack the DNS queries for `cm2.xlink.cn` and `api2.xlink.cn` and redirect them to your server.

`api2.xlink.cn` is used by the Ronin WiFi mobile app [ [ios](https://apps.apple.com/us/app/ronin-wifi/id1392877882) | [android](https://play.google.com/store/apps/details?id=com.keeson.rondurewifi) ].

`cm2.xlink.cn` is used by the bed.  The bed creates a persistent socket connection to this address.

Use of the mobile app is required to perform the initial setup and get the bed hooked up to your wireless network.  Once you have it setup, use of the mobile app is optional.

### Mobile App API

The HTTP API is exposed on port `80` and provides endpoints that will allow you to log into the app without creating an account.

#### Setup

1. An [example](https://github.com/trevorlauder/bn-adjustable-bed/blob/main/docker-compose.yml.example) Docker Compose Config File is provided.  It uses a default bridge network for communcation to the redis instance and configures the other 3 services to use an IP on a `macvlan` network named `lan`.  Change `<IP>` in the example file based on your network, they all need to be unique.  If you prefer, you could use the [main](https://github.com/trevorlauder/bn-adjustable-bed/blob/main/docker-compose.yml) Docker Compose Config File used for development as a start, it uses the default network and exposes the service ports through a single IP instead.  In this case the `Bed Controller API` will be on port `8080` instead of `80`.

1. Setup a directory for the services and run Docker Compose to start the 4 services (Redis, App API, Bed Socket Interface and Controller API).

```bash
mkdir bn-adjustable-bed

cd bn-adjustable-bed

wget https://github.com/trevorlauder/bn-adjustable-bed/blob/main/docker-compose.yml.example -O docker-compose.yml

# adjust <IP> and config for your network

docker-compose up
```

1. Hijack DNS queries to `api2.xlink.cn` and `cm2.xlink.cn` on your network so that they resolve to the IP address of your docker services.  If you're using separate IP's for each service, `api2.xlink.cn` should be pointed at the `app-api` service and `cm2.xlink.cn` should be pointed at the `bed-socket` service.

1. Log into the Ronin Wifi mobile app using any email address and password, neither need to be valid.  Make sure your mobile device is connected to your network so that is resolves your hijacked domains properly.

1. Select `My Bed` from the menu and then `Connect new bed`

    * Follow the instructions in the app to "_Long press the Foot Up and Down buttons for 5 seconds until you hear a beep every 3 seconds_".  Click `Next`

    * Connect your mobile device to the `KeesonAp-XXXXXXXXXX` Wireless SSID.  Click `Next`

    * Continue with the instructions and provide the Wireless network credentials for the network you wish to connect the bed to.

    * The bed will beep a couple times and connect to your Wireless Network.  The bed should show up shortly in the list with an option to `Connect`.  Skip this part as not enough of the communications protocol has been reverse engineered at this point for the app to completely perform the setup.  At this point you can force quit the app and re-open it, you should be able to control the bed now and see it in the list of beds.

### Bed Controller API

The Bed Controller API is exposed on port `80` and provides an endpoint that allows you to send commands to the bed.

This can be easily added to Siri Shortcuts or similar tools to add bed control to whatever automation platform you use.

```bash

# Tell the bed to move to the flat position
curl -X 'PUT' \
  'http://bn-adjustable-bed-controller.changethistoyourdomain.com/command?name=flat' \
  -H 'accept: application/json'

# Tell the bed to move to the Zero-G position
curl -X 'PUT' \
  'http://bn-adjustable-bed-controller.changethistoyourdomain.com/command?name=zero_g' \
  -H 'accept: application/json'

# Tell the bed to move to the Preset I position
curl -X 'PUT' \
  'http://bn-adjustable-bed-controller.changethistoyourdomain.com/command?name=preset_one' \
  -H 'accept: application/json'

# Tell the bed to move to the Preset II position
curl -X 'PUT' \
  'http://bn-adjustable-bed-controller.changethistoyourdomain.com/command?name=preset_two' \
  -H 'accept: application/json'

# Tell the bed to move to the Preset III position
curl -X 'PUT' \
  'http://bn-adjustable-bed-controller.changethistoyourdomain.com/command?name=preset_three' \
  -H 'accept: application/json'
```
