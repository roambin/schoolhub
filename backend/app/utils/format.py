def obj_to_dict(self):
    res = {}
    for key in self.__mapper__.c.keys():
        if getattr(self, key) is not None:
            res[key] = str(getattr(self, key))
        else:
            res[key] = getattr(self, key)
    return res

