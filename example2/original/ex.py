class rep():
  def log(self,str):
    print(str)
  
  def test(self):
    text = 'Started Testing of Model'
    log(text)
  
  def train(self):
    text = 'Started Training of Model'
    log(text)
  
  def comb(self):
    train()
    test()
