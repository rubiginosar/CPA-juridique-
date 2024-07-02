create database db_cpa
use db_cpa
/*création des tables*/
CREATE TABLE agence (
    code INT(5) PRIMARY KEY,
    intitule VARCHAR(70)
);
create table utilisateur (folio int(5) PRIMARY KEY , 
MDP int(5) , nom varchar(50) , prenom varchar(50) , qualite varchar(50));
ALTER TABLE utilisateur MODIFY MDP VARCHAR(50) NOT NULL;

CREATE TABLE agence (
    CODE_AGENCE INT PRIMARY KEY,
    AGENCE_NAME VARCHAR(70) -- Assuming you have a name or some attribute for the 'agence'
);

CREATE TABLE dossier (
    id_client VARCHAR(20) PRIMARY KEY,
    raison_sociale VARCHAR(100),
    nom VARCHAR(50),
    prenom VARCHAR(50),
    num_compte VARCHAR(20),
    agence VARCHAR(70),
    ACTIVITE VARCHAR(100),
    date_ouverture DATE,
    DATE_CLOTURE DATE,
    adresse VARCHAR(250),
    NUMEROTEL VARCHAR(20),
    CAUSE VARCHAR(200),
    NUM_REG_COM VARCHAR(50),
    DATE_REG_COM DATE,
    CODE_AGENCE INT(5),
    FOREIGN KEY (CODE_AGENCE) REFERENCES agence(code)
);


CREATE TABLE datetransmis (
    id INT(11) NOT NULL,
    daterecp DATE,
    dateenvoi DATE,
    etat VARCHAR(50),
    descriptif VARCHAR(500),
    folio INT(5),
    id_client VARCHAR(20),
    PRIMARY KEY (id_client, folio, id),
    CONSTRAINT fk_folio FOREIGN KEY (folio) REFERENCES utilisateur(folio),
    CONSTRAINT fk_id_client FOREIGN KEY (id_client) REFERENCES dossier(id_client)
);
alter table datetransmis add nom_agence varchar(70);         /*zedttttttt atttribuuuuuuuuuuuut la table datetransmiiis*/
DELIMITER //

CREATE TRIGGER before_insert_datetransmis
BEFORE INSERT ON datetransmis
FOR EACH ROW
BEGIN
    DECLARE max_id INT;

    -- Find the maximum id value for the given id_client and folio
    SELECT COALESCE(MAX(id), 0) INTO max_id
    FROM datetransmis
    WHERE id_client = NEW.id_client AND folio = NEW.folio;

    -- Increment the id value
    SET NEW.id = max_id + 1;
END //

DELIMITER ;



CREATE TABLE docs (
    id INT(11) NOT NULL AUTO_INCREMENT,
    id_client VARCHAR(50),
    element TEXT,
    PRIMARY KEY (id)
    CONSTRAINT fk_clinet FOREIGN KEY (id_client) REFERENCES dossier(id_client)
);

INSERT INTO agence (CODE, INTITULE) VALUES ( 118, 'Hussein Dey');
INSERT INTO agence (CODE, INTITULE) VALUES ( 119, 'Kouba');
INSERT INTO agence (CODE, INTITULE) VALUES ( 121, 'Ravin de femme sauvage');
INSERT INTO agence (CODE, INTITULE) VALUES ( 125, 'Kouba2');
INSERT INTO agence (CODE, INTITULE) VALUES ( 142, 'Les vergers');
INSERT INTO agence (CODE, INTITULE) VALUES ( 145, 'Sidi Moussa');
INSERT INTO agence (CODE, INTITULE) VALUES ( 146, 'Bab Ezzouar');
INSERT INTO agence (CODE, INTITULE) VALUES ( 154, 'El harrach');
INSERT INTO agence (CODE, INTITULE) VALUES ( 160, 'Mouhammadia');
INSERT INTO agence (CODE, INTITULE) VALUES ( 178, 'Rouiba');
INSERT INTO agence (CODE, INTITULE) VALUES ( 183, 'Baraki');
INSERT INTO agence (CODE, INTITULE) VALUES ( 185, 'Riad El Fatah');
INSERT INTO agence (CODE, INTITULE) VALUES ( 502, 'Guichet T4 aeroport d"Alger ');


INSERT INTO utilisateur (FOLIO, MDP, NOM, PRENOM, QUALITE) VALUES
         ('11111', '11111', 'Secrétaire', '', 'Secrétaire'),
         ('22222', '22222', 'Charge Étude', '', 'Charge étude'),
         ('33333', '33333', 'Charge Validation', '', 'Charge de validation'),
         ('44444', '44444', 'Directeur', '', 'Directeur');

alter table datetransmis add date_agence date;