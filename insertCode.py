import ast
import astor
import logging

# Add `import TensorFI as ti`
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
    ast.fix_missing_locations(parse_src)
    # print(ast.dump(parse_src))
    # print(astor.to_source(parse_src))
    return parse_src

# Add TensorFI init function
# `fi = ti.TensorFI(sess,configFileName='./confFiles/eb/default-1eb.yaml', logLevel = 10, name = "lenet", disableInjections=False)`

def addFi(parse_src, # Parsed code
          configFileName="confFiles/default.yaml",  # Config file for reading fault configuration
          logDir="faultLogs/",  # Log directory for the Fault log (Not to be confused with the logging level below)
          logLevel=logging.DEBUG,  # Logging level {DEBUG=10, INFO=20, ERROR=30}
          disableInjections=False,  # Should we disable injections after instrumenting ?
          name="NoName",  # The name of the injector, used in statistics and logging
          fiPrefix="fi_"):  # Prefix to attach to each node inserted for fault injection

    # org_parse = parse_src
    # print(ast.dump(ast.parse(org_parse)))

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
    ast.fix_missing_locations(parse_src)

    # print(ast.dump(ast.parse(org_parse)))
    print(astor.to_source(parse_src))
    return parse_src


# TODO: Add code to find the correctIndex
# `correct = sess.run(correct_prediction, feed_dict={x: X_test, y: y_test})
#  correctIndex = np.argwhere(correct == True)
#  correctIndex = correctIndex.flatten()`
# FIXME: Add exception to determine whether the function the User insert is correct
# E.g., parse_src = addCorrect(ast.parse(source), 'correct_prediction', {'x': 'X_test', 'y': 'y_test'})
def addCorrect(parse_src, corrFun, feed_dict):
    # FIXME: Add location to insert
    body, tar1, tar2, tar3 = [], [], [], []

    # FIXME: Replace 'sess'; Add import numpy as np
    func1 = ast.Attribute(ast.Name('sess', ast.Load()), 'run', ast.Load())
    func2 = ast.Attribute(ast.Name('np', ast.Load()), 'argwhere', ast.Load())
    func3 = ast.Attribute(ast.Name('correctIndex', ast.Load()), 'flatten', ast.Load())

    ops, arg1, arg2, cpor = [], [], [], []
    ops.append(ast.Eq())
    cpor.append(ast.Name('True', ast.Load()))
    arg1.append(ast.Name(corrFun, ast.Load()))
    arg2.append(ast.Compare(ast.Name('correct', ast.Load()), ops, cpor))

    keyw1, keys, vals = [], [], []
    keyw1.append(ast.keyword('feed_dict', ast.Dict(keys, vals)))
    for k, v in feed_dict.items():
        keys.append(ast.Name(k, ast.Load()))
        vals.append(ast.Name(v, ast.Load()))

    val1 = ast.Call(func1, arg1, keyw1, None, None)
    val2 = ast.Call(func2, arg2, [], None, None)
    val3 = ast.Call(func3, [], [], None, None)

    ass1 = ast.Assign(tar1, val1)
    ass2 = ast.Assign(tar2, val2)
    ass3 = ast.Assign(tar3, val3)
    body.append(ass1)
    body.append(ass2)
    body.append(ass3)

    tar1.append(ast.Name('correct', ast.Store()))
    tar2.append(ast.Name('correctIndex', ast.Store()))
    tar3.append(ast.Name('correctIndex', ast.Store()))

    # FIXME: Add location to insert
    parse_src = ast.Module(body)
    return parse_src



# TODO: Add SDC code
# `totalSDC = 0
#  totalFI = 10
#  resFile = open("lenet-bitFI10.csv", "a")`
# FIXME: filename only exists in debug setting; Now default it is debug; Add location to insert
# E.g., parse_src =addSDC('lenet-bitFI10.csv')
def addSDC(filename):
    body, ass1, ass2, ass3, args, tar1, tar2, tar3 = [], [], [], [], [], [], [], []

    args.append(ast.Str(s=filename))
    args.append(ast.Str(s='a'))
    val = ast.Call(ast.Name('open', ast.Load()), args, [], None, None)

    tar1.append(ast.Name('totalSDC', ast.Store()))
    tar2.append(ast.Name('totalFI', ast.Store()))
    tar3.append(ast.Name('resFile', ast.Store()))

    ass1 = ast.Assign(tar1, ast.Num(0))
    # FIXME: Change num -> 1000
    ass2 = ast.Assign(tar2, ast.Num(10))
    ass3 = ast.Assign(tar3, val)

    body.append(ass1)
    body.append(ass2)
    body.append(ass3)

    # FIXME: Add location to insert
    parse_src = ast.Module(body)
    return parse_src

# TODO: Add for loop to calculate SDC
# `    for i in range(10):
#         # construct single input
#         SDC = 0
#         tx = X_test[correctIndex[i]]
#         ty = y_test[correctIndex[i]]
#         tx = tx.reshape(1, 32, 32, 1)
#         ty = ty.reshape(1)
#         for j in range(totalFI):
#             acy = sess.run(correct_prediction, feed_dict={x: tx, y: ty})
#             # FI does not result in SDC
#             if (acy == True):
#                 resFile.write(`1` + ",")
#             else:
#                 resFile.write(`0` + ",")
#                 SDC +=1
#         totalSDC += SDC
#         resFile.write("\n")
#       print("SDC rates", totalSDC/100.0)`

def addFor():
    print()

if __name__ == '__main__':
    parse_src_import=addImport('lenet-mnist-no-FI.py')
    parse_src_fi = addFi(parse_src_import,  'testGen.yaml', "faultLogs/", logging.DEBUG, 'False', 'convolutional', 'fi_')
    # Execute the parsed code
    # parse_src_import = ast.parse(open('sample.py').read())
    # global_env = {}
    # local_env = {}
    exec (compile(parse_src_fi, filename="<ast>", mode="exec"), globals())
    # exec (compile(parse_src_fi, filename="<ast>", mode="exec"),global_env, local_env)
    # print('global_env'+global_env)
    # print('local_env'+local_env)