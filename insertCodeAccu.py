
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
    # body = []
    nameList = []
    nameList.append(ast.Name('test_accuracy', ast.Store()))
    argList = []
    argList.append(ast.Name(testX, ast.Load()))
    argList.append(ast.Name(testY, ast.Load()))
    accCall = ast.Call(ast.Name(evaFun, ast.Load()),argList, [], None, None)
    assiName = ast.Assign(nameList, accCall)
    return assiName
    # body.append(assiName)
    # return body

# ----------------------Add accuracy function-----------------------------
# E.g., accFile = open('accuracy.csv', 'a')
def addFiles(csvName):
    body = []
    nameList = []
    argsList = []
    nameList.append(ast.Name('accFile', ast.Store()))
    argsList.append(ast.Str(csvName+'.csv'))
    argsList.append(ast.Str('a'))
    assibody = ast.Assign(nameList, ast.Call(ast.Name('open', ast.Load()), argsList, [], None, None))
    body.append(assibody)
    return body

# E.g., fiCount = 1000

def addCount(num):
    body = []
    nameList = []
    nameList.append(ast.Name('fiCount', ast.Store()))
    assibody = ast.Assign(nameList, ast.Num(num))
    body.append(assibody)
    return body


def writeFiles():
    # body = []
    binList = []
    nameList = []
    nameList.append(ast.Name('test_accuracy', ast.Load()))
    binList.append(ast.BinOp(ast.Call(ast.Name('str', ast.Load()),
                                      nameList,
                                      [],
                                      None, None),
                             ast.Add(),
                             ast.Str('\n')))
    expbody = ast.Expr(ast.Call(ast.Attribute(ast.Name('accFile', ast.Load()), 'write', ast.Load()),
                                binList,
                                [],
                                None,
                                None))
    return expbody
    # body.append(expbody)
    # return body


# E.g.,
#     for j in range(fiCount):
#         test_accuracy = evaluate(X_test, y_test)
#         accFile.write(str(test_accuracy) + '\n')

def addForloop(testX, testY, evaFun):
    # body = []
    nameList = []
    nameList.append(ast.Name('fiCount', ast.Load()))
    mainbody = []
    accBody = addAcc(testX, testY, evaFun)
    writeBody = writeFiles()
    mainbody.append(accBody)
    mainbody.append(writeBody)
    forbody = ast.For(ast.Name('j', ast.Store()),
                      ast.Call(ast.Name('range', ast.Load()), nameList, [], None, None),
                      mainbody,
                      []
                      )
    return forbody
    # body.append(forbody)
    # return body




# ------------------------------- Add TensorFI init function -----------------------------------
# `fi = ti.TensorFI(sess,configFileName='./confFiles/eb/default-1eb.yaml', logLevel = 10, name = "lenet", disableInjections=False)`
#                         'testGen.yaml', "faultLogs/", logging.DEBUG, 'False', 'convolutional', 'fi_')

def addFi(parse_src, # Parsed code
          testX,
          testY,
          evaFun,
          configFileName,
          csvName,
          num):  # Prefix to attach to each node inserted for fault injection


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
    fiKeyList.append(confKey)
    tiAttr = ast.Attribute(tiName, 'TensorFI', ast.Load())
    tiCall = ast.Call(tiAttr, sessNameList, fiKeyList, None, None)

    tiBody = []

    tiBody.append(ast.Assign(fiNameList, tiCall))

    fileBody = addFiles(csvName)
    for i in fileBody:
        tiBody.append(i)

    countBody = addCount(num)
    for i in countBody:
        tiBody.append(i)

    loopBody = addForloop(testX, testY, evaFun)
    # for i in loopBody:
    tiBody.append(loopBody)

    for i in range(len(tiBody)):
        withNode.body.insert(pos + i, tiBody[i])

    ast.fix_missing_locations(parse_src)

    # print(astor.to_source(parse_src))
    # print(ast.dump(parse_src))
    return parse_src




if __name__ == '__main__':
    parse_src_import=addImport('./Tests/lenet-mnist-no-FI.py')
    parse_src_fi = addFi(parse_src_import,
                         'X_test', 'y_test', 'evaluate',
                         '/home/elaine/pycharmProjects/yamlTest/test-1.yaml', 'accuracy', 100)
    print(astor.to_source(parse_src_fi))
    # exec (compile(parse_src_fi, filename="", mode="exec"))