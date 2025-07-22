import pickle  # importer le module pickle


class TopicMgr:  # Définir une classe nommée TopicMgr
    def load_topics(self):  # La fonction de chargement des sujets
        try:  # Essayez d'exécuter le code suivant
            with open(f'topics.pkl', 'rb') as file:  #  Ouvrez le fichier topic en mode de lecture binaire
                return pickle.load(file)  # Retourner les données chargées à partir du fichier
        except:  # Si une exception se produit
            return {}  # retourner un dict vide

    def save_topics(self, dct_data):  # la fct pour enregistrer le sujets 
        with open(f'topics.pkl', 'wb') as file:  # Ouvrez le fichier topic en mode de lecture binaire
            pickle.dump(dct_data, file, 0)  # ecrire les données dans le fichier
