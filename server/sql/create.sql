-- Copyright (C) 2015 Jeffrey Meyers
--
-- This program is released under the "MIT License".
-- Please see the file COPYING in this distribution for
-- license terms.

BEGIN;

DROP TABLE IF EXISTS active;
CREATE TABLE active (
    vendor_id VARCHAR NOT NULL,
    tstamp TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    active BOOLEAN,
    PRIMARY KEY (vendor_id, tstamp)
);

DROP TABLE IF EXISTS locations;
CREATE TABLE locations (
    vendor_id VARCHAR NOT NULL,
    tstamp TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    geom GEOMETRY(Point, 4326),
    PRIMARY KEY (vendor_id, tstamp)
);

COMMIT;

