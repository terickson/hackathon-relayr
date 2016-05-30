# $Id$
import requests
import json


class Infoblox(object):

    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd
        self.nfoUri = 'https://10.255.16.252/wapi/v1.6/'
        requests.packages.urllib3.disable_warnings()
        self.nfoReq = requests.Session()
        self.headers = {
            'Content-type': 'application/json', 'Accept': 'application/json'}
        self.loggedIn = False
        # Initialize REQ Session
        req = self.nfoReq.get(
            url=self.nfoUri + 'grid',
            headers=self.headers,
            verify=False,
            auth=(self.user, self.pwd)
        )
        if req.status_code == 200:
            print 'Logged In Successfully.'
            self.loggedIn = True
        if req.status_code == 401:
            self.loggedIn = False

    def _nfoReq(self, method, path, data):
        # Make REQ
        if data:
            payload = json.dumps(data)
        else:
            payload = None
        req = requests.Request(
            method,
            url=self.nfoUri + path,
            data=payload,
            headers=self.headers
        )
        preReq = self.nfoReq.prepare_request(req)
        resp = self.nfoReq.send(preReq, verify=False)
        return resp

    def get_next_ips(self, network, num):
        # Get Network REF
        net_ref = self.get_netw(network)
        path = net_ref + '?_function=next_available_ip'
        data = {'num': num}
        # Get Next IP(s) up to 20 in Subnet
        next = self._nfoReq('POST', path, data)
        return next

    def get_netw(self, network):
        path = 'network?network=' + network
        netw = self._nfoReq('GET', path, None)
        # Return Reference (Path URL) to Network Specified
        try:
            return json.loads(netw.text)[0]['_ref']
        except:
            cont_subnets = []
            print 'Subnet could be a Container...'
            print 'Checking Container for Containers and Subnets.'
            containers = self.get_netcont(network)
            if containers:
                cont_dict = {}
                cont_dict['containers'] = json.loads(containers.text)
                cont_subnets.append(cont_dict)
            else:
                print 'No Containers in container.'
            subnets = self.get_net_cont(network)
            if subnets:
                sub_dict = {}
                sub_dict['subnets'] = json.loads(subnets.text)
                cont_subnets.append(sub_dict)
            else:
                print 'No Subnets in container'
            if not cont_subnets:
                print 'Network does not exist on this system.'
            return cont_subnets

    def get_netcont(self, container):
        cont_path = 'networkcontainer?network_container=' + container
        return self._nfoReq('GET', cont_path, None)

    def get_net_cont(self, container):
        cont_path = 'network?network_container=' + container
        return self._nfoReq('GET', cont_path, None)

    def gethost_ip(self, ipv4):
        path = 'ipv4address?ip_address=' + ipv4
        host = self._nfoReq('GET', path, None)
        return json.loads(host.text)

    def create_host(self, address, fqdn):
        path = 'record:host'
        nfo_data = {
            'name': fqdn,
            'configure_for_dns': False,
            'ipv4addrs': [{'ipv4addr': address}]
        }
        req = self._nfoReq('POST', path, nfo_data)
        return json.loads(req.text).replace('"', '')

    def reclaim_host(self, ref):
        req = self._nfoReq('DELETE', ref, None)

    def logout(self):
        return self._nfoReq('POST', 'logout', None).status_code
