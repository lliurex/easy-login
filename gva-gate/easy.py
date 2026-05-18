from n4d.client import Client
from n4d.client import CallFailedError

from llxgvagate.user import User, Group
from llxgvagate.base_plugin import BasePlugin
from llxgvagate.error import GvaGateError

class Easy(BasePlugin):
    def __init__(self):
        pass

    @property
    def name(self):
        return "easy"

    def authenticate(self, username, password, callback):
        server = "server"
        if server is not None:
            n4d_remote = Client("https://"+server+":9779")
            try:
                result = n4d_remote.EasyLogin.validate_easy_user(username, password)
            except CallFailedError as e:
                if e.code == -1: 
                    return None, GvaGateError.UserNotFound
                if e.code == -2:
                    return None, GvaGateError.InvalidPassword
                if e.code == -10:
                    return None, GvaGateError.ServerNotFound
            except Exception:
                # Adi not found
                return None, GvaGateError.Error
        else:
            return None, GvaGateError.ServerNotFound
        user = User(result['login'])
        user.name = result['name']
        user.surname = result['surname']
        user.home = result['home']
        user.shell = result['shell']
        user.uid = result['uid']
        user.groups.append(Group(result['group'],70000))
        user.populate_user()
        return user, GvaGateError.Allowed
