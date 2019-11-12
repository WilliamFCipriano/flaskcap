import glob


# I want to write lua in .lua files for portability
# I also want to include it into the package as a .py file, also for portability
def compile_lua_scripts(location='lua'):
    files = glob.glob('%s\\*.lua' % location)

    script_elements = dict()
    index = "__index__ = ["

    for file in files:
        name = file.replace('%s\\' % location, '') \
            .replace('.lua', '')

        index = '%s"%s", ' % (index, name)

        with open(file, 'r') as f:
            script_elements[name] = """__%s__ = \"\"\"%s
                            \"\"\"""" % (name, f.read())

    index = index[:-2]
    index = '%s]' % index

    onload_function = """
def get_scripts():
    
    scripts = dict()
        
    for script in __index__:
        scripts[script] = globals()["__%s__" % script]
    
    return scripts
    """

    script = '%s\n%s\n' % (index, onload_function)

    for element in script_elements:
        script = '%s\n%s' % (script, script_elements[element])

    return script


print(compile_lua_scripts())
