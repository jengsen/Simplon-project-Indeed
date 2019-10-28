import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords
from gensim.utils import tokenize
import pickle
from sklearn.feature_extraction.text import CountVectorizer


class PreprocessIndeed():
    def __init__(self, pathJSON):
        self.pathJSON = pathJSON
        self.data = pd.read_json(pathJSON, lines=True, encoding='utf-8')
        self.df = self.data.copy()

    def preprocess_df(self, nlp_object_titre, nlp_object_description, correlation_titre=0, correlation_description=0,
                      save_name='preprocess'):
        """
        Preprocess the main dataframe
        :return:
        """

        # remove offers without salary
        self.df = self.df.loc[self.df['Salaire'] != 'None', :]

        # remove offers without job description
        self.df = self.df.loc[self.df['Descriptif_du_poste'] != 'None', :]

        # group cities : main city or suburb
        self.df['Ville'] = self.df.apply(lambda x: preprocess_villes(x.Ville, x.Scrapped_location), axis=1)
        df_ville = pd.get_dummies(self.df['Ville'], drop_first=True)
        self.df['Ville_' + df_ville.columns] = df_ville[df_ville.columns]

        # group salaries
        # delete salaries XX € per week : too many mistakes and it is only 2% of the offers
        self.df = self.df.loc[self.df['Salaire'].apply(lambda x: 'semaine' not in x), :]
        # preprocess strings in Salaire
        self.df['Salaire'] = self.df['Salaire'].apply(preprocess_salaires)
        # create classes in Salaire
        self.df['Salaire'] = self.df['Salaire'].apply(preprocess_salaires_kmean_clusters)

        # NLP titre
        # stop_words
        stop_words = set(stopwords.words('french'))
        nlp_object_titre.set_params(stop_words=stop_words)
        df_titre = nlp(self.df['Titre'], nlp_object_titre, save_name='titre'+save_name)

        # correlation matrix with the salary if correlation > 0
        if correlation_titre == 0:

            self.df['Titre_' + df_titre.columns] = df_titre[df_titre.columns]
        else:
            # keep features with correlation with Salaire > correlation_titre
            df_titre['Salaire'] = self.df['Salaire']
            kept_features = df_titre.loc[:, df_titre.corr()['Salaire'].apply(lambda x: abs(x) > correlation_titre)].columns
            self.df['Titre_' + kept_features] = df_titre[kept_features]
            self.df.drop(['Titre_Salaire'], inplace=True, axis=1)

        # NLP description
        # stop_words
        stop_words = set(stopwords.words('french'))
        nlp_object_description.set_params(stop_words=stop_words)
        df_description = nlp(self.df['Descriptif_du_poste'], nlp_object_description, save_name='description'+save_name)

        # correlation matrix with the salary if correlation > 0
        if correlation_description == 0:
            self.df['Description_' + df_description.columns] = df_description[df_description.columns]
        else:
            # keep features with correlation with Salaire > correlation_description
            df_description['Salaire'] = self.df['Salaire']
            kept_features = df_description.loc[:, df_description.corr()['Salaire'].apply(lambda x: abs(x) > correlation_description)].columns
            self.df['Description_' + kept_features] = df_description[kept_features]
            self.df.drop(['Description_Salaire'], inplace=True, axis=1)

        # drop columns that are not used
        self.df.drop(['_id', 'Entreprise', 'Type_de_contrat', 'Ville', 'Date_de_publication', 'Scrapped_job',
                      'Scrapped_location', 'Titre', 'Descriptif_du_poste'], inplace=True, axis=1)


def nlp(df, nlpObject, save_name='preprocess'):
    """
    tokenize and vectorize the df according to nlpObject
    :param save_name: name of the file saved
    :param nlpObject: nlpObject (countverizer, word2vec...)
    :param df: dataframe containing the strings to countvectorize
    :return: df containing max_features rows with the number of appearance of each word
    """
    # tokenize
    df_nlp = df.apply(lambda x: list(tokenize(x, lowercase=True)))
    df_nlp['Tokens'] = df.apply(lambda x: list(tokenize(x, lowercase=True, deacc=True)))
    df_nlp['Cleaned_strings'] = [" ".join(txt) for txt in df_nlp['Tokens'].values]

    # vectorize
    nlpObject.fit(df_nlp['Cleaned_strings'])
    columns = [column.replace(' ', '_') for column in nlpObject.get_feature_names()]

    # Save the fitted object in a file
    pickle.dump(nlpObject, open('serialized_models/' + save_name, 'wb'))
    return pd.DataFrame(nlpObject.transform(df_nlp['Cleaned_strings']).todense(), columns=columns,
                        index=df.index)


def preprocess_villes(ville, scrappedLocation):
    """
    function to apply to preprocess the Ville column to cluster cities
    :param ville: ville scrapped in the job offer
    :param scrappedLocation: location searched for the scrapping
    :return:
    """
    #### PARIS ET BANLIEUE DE PARIS ####
    if scrappedLocation == 'Paris':
        if '75' in ville or 'Paris' in ville:
            return 'Paris'
        elif ('92' in ville) or ('Hauts-de-Seine' in ville):
            return '92'
        else:
            return 'Banlieue_de_Paris'

    #### LYON ET SA BANLIEUE ####
    if scrappedLocation == 'Lyon':
        if 'Lyon' in ville:
            return 'Lyon'
        else:
            return 'Banlieue_de_Lyon'

    #### TOULOUSE ET SA BANLIEUE ####
    if scrappedLocation == 'Toulouse':
        if 'Toulouse' in ville:
            return 'Toulouse'
        else:
            return 'Banlieue_de_Toulouse'

    #### NANTES ET SA BANLIEUE ####
    if scrappedLocation == 'Nantes':
        if 'Nantes' in ville:
            return 'Nantes'
        else:
            return 'Banlieue_de_Nantes'

    #### BORDEAUX ET SA BANLIEUE ####
    if scrappedLocation == 'Bordeaux':
        if 'Bordeaux' in ville:
            return 'Bordeaux'
        else:
            return 'Banlieue_de_Bordeaux'
    return 'Delete'


def preprocess_salaires(salary):
    """
    function to apply to preprocess the Salaire column to get an unique
    value when an interval is given (average of the min and max)
    :param salary: scrapped salary
    :return:
    """
    sal = salary.replace(' ', '')
    ########### On parse si le salaire est "par an"

    if 'par an' in salary:
        if '-' in salary:
            x = re.findall('\d+', sal)
            avg = (int(x[0]) + int(x[1])) / (len(x))
            return avg
        else:
            x = re.findall('\d+', sal)
            return int(x[0])

    ########## Sinon on parse si le salaire est "par mois"

    elif 'par mois' in salary:
        if '-' in salary:
            x = re.findall('\d+', sal)
            avg = (int(x[0]) + int(x[1])) / (len(x))
            return (avg * 12)
        else:
            x = re.findall('\d+', sal)
            return (int(x[0]) * 12)

    ########## Sinon on parse si le salaire est "par semaine"

    elif 'par semaine' in salary:
        if '-' in salary:
            x = re.findall('\d+', sal)
            avg = (int(x[0]) + int(x[1])) / (len(x))
            return (avg * 52)
        else:
            x = re.findall('\d+', sal)
            return (int(x[0]) * 4 * 12)


    ########## Sinon on parse si le salaire est "par jour"

    elif 'par jour' in salary:
        if '-' in salary:
            x = re.findall('\d+', sal)
            avg = (int(x[0]) + int(x[1])) / (len(x))
            return (avg * 20 * 12)
        else:
            x = re.findall('\d+', sal)
            return (int(x[0]) * 20 * 12)

    ########## Sinon on parse si le salaire est "par heure"

    elif 'par heure' in salary:
        if '-' in salary:
            x = re.findall('\d+', sal)
            avg = (int(x[0]) + int(x[1])) / (len(x))
            return (avg * 35 * 4 * 12)
        else:
            x = re.findall('\d+', sal)
            return (int(x[0]) * 35 * 52)


def preprocess_salaires_kmean_clusters(salaire):
    '''
    creates 3 Salaire classes
    :param salaire:
    :return:
    '''
    # hist=[0, 16200, 42480]
    hist = [0, 24364.6, 43901.1, 67562.4]
    for i in range(0,len(hist)-1):
        if salaire < hist[i+1]:
            return i
    return len(hist)-1