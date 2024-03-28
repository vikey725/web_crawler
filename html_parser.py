"""The html Parser Module"""

from copy import copy

from bs4 import BeautifulSoup

from configs import Configs


class HtmlParser:
    '''HTML parser class'''

    def __init__(self) -> None:
        pass


    def parse_table(self, web_element):
        # print(web_element)
        tbody = web_element.find('tbody')
        if tbody is None:
            return None
        trs = tbody.findAll('tr')
        if len(trs) == 0:
            return None
        num_rows, num_cols = len(trs), 0
        headers = []
        for elem in (trs[0].findAll('th') or trs[0].findAll('tr')):
            num_cols += int(elem.get('colspan', '1'))

        table_data = [['' for _ in range(num_cols)] for _ in range(num_rows)]

        for idx, tr in enumerate(trs):
            row_data = tr.findAll('th') or tr.findAll('td')
            for elem in row_data:
                j = 0
                while table_data[idx][j] != '':
                    j += 1
                colspan = int(elem.get('colspan', '1'))
                rowspan = int(elem.get('rowspan', '1'))
                for k in range(rowspan):
                    for l in range(colspan):
                        table_data[idx + k][j + l] = elem.get_text().strip()

        return table_data


    def parse_webpage_basic(self, page_source):
        stack, result = [], []
        soup = BeautifulSoup(page_source, 'html.parser')
        web_element = soup.find(Configs.TOP_ELEMENT, id=Configs.CONTENT_COMMON_ID)
        stack.append(web_element)

        while len(stack) > 0:
            web_element = stack.pop()
            children_web_elements = web_element.findChildren(recursive=False)
            tag_name = web_element.name

            if tag_name == 'a':
                result.append({
                    'tag_name': tag_name,
                    'text': web_element.get_text().strip(),
                    'link': Configs.BASE_URL + web_element['href']
                })
            elif tag_name == 'table':
                table_data = self.parse_table(web_element)
                if table_data:
                    result.append({
                        'tag_name': tag_name,
                        'table_data': table_data
                    })
            elif tag_name == 'img':
                result.append({
                    'tag_name': tag_name,
                    'img_src': Configs.BASE_URL + web_element.get('src')
                })

            elif len(children_web_elements) == 0:
                result.append({
                    'tag_name': tag_name,
                    'text': web_element.get_text().strip()
                })

            else:
                children_web_elements.reverse()
                stack.extend(children_web_elements)

        return result
    

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
        if web_element.name in ['td', 'th']:
            data['colspan'] = str(web_element.attrs.get('colspan', '1'))
            data['rowspan'] = str(web_element.attrs.get('rowspan', '1'))
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
       
        return result
