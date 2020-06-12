# Projet_TravailBachelor

### Avant d'exécuter le code, il faut exécuter les commandes suivantes :

* Installer le Framework Flask

<code>pip install Flask</code>

* Installer l'extension permettant de créer une zone de glisser-déposer avec Flask

<code>pip install flask flask-uploads flask-dropzone</code>

* Mettre l'environnement de développement avant d'exécuter l'application web

<code>set FLASK_ENV=development</code>

* Exécuter l'application web

<code>python app.py</code>

### Problèmes rencontrés

Dans le fichier app.py qui se trouve dans Mon_APP, la fonction analyse() réalise les tâches suivantes :
1.	télécharger le fichier que l’utilisateur a glissé dans la zone de glisser-déposer ;
2.	appeller le modèle pour déduire la structure du document ;
3.	sauvegarder le résultat dans le dossier uploads ;
4.	afficher le résultat dans l’interface.

Le problème est que je voudrais afficher le résultat dans l’interface, mais je n’y arrive pas. Donc j’ai créé une fonction setsrc pour mettre le chemin du fichier qui contient le résultat dans la balise img du fichier index.html.

La fonction cancel() est exécutée lorsque l’utilisateur clique sur le bouton « Annuler ». Elle doit supprimer le fichier qui a été téléchargé dans le dossier uploads.
