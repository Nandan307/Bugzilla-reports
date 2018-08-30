#!/usr/bin/python3.6
import ldap
import json
from functools import reduce
from builtins import FileNotFoundError
import logging
from .reports import config


class Team():
    """
    Class that sorts and writes to JSON file the Common name and active emails
    of employees directly as well as indirectly reporting to the Manager
    """

    def __init__(self, json_file):
        """
        Class Constructor expecting a JSON file as a parameter to further
        write to
        """
        self.json_file = json_file
        self.read_team_list(json_file)

    def Update(self, ldap_url, ldap_base, email_alias_base,
               skip, static_members):
        """
        Class Function initiating the search from LDAP
        """
        self.ldap_init(ldap_url)
        # Employees directly and indirectly reporting to the manager
        self.team = self.find_employees(config.return_manager_name(),
                                        ldap_base,
                                        email_alias_base, skip)
        # Update the Dict team with hardcoded static members
        self.team.update(static_members)
        self.write_output_to_json(self.json_file, self.team)

    def find_employees(self, manager, ldap_base,
                       email_alias_base, skip):
        """
        Finds employees (direct and indirect) reporting to the Manager
        """
        # List to keep track of employees reporting to
        # Managers and Associate Managers
        employees = self.ldap_direct_employees(manager,
                                               ldap_base)
        team = {}
        emp_multiple_emails = []

        for emp in employees:
            # Skip direct reports to Managers(employees) in "skip variable"
            if self.ldap_emp_cn(emp) in skip:
                print("Skipping Manager:", self.ldap_emp_cn(emp), "and the",
                      "employees reporting to him/her\n")
                continue

            # Find direct reports to this employee
            emp_name = self.ldap_direct_employees(self.ldap_emp_uid(emp),
                                                  ldap_base)
            employees.extend(emp_name)
            # Add team_member to Dict team
            team_member_emp = self.team_member(emp)

            # Gather Multiple emails of the employees in emp_multiple_emails
            # Here ldap_emp_uid(emp) returns the employee's uid for aliases
            emp_multiple_emails = self.email_aliases(email_alias_base,
                                                     self.ldap_emp_uid(emp))

            # Here ldap_emp_cn(emp) returns the emp name which is used
            # as a key to access the items in Dict team_member_emp
            team_member_emp[self.ldap_emp_cn(emp)].extend(emp_multiple_emails)
            team.update(team_member_emp)

        return team

    def ldap_direct_employees(self, manager, ldap_base):
        """
        Finds Direct Employees reporting to the Sub-Managers
        """
        # Intializing the query values
        searchScope = ldap.SCOPE_SUBTREE
        query = "manager=uid={},ou=users,dc=companyname,dc=com".format(manager)
        retrieveAttributes = ["name", "uid", "cn", "mail"]  # Get Attributes

        ldap_obj_return = self.ldap_obj.search_s(ldap_base, searchScope, query,
                                                 retrieveAttributes)
        return ldap_obj_return

    def ldap_init(self, ldap_url):
        """
        Uses GSSAPI mechanism to initialize attribute "ldap_obj"
        """
        # Ideally, "ldap_url" would consit company's LDAP server
        self.ldap_obj = ldap.initialize(ldap_url)
        try:
            self.ldap_obj.simple_bind_s()
        except ldap.INVALID_CREDENTIALS:
            print("Couldn't authenticate!")

        # Specifically use GSSAPI mechanism
        # Commented the code below so that bzreports can run
        # without having to autenticate
        # self.ldap_obj.sasl_gssapi_bind_s(serverctrls=None,
        #                                  clientctrls=None,
        #                                  sasl_flags=ldap.SASL_QUIET,
        #                                  authz_id="")

    def ldap_emp_uid(self, emp):
        """
        To get the name of the employee to pass as an argument,
        we need to decode since bytes are passed as arguments while
        and we need str objects to be passed as arguments
        """
        return emp[1]["uid"][0].decode("utf-8")

    def ldap_emp_cn(self, emp):
        """
        Employee's Common Name returns bytes.
        Decodes and returns a string
        """
        return emp[1]["cn"][0].decode("utf-8")

    def ldap_emp_mail(self, emp):
        """
        Employee's Email returns bytes.
        Decodes and returns a string
        """
        return emp[1]["mail"][0].decode("utf-8")

    def team_member(self, emp):
        """
        Returns the Dict with employee's name as a key and
        list(email) as a value
        """
        name = self.ldap_emp_cn(emp)
        email = self.ldap_emp_mail(emp)
        return {name: [email]}

    # Write the items in Dict Team to the json_file
    def write_output_to_json(self, json_file, team):
        """
        Writes output to the JSON file (in JSON format)
        """
        fp = open(json_file, "w")
        # Writing to the json_file
        json.dump(team, fp, indent=True, sort_keys=True)
        fp.close()

    # Return every employee's email_aliases
    def email_aliases(self, email_alias_base, employee):
        """
        Returns individual employee's email_aliases
        """
        searchScope = ldap.SCOPE_SUBTREE
        alias_value = "sendmailMTAAliasValue={}".format(employee)
        retrieveAttributes = ["companyEmailAddress", "sendmailMTAAliasValue"]

        tmp = self.ldap_obj.search_s(email_alias_base, searchScope,
                                     alias_value, retrieveAttributes)

        # If and only if len(x[1]['sendmailMTAAliasValue']) equals 1 then
        # the email_alias is valid
        tmp = filter(lambda x: len(x[1]["sendmailMTAAliasValue"]) == 1, tmp)
        # Attribute "companyEmailAddress" has the email_aliases
        tmp = map(lambda x: x[1]["companyEmailAddress"], tmp)
        # Check if a list is returned, if true then the email is the first
        # field in the list, else just get the email field
        tmp = map(lambda x: x[0] if isinstance(x, list) else x, tmp)
        # Now the email is in byte format.
        # Need to make it a string
        str_emails = map(lambda byte_mail: byte_mail.decode("utf-8"), tmp)
        return str_emails

    def read_team_list(self, json_file):
        """
        Loads the JSON file if it exists, else intializes attribute "team"
        """
        try:
            fp = open(json_file, 'r')
            self.team = json.load(fp)
        except FileNotFoundError:
            logging.debug("File {} doesn't exist! Creating a new file..."
                          .format(json_file))
            self.team = {}

    def all_emails(self):
        """
        Returns every active email
        """
        emails = reduce(lambda x, y: x+y, self.team.values())
        emails.sort()
        return emails

    def members(self):
        """
        Returns every employee's common name
        """
        members = list(self.team.keys())
        members.sort()
        return members

    def individual_emails(self, member):
        """
        Returns individual employee's active emails
        """
        return self.team[member]
