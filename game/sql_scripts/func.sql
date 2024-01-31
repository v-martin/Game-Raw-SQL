CREATE OR REPLACE FUNCTION createCountry(token_name varchar(100), schemeId BIGINT)
    RETURNS BIGINT
AS
$$
DECLARE
    basic_gold INT = 1000;
    ci         INT;
BEGIN
    INSERT INTO play_country(schema_id, token, gold, active)
    VALUES (schemeId, token_name, basic_gold, TRUE)
    RETURNING id INTO ci;
    RETURN ci;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION createUserCountry(tokenName varchar(100), countryName varchar(50), countryKing varchar(100))
    RETURNS BIGINT
AS
$$
DECLARE
    schemeId INT;
    ci       INT;
BEGIN
    INSERT INTO play_countryschema(name, king) VALUES (countryName, countryKing) RETURNING id INTO schemeId;
    SELECT INTO ci createCountry(tokenName, schemeId);
    RETURN ci;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE createBotCountries(tokenName varchar(100))
AS
$$
DECLARE
    scheme play_countryschema%ROWTYPE;
BEGIN
    FOR scheme IN
        SELECT * FROM play_countryschema WHERE id < 10
        LOOP
            PERFORM createCountry(tokenName, scheme.id);
        END LOOP;
END
$$
    LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION chooseWarWinner(firstCountry INT, secondCountry INT)
    RETURNS INT
AS
$$
DECLARE
    first  play_army%ROWTYPE;
    second play_army%ROWTYPE;
BEGIN
    SELECT * INTO first FROM play_army WHERE country_id = firstCountry;
    SELECT * INTO second FROM play_army WHERE country_id = secondCountry;
    IF first.size * first.level > second.size * second.level THEN
        INSERT INTO play_war (loser_id, winner_id) VALUES (second.country_id, first.country_id);
        RETURN first.country_id;
    ELSE
        INSERT INTO play_war (loser_id, winner_id) VALUES (first.country_id, second.country_id);
        RETURN second.country_id;
    END IF;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION sellMaterial(materialTypeId INT, size INT, countryId INT, hubId INT)
    RETURNS VOID
AS
$$
DECLARE
    mat_cost INT;
BEGIN
    SELECT cost INTO mat_cost FROM play_materialcost WHERE material_type_id = materialTypeId AND hub_id = hubId;
    UPDATE play_material
    SET amount = amount - size
    WHERE country_id = countryId
      AND material_type_id = materialTypeId;
    UPDATE play_country
    SET gold = gold + mat_cost * size
    WHERE id = countryId;
END;
$$
    LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION getMaterialFromConstruction(constructionId INT, constructionProduction INT)
    RETURNS INT
AS
$$
DECLARE
    constr   play_construction%ROWTYPE;
    constr_t play_constructiontype%ROWTYPE;
    ano      INT;
BEGIN
    SELECT * INTO constr FROM play_construction WHERE id = constructionId;
    SELECT * INTO constr_t FROM play_constructiontype WHERE id = constr.construction_type_id;
    UPDATE play_material
    SET amount = amount + constr.level * constructionProduction
    WHERE country_id = constr.country_id
      AND material_type_id = constr_t.material_type_id
    RETURNING amount INTO ano;
    RETURN ano;
END;
$$
    LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION increaseArmyLevel(countryId INT, armyCost INT)
    RETURNS INT
AS
$$
DECLARE
    lev INT;
BEGIN
    UPDATE play_army
    SET level = level + 1
    WHERE country_id = countryId
    RETURNING level INTO lev;
    update play_country
    set gold = gold - armyCost * lev
    where id = countryId;
    RETURN lev;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION increaseConstructionLevel(constructionId INT, constructionCost INT)
    RETURNS INT
AS
$$
DECLARE
    lev       INT;
    countryId INT;
BEGIN
    UPDATE play_construction
    SET level = level + 1
    WHERE id = constructionId
    RETURNING level, country_id INTO lev, countryId;
    update play_country
    set gold = gold - constructionCost * lev
    where id = countryId;
    RETURN lev;
END;
$$ LANGUAGE plpgsql;