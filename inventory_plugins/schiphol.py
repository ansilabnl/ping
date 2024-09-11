DOCUMENTATION = r'''
    name: schiphol
    plugin_type: inventory
    short_description: Creates a dynamic inventory from an URL
    description: Returns Ansible inventory from nothingness
    options:
      plugin:
          description: Name of the plugin
          required: true
          choices: ['schiphol']
      url:
        description: url to get the file from
        required: true
'''

from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.utils.display import Display
from ansible.module_utils.urls import open_url

display = Display()

class InventoryModule(BaseInventoryPlugin):

    NAME = "schiphol"

    def parse(self, inventory, loader, path, cache=True):

        # call base method to ensure properties are available for
        # use with other helper methods
        super(InventoryModule, self).parse(inventory, loader, path, cache)

        self._read_config_data(path)        # Get configuration
        url = self.get_option('url')        # Get "url" from configuration

        display.vvvv("Schiphol GET %s" % url)
        try:
            response = open_url(url, method="GET")
        except Exception as ex:
            raise Exception("Received HTTP error %s" % ex)

        # Get data from URL, decode as it is in bytes and split on line-ends
        data = list(map(str.strip, str(response.read().decode('utf-8')).split('\n')))
        display.vvvv("Schiphol data %s" % data)

        # Find all hosts and add these to the inventory
        for line in data:
            # Skip empty and comment lines
            if not line:
                continue
            if line[0] == '':
                continue
            if line[0] == '#':
                continue

            # Here we got a decent line. Parse it
            hi = line.split(';')

            # Host is the first field. Add it to the inventory
            host = hi[0].strip()
            self.inventory.add_host(host)

            # Add the variables, if there are any
            for v in hi[1:]:
                kv = list(map(str.strip, v.split('=')))
                self.inventory.set_variable(host, kv[0], kv[1])

