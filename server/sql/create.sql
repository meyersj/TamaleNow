-- Copyright (C) 2015 Jeffrey Meyers

BEGIN;

DROP TABLE IF EXISTS active;
CREATE TABLE active (
    vendor_id VARCHAR PRIMARY KEY,
    active BOOLEAN
);

DROP TABLE IF EXISTS locations;
CREATE TABLE locations (
    vendor_id VARCHAR NOT NULL,
    tstamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    geom GEOMETRY(Point, 4326),
    PRIMARY KEY (vendor_id, tstamp)
);

COMMIT;

