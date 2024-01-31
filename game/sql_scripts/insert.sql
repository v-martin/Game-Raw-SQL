INSERT INTO play_materialtype (name)
VALUES ('Камень'),
       ('Железо'),
       ('Древесина'),
       ('Зерно');

INSERT INTO play_constructiontype (name, material_type_id)
VALUES ('Каменоломня', 1),
       ('Шахта', 2),
       ('Лесопилка', 3),
       ('Ферма', 4);

INSERT INTO play_countryschema (name, king)
VALUES ('Британия', 'Виктория'),
       ('Испания', 'Хосе'),
       ('Россия', 'Петр Великий'),
       ('Швеция', 'Карл 12'),
       ('Румыния', 'Дракула'),
       ('Франция', 'Наполеон'),
       ('Германия', 'Вильгельм 2'),
       ('Китай', 'Мао Цзе Дун'),
       ('Япония', 'Хирохито'),
       ('США', 'Рузвельт');

CREATE OR REPLACE FUNCTION createTradingHub()
    RETURNS VOID
AS
$$
DECLARE
    hub_id INT;
BEGIN
    FOR i IN 1..100
        LOOP
            INSERT INTO play_tradinghub (location) VALUES ('точка торговли ' || i) RETURNING id INTO hub_id;
            INSERT INTO play_materialcost (material_type_id, hub_id, cost)
            VALUES (1, hub_id, CASE i % 4 WHEN 1 THEN 40 ELSE 10 END),
                   (2, hub_id, CASE i % 4 WHEN 2 THEN 40 ELSE 10 END),
                   (3, hub_id, CASE i % 4 WHEN 3 THEN 40 ELSE 10 END),
                   (4, hub_id, CASE i % 4 WHEN 4 THEN 40 ELSE 10 END);
        END LOOP;
END;
                  $$
LANGUAGE plpgsql;

SELECT createtradinghub();
