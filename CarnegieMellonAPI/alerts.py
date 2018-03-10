'''
The Carnegie Mellon API, to access workable data of Carnegie Mellon University
Copyright (C) 2018 Ritwik Gupta

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any

session = requests.session()


def get_service_alerts() -> List[Dict[str, str]]:
    """Fetches text of status/machines of all labs."""
    page = session.get('https://www.cmu.edu/computing/rss-feeds/alerts.rss')
    soup = BeautifulSoup(page.text, 'lxml')

    items = soup.find_all('item')

    alerts = []

    for item in items:
        title = item.find('title').text.strip()
        link = item.find('link').text.strip()
        print(item.find('description'))
        desc = item.find('description').text.strip()
        # Ugly hack to remove CDATA
        desc = desc.replace('![CDATA[', '')[:-2]
        pub_date = item.find('pubdate').text


        alerts.append({
            'title': title,
            'link': link,
            'description': desc,
            'publication_date': pub_date
            })

    return alerts
