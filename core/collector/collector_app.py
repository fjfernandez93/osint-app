import logging.config
import logging
import yaml
import configparser

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from collector.pastebin.paste_collector import PasteParser
from models.model import PasteData, HitData

if __name__ == '__main__':

    with open('/users/paco/proyectos/osint/core/collector/log.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictconfig(config)

    logger = logging.getlogger('pastes')

    cfg = configparser.configparser()
    cfg.read('/users/paco/proyectos/osint/core/collector/config.ini')


    engine = create_engine('mysql+pymysql://dev:xxxxx@localhost/testing')
    session = sessionmaker(bind=engine)
    session = session()
    data_sources = {
        'paste': pastedata(session),
        'hit': hitdata(session)
    }
    pasteparser(data_sources['paste'], data_sources['hit'], cfg['pastebin']).start_scrapping()

