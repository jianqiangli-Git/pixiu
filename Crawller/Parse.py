'''
页面解析类
'''
from bs4 import BeautifulSoup

# BeautifulSoup 解析器
class BSParser(object):
    # beautifulsoup 官方推荐使用 lxml 解析器，比默认的html.parser容错率高且效率更高
    def __init__(self,html,parser='lxml'):
        self._parse = BeautifulSoup(html,parser)

# if __name__ == '__main__':
#     html_doc = """
# <div class="panel">
#     <div class="panel-heading">
#         <h4>Hello World</h4>
#     </div>
#
#     <div class="panel-body">
#         <ul class="list" id="list-1">
#            <li class="element">Foo</li>
#            <li class="element">Bar</li>
#            <li class="element">Jay</li>
#         </ul>
#
#         <ul class="list list-samll" id="list-2">
#            <li class="element">Fool</li>
#            <li class="element">Bar</li>
#            <li class="element">Jay</li>
#         </ul>
#     </div>
#     </div>
# </div>
# """
#     bs = BSParser(html_doc)
#     r = bs._parse.find(class_="panel-body")
#     print(r.text)