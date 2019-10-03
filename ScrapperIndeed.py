from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class ScrapperIndeed():
    def __init__(self, mongoCollection):
        """

        :param mongoCollection: collection mongo
        :param browser: selenium object webdriver.Chrome()
        """
        self.mongoCollection=mongoCollection
        self.browser=webdriver.Chrome()


    def scrapp_page(self, job, location):
        """
        scrapps the current page
        :param job: string current job searched
        :param location: string current location searched
        :return:
        """
        for chaque in self.browser.find_elements_by_class_name('result'):
            chaque.find_element_by_class_name('jobtitle').click()
            time.sleep(0.3)
            try:
                title = chaque.find_element_by_class_name('jobtitle').text
            except:
                title = 'None'
            # Scraping le nom de la boite sinon rien
            try:
                boite = chaque.find_element_by_class_name('company').text
            except:
                boite = 'Nane'
            # Scraping le Ville sinon rien
            try:
                city = chaque.find_element_by_class_name('location').text
            except:
                city = 'None'
            # Scraping le salaire sinon rien
            try:
                salary = chaque.find_element_by_class_name('salaryText').text
            except:
                salary = 'None'
            # Scraping le type de contrat sinon chercher une autre position
            try:
                if len(self.browser.find_elements_by_class_name('jobMetadataHeader-itemWithIcon-label')) == 2:
                    if self.browser.find_elements_by_class_name('jobMetadataHeader-itemWithIcon-label')[1] != salary:
                        contrat = self.browser.find_element_by_class_name('jobMetadataHeader-itemWithIcon-label')[1].text
                elif len(self.browser.find_elements_by_class_name('jobMetadataHeader-itemWithIcon-label')) == 3:
                    if self.browser.find_elements_by_class_name('jobMetadataHeader-itemWithIcon-label')[1] != salary:
                        contrat = self.browser.find_element_by_class_name('jobMetadataHeader-itemWithIcon-label')[1].text
                if salary == contrat:
                    contrat = None
            except:
                try:
                    contrat = browser.find_element_by_xpath('//*[@id="vjs-tab-job"]/div[1]/div[2]/span[2]').text
                except:
                    contrat = None
            # Scraping le description sinon rien
            try:
                describe = chaque.find_element_by_class_name('summary').text
            except:
                describe = 'None'
            # Scraping le date de publication sinon rien
            try:
                publish_date = self.browser.find_element_by_xpath('//*[@id="vjs-footer"]/div[1]/div/span[1]').text
            except:
                publish_date = 'None'
            w = {"Titre": title, "Entreprise": boite, "Ville": city, "Salaire": salary, "Type_de_contrat": contrat,
                 "Descriptif_du_poste": describe, "Date_de_publication": publish_date, "Scrapped_job" : job, "Scrapped_location" : location}

            if self.mongoCollection.find_one({"Titre": title, 'Descriptif_du_poste': describe}) == None:
                self.mongoCollection.insert_one(w)

    def start(self):
        """
        Opens Indeed.com in browser and maximize the window
        :return:
        """
        self.browser = webdriver.Chrome()
        self.browser.get('https://www.indeed.fr/')
        self.browser.maximize_window()


    def check_pop_up(self):
        """
        Check if the pop-up asking for email popped.
        To be used everytime a new search is done or when a new page is visited
        
        :return: 
        """
        try:
            popUp = self.browser.find_element_by_xpath('//*[@id="popover-x"]/a')
            popUp.click()
            time.sleep(1)
        except:
            time.sleep(0.1)



    def next_page(self):
        """
        clicks on the next button
        :return: boolean True if the next button exists and False otherwise
        """
        try:
            buttons = self.browser.find_elements_by_class_name("np")
            # If first/last page
            if len(buttons) == 1:
                # If
                if 'Précédent' in buttons[0].text:
                    return False
                next_button = buttons[0]
            # If not first page
            else:
                next_button = buttons[1]
            next_button.click()
            time.sleep(3)
            self.check_pop_up()
            return True
        except:
            return False


    def search_offers(self, job, location):
        """
        Searches offers of job in a location to scrapp them
        :param job: string of job
        :param location: string of location
        :return:
        """
        # Write job
        entrer_job = self.browser.find_element_by_xpath('//*[@id="text-input-what"]')
        entrer_job.send_keys(job)
        time.sleep(1)
        # write location
        entrer_city = self.browser.find_element_by_xpath('//*[@id="text-input-where"]')
        entrer_city.send_keys(location)
        time.sleep(1)
        # search
        button_search = self.browser.find_element_by_class_name("icl-Button")
        button_search.click()
        time.sleep(3)

    def scrapp_search(self, job, location):
        """
        Scrapps every page of job offers associated with job and location
        :param job: string of job
        :param location: string of location
        :return:
        """
        self.start()
        self.search_offers(job, location)
        self.scrapp_page(job, location)
        while self.next_page():
            self.scrapp_page(job, location)
        self.browser.quit()



    def scrapp_searches(self,jobs, locations):
        """
        scrapps Indeed jobs in locations and stores it in a mongo db

        :param jobs: list of strings of the jobs to be searched
        :param locations: list of strings of the locations to be searched
        :return:
        """
        for location in locations:
            for job in jobs:
                self.scrapp_search(job, location)


