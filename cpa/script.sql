/*création des tables*/

CREATE TABLE agence (
    code INT(5) PRIMARY KEY,
    intitule VARCHAR(70)
);
create table utilisateur (folio int(5) PRIMARY KEY , 
MDP int(5) , nom varchar(50) , prenom varchar(50) , qualite varchar(50));
ALTER TABLE utilisateur MODIFY MDP VARCHAR(50) NOT NULL;

create table dossier(id_client varchar(20) primary key , raison_sociale varchar(100) , nom varchar(50) , 
prenom varchar(50), num_compte varchar(20) , agence varchar(70), ACTIVITE  varchar(100) 
date_ouverture date ,DATE_CLOTURE date , adresse varchar(250) , NUMEROTEL   varchar(20)  , 
CAUSE  varchar(200) , NUM_REG_COM  varchar(50), DATE_REG_COM date  , CODE_AGENCE  int(5) REFERENCES(agence));

CREATE TABLE datetransmis (
    id INT(11) AUTO_INCREMENT,
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
         ('F1', 'mdp1', 'Secrétaire', '', 'Secrétaire'),
         ('F2', 'mdp2', 'Charge Étude', '', 'Charge étude'),
         ('F3', 'mdp3', 'Charge Validation', '', 'Charge de validation'),
         ('F4', 'mdp4', 'Directeur', '', 'Directeur');

