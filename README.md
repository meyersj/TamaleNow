# TamaleNow

Copyright (C) 2015 Jeffrey Meyers.
This program is released under the "MIT License".
Please see the file COPYING in this distribution for license terms.

#### Description

This repo contains an android app that a tamale vendor can use to broadcast their location.
The server code (Python/Flask) will recieve the location updates and store them in a Postgres database.
The database can then be queried through a simple api to check if any vendors are active
and where their current location is.

You can check out the [live display](http://meyersj.github.io/TamaleNow), but it will probably not
be very exciting as no vendors have started broadcasting their location.
