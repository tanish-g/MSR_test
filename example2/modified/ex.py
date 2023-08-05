class rep():
    def log(self, str, loglevel='debug'):
        print(str, ' loglevel : ', loglevel)

    def test(self, loglevel='debug'):
        text = 'Started Testing of Model'
        self.log(text, loglevel=loglevel)

    def train(self, loglevel='debug'):
        text = 'Started Training of Model'
        self.log(text, loglevel=loglevel)

    def comb(self):
        self.train()
        self.test()
