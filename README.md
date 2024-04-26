# web_crawler
Crawler for any dynamic website

1. Clone the repo
   ```
   git clone https://github.com/vikey725/web_crawler.git
   ```
2. get into chatbot directory
   ```
   cd web_crawler
   ```
3. create conda environment using provided environment.yml
   ```
   conda env create -f environment.yml
   ```
4. Activate the environment
   ```
   conda activate crawler
   ```
6. Edit configs.py as per instruction provided in it
7. Run the web crawler
   ```
   python web_crawler.py
   ```

The webcrawler uses DFS to crawl all the urls available on the website recursively. 
