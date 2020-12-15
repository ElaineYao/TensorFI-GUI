import ast
import astor
import logging

def addImport(fPath):

    i = 0;
    parse_src = ast.parse(open(fPath).read())

    for node in ast.walk(parse_src):
        i = i+1;
        if isinstance(node, ast.Import):
            alia = ast.alias('TensorFI', 'ti')
            aliaList = []
            aliaList.append(alia)
            importBody = ast.Import(aliaList)
            parse_src.body.insert(i, importBody)
            break

    # print(ast.dump(parse_src))
    # print(astor.to_source(parse_src))
    return parse_src


def addFi(parse_src, # Source file path
          configFileName="confFiles/default.yaml",  # Config file for reading fault configuration
          logDir="faultLogs/",  # Log directory for the Fault log (Not to be confused with the logging level below)
          logLevel=logging.DEBUG,  # Logging level {DEBUG=10, INFO=20, ERROR=30}
          disableInjections=False,  # Should we disable injections after instrumenting ?
          name="NoName",  # The name of the injector, used in statistics and logging
          fiPrefix="fi_"):  # Prefix to attach to each node inserted for fault injection

    s = 'tf.Session' # This is the session from tensorFlow
    i=0 # Index in body node
    j=0 # Index in with node

    for node in ast.iter_child_nodes(parse_src):
        i = i+1
        # Find 'with tf.Session as sess', instead of other 'with' expressions
        if isinstance(node, ast.With) and node.context_expr.func.attr == 'Session':
            s = node.body[0].value.func.value.id
            break

    withNode = parse_src.body[i-1]

    for node in ast.walk(withNode):
        j = j+1

    sessName = ast.Name(s, ast.Load())
    sessNameList = []
    sessNameList.append(sessName)
    tiName = ast.Name('ti', ast.Load())
    fiName = ast.Name('fi', ast.Store())
    fiNameList = []
    fiKeyList = []
    fiNameList.append(fiName)
    confKey = ast.keyword('configFileName', ast.Str(configFileName))
    logDKey = ast.keyword('logDir', ast.Str(logDir))
    logKey = ast.keyword('logLevel', ast.Num(logLevel))
    disaKey = ast.keyword('disableInjections', ast.Name(disableInjections, ast.Load()))
    nameKey = ast.keyword('name', ast.Str(name))
    preKey = ast.keyword('fiPrefix', ast.Str(fiPrefix))
    fiKeyList.append(confKey)
    fiKeyList.append(logDKey)
    fiKeyList.append(logKey)
    fiKeyList.append(disaKey)
    fiKeyList.append(nameKey)
    fiKeyList.append(preKey)
    tiAttr = ast.Attribute(tiName, 'TensorFI', ast.Load())
    tiCall = ast.Call(tiAttr, sessNameList, fiKeyList, None, None)
    tiBody = ast.Assign(fiNameList, tiCall)

    withNode.body.insert(j, tiBody)

    # print(ast.dump(ast.parse(source1)))
    print(astor.to_source(parse_src))


if __name__ == '__main__':
    # addImport('astTest.py')
    addFi('sample.py', 'default.yaml', "faultLogs/", logging.DEBUG, 'False', 'convolutional', 'fi_')