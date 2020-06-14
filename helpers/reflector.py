# Reflection helper methods

def get_enum(enumType, enumName: str):
    for enm in list (enumType):
        if enumName.lower() in str(enm).lower():
            return enm
    return None