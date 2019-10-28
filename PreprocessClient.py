import numpy as np
import pandas as pd
from PreprocessIndeed import preprocess_villes
import pickle
from gensim.utils import tokenize


class PreprocessClient():

    def __init__(self, pathJSON):
        self.data = pd.read_json(pathJSON, lines=True, encoding='utf-8')
        self.df = self.data.copy()

    def preprocess_main_features(self, nlp_model_name='preprocess'):
        """
        Preprocess the main dataframe
        :return:
        """
        self.df = self.data.copy()

        # keep offers without salary
        self.df = self.df.loc[self.df['Salaire'] == 'None', :]

        # remove offers without job description
        self.df = self.df.loc[self.df['Descriptif_du_poste'] != 'None', :]

        # group cities : main city or suburb
        self.df['Ville'] = self.df.apply(lambda x: preprocess_villes(x.Ville, x.Scrapped_location), axis=1)
        df_ville = pd.get_dummies(self.df['Ville'], drop_first=True)
        self.df['Ville_' + df_ville.columns] = df_ville[df_ville.columns]

        # NLP titre
        nlp_object_titre = pickle.load(open('titre' + nlp_model_name, 'rb'))
        df_nlp = self.df['Titre'].apply(lambda x: list(tokenize(x, lowercase=True)))
        df_nlp['Tokens'] = self.df['Titre'].apply(lambda x: list(tokenize(x, lowercase=True, deacc=True)))
        df_nlp['Cleaned_strings'] = [" ".join(txt) for txt in df_nlp['Tokens'].values]

        # columns to keep
        columns = [column.replace(' ', '_') for column in nlp_object_titre.get_feature_names()]
        kept_features = ['chef_projet', 'data', 'data_scientist', 'developpeur_web', 'directeur', 'freelance',
                         'junior', 'lead_data', 'marketing', 'senior', 'stage', 'web']

        df_titre = pd.DataFrame(nlp_object_titre.transform(df_nlp['Cleaned_strings']).todense(), columns=columns,
                                index=self.df.index)

        for feature in kept_features:
            self.df['Titre_' + feature] = df_titre[feature]

        # NLP description
        nlp_object_description = pickle.load(open('description' + nlp_model_name, 'rb'))
        df_nlp = self.df['Descriptif_du_poste'].apply(lambda x: list(tokenize(x, lowercase=True)))
        df_nlp['Tokens'] = self.df['Descriptif_du_poste'].apply(lambda x: list(tokenize(x, lowercase=True, deacc=True)))
        df_nlp['Cleaned_strings'] = [" ".join(txt) for txt in df_nlp['Tokens'].values]

        # columns to keep
        columns = [column.replace(' ', '_') for column in nlp_object_description.get_feature_names()]
        kept_features = ['alternance', 'architecture', 'aws', 'bac',
                         'backend', 'bts', 'confirme', 'data',
                         'data_scientist', 'developer', 'dut',
                         'ecole_commerce', 'frontend', 'html_css',
                         'lead',
                         'licence', 'machine_learning', 'responsabilites',
                         'spark', 'stage', 'web']

        df_description = pd.DataFrame(nlp_object_description.transform(df_nlp['Cleaned_strings']).todense(),
                                      columns=columns,
                                      index=self.df.index)

        for feature in kept_features:
            self.df['Description_' + feature] = df_description[feature]

        # drop columns that are not used
        self.df.drop(['_id', 'Entreprise', 'Type_de_contrat', 'Ville', 'Date_de_publication', 'Scrapped_job',
                      'Scrapped_location', 'Titre', 'Descriptif_du_poste'], inplace=True, axis=1)


    def preprocess_all_features(self, nlp_model_name='preprocess'):
        """
        Preprocess the main dataframe
        :return:
        """
        self.df = self.data.copy()

        # keep offers without salary
        self.df = self.df.loc[self.df['Salaire'] == 'None', :]

        # remove offers without job description
        self.df = self.df.loc[self.df['Descriptif_du_poste'] != 'None', :]

        # group cities : main city or suburb
        self.df['Ville'] = self.df.apply(lambda x: preprocess_villes(x.Ville, x.Scrapped_location), axis=1)
        df_ville = pd.get_dummies(self.df['Ville'], drop_first=True)
        self.df['Ville_' + df_ville.columns] = df_ville[df_ville.columns]

        # NLP titre
        nlp_object_titre = pickle.load(open('serialized_models/titre' + nlp_model_name, 'rb'))
        df_nlp = self.df['Titre'].apply(lambda x: list(tokenize(x, lowercase=True)))
        df_nlp['Tokens'] = self.df['Titre'].apply(lambda x: list(tokenize(x, lowercase=True, deacc=True)))
        df_nlp['Cleaned_strings'] = [" ".join(txt) for txt in df_nlp['Tokens'].values]

        # columns to keep
        columns = [column.replace(' ', '_') for column in nlp_object_titre.get_feature_names()]
        kept_features = ['chef_projet', 'data', 'data_scientist', 'developpeur_web', 'directeur', 'freelance', 'junior',
                         'lead_data', 'marketing', 'mois', 'projet', 'ref', 'scientist', 'senior', 'stage',
                         'stage_chef', 'stage_developpeur', 'stagiaire', 'web']

        df_titre = pd.DataFrame(nlp_object_titre.transform(df_nlp['Cleaned_strings']).todense(), columns=columns,
                                index=self.df.index)

        for feature in kept_features:
            self.df['Titre_' + feature] = df_titre[feature]

        # NLP description
        nlp_object_description = pickle.load(open('serialized_models/description' + nlp_model_name, 'rb'))
        df_nlp = self.df['Descriptif_du_poste'].apply(lambda x: list(tokenize(x, lowercase=True)))
        df_nlp['Tokens'] = self.df['Descriptif_du_poste'].apply(lambda x: list(tokenize(x, lowercase=True, deacc=True)))
        df_nlp['Cleaned_strings'] = [" ".join(txt) for txt in df_nlp['Tokens'].values]

        # columns to keep
        columns = [column.replace(' ', '_') for column in nlp_object_description.get_feature_names()]
        kept_features = ['alternance', 'an', 'an_souhaite', 'ans_experience', 'ans_paris', 'apprentissage',
                         'architecture', 'aws', 'bac', 'bac_bac', 'bac_bts', 'bac_minimum', 'backend',
                         'backend_developer', 'bonnes_pratiques', 'brut', 'bts', 'bts_dut', 'capacite_travailler',
                         'cdd', 'cdi_environ', 'commerce', 'confirme', 'css', 'cto', 'curieux', 'data',
                         'data_scientist', 'data_scientists', 'debut', 'deug', 'developer', 'developer_backend',
                         'developer_cdi', 'developpement_informatique', 'duree', 'dut', 'dut_deug', 'ecole_commerce',
                         'embauche', 'emploi', 'emploi_stage', 'emploi_temps', 'environ', 'environ_ans', 'etude',
                         'excel', 'fin', 'formation', 'formation_bac', 'fr', 'frontend', 'grand', 'html', 'html_css',
                         'http', 'immobilier', 'industrialisation', 'informations', 'informatique', 'lead',
                         'lead_developer', 'learning', 'licence', 'machine', 'machine_learning', 'missions', 'mois',
                         'mois_experience', 'paris_poste', 'pourquoi', 'pourquoi_venir', 'pourvoir', 'pratiques',
                         'profil', 'recruter', 'remboursement', 'renforce', 'responsabilites', 'rigoureux', 'salaire',
                         'salaire_mois', 'scientist', 'scientists', 'similaire', 'similaire_an', 'site', 'solide',
                         'souhaite', 'spark', 'specialisee', 'stack', 'stack_developer', 'stage', 'stage_salaire',
                         'tdd', 'temps', 'temps_plein', 'transport', 'type', 'type_contrat', 'type_emploi', 'variees',
                         'venir', 'venir_chez', 'web', 'wordpress']

        df_description = pd.DataFrame(nlp_object_description.transform(df_nlp['Cleaned_strings']).todense(),
                                      columns=columns,
                                      index=self.df.index)

        for feature in kept_features:
            self.df['Description_' + feature] = df_description[feature]

        # drop columns that are not used
        self.df.drop(['_id', 'Entreprise', 'Type_de_contrat', 'Ville', 'Date_de_publication', 'Scrapped_job',
                      'Scrapped_location', 'Titre', 'Descriptif_du_poste'], inplace=True, axis=1)
