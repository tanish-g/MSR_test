from sklearn.metrics import mean_squared_error, f1_score, log_loss,mean_absolute_error,accuracy_score

class composed_metrics():
  
  def __init__(self,handler):
    self.handler = handler

  def mae(self,y_true, y_pred):
      score = mean_absolute_error(y_true, y_pred) # RMSE
      self.handler.logger('mae : ' + str(score))
      return score

  def accuracy(self,y_true, y_pred):
      score = accuracy_score(y_true, y_pred)
      self.handler.logger('accuracy : ' + str(score))
      return score
