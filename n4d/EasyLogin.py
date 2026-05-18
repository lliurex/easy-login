import bson
from pathlib import Path
from yaml import safe_load
import n4d.responses
from random import randrange, randint
from n4d.server.core import Core



class EasyLogin:
    USER_NOT_FOUND = -1
    PASSWORD_INVALID = -2
    USER_NOT_IN_CACHE = -10
    USER_CACHE_EXPIRED = -11
    GENERIC_ERROR = -20
    WRONG_SAVE = -30

    def __init__(self) -> None:
        self.load_default_paths()
        self.load_config()
        self.core = Core.get_core()
        theme_path = Path(self.config['theme']['path'])
        if theme_path.exists():
            self.sorted_index_keys   = sorted(list(map(lambda a: int(a.stem),theme_path.glob("*"))))
        else:
            self.min_index = 0
            self.max_index = 8

    def load_default_paths(self):
        self.config_path = Path("/etc/easy-login/config.yaml")
        self.db_path = Path("/var/lib/easy-login/shadow.db")

    
    def get_config(self) -> Path:
        return n4d.build_successful_call_response(self.config)

    def load_config(self) -> None:
        self.config = safe_load(self.config_path.read_text()) if self.config_path.exists() else { "initial_uid": 70000, "password_lenght": 4, "theme": {"path": "/usr/share/easy-login/themes/animals"} }

    def set_status_service(self, status) -> bool:
        self.core.set_variable("EASYLOGIN_STATUS", status)
        return n4d.responses.build_successful_call_response(True)

    def get_status_service(self) -> bool:
        status = self.core.get_variable("EASYLOGIN_STATUS").get('return',True)
        return n4d.responses.build_successful_call_response(status)

    def get_user_list(self) -> dict:
        self.exists_or_build_db()
        try:
            with self.db_path.open("br") as fd:
                users_db = bson.decode(fd.read())
            return n4d.responses.build_successful_call_response({k:v["info"] for k,v in users_db.items()})
        except Exception:
            return n4d.responses.build_failed_call_response(EasyLogin.USER_NOT_IN_CACHE)

    def get_valid_username(self):
        self.exists_or_build_db()
        with self.db_path.open("br") as fd:
            cache = bson.decode(fd.read())
        excluded = [ int(x)for x in cache.keys() ]
        
        d = len(self.sorted_index_keys)
        total = d ** self.config["password_lenght"]
        n_available = total - len(excluded)
        if n_available <= 0:
            return n4d.responses.build_failed_call_response("database full")

        pick = randint(0, n_available - 1)

        locked_indices = sorted(
                index for s in excluded
                if len(s) == self.config["password_lenght"] and all(c in self.sorted_index_keys for c in s)
                if (index := self._string_to_index(s, self.sorted_index_keys)) is not None
                )
        
        for idx in locked_indices:
            if idx <= pick:
                pick += 1
            else:
                break
        result = self._index_to_string(pick, self.sorted_index_keys, self.config["password_lenght"])
        return n4d.responses.build_successful_call_response(result)
        #return n4d.responses.build_successful_call_response( 
        #           str(result).rjust( int( self.config["password_lenght"] ), str( self.min_index ) ) )


    def _string_to_index(self, s: str, allowed: list[str]) -> int | None:
        allowed = sorted(allowed)
        d = len(allowed)
        idx = 0
        for c in s:
            if c not in allowed:
                return None
            idx = idx * d + allowed.index(c)
        return idx

    def _index_to_string(self, idx: int, allowed: list[str], length: int) -> str:
        allowed = sorted(allowed)
        d = len(allowed)
        digits = []
        for _ in range(length):
            digits.append(allowed[idx % d])
            idx //= d
        return "".join(reversed(digits))

    def validate_easy_user(self, username, password) -> n4d.responses:
        status = self.core.get_variable("EASYLOGIN_STATUS").get('return',True)
        if not status:
            return n4d.responses.build_failed_call_response(EasyLogin.USER_NOT_IN_CACHE)
        user = self.load_user(username.split("@")[0])
        if user is None:
            return n4d.responses.build_failed_call_response(EasyLogin.USER_NOT_FOUND)
        result = True 
        if result:
            user.pop("hash", None)
            return n4d.responses.build_successful_call_response(user["info"])
        return n4d.responses.build_failed_call_response(EasyLogin.PASSWORD_INVALID)

    def store_id_user(self, username, info) -> n4d.responses:
       
        user = {
                "login":".easy",
                "name":"",
                "surname":"",
                "home":"/home/",
                "shell":"/bin/bash",
                "uid": 70000,
                "group": "alumnos"
                }
        
        if "name" in info:
            user["name"] = info["name"]
        if "surname" in info:
            user["surname"] = info["surname"]
        if "login" in info:
            user["login"] = info["login"] + user["login"].lower()
        else:
            aux = ""
            if "name" in info:
                aux = info["name"][0:3]
            if "surname" in info:
                aux = aux + info["surname"][0:3]
            if aux == "":
                aux = ''.join([chr(randrange(97, 123)) for i in range(6)])
            user["login"] = aux + user["login"].lower()
        user["home"] = user["home"] + user["login"]
        
        if "uid" in user.keys() and user["uid"] != "":
            user["uid"] = info["uid"]
        else:
            user["uid"] = self.get_next_uid()

        if user is not None:
            user_info = {}
            user_info['info'] = user
            pass_hash = "" 
            user_info["hash"] = pass_hash
            if self.save_info(username, user_info):
                return n4d.responses.build_successful_call_response(True)
        return n4d.responses.build_failed_call_response(EasyLogin.WRONG_SAVE)


    def save_info(self, username, info) -> bool:
        self.exists_or_build_db()
        try:
            with self.db_path.open("br") as fd:
                users_db = bson.decode(fd.read())
        except Exception:
            users_db = {}
        try:
            users_db[username] = info
            with self.db_path.open("bw") as fd:
                fd.write(bson.encode(users_db))
            return True
        except Exception:
            return False

    def remove_entry(self, username) -> n4d.responses:
        self.exists_or_build_db()
        try:
            with self.db_path.open("br") as fd:
                cache = bson.decode(fd.read())
            if username in cache:
                del cache[username]
            with self.db_path.open("bw") as fd:
                fd.write(bson.encode(cache))
            return n4d.responses.build_successful_call_response(True)
        except Exception:
            return n4d.responses.build_failed_call_response(EasyLogin.GENERIC_ERROR)

    def _load_user(self, username) -> dict:
        self.exists_or_build_db()
        with self.db_path.open("br") as fd:
            cache = bson.decode(fd.read())
        if username in cache:
            return cache[username]
        return None

    def load_user(self, username) -> dict:
        result = self._load_user(username) 
        if result is not None:
            result.pop("hash", None)
            return n4d.responses.build_successful_call_response(result["info"])
        return n4d.responses.build_failed_call_response(EasyLogin.USER_NOT_IN_CACHE)

    def get_next_uid(self) -> int:
        self.exists_or_build_db()
        try:
            with self.db_path.open("br") as fd:
                users_db = bson.decode(fd.read())
        except Exception:
            users_db = {}
        if len(users_db) == 0:
            return self.config["initial_uid"]

        max_uid = max([user["info"]["uid"] for user in users_db.values()])
        return max_uid + 1

    def exists_or_build_db(self) -> bool:
        if not self.db_path.parent.exists():
            self.db_path.parent.mkdir(parents=True,
                                         exist_ok=True,
                                         mode=0o700)
        if not self.db_path.exists():
            self.db_path.touch(mode=0o600)
            self._wipe_db()
        return True

    def wipe_db(self) -> n4d.responses:
        self.exists_or_build_db()
        self._wipe_db()
        return n4d.responses.build_successful_call_response(True)

    def _wipe_db(self):
        with self.db_path.open("bw") as fd:
            fd.write(bson.encode({}))
