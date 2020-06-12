
import os
import glob
import importlib.util


def importmodule(modulename: str, folderpath: []):
    for fpath in folderpath:
        for path in glob.glob(f'{fpath}/[!_]*.py'):
            name, ext = os.path.splitext(os.path.basename(path))

            if name == modulename:
                spec = importlib.util.spec_from_file_location(
                    name, path.replace("\\", "/"))

                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                return module
    return None


def getinstance(classname: str, folderpath: [], nameGetter=None, **args):
    modulename = classname.lower() if nameGetter == None else nameGetter(classname)
    module = importmodule(modulename, folderpath)

    if module != None:
        klass = getattr(module, classname)
        return klass(**args)

    return None
