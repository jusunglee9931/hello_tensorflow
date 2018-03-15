import argparse
import mnist_input_data
import tensorflow as tf
import numpy as np


def parser():
    parser = argparse.ArgumentParser(description = 'variable about parameter')
    parser.add_argument('--epoch-steps',type= int, default =1000,
                         help='the number of epoch steps')
    parser.add_argument('--hidden-size',type= int, default = 100,
                         help='the number of hidden size')
    parser.add_argument('--batch-size', type= int, default = 64,
                         help='size of minibatch')
    parser.add_argument('--mnist-folder', type= str,default ='MNIST_data',
                         help='mnist dataset folder name')
    parser.add_argument('--weight-save-filename',type= str,default='weight.ckpt',
                         help='filename of saved weight')
    return parser.parse_args()


def linear(input,output):
 w= tf.get_variable('w',[input.get_shape()[1],output], 
 initializer = tf.random_normal_initializer())
 b= tf.get_variable('b',[output], 
 initializer = tf.constant_initializer(0.0) )
 return tf.matmul(input,w) + b


class mlp(object):
    def __init__(self,params,inputsize):
      self.hidden_size = params.hidden_size
      self.batch_size = params.batch_size
      self.input = tf.placeholder(tf.float32,[None, inputsize])
      self.outph = tf.placeholder(tf.float32,[None, 10])
      self.out = self.make()
      self.epoch = params.epoch_steps
      self.vsstr = params.weight_save_filename
    def make(self):
      with tf.variable_scope('hidden1'):
       h0 = tf.nn.relu(linear(self.input,self.hidden_size))
      with tf.variable_scope('out'):
       return tf.nn.softmax(linear(h0,10))



def train(model,mnist):
    saver = tf.train.Saver()
    with tf.Session() as sess:
      init = tf.global_variables_initializer()     
      sess.run(init)
      loss = tf.losses.mean_squared_error(labels = model.outph, predictions = model.out)
      optimizer = tf.train.GradientDescentOptimizer(0.01)
      train = optimizer.minimize(loss)
      for i in range(model.epoch):
       #t_loss = 0
       for j in range(0 , mnist.train.num_examples - model.batch_size , model.batch_size):
        tp = mnist.train.images[j:j+model.batch_size]
        lp = mnist.train.labels[j:j+model.batch_size]
        _, loss_value = sess.run((train,loss),feed_dict = {model.input:tp,model.outph:lp})
       #t_loss += loss_value
       #print(t_loss)
      saver.save(sess,"./"+model.vsstr)

'''
       correct_prediction = tf.equal(tf.argmax(model.out,1),tf.argmax(model.outph,1))
       accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
       print(sess.run(accuracy, feed_dict={model.input:mnist.test.images, model.outph :mnist.test.labels}))
'''

def eval(model,mnist):
    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess,"./"+model.vsstr)
        correct_prediction = tf.equal(tf.argmax(model.out,1),tf.argmax(model.outph,1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
        print("test accuracy : %f" % sess.run(accuracy, feed_dict={model.input:mnist.test.images, model.outph : mnist.test.labels}))


def main(args):
    mnist = mnist_input_data.input_data.read_data_sets(args.mnist_folder+"/",one_hot=True)
    model = mlp(args,mnist.train.images[0].size)
    writer = tf.summary.FileWriter('.')
    train(model,mnist)
    writer.add_graph(tf.get_default_graph())
    eval(model,mnist)


if __name__ == '__main__' :
    main(parser())


