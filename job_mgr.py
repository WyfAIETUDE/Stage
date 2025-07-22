import pickle  #Importer le module pickle :


class JobMgr:  #Définir une classe nommée JobMgr
    def load_jobs(self):  # La fonction de chargement des postes 
        try:  # Essayez d'exécuter le code suivant
            with open(f'jobs.pkl', 'rb') as file:  # Ouvrir le fichier nommé 'jobs.pkl' en mode lecture binaire
                return pickle.load(file)  # Retourner les données chargées à partir du fichier 
        except:  # Si une exception se produit 
            return []  # Retourner une liste vide

    def save_jobs(self, lst_data):  # La fonction pour sauvegarder les postes
        with open(f'jobs.pkl', 'wb') as file:  # Ouvrir le fichier nommé 'jobs.pkl' en mode écriture binaire :
            pickle.dump(lst_data, file, 0)  # Écrire les données dans le fichier 

    def is_company_job_exists(self, company_name, job_name):  # La fonction pour vérifier si un poste dans une entreprise existe
        for l in self.load_jobs():  # Parcourir les postes chargés
            if l[0] == company_name and l[1] == job_name:  # Si le nom de l'entreprise correspond au titre du poste
                return True  # Retourne True
        return False  # Si aucun poste ne correspond, retourne False

    def add_job(self, data):  # Ceci est un exemple simplifié, vous devrez l'adapter à votre propre système.
        lst_jobs = self.load_jobs()  # Charger la liste des postes
        lst_jobs.append(data)  # Ajouter les nouvelles données de poste à la liste.
        self.save_jobs(lst_jobs)  # Enregistrer la liste des postes mise à jour

    # une fonction d'Obtenir la poste spécifique d'une entreprise
    def get_company_job(self, company_name, job_name):
        for l in self.load_jobs():  # Parcourir les postes chargés
            if l[0] == company_name and l[1] == job_name:  #  si le nom de l'entreprise correspond au nom du poste
                return l  # retourne ce poste
        return None  # sinon retourne None

    # La fonction qui modifie la poste spécifique d'une entreprise.
    def mod_company_job(self, company_name, job_name, data):
        lst_jobs = self.load_jobs()  # Charger la liste des postes
        for l in lst_jobs:  # Parcourir la liste des postes.
            if l[0] == company_name and l[1] == job_name:  # Si le nom de l'entreprise correspond au nom du poste.
                # Modifier les données du poste
                l[1] = data[0]
                l[2] = data[1]
                l[3] = data[2]
                break  # Sortie du boucle
        self.save_jobs(lst_jobs)  # Enregistrer la liste des postes mise à jour

    # la fonction qui supprime la poste spécifique d'une entreprise.
    def del_company_job(self, company_name, job_name):
        lst_jobs = self.load_jobs()  # Charger la liste des postes
        for idx, l in enumerate(lst_jobs):  #Parcourir la liste des postes.
            if l[0] == company_name and l[1] == job_name:  # Si le nom de l'entreprise correspond au nom du poste.
                del lst_jobs[idx]  # Supprimer ce poste
                break  # Sortie du boucle
        self.save_jobs(lst_jobs)  # Enregistrer la liste des postes mise à jour

    # la fonction qui obtenu toutes les poste de l'entreprise
    def get_company_jobs(self, company_name):
        lst = []  # Créer une liste vide
        for l in self.load_jobs():  # Parcourir la liste des postes
            if l[0] == company_name:  # Si le nom de l'entreprise correspond au nom du poste
                lst.append(l)  # Ajouter ce poste à la liste.
        return lst  # Retourner la liste des postes.

    # la fonction qui ostule pour un poste
    def apply_job(self, company_name, job_name, stu_info):
        lst = self.load_jobs()  # Charger la liste des postes
        for l in lst:  # Parcourir la liste des postes.
            if l[0] == company_name and l[1] == job_name:  # Si le nom de l'entreprise correspond au nom du poste
                if l[-3] != 0:  # Si l'état du poste n'est pas 0.
                    return 0  # retourne 0
                for _l in l[-1]:  # Parcourir la liste des étudiants candidats pour le poste
                    if _l[0] == stu_info[0]:  # Si les informations de l'étudiant correspondent
                        return 1  # Retourne 1
                l[-1].append(stu_info)  # Ajouter les informations de l'étudiant à la liste des candidats pour le poste
                self.save_jobs(lst)  # Enregistrer la liste mise à jour des postes
                return 2  # Retourner 2

    # la fct qui peut obtenir la liste des étudiants candidats pour le poste
    def get_job_apply_students(self, company_name, job_name):
        for l in self.load_jobs():  # Parcourir les postes chargés
            if l[0] == company_name and l[1] == job_name:  # Si le nom de l'entreprise correspond au nom du poste
                return l[-1]  # Retourner la liste des étudiants candidats pour le poste
        return []  # Si aucun poste ne correspond, retourner une liste vide

    # la fct qui peut obtenir la liste des postes auxquels l'étudiant a postulé
    def get_student_apply_jobs(self, stu_act):
        result = []  # Créer une liste vide
        for l in self.load_jobs():  # Parcourir les postes chargés
            for _l in l[-1]:  # Parcourir la liste des étudiants candidats pour le poste
                if _l[0] == stu_act:  # Si les informations de l'étudiant correspondent
                    result.append([l[0], l[1], *_l[2:]])  # Ajouter les informations du poste à la liste de résultats
        return result  # Retourner la liste de résultats

    # la fct qui peut révoquer la candidature
    def undo_apply(self, stu_act, company_name, job_name):
        lst_jobs = self.load_jobs()  # Charger la liste des postes
        for job in lst_jobs:  # Parcourir la liste des postes.
            if company_name == job[0] and job_name == job[1]:  # Si le nom de l'entreprise correspond au nom du poste
                for idx, l in enumerate(job[-1]):  # Parcourir la liste des étudiants ayant postulé pour le poste
                    if l[0] == stu_act:  # Si les informations de l'étudiant correspondent
                        del job[-1][idx]  # Supprimer les informations de candidature de cet étudiant.
                        self.save_jobs(lst_jobs)  # Enregistrer la liste des postes mise à jour.
                        return  # arreter le fct

    # le fct qui obtenu l'état du poste
    def get_job_state(self, company_name, job_name):
        for job in self.load_jobs():  # Parcourir les postes chargés
            if job[0] == company_name and job[1] == job_name:  # Si le nom de l'entreprise correspond au nom du poste
                return job[-3]  # Retourner l'état du poste

    # le fct qui vérifie si l'entreprise a accepté la candidature de l'étudiant
    def is_company_agree_my_apply(self, company_name, job_name, stu_act):
        for job in self.load_jobs():  # Parcourir les postes chargés
            if job[0] == company_name and job[1] == job_name:  # Si le nom de l'entreprise correspond au nom du poste
                return stu_act == job[-2]  # Retourner si le compte étudiant correspond au compte approuvé
        return False  # Si aucun poste ne correspond, retourner False

    #le fct qui Refuse la candidature de l'étudiant
    def disagree_student_apply(self, company_name, job_name, idx):
        lst_jobs = self.load_jobs()  # Charger la liste des postes
        for job in lst_jobs:  # Parcourir la liste des postes.
            if company_name == job[0] and job_name == job[1]:  # Si le nom de l'entreprise correspond au nom du poste
                del job[-1][idx]  # Supprimer les informations de candidature de cet étudiant
                self.save_jobs(lst_jobs)  # Enregistrer la liste des postes mise à jour
                break  # Sortie du boucle

    # le fct qui peut accepter la candidature de l'étudiant
    def agree_student_apply(self, company_name, job_name, idx):
        lst_jobs = self.load_jobs()  # Charger la liste des postes
        for job in lst_jobs:  # Parcourir la liste des postes.
            if company_name == job[0] and job_name == job[1]:  # Si le nom de l'entreprise correspond au nom du poste
                job[-3] = 1  # Définir l'état du poste sur 1
                job[-2] = job[-1][idx][0]  # Ajouter le compte de l'étudiant approuvé aux informations du poste.
                self.save_jobs(lst_jobs)  # Enregistrer la liste des postes mise à jour
                break  # sortie du boucles

    # la fct qui refuse le poste par l'étudiant
    def disagree_job(self, company_name, job_name, stu_act):
        lst_jobs = self.load_jobs()  # Charger la liste des postes
        for job in lst_jobs:  # Parcourir la liste des postes.
            if job[0] == company_name and job[1] == job_name:  # Si le nom de l'entreprise correspond au nom du poste
                job[-3] = 0  # Définir l'état du poste sur 0
                job[-2] = ''  # Effacer le compte de l'étudiant approuvé
                for idx, j in enumerate(job[-1]):  # Parcourir la liste des étudiants candidats pour le poste.
                    if j[0] == stu_act:  # Si les informations de l'étudiant correspondent
                        del job[-1][idx]  # Supprimer les informations de candidature de cet étudiant.
                        break  # sortie du boucle
                self.save_jobs(lst_jobs)  # Enregistrer la liste des postes mise à jour
                break  # sortie du grand boucle

    #la fct qui accepte le poste par l'etudiant
    def agree_job(self, company_name, job_name):
        lst_jobs = self.load_jobs()  # Charger la liste des postes
        for job in lst_jobs:  # Parcourir la liste des postes.
            if job[0] == company_name and job[1] == job_name:  # Si le nom de l'entreprise correspond au nom du poste
                job[-3] = 2  # Mettre le statut du poste à 2
                self.save_jobs(lst_jobs)  # Enregistrer la liste des postes mise à jour
                break  # sortie du boucle

    # le fct qui supprime toutes les candidatures
    def del_all_apply(self, stu_act):
        lst_jobs = self.load_jobs()  # Charger la liste des postes
        for job in lst_jobs:  # Parcourir la liste des postes.
            for idx, j in enumerate(job[-1]):  # Parcourir la liste des étudiants candidats pour chaque poste
                if j[0] == stu_act:  #Si les informations de l'étudiant correspondent
                    del job[-1][idx]  #Supprimer les informations de candidature de cet étudiant
                    break  #sortie du boucle
        self.save_jobs(lst_jobs)  # Enregistrer la liste des postes mise à jour

    # le fct d'obtenir le poste de l'étudiant
    def get_my_job(self, stu_act):
        for job in self.load_jobs():  # Parcourir les postes chargés
            if job[-3] == 2 and job[-2] == stu_act:  # "Si le statut du poste est 2 et le compte de l'étudiant accepté correspond au compte de l'étudiant
                return job  # Retourner ce poste
        return None  # sinon retourner None

    # le fct d'obtenir la liste des postes auxquels j'ai été refusé
    def get_my_refused_apply(self, stu_act):
        result = []  # Créer une liste vide
        lst_jobs = self.load_jobs()  # Charger la liste des postes
        for job in lst_jobs:  # Parcourir la liste des postes.
            if job[-3] == 2:  # Si l'état du poste est 2.
                for idx, j in enumerate(job[-1]):  #Parcourir la liste des étudiants candidats pour chaque poste
                    if j[0] == stu_act:  # Si les informations de l'étudiant correspondent
                        result.append(job)  # Ajouter les informations du poste à la liste des résultats
                        del job[-1][idx]  # Supprimer les informations de candidature de cet étudiant
                        break  # sortie du boucle
        self.save_jobs(lst_jobs)  # Enregistrer la liste des postes mise à jour.
        return result  #Retourner la liste des résultats
