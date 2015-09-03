import ldap
import ldap.modlist as modlist


class LdapApiError(Exception):
    pass


class Client(object):
    def __init__(self, ldap_server, bind_dn, bind_password, network_timeout=30):
        self.ldap_server = ldap_server
        self.bind_dn = bind_dn
        self.bind_password = bind_password
        self._connection = None
        self._network_timeout = network_timeout

    def connect(self):
        if self._connection:
            self.disconnect()
        try:
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, 0)
            ldap.set_option(ldap.OPT_NETWORK_TIMEOUT, self._network_timeout)
            self._connection = ldap.initialize(self.ldap_server)
            self._connection.simple_bind_s(self.bind_dn, self.bind_password)
        except ldap.LDAPError, error_message:
            raise LdapApiError(error_message)

        return Session(self._connection)

    def disconnect(self):
        if self._connection:
            self._connection.unbind_s()
        self._connection = None


class Session(object):
    def __init__(self, connection):
        self._connection = connection

    def search_user(self, username, base_dn):
        username = username.encode('utf-8')
        base_dn = base_dn.encode('utf-8')
        results = []
        try:
            results = self._connection.search_s(
                base_dn, ldap.SCOPE_SUBTREE,
                '(&(sAMAccountName=' +
                username +
                ')(objectClass=person))',
                ['distinguishedName']
            )
        except ldap.LDAPError, error_message:
            raise LdapApiError(error_message)

        return results

    def create_user(self, username, base_dn, domain, password='', first_name='', last_name='', email='', group=''):
        """
        Create a new user account in Active Directory.
        """
        username = username.encode('utf-8')
        fname = first_name.encode('utf-8')
        lname = last_name.encode('utf-8')
        domain = domain.encode('utf-8')
        email = email.encode('utf-8')
        group = group.encode('utf-8')

        user_dn = 'cn=%s,%s' % (username, base_dn)

        user_attrs = {
            'objectClass': ['top', 'person', 'organizationalPerson', 'user'],
            'cn': username,
            'userPrincipalName': username + '@' + domain,
            'sAMAccountName': username,
            'givenName': fname,
            'sn': lname,
            # 'member': 'CN=%s,CN=Users,DC=tatar,DC=local' % (group,),
            'displayName': '%s %s' % (fname, lname),
            'unicodePwd': (u'\"%s\"' % password).encode('utf-16-le'),
            'userAccountControl': '66048'
        }
        if email:
            user_attrs['mail'] = email


        user_ldif = modlist.addModlist(user_attrs)

        try:
            self._connection.add_s(user_dn, user_ldif)
        except ldap.LDAPError, error_message:
            raise LdapApiError(error_message)

        # if group:
        #     # user_attrs['member'] = 'CN=%s,CN=Users,DC=tatar,DC=local' % [group]
        #     user_ldif = modlist.addModlist({
        #         'member': 'CN=%s,CN=Users,DC=tatar,DC=local' % (group,),
        #     })
        #     print user_ldif
        #     try:
        #         self._connection.add_s(user_dn, user_ldif)
        #     except ldap.LDAPError, error_message:
        #         raise LdapApiError(error_message)


    def update_user(self, username, base_dn, domain='', password='', first_name='', last_name='', email='', group=''):
        """
        Create a new user account in Active Directory.
        """
        username = username.encode('utf-8')
        fname = first_name.encode('utf-8')
        lname = last_name.encode('utf-8')
        domain = domain.encode('utf-8')
        mail = email.encode('utf-8')
        group = group.encode('utf-8')

        user_dn = 'cn=%s,%s' % (username, base_dn)

        modifs = []

        if first_name:
            modifs.append((
                ldap.MOD_REPLACE, 'givenName', fname
            ))

        if last_name:
            modifs.append((
                ldap.MOD_REPLACE, 'sn', lname
            ))

        if domain:
            modifs.append((
                ldap.MOD_REPLACE, 'userPrincipalName', username + '@' + domain
            ))

        if mail:
            modifs.append((
                ldap.MOD_REPLACE, 'mail', mail
            ))


        if password:
            modifs.append((
                ldap.MOD_REPLACE, 'unicodePwd', (u'\"%s\"' % password).encode('utf-16-le')
            ))

        if modifs:
            try:
                self._connection.modify_s(user_dn, [(
                    ldap.MOD_REPLACE, 'userAccountControl', '514'
                )])
            except ldap.LDAPError, error_message:
                raise LdapApiError(error_message)

            try:
                self._connection.modify_s(user_dn, modifs)
            except ldap.LDAPError, error_message:
                raise LdapApiError(error_message)

            try:
                self._connection.modify_s(user_dn, [(
                    ldap.MOD_REPLACE, 'userAccountControl', '66048'
                )])
            except ldap.LDAPError, error_message:
                raise LdapApiError(error_message)

        return True

    def delete_user(self, username, base_dn):
        username = username.encode('utf-8')
        base_dn = base_dn.encode('utf-8')
        try:
            self._connection.delete_s('cn=%s,%s' % (username, base_dn))
        except ldap.LDAPError, error_message:
            raise LdapApiError(error_message)
