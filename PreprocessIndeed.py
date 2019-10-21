import pandas as pd
import numpy as np


class PreprocessIndeed():
    def __init__(self, pathJSON):
        self.pathJSON = pathJSON
        self.data = pd.read_json(pathJSON, lines=True, encoding='utf-8')
        self.df = self.data

    def preprocess_df(self):
        '''
        Preprocess the main dataframe:
        keep rows with Salaire and Descriptif_du_poste
        :return:
        '''
        self.df = self.df.loc[self.df['Salaire'] != 'None', :]
        self.df = self.df.loc[self.df['Descriptif_du_poste'] != "None", :]
        self.df['Ville'] = self.df.apply(lambda x: preprocess_villes(x.Ville, x.Scrapped_location), axis=1)

def preprocess_villes(ville, scrappedLocation):
    '''
    function to apply to preprocess the Ville column to cluster cities
    :param ville: ville scrapped in the job offer
    :param scrappedLocation: location searched for the scrapping
    :return:
    '''
    #### PARIS ET BANLIEUE DE PARIS ####
    if scrappedLocation == 'Paris':
        if '75' in ville or 'Paris' in ville:
            return 'Paris'
        elif ('92' in ville) or ('Hauts-de-Seine' in ville):
            return '92'
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

