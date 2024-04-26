"""Module to store configurations for the project"""

class Configs:
    """Configs class for storing global variables"""

    PAGE_URL = "<URL>" # The website URL, from where you start crawling
    BASE_URL = "<URL>" # base URL of the website
    PAGE_COMMON_ID = "rw_main" # ID for which selenium will wait befor extracting the page content
    CONTENT_COMMON_ID = "printable_document" # ID of the element containing the content to be crawled
    MAX_WAITING_TIME = 20 # wait time after PAGE_COMMON_ID will be visible, finetune it for yur use case, 0 for non-js websites
    SAVE_AFTER = 10 # save the visited and queue after # of urs being crawled
    DATA_DIR = "content" # Place where the extracted content will be saved
    IMAGE_DIR = "images" # place where images will be saved
    VISITED_PKL = "" # directory to save visited data
    QUEUE_PKL = "" # directory to save queue data
    TOP_ELEMENT = "div" # tag of the element containing all pages
