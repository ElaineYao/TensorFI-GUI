import TensorFI as ti
...
fi = ti.TensorFI(s, fiConf, logLevel, name, disableInjections, fiPrefix)

def evaluate(X_data, y_data):
    ...
    accuracy = sess.run(accuracy_operation, feed_dict={x: X_data, y: y_data})
return accuracy 
