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



# ---------------------------- Add code to find the correctIndex -----------------------------------------
# `correct = sess.run(correct_prediction, feed_dict={x: X_test, y: y_test})
#  correctIndex = np.argwhere(correct == True)
#  correctIndex = correctIndex.flatten()`
# FIXME: Add exception to determine whether the function the User insert is correct
# E.g., parse_src = addCorrect('correct_prediction', {'x': 'X_test', 'y': 'y_test'}, 'sess')
def addCorrect(corrFun, feed_dict, sess):
    body, tar1, tar2, tar3 = [], [], [], []

    func1 = ast.Attribute(ast.Name(sess, ast.Load()), 'run', ast.Load())
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

    return body



# ----------------  Add new reshape code -------------------------
# `totalSDC = 0
#  totalFI = 10
#  resFile = open("lenet-bitFI10.csv", "a")
#  XtestShape = list(X_test.shape)
#  ytestShape = list(y_test.shape)
#  XtestShape[0] = 1
#  ytestShape[0] = 1
#  txShape = tuple(XtestShape)
#  tyShape = tuple(ytestShape)`
# E.g., parse_src =addSDC('lenet-sdcrates.csv', 10,'X_test', 'y_test')
def addSDC(filename, totFI, Xtest, ytest):
    body, ass1, ass2, ass3= [], [], [], []

    args, args4, args5, args8, args9 = [], [], [], [], []
    args.append(ast.Str(s=filename))
    args.append(ast.Str(s='a'))
    args4.append(ast.Attribute(ast.Name(Xtest, ast.Load()), 'shape', ast.Load()))
    args5.append(ast.Attribute(ast.Name(ytest, ast.Load()), 'shape', ast.Load()))
    args8.append(ast.Name('XtestShape', ast.Load()))
    args9.append(ast.Name('ytestShape', ast.Load()))

    tar1, tar2, tar3, tar4, tar5, tar6, tar7, tar8, tar9 = [], [], [], [], [], [], [], [], []

    tar1.append(ast.Name('totalSDC', ast.Store()))
    tar2.append(ast.Name('totalFI', ast.Store()))
    tar3.append(ast.Name('resFile', ast.Store()))
    tar4.append(ast.Name('XtestShape', ast.Store()))
    tar5.append(ast.Name('ytestShape', ast.Store()))
    tar6.append(ast.Subscript(ast.Name('XtestShape', ast.Load()), ast.Index(ast.Num(0)), ast.Store()))
    tar7.append(ast.Subscript(ast.Name('ytestShape', ast.Load()), ast.Index(ast.Num(0)), ast.Store()))
    tar8.append(ast.Name('txShape', ast.Store()))
    tar9.append(ast.Name('tyShape', ast.Store()))

    val = ast.Call(ast.Name('open', ast.Load()), args, [], None, None)
    val4 = ast.Call(ast.Name('list', ast.Load()), args4, [], None, None)
    val5 = ast.Call(ast.Name('list', ast.Load()), args5, [], None, None)
    val8 = ast.Call(ast.Name('tuple', ast.Load()), args8, [], None, None)
    val9 = ast.Call(ast.Name('tuple', ast.Load()), args9, [], None, None)

    ass1 = ast.Assign(tar1, ast.Num(0))
    ass2 = ast.Assign(tar2, ast.Num(totFI))
    ass3 = ast.Assign(tar3, val)
    ass4 = ast.Assign(tar4, val4)
    ass5 = ast.Assign(tar5, val5)
    ass6 = ast.Assign(tar6, ast.Num(1))
    ass7 = ast.Assign(tar7, ast.Num(1))
    ass8 = ast.Assign(tar8, val8)
    ass9 = ast.Assign(tar9, val9)

    body.append(ass1)
    body.append(ass2)
    body.append(ass3)
    body.append(ass4)
    body.append(ass5)
    body.append(ass6)
    body.append(ass7)
    body.append(ass8)
    body.append(ass9)

    return body

# ------------------- Add for loop to calculate SDC -------------------------
# `    for i in range(10):
#         SDC = 0
#         tx = X_test[correctIndex[i]]
#         ty = y_test[correctIndex[i]]
#         tx = tx.reshape(txShape)
#         ty = ty.reshape(tyShape)
#         for j in range(totalFI):
#             acy = sess.run(correct_prediction, feed_dict={x: tx, y: ty})
#             if (acy == False):
#                 SDC +=1
#         totalSDC += SDC
#     SDCrates = totalSDC/(10.0*totalFI)
#     resFile.write(str(SDCrates))
#     print("SDC rates: ", SDCrates)
# E.g., parse_src = addLoop('X_test', 'y_test', {'x': 'X_test', 'y': 'y_test'}, 'sess')

def addLoop(Xtest, ytest, sess):

    body, fbody, fName1, fName2, fName3, fNum, aTarg, exargs, eCargs, pvals, pelts, arg3, arg4, argfor, bodyfor= [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

    fNum.append(ast.Num(10))
    fName1.append(ast.Name('SDC', ast.Store()))
    fName2.append(ast.Name('tx', ast.Store()))
    fName3.append(ast.Name('ty', ast.Store()))

    arg3.append(ast.Name('txShape', ast.Load()))
    arg4.append(ast.Name('tyShape', ast.Load()))

    bodyTar, bodyAttrArgs, ops, ifname, ifbody = [], [], [], [], []

    bodyTar.append(ast.Name('acy', ast.Store()))
    bodyAttrArgs.append(ast.Name('correct_prediction', ast.Load()))

    bodyKey, keys, vals = [], [], []
    bodyKey.append(ast.keyword('feed_dict', ast.Dict(keys, vals)))

    keys.append(ast.Name('x', ast.Load()))
    keys.append(ast.Name('y', ast.Load()))
    vals.append(ast.Name('tx', ast.Load()))
    vals.append(ast.Name('ty', ast.Load()))

    ops.append(ast.Eq())
    ifname.append(ast.Name('False', ast.Load()))
    ifbody.append(ast.AugAssign(ast.Name('SDC', ast.Store()), ast.Add(), ast.Num(1)))

    argfor.append(ast.Name('totalFI', ast.Load()))
    bodyfor.append(ast.Assign(bodyTar, ast.Call(ast.Attribute(ast.Name(sess, ast.Load()), 'run', ast.Load()), bodyAttrArgs,
                                       bodyKey, None, None)))
    bodyfor.append(ast.If(ast.Compare(ast.Name('acy', ast.Load()), ops, ifname), ifbody, []))

    ass1 = ast.Assign(fName1, ast.Num(0))
    ass2 = ast.Assign(fName2, ast.Subscript(ast.Name(Xtest, ast.Load()), ast.Index(ast.Subscript(ast.Name('correctIndex', ast.Load()), ast.Index(ast.Name('i', ast.Load())), ast.Load())), ast.Load()))
    ass3 = ast.Assign(fName3, ast.Subscript(ast.Name(ytest, ast.Load()), ast.Index(ast.Subscript(ast.Name('correctIndex', ast.Load()), ast.Index(ast.Name('i', ast.Load())), ast.Load())), ast.Load()))
    ass4 = ast.Assign(fName2, ast.Call(ast.Attribute(ast.Name('tx', ast.Load()), 'reshape', ast.Load()), arg3, [], None, None))
    ass5 = ast.Assign(fName3, ast.Call(ast.Attribute(ast.Name('ty', ast.Load()), 'reshape', ast.Load()), arg4, [], None, None))
    for2 = ast.For(ast.Name('j', ast.Store()), ast.Call(ast.Name('range', ast.Load()), argfor, [], None, None), bodyfor, [])
    augs = ast.AugAssign(ast.Name('totalSDC', ast.Store()),ast.Add(), ast.Name('SDC', ast.Load()))

    fbody.append(ass1)
    fbody.append(ass2)
    fbody.append(ass3)
    fbody.append(ass4)
    fbody.append(ass5)
    fbody.append(for2)
    fbody.append(augs)

    foR = ast.For(ast.Name('i', ast.Store()), ast.Call(ast.Name('range', ast.Load()), fNum, [], None, None), fbody, [])

    aTarg.append(ast.Name('SDCrates', ast.Store()))
    assi = ast.Assign(aTarg, ast.BinOp(ast.Name('totalSDC', ast.Load()), ast.Div(), ast.BinOp(ast.Num(10.0), ast.Mult(), ast.Name('totalFI', ast.Load()))))

    eCargs.append(ast.Name('SDCrates', ast.Load()))
    exargs.append(ast.BinOp(ast.Call(ast.Name('str', ast.Load()), eCargs, [], None, None), ast.Add(), ast.Str(', ')))
    expr = ast.Expr(ast.Call(ast.Attribute(ast.Name('resFile', ast.Load()), 'write', ast.Load()), exargs, [], None, None))

    pelts.append(ast.Str('SDC rates: '))
    pelts.append(ast.Name('SDCrates', ast.Load()))
    pvals.append(ast.Tuple(pelts, ast.Load()))
    prit = ast.Print(None, pvals, True)

    body.append(foR)
    body.append(assi)
    body.append(expr)
    body.append(prit)

    return body




# ------------------------------- Add TensorFI init function -----------------------------------
# `fi = ti.TensorFI(sess,configFileName='./confFiles/eb/default-1eb.yaml', logLevel = 10, name = "lenet", disableInjections=False)`
# E.g.,  parse_src_fi = addFi(parse_src, 'correct_prediction', {'x': 'X_test', 'y': 'y_test'}, 'lenet-sdcrates.csv', 10,'X_test', 'y_test',
#                          'testGen.yaml', "faultLogs/", logging.DEBUG, 'False', 'convolutional', 'fi_')

def addFi(parse_src, # Parsed code
          corrFun, # Function to get the correct prediction
          feed_dict, # feed_dict in sess.run()
          filename, # Name of file to restore the SDC rates.
          totFI, # Number of fault injection
          Xtest, # Variable name of testset X
          ytest, # Variable name of testset Y
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

    corrBody = addCorrect(corrFun, feed_dict, s)
    for i in corrBody:
        tiBody.append(i)

    tiBody.append(ast.Assign(fiNameList, tiCall))

    sdcBody = addSDC(filename, totFI, Xtest, ytest)
    for i in sdcBody:
        tiBody.append(i)

    loopBody = addLoop(Xtest, ytest, s)
    for i in loopBody:
        tiBody.append(i)

    for i in range(len(tiBody)):
        withNode.body.insert(pos+i, tiBody[i])

    ast.fix_missing_locations(parse_src)

    print(astor.to_source(parse_src))
    # print(ast.dump(parse_src))
    return parse_src


if __name__ == '__main__':
    parse_src_import=addImport('lenet-mnist-no-FI.py')
    parse_src_fi =addFi(parse_src_import, 'correct_prediction', {'y': 'y_test', 'x': 'X_test'}, 'lenet-sdcrates.csv', 5,'X_test', 'y_test',
                         '/home/elaine/pycharmProjects/yamlTest/test-1.yaml', "/home/elaine/pycharmProjects/yamlTest/faultLogs/", logging.DEBUG, 'False', 'test', 'fi_')
    with open("Output.py", "w") as f:
        f.write(astor.to_source(parse_src_fi))
    # Execute the parsed code
    # parse_src_import = ast.parse(open('sample.py').read())
    # exec (compile(parse_src_fi, filename="<ast>", mode="exec"), globals())