import requests
import datetime
import os
import time
import logging

import analyzer.pastebin.an_modules as modules
from models.model import Paste, Hit
logger = logging.getLogger('pastes')


class PasteParser:

    def __init__(self, paste_data, hit_data, paste_config):
        self.iterations = 0
        self.active = 0
        self.paste_config = paste_config
        self.modules = ['ip', 'email']
        # Data managers
        self.hit_data = hit_data
        self.paste_data = paste_data
        self.paste_data = paste_data


    @staticmethod
    def sanitize(paste):
        paste.title = paste.title.replace("'", "''")
        paste.username = paste.username.replace("'", "''")
        paste.syntax = paste.syntax.replace("'", "''")

    def save_document(self, paste, text):
        pastes_path = self.paste_config['base_folder']
        folder_name = datetime.datetime.now().strftime('%Y-%m-%d')
        folder_path = os.path.join(pastes_path, folder_name)

        try:
            if not os.path.isdir(folder_path):
                os.mkdir(folder_path)
            file_name = "{}.txt".format(paste.key)
            paste_file = os.path.join(folder_path, file_name)
            with open(paste_file, 'wb') as f:
                f.write(text.encode("utf-8"))
            paste.file_path = paste_file

        except IOError as e:
            logger.error("ERROR 001: {}".format(e))
            return False

    def get_paste(self, key):
        url_paste = self.paste_config['url_paste']

        try:
            r = requests.get(url_paste.format(key))
        except Exception as err:
            logger.error("ERROR 002: {}".format(err))
            return None
        return r.text

    def scrap_pastes(self):
        new_pastes = 0
        url_all = self.paste_config['url_all']
        # Call the API endpoint and extract the info in JSON format.
        r = requests.get(url_all)
        json_data = r.json()
        # Iterate over all the data received
        for p in json_data:
            try:
                exists = self.paste_data.get_by(key=p['key'])
                if not exists:
                    # If not exists, create a object and store it in database.
                    paste = Paste(key=p['key'], date=p['date'], scrape_url=p['scrape_url'], full_url=p['full_url'],
                                  size=p['size'], expire=p['expire'], title=p['title'], syntax=p['syntax'],
                                  username=p['user'], positive=0)
                    self.paste_data.add(paste)
                    # Get the complete text of the paste
                    text = self.get_paste(paste.key)
                    # Save the file to local storage.
                    self.save_document(paste, text)
                    success = self.analyze_item(paste)
                    if success:
                        paste.positive = 1
                        self.paste_data.commit()
                    new_pastes += 1
            except Exception as err:
                logger.error("Exception reading paste {}: {}".format(p, str(err)))
        # Commit the changes in database.
        self.paste_data.commit()
        return new_pastes

    def start_scrapping(self):
        self.active = 1
        while self.active == 1:
            logger.info("Starting iteration: {}".format(self.iterations))
            new_pastes = self.scrap_pastes()
            logger.info("Finished iteration. Added {} new pastes. Going to sleep 120 seconds...".format(new_pastes))
            self.iterations += 1
            time.sleep(120)

    """
    Analysis methods
    """

    def analyze_item(self, paste):
        hit_found = False
        for module in self.modules:
            if self.execute_an_module(paste, module):
                hit_found = True
        return hit_found

    def execute_an_module(self, paste, module):
        """
        Execute the correct method for a module label.
        :param paste: Paste to analyze
        :param module: Name of the module
        :return: True if some hit found.
        """
        result = False
        if module == 'ip':
            result = self.execute_ip_module(paste)
        elif module == 'email':
            result = self.execute_email_module(paste)

        return result

    def execute_ip_module(self, paste):
        """
        Execute the ip scanner for a paste content
        :param paste: Paste object to scan
        :return: None
        """
        success = False
        with open(paste.file_path, 'rb') as f:
            text = f.read().decode('utf-8')
        try:
            result = modules.detect_ip(text)
            if len(result) != 0:
                logger.info(f'Match for IP(s) in paste {paste.id}. Found {len(result)} IPs.')
                self.handle_hit('ip', paste.id, result)
                success = True
        except Exception as err:
            logger.error(f'Exception processing paste {paste.id} in module IPs: {err}')

        return success

    def execute_email_module(self, paste):
        """
        Execute the email scaner for a paste content
        :param paste: Paste object to scan
        :return: None
        """
        success = False
        with open(paste.file_path, 'rb') as f:
            text = f.read().decode('utf-8')
        try:
            result = modules.detect_email(text)
            if len(result) != 0:
                logger.info(f'Match for an email in paste {paste.id}. Found {len(result)} emails')
                self.handle_hit('email', paste.id, result)
                success = True
        except Exception as err:
            logger.error(f'Exception processing paste {paste.id} in module emails: {err}')
        return success

    def handle_hit(self, entity, source_id, value_list):
        """
        Save the hits from an analysis module into database
        :param entity: type of entity found.
        :param source_id: id of the paste analyzed.
        :param value_list: entity value.
        :return: None
        """
        for value in value_list:
            hit = Hit()
            hit.entity = entity
            hit.source_type = 'pastebin'
            hit.source_id = source_id
            hit.value = value
            self.hit_data.add(hit)