CREATE TABLE "Rental" (
    "id" VARCHAR PRIMARY KEY,
    "title" VARCHAR,
    "price" INT,
    "sqft" INT,
    "image" VARCHAR,
    "url" VARCHAR,
    "post_published_date" DATE,
    "lat" FLOAT,
    "long" FLOAT,
    "postal_code" VARCHAR,
    "FSA" VARCHAR,
    "rental_type" VARCHAR,
    "bedrooms" INT,
    "bathrooms" INT,
    "furnished" BOOL,
    "pet_friendly" BOOL,
    "description" VARCHAR,
    "source" VARCHAR NOT Null
);

CREATE TABLE "Crime" (
    "id" VARCHAR PRIMARY KEY,
    "lat" FLOAT,
    "long" FLOAT,
    "occurrencedate" DATE,
    "reporteddate" DATE,
    "premisetype" VARCHAR,
    "offence" VARCHAR,
    "MCI" VARCHAR,
    "division" VARCHAR,
    "neighbourhood" VARCHAR
);

CREATE TABLE "Bridge_Rental_Crime" (
    "id" VARCHAR PRIMARY KEY,
    "crime_id" VARCHAR NOT NULL,
    "rental_id" VARCHAR NOT NULL,
    "distance_rental_crime" float NOT NULL
);

CREATE TABLE "Community_Assets" (
    "id" VARCHAR PRIMARY KEY,
    "agency_name" VARCHAR,
    "site_name" VARCHAR,
    "service_name" VARCHAR,
    "service_name_2" VARCHAR,
    "address" VARCHAR,
    "site_city" VARCHAR,
    "site_postal_code" VARCHAR,
    "application" VARCHAR,
    "crisis_phone" VARCHAR,
    "service_description" VARCHAR,
    "eligibility" VARCHAR,
    "email" VARCHAR,
    "hours" VARCHAR,
    "languages" VARCHAR,
    "office_phone" VARCHAR,
    "primary_contact" VARCHAR,
    "primary_contact_email" VARCHAR,
    "toll_free_phone" VARCHAR,
    "website" VARCHAR,
    "taxonomy" VARCHAR,
    "fees" VARCHAR,
    "funding" VARCHAR,
    "dd_code" VARCHAR,
    "physical_access" VARCHAR,
    "category" VARCHAR,
    "FSA" VARCHAR
);

CREATE TABLE "Income" (
    "ID" VARCHAR PRIMARY KEY,
    "avg_income" INT,
	"FSA" VARCHAR UNIQUE
);

CREATE TABLE "FSA" ("FSA" VARCHAR PRIMARY KEY)

ALTER TABLE "Rental" ADD CONSTRAINT "fk_Rental_FSA" FOREIGN KEY("FSA")
REFERENCES "FSA" ("FSA");

ALTER TABLE "Community_Assets" ADD CONSTRAINT "fk_Community_Assets" FOREIGN KEY("FSA")
REFERENCES "FSA" ("FSA");

ALTER TABLE "Bridge_Rental_Crime" ADD CONSTRAINT "fk_Bridge_Rental_Crime_crime_id" FOREIGN KEY("crime_id")
REFERENCES "Crime" ("id");

ALTER TABLE "Bridge_Rental_Crime" ADD CONSTRAINT "fk_Bridge_Rental_Crime_rental_id" FOREIGN KEY("rental_id")
REFERENCES "Rental" ("id");

ALTER TABLE "Community_Assets" ADD CONSTRAINT "fk_Community_Assets_FSA" FOREIGN KEY("FSA")
REFERENCES "Income" ("FSA");

