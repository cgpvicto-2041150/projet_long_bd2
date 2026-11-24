
/*Insertion des données*/
INSERT INTO garnitures(nom) VALUES("Pepperoni"), ("Champignons"), ("Oignons"), ("Poivrons"), 
	("Olives"), ("Anchois"), ("Bacon"), ("Poulet"), ("Maïs"), ("Fromage"), ("Piments forts");
    
INSERT INTO croutes(nom) VALUES("Classique"), ("Mince"), ("Épaisse");

INSERT INTO sauces(nom) VALUES("Tomate"), ("Spaghetti"), ("Alfredo");

/*Données tests*/
INSERT INTO clients (nom, numero_de_telephone)
VALUES ('Marie Tremblay', '819-555-1234'), ("Toto tata","888-917-9202");

INSERT INTO commandes (id_client, adresse)
VALUES (1, '123 rue Principale, Victoriaville'), ('2', '321 rure principale, Totoville');

INSERT INTO pizzas (id_croute, id_sauce, id_commande)
VALUES (1, 1, 1), (2,3,2);

INSERT INTO pizzas_garnitures (id_pizza, id_garniture)
VALUES (1, 1), (1, 2), (2,5),(2,3), (2,4);

