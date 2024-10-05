import logging

# Configuration du fichier de log
logging.basicConfig(
    filename='colis.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)
