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


def get_status() -> List[Dict[str, Any]]:
    """Fetches text of status/machines of all labs."""
    page = session.get('https://clusters.andrew.cmu.edu/printerstats/index.php')
    soup = BeautifulSoup(page.text.strip(), 'lxml')
    data_table = soup.find('table', {'class': 'epi-dataTable'})  # Target the table with data
    rows = data_table.find_all('tr')
    del rows[0]  # Remove the header row

    printers = []

    for row in rows:
        info = row.find_all('td')

        inner_dict = dict()
        inner_dict['name'] = info[0].text.strip()
        inner_dict['visual_status'] = info[1].find('img')['src'].replace('.gif', '')
        inner_dict['lcd_message'] = info[2].text.strip()
        inner_dict['status'] = info[3].text.strip()
        inner_dict['tray_status'] = [{'tray_{}'.format(ix): f.text.strip()}
                for ix, f in enumerate(info[4].find_all('font'))]
        inner_dict['as_of'] = info[5].text.strip().replace(u'\xa0', ' ')

        printers.append(inner_dict)

    return printers
