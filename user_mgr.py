import pickle  # importer le module pickle


class UserMgr:  # definir le nom de la class
    def load_users(self, user_type):  # le fct d'initialement
        try:  # Essayez d'exécuter le code suivant
            with open(f'{user_type}.pkl', 'rb') as file:  # Ouvrez le fichier correspondant en mode de lecture binaire
                return pickle.load(file)  # Retournez les données chargées à partir du fichier
        except:  # Si une exception se produit.
            return {}  # Retourner un dictionnaire vide

    def save_users(self, user_type, dct_data):  # La fonction pour sauvegarder les utilisateur
        with open(f'{user_type}.pkl', 'wb') as file:  #Ouvrir le fichier correspondant en mode écriture binaire 
            pickle.dump(dct_data, file, 0)  # Écrire les données dans le fichier :
    def is_company_exists(self, company_name, com_act=None):  #La fonction pour vérifier si une entreprise existe 
        dct = self.load_users('company')  #Charger les informations sur les utilisateurs de l'entreprise
        for k, v in dct.items():  # Parcourir le dictionnaire des informations sur les utilisateurs de l'entreprise
            if v[2] == company_name:  #Si le nom de l'entreprise correspond
                if com_act is None:  # Si aucun compte d'entreprise n'est fourni
                    return True  # Retourner True
                else:  # sinon
                    if com_act != k:  # Si le compte d'entreprise fourni ne correspond pas au compte actuellement parcouru
                        return True  #retourne true
        return False  # Si aucune entreprise correspondante n'est trouvée, retourner False





