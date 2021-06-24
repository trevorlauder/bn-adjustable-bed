# BN Adjustable Bed Mock API and Socket Interface

[![CI](https://github.com/trevorlauder/bn_adjustable_bed/actions/workflows/ci.yml/badge.svg)](https://github.com/trevorlauder/bn_adjustable_bed/actions/workflows/ci.yml)
[![Release](https://github.com/trevorlauder/bn_adjustable_bed/actions/workflows/release.yml/badge.svg)](https://github.com/trevorlauder/bn_adjustable_bed/actions/workflows/release.yml)

<img alt="image" src="screenshots/controller_api.jpg">
<img alt="image" src="screenshots/bed_socket.jpg">


This project sets up an API and Socket Interface for the [Blissful Nights Wall Hugger Adjustable Bed with Massage and Alexa Voice Command](https://www.blissfulnights.com/collections/adjustable-bed-bases/products/wall-glide-adjustable-bed-with-massage-and-voice-command).

It allows you to control the bed using an HTTP API or the mobile app without having the mobile app or bed connect to the official servers hosted in AWS.

Not all of the socket communication protocol is understood, but enough of it has been reverse engineered to provide this funcionality.

## Docker Hub Links

* [app_api](https://hub.docker.com/r/trevorlauder/bn_adjustable_bed-app_api)
* [bed_socket](https://hub.docker.com/r/trevorlauder/bn_adjustable_bed-bed_socket)
* [controller_api](https://hub.docker.com/r/trevorlauder/bn_adjustable_bed-bed_socket)

## How to Use

To use it, you must hijack the DNS queries for `cm2.xlink.cn` and `api2.xlink.cn` and redirect them to your server.

`api2.xlink.cn` is used by the Ronin WiFi mobile app [ [ios](https://apps.apple.com/us/app/ronin-wifi/id1392877882) | [android](https://play.google.com/store/apps/details?id=com.keeson.rondurewifi) ].

`cm2.xlink.cn` is used by the bed.  The bed creates a persistent socket connection to this address.

Use of the mobile app is required to perform the initial setup and get the bed hooked up to your wireless network.  Once you have it setup, use of the mobile app is optional.

### Mobile App API

The HTTP API is exposed on port `80` and provides endpoints that will allow you to log into the app without creating an account.

#### Setup

1. An [example](https://github.com/trevorlauder/bn_adjustable_bed/blob/main/docker-compose.yml.example) Docker Compose Config File is provided.  It uses a default bridge network for communcation to the redis instance and configures the other 3 services to use an IP on a `macvlan` network named `lan`.  Change `<IP>` in the example file based on your network, they all need to be unique.  If you prefer, you could use the [main](https://github.com/trevorlauder/bn_adjustable_bed/blob/main/docker-compose.yml) Docker Compose Config File used for development as a start, it uses the default network and exposes the service ports through a single IP instead.  In this case the `Bed Controller API` will be on port `8080` instead of `80`.

1. Setup a directory for the services and run Docker Compose to start the 4 services (Redis, App API, Bed Socket Interface and Controller API).

```bash
mkdir bn_adjustable_bed

cd bn_adjustable_bed

wget https://github.com/trevorlauder/bn_adjustable_bed/blob/main/docker-compose.yml.example -O docker-compose.yml

# adjust <IP> and config for your network

docker-compose up
```

1. Hijack DNS queries to `api2.xlink.cn` and `cm2.xlink.cn` on your network so that they resolve to the IP address of your docker services.  If you're using separate IP's for each service, `api2.xlink.cn` should be pointed at the `app_api` service and `cm2.xlink.cn` should be pointed at the `bed_socket` service.

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
