from n4d.client import Client
from n4d.client import CallFailedError
from llxfederation import User, Group

class EasyLogin:
    def __init__(self):
        pass

    def auth_easy(self, username, password):
        n4d_local = Client("https://localhost:9779")
        try:
            server = n4d_local.get_variable('SRV_IP')
        except Exception:
            return None, "temporary_unavailable"
        if server is not None:
            n4d_remote = Client("https://"+server+":9779")
            try:
                result = n4d_remote.EasyLogin.validate_easy_user(username, password)
            except CallFailedError as e:
                if e.code == -1: 
                    return None, "invalid_user"
                if e.code == -2:
                    return None, "invalid_password"
            except Exception:
                # Adi not found
                return None, "invalid_response"
        else:
            return None, "temporary_unavailable"
        user = User(result['login'])
        user.name = result['name']
        user.surname = result['surname']
        user.home = result['home']
        user.shell = result['shell']
        user.uid = result['uid']
        user.groups.append(Group(result['group'],70000))
        user.populate_user()
        return user, None
