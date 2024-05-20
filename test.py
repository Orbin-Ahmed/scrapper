from py3pin.Pinterest import Pinterest
from proxy import get_random_proxy

file_path = "E:/Next Js/scrapper/Free_Proxy_List.json"
p = get_random_proxy(file_path)

pinterest = Pinterest(email='acantoahmed@hotmail.com',
                      password='Pranto@123',
                      username='acantoahmed3898',
                      cred_root='cred_root',
                      proxies=p
                      )

search_batch = pinterest.search(scope='pins', query='interior Design', page_size=1)
print(search_batch)