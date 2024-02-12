CREATE OR REPLACE FUNCTION createSubObject()
    RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO play_army (size, level, country_id) VALUES (1, 1, new.id);
    INSERT INTO play_material (country_id, material_type_id, amount)
    VALUES (new.id, 1, 0),
           (new.id, 2, 0),
           (new.id, 3, 0),
           (new.id, 4, 0);
    INSERT INTO play_traderelation (country_id, hub_id)
    VALUES (new.id, new.id % 100 + 1),
           (new.id, (new.id * 2) % 100 + 1),
           (new.id, (new.id * 3) % 100 + 1),
           (new.id, (new.id * 4) % 100 + 1);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION loserArmyFunc()
    RETURNS TRIGGER AS
$$
BEGIN
    DELETE
    FROM play_army
    WHERE country_id = NEW.loser_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION winnerArmyFunc()
    RETURNS TRIGGER AS
$$
BEGIN
    WITH loser AS (SELECT *
                   FROM play_army
                   WHERE country_id = NEW.loser_id)
    UPDATE play_army AS a
    SET size = CEIL((a.size * a.level - (loser.size * loser.level * 0.5)) / a.level)
    FROM loser
    WHERE a.country_id = NEW.winner_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION changeConstructionOwnership()
    RETURNS TRIGGER AS
$$
BEGIN
    UPDATE play_construction
    SET country_id = NEW.winner_id
    WHERE country_id = NEW.loser_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION deactivateCountry()
    RETURNS TRIGGER AS
$$
BEGIN
    UPDATE play_country
    SET active = FALSE
    WHERE id = NEW.loser_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION changeTradingRelations()
    RETURNS TRIGGER AS
$$
BEGIN
    UPDATE play_traderelation
    SET country_id = NEW.winner_id
    WHERE country_id = NEW.loser_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER loserArmy
    AFTER INSERT
    ON play_war
    FOR EACH ROW
EXECUTE PROCEDURE loserArmyFunc();

CREATE OR REPLACE TRIGGER winnerArmy
    AFTER INSERT
    ON play_war
    FOR EACH ROW
EXECUTE PROCEDURE winnerArmyFunc();

CREATE OR REPLACE TRIGGER subObjCreation
    AFTER INSERT
    ON play_country
    FOR EACH ROW
EXECUTE PROCEDURE createSubObject();

CREATE OR REPLACE TRIGGER constructionOwnership
    AFTER INSERT
    ON play_war
    FOR EACH ROW
EXECUTE PROCEDURE changeConstructionOwnership();

CREATE OR REPLACE TRIGGER countryDeactivation
    AFTER INSERT
    ON play_war
    FOR EACH ROW
EXECUTE PROCEDURE deactivateCountry();

CREATE OR REPLACE TRIGGER tradingRelations
    AFTER INSERT
    ON play_war
    FOR EACH ROW
EXECUTE PROCEDURE changeTradingRelations();