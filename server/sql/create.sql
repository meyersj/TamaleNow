-- Copyright (C) 2015 Jeffrey Meyers

BEGIN;

DROP TABLE IF EXISTS active;
CREATE TABLE active (
    vendor_id VARCHAR PRIMARY KEY,
    active BOOLEAN
);

DROP TABLE IF EXISTS locations;
CREATE TABLE locations (
    vendor_id VARCHAR PRIMARY KEY,
    tstamp TIMESTAMP WITHOUT TIME ZONE,
    geom GEOMETRY(Point, 4326)
);

COMMIT;

