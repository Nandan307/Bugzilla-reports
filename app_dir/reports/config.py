"""
Configurations for the BZ reports/dashboard
"""

# Harcode latest RPL bugs
rpl = {}

products = [
    'RHEL7',
    'RHEL6',
    'RHEL5'
    ]


# MAIL configuration
def mail_config(app):
    app.config["MAIL_SERVER"] = "smtp.companyname.com"
    app.config["MAIL_PORT"] = 0


# Manager's kerberos login name
def return_manager_name():
    manager_name = "xyz"
    return manager_name
