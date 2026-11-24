drop database if exists pizzeria_projet_long;
create database if not exists pizzeria_projet_long;
use pizzeria_projet_long;

DROP TABLE IF EXISTS croutes;
CREATE TABLE IF NOT EXISTS croutes(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nom VARCHAR(50)
);

DROP TABLE IF EXISTS sauces;
CREATE TABLE IF NOT EXISTS sauces(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nom VARCHAR(50)
);

DROP TABLE IF EXISTS garnitures;
CREATE TABLE IF NOT EXISTS garnitures(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nom VARCHAR(50)
);

DROP TABLE IF EXISTS clients;
CREATE TABLE IF NOT EXISTS clients(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nom VARCHAR(50) NOT NULL,
    numero_de_telephone VARCHAR(15) NOT NULL
);

DROP TABLE IF EXISTS commandes;
CREATE TABLE IF NOT EXISTS commandes(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    statut ENUM('en attente de livraison', 'livrée') NULL,
    date_de_commande DATETIME,
    id_client INT,
    adresse VARCHAR(255) NOT NULL,
    FOREIGN KEY(id_client) REFERENCES clients(id)
);

DROP TABLE IF EXISTS pizzas;
CREATE TABLE IF NOT EXISTS pizzas(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    id_croute INT NOT NULL,
    id_sauce INT NOT NULL,
    id_commande INT,
    FOREIGN KEY(id_croute) REFERENCES croutes(id),
    FOREIGN KEY(id_sauce) REFERENCES sauces(id),
    FOREIGN KEY(id_commande) REFERENCES commandes(id)
);

DROP TABLE IF EXISTS pizzas_garnitures;
CREATE TABLE IF NOT EXISTS pizzas_garnitures(
    id_pizza INT NOT NULL,
    id_garniture INT NOT NULL,
    PRIMARY KEY(id_pizza, id_garniture),
    FOREIGN KEY(id_pizza) REFERENCES pizzas(id),
    FOREIGN KEY(id_garniture) REFERENCES garnitures(id)
);

/*Déclencheur*/
DELIMITER $$
CREATE TRIGGER statut_commande
BEFORE INSERT ON commandes
FOR EACH ROW
BEGIN
    SET NEW.statut = "en attente de livraison";
    SET NEW.date_de_commande = NOW();
END
$$
DELIMITER ;