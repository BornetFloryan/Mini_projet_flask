DROP TABLE IF EXISTS depense, categorie_depense;


CREATE TABLE categorie_depense (
    id_categorie INT AUTO_INCREMENT,
    libelle_categorie VARCHAR(255),
    PRIMARY KEY (id_categorie)
);

CREATE TABLE depense (
    id_depense INT AUTO_INCREMENT,
    destinataire_depense VARCHAR(255),
    montant DECIMAL(10,2),
    description VARCHAR(255),
    date_depense DATE,
    categorie_id INT,
    destinataire VARCHAR(255),
    image VARCHAR(255),
    PRIMARY KEY (id_depense),
    FOREIGN KEY (categorie_id) REFERENCES categorie_depense(id_categorie)
);


INSERT INTO categorie_depense(id_categorie, libelle_categorie)VALUES
(NULL,'Autoroute'),
(NULL,'Carburant'),
(NULL,'Repas'),
(NULL,'Hebergement');

INSERT INTO depense(id_depense, destinataire_depense, montant, description, date_depense,categorie_id, destinataire,image)  VALUES
(NULL,'Service d\'autoroute Vinci',35,'Péages Belfort-Lyon','2014-04-20',1,'Autoroute Paris/Rhone','img_depense_1.png'),
(NULL,'Organisation ACD',410.47,'Comité de direction','2014-07-03',3,NULL,'img_depense_2.png'),
(NULL,'intendance UTBM',120,'forum étudiants','2014-08-18',1, NULL,'img_depense_4.png'),
(NULL,'Autoroute Ouest',25.5,'Péages Paris-Nantes','2014-07-28',1,NULL,'img_depense_3.png'),
(NULL,'TotalEnergies',45,'Sans plomb 95 35L','2014-04-14',2,NULL,'img_depense_5.png'),
(NULL,'Hilton Hotels & Resorts' ,842,'Hotel mercure Paris','2014-01-06',4,'Hotel Hilton Paris','img_depense_6.png'),
(NULL,'Service d\'autoroute Vinci' ,42.00,'Péages Belfort-Paris','2014-12-07',1,NULL,'img_depense_1.png'),
(NULL,'TotalEnergies' ,75,'Diezel 60L','2014-10-31',2,NULL,'img_depense_3.png');