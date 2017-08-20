import tensorflow as tf

from test_game import model


def _hparams(vae_type):
    hparams = model.hparams()
    hparams.vae_type = vae_type
    hparams.check_numerics = True
    return hparams

class ModelTest(tf.test.TestCase):

    def _test_training(self, vae_type):
        hparams = _hparams(vae_type)
        vae = model.make_vae(hparams)
        train_op, debug_tensors = model.train_graph(hparams, vae)
        with self.test_session() as sess:
            sess.run(tf.global_variables_initializer())
            elbo_1 = sess.run(debug_tensors["elbo_opt"])
            for _ in range(100):
                sess.run(train_op)
            elbo_2 = sess.run(debug_tensors["elbo_opt"])
            self.assertGreater(elbo_2, elbo_1)

    def _test_generating(self, vae_type):
        hparams = _hparams(vae_type)
        vae = model.make_vae(hparams)
        env_inputs, latents, generated = model.gen_graph(
            hparams, vae)
        with self.test_session() as sess:
            sess.run(tf.global_variables_initializer())
            sess.run([env_inputs, latents, generated])

    def testTrainingISEQ(self):
        self._test_training("ISEQ")

    def testGeneratingISEQ(self):
        self._test_generating("ISEQ")

    def testTrainingRNN(self):
        self._test_training("RNN")

    def testGeneratingRNN(self):
        self._test_generating("RNN")

    def testTrainingSRNN(self):
        self._test_training("SRNN")

    def testGeneratingSRNN(self):
        self._test_generating("SRNN")


if __name__ == "__main__":
    tf.test.main()