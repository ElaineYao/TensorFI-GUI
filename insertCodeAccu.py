
# Add the following code in 'with statement'

# fi = ti.TensorFI(sess, logLevel = 10, name = "lenet", disableInjections=False)
# test_accuracy = evaluate(X_test, y_test)
# print("Accuracy (with injections): {:.3f}".format(test_accuracy))

# ------------------------------------------Start------------------------------------------

import ast
import astor
import logging

# ---------------- Add `import TensorFI as ti`, 'import numpy as np' -----------------
# FIXME: Developer may import numpy as xxx, and this will cause exception
def addImport(fPath):
    i = 0;
    parse_src = ast.parse(open(fPath).read())

    for node in ast.walk(parse_src):
        i = i+1;
        if isinstance(node, ast.Import):
            alia = ast.alias('TensorFI', 'ti')
            alia2 = ast.alias('numpy', 'np')
            aliaList = []
            alia2List = []
            aliaList.append(alia)
            alia2List.append(alia2)
            importBody = ast.Import(aliaList)
            import2Body = ast.Import(alia2List)
            parse_src.body.insert(i, importBody)
            parse_src.body.insert(i+1, import2Body)
            break
    ast.fix_missing_locations(parse_src)
    # print(ast.dump(parse_src))
    # print(astor.to_source(parse_src))
    return parse_src

# -----------------------Add accuracy calculation function----------------------------
# E.g., test_accuracy = evaluate(X_test, y_test)

def addAcc(testX,
           testY,
           evaFun):
    body = []
    nameList = []
    nameList.append(ast.Name('test_accuracy', ast.Store()))
    argList = []
    argList.append(ast.Name(testX, ast.Load()))
    argList.append(ast.Name(testY, ast.Load()))
    accCall = ast.Call(ast.Name(evaFun, ast.Load),argList, [], None, None)
    assiName = ast.Assign(nameList, accCall,)
    body.append(assiName)
    return body

# ----------------------Add accuracy printing function-----------------------------
# E.g., print("Accuracy (with injections): {:.3f}".format(test_accuracy))

def addPrint():
    body = []
    callList = []
    nameList = []
    nameList.append(ast.Name('test_accuracy', ast.Load()))
    callList.append(ast.Call(ast.Attribute(ast.Str('Accuracy (with injections): {:.3f}'), 'format', ast.Load()),
                             nameList,
                             [], None, None))
    printBody = ast.Print(None, callList, True)
    body.append(printBody)
    return body

# ------------------------------- Add TensorFI init function -----------------------------------
# `fi = ti.TensorFI(sess,configFileName='./confFiles/eb/default-1eb.yaml', logLevel = 10, name = "lenet", disableInjections=False)`
#                         'testGen.yaml', "faultLogs/", logging.DEBUG, 'False', 'convolutional', 'fi_')

def addFi(parse_src, # Parsed code
          testX,
          testY,
          evaFun,
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
            s = node.optional_vars.id
            break

    withNode = parse_src.body[i-1]

    pos = len(withNode.body)

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

    tiBody = []

    tiBody.append(ast.Assign(fiNameList, tiCall))

    accBody = addAcc(testX, testY, evaFun)
    for i in accBody:
        tiBody.append(i)

    printBody = addPrint()
    for i in printBody:
        tiBody.append(i)

    for i in range(len(tiBody)):
        withNode.body.insert(pos + i, tiBody[i])

    ast.fix_missing_locations(parse_src)

    print(astor.to_source(parse_src))
    # print(ast.dump(parse_src))
    return parse_src




if __name__ == '__main__':
    parse_src_import=addImport('./Tests/lenet-mnist-no-FI.py')
    parse_src_fi = addFi(parse_src_import,
                         'X_test', 'y_test', 'evaluation',
                         '/home/elaine/pycharmProjects/yamlTest/test-1.yaml',
                         "/home/elaine/pycharmProjects/yamlTest/faultLogs/", logging.DEBUG, 'False', 'test', 'fi_')
    print(astor.to_source(parse_src_fi))