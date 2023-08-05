class Handler():
  def __init__(self,filename):
     self.filename = filename
  
  def logger(self,string,loglevel='debug'):
     print(str, ' loglevel : ', loglevel)
