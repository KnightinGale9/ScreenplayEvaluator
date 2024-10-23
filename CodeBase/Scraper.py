class Scraper(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Scraper, cls).__new__(cls)
        return cls.instance
    def screenplay_scrape(self):
        pass
    def dataframe_creation(self,character_removal=[]):
        pass
    def get_filename(self):
        return self.filename
    def get_fulldf(self):
        return self.fulldf
    def get_characterdict(self):
        return self.characterdict
    def get_headingdf(self):
        return self.headingdf
    def get_locationdf(self):
        return self.locationdf
    def get_dialoguedf(self):
        return self.dialoguedf
    def get_locationcocurence(self):
        return self.locationcocurence