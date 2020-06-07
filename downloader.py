from flickrapi import FlickrAPI     
import urllib
import os

class ImageDownloader:

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.flickr = FlickrAPI(key, secret)

    def _get_image_urls(self, search_term, n_results=100):
        """
        Get URLS for the top n image search results from flickr for a certain 
        search term. Only return the images with a permissible license.
        100 is the max value. 
        """
        
        results = self.flickr.walk(
            text=search_term,
            extras='url_o',
            license=10,
            safe_search=1,
            content_type=1,
            sort='relevance'
        )

        urls = [result.get('url_o') for idx, result in enumerate(results) if idx < n_results]

        return urls

    def _download_images(self, urls, output_folder):
        
        for url in urls:
            image_name = url.rsplit('/', 1)[-1]
            path = os.path.join(output_folder, image_name)
            urllib.request.urlretrieve(url, path)

    def run(self, search_terms, n_results, parent_folder=None):

        for search_term in search_terms:

            if parent_folder:
                if not os.path.isdir(parent_folder):
                    os.mkdir(parent_folder)
                output_folder = os.path.join(parent_folder, search_term)
            else:
                output_folder = search_term

            if not os.path.isdir(output_folder):
                os.mkdir(output_folder)

            urls = self._get_image_urls(search_term, n_results)
            self._download_images(urls, output_folder)
        
            print('Downloaded {} results for the search term "{}"'.format(len(urls), search_term))


if __name__=='__main__':

    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument('key', help='your flickr account api key')
    parser.add_argument('secret', help='your flickr account secret')
    parser.add_argument('n', help='number of examples to collect for each class')
    parser.add_argument('search_terms_json', help='json file with a list of search terms')
    parser.add_argument('parent_folder', help='folder to store the images', default=None)
    
    args = parser.parse_args()

    with open(args.search_terms_json, 'r') as f:
        search_terms = json.loads(f)['search_terms']

    downloader = ImageDownloader(args.key, args.secret)

    downloader.run(search_terms, 100, parent_folder=args.parent_folder)

