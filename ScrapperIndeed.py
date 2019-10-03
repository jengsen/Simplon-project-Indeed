class ScrapperIndeed():
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    #from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    import pandas as pd
    import time

    def __init__(self, mongoCollection,browser):
        """

        :param mongoCollection: collection mongo
        :param browser: selenium object webdriver.Chrome()
        """
        self.mongoCollection=mongoCollection
        self.browser=browser


    def scrapp_page(self, job, location):
        """
        scrapps the current page
        :param job: string current job searched
        :param location: string current location searched
        :return:
        """
        # Code Ursula

        if self.mongoCollection.find_one({"Titre": titre, 'Descriptif du poste': describe}) == None:
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
            pass



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

    def search_offers(self, job, location):
        """
        Searches offers of job in a location to scrapp them
        :param job: string of job
        :param location: string of location
        :return:
        """

    def scrapp_search(self, job, location):
        """
        Scrapps every page of job offers associated with job and location
        :param job: string of job
        :param location: string of location
        :return:
        """
        self.start()
        self.search_offers(job, location)
        self.scrapp_page(job,location)
        while self.next_page():
            self.scrapp_page()
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


