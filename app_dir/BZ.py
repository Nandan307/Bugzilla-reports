import bugzilla


class BZ():
    def __init__(self):
        self.defaults = {}
        self.__bz_init()

        # We usually work only with open bugs and on RHEL products
        self.set_default('product',
                         [
                          'Red Hat Enterprise Linux 7',
                          'Red Hat Enterprise Linux 6',
                          'Red Hat Enterprise Linux 5'
                         ]
        )
        self.set_default('status',
                         ['NEW', 'ASSIGNED', 'ON_DEV']
                        )
        self.set_default('include_fields', ['id', 'status', 'priority',
                         'severity', 'summary', 'assigned_to', 'blocks',
                         'product', 'component', 'sub_component','sub_components'
                         'keywords', 'flags', 'classification', "version"]
                        )

    def __bz_init(self):
        self.bz = bugzilla.Bugzilla(url="bugzilla.companyname.com")

    def set_default(self, key, value):
        if value is None:
            if key in self.defaults.keys():
                del self.defaults[key]
            return
        self.defaults[key] = value

    def get_default(self, key):
        if key in self.defaults.keys():
            return self.defaults[key]
        return None

    def build_query(self, **kwargs):
        args = self.defaults
        args.update(kwargs)
        return self.bz.build_query(**args)


def bz_has_flag(bz, flag_name, status):
    for flag in bz.flags:
        if flag['name'] == flag_name:
            if flag['status'] in status:
                return True
    return False
