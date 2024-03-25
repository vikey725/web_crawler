"""The html Parser Module"""

from copy import copy

from bs4 import BeautifulSoup

from configs import Configs


class HtmlParser:
    '''HTML parser class'''

    def __init__(self) -> None:
        pass


    def get_data(self, web_element, no_of_children=0):
        data = {
        }
        data['tag_name'] = web_element.name
        if no_of_children == 0:
            if web_element.get_text().strip() != '':
                data['tag_text'] = web_element.get_text().strip()
        if web_element.name == 'a':
            data['tag_link'] = web_element['href']
        if web_element.name == 'img':
            data['image_link'] = web_element.get('src')
        return data


    def parse_webpage(self, page_source):
        """Recursively parses the source of a web page

        Args:
            page_source (BeautifulSoup): _description_

        Returns:
            list(touple): a list of tuple of elements and related values
        """
        stack, result = [], []
        soup = BeautifulSoup(page_source, 'html.parser')
        web_element = soup.find(Configs.TOP_ELEMENT, id=Configs.CONTENT_COMMON_ID)
        stack.append((web_element, [0]))
        result = [{
            'data': {'tag_name': Configs.TOP_ELEMENT},
            'children': []
        }]
        current_data = result
        while len(stack) > 0:
            web_element, parent_index_sequences = stack.pop()
            index_sequences = parent_index_sequences.copy()
            print('index_sequences: ', index_sequences)
            # print(current_data)
            for idx in index_sequences[:-1]:
                current_data = current_data[idx]['children']
            current_data = current_data[index_sequences[-1]]

            children_web_elements = web_element.findChildren(recursive=False)
            current_data['data'] = self.get_data(web_element, no_of_children=len(children_web_elements))
            
            for idx, child_web_element in enumerate(children_web_elements):
                current_data['children'].append({
                    'data': {},
                    'children': []
                })

            children_web_elements.reverse()
            for idx, child_web_element in enumerate(children_web_elements):
                index_sequences = parent_index_sequences.copy()
                index_sequences.append(len(children_web_elements) - idx - 1)
                stack.append((child_web_element, index_sequences))
            current_data = result
        print(result[0]['children'][0])
        
        return result


    def parse_table(self):
        pass 
