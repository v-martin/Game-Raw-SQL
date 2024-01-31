CREATE INDEX ON play_countryschema USING btree (id);
CREATE INDEX ON play_army USING btree (size, level);
CREATE INDEX ON play_army USING hash (country_id);
CREATE INDEX ON play_materialcost USING hash (hub_id);
CREATE INDEX ON play_materialcost USING hash (material_type_id);
CREATE INDEX ON play_material USING hash (country_id);
CREATE INDEX ON play_material USING hash (material_type_id);
CREATE INDEX ON play_country USING hash (id);
CREATE INDEX ON play_construction USING hash (id);
CREATE INDEX ON play_constructiontype USING hash (id);



