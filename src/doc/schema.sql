

--------DELETE TABLE-----------
DROP TABLE IF EXISTS organizations;
DROP TABLE IF EXISTS devices;
DROP TABLE IF EXISTS sensors;
DROP TABLE IF EXISTS sensor_data;



-- Install UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create organizations

CREATE TABLE organizations (
    organization_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    organization_name VARCHAR(255) NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Test entries for organizations
INSERT INTO organizations (organization_id, organization_name)
VALUES (uuid_generate_v4(), 'Neurithm');
INSERT INTO organizations (organization_id, organization_name)
VALUES (uuid_generate_v4(), 'Wingman');
INSERT INTO organizations (organization_id, organization_name)
VALUES (uuid_generate_v4(), 'GradientLabs');



CREATE TABLE devices (
    device_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    device_name VARCHAR(255) NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    organization_id UUID REFERENCES organizations(organization_id) ON DELETE CASCADE
);

CREATE TABLE sensors (
    sensor_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    sensor_type VARCHAR(100) NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    device_id UUID REFERENCES devices(device_id) ON DELETE CASCADE
);

CREATE TABLE sensor_data (
    sensor_id UUID REFERENCES sensors(sensor_id) ON DELETE CASCADE,
    value FLOAT NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



--------DELETE ALL ROWS-----------
DELETE FROM organizations;
DELETE FROM devices;
DELETE FROM sensors;
DELETE FROM sensor_data;



--------SELECT ROWS------------
SELECT * FROM organizations;
SELECT * FROM devices;
SELECT * FROM sensors;
SELECT * FROM sensor_data;


















