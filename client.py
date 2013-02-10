# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests

API_URI = "https://api.digitalocean.com/"

class Client:
    def __init__(self, client_id, api_key):
        self.client_id = client_id
        self.api_key = api_key
    def droplet(self, *args, **kwargs):
        return Droplet(self, *args, **kwargs)
class Droplet:
    def __init__(self, client, droplet_id=None):
        self.client = client
        self.droplet_id = droplet_id
        self.client_id = self.client.client_id
        self.api_key = self.client.api_key
    def create(self, name, size_num, image_id, region_id): #size_num != size id.  the higher the number, the bigger the server.  image ids: 12573 is debian x64. region ids: 1 = new york 1, 2 = amsterdam 1.  
        sizes=requests.get(API_URI+"sizes/",params={"client_id": self.client_id, "api_key": self.api_key}).json().get("sizes")
        size_id=sizes[size_num]['id']
        r=self.request("droplets/new",payload={"name":name,"size_id":size_id,'image_id':image_id,'region_id':region_id})
        self.droplet_id = r.json()['droplet']['id']
    def destroy(self):
        if self.droplet_id == None:
            return False
        self.request("droplets/"+str(self.droplet_id)+"/destroy")
        return True
    def info(self):
        if self.droplet_id == None:
            return False
        droplet_info=self.request("droplets/"+str(self.droplet_id),payload={"client_id": self.client_id, "api_key": self.api_key}).json()['droplet']
        return droplet_info
    def list_images(self):
        return self.request("/images").json['images']
    def request(self, target, payload={}, action="servers"):
        headers = {'User-Agent': 'SilkServer/git'}
        payload['client_id'] = self.client_id
        payload['api_key'] = self.api_key
        r = requests.get(API_URI+target+"/", headers=headers, params=payload)
        assert r.json.get("status") != "ERROR"
        return r
        