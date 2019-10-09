This app uses the USPS Track/Confirm Fields API to get tracking information for each tracking number.

https://www.usps.com/business/web-tools-apis/track-and-confirm-api.pdf (See page 8 for more details).

This app is capable of doing asyncronous requests! This greatly improves speed because there is less downtime waiting for responses. It also includes a way to limit the amount of requests at any given time.

In the future I want to implement a way to not only limit simultaneous connections, but also limit the amount of requests in a given period.
