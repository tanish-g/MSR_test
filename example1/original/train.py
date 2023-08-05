from tqdm import tqdm
from utils import composed_metrics,Handler

class AverageMeter(object):

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

def train(model,optimizer,loss_fn,train_loader,device):
  
  model.train()
  losses = AverageMeter()
  tk = tqdm(train_loader,total = len(train_loader))
  handler = Handler('test')
  metrics = composed_metrics(handler)

  for i,(batch,label) in enumerate(tk):

    batch,label = batch.to(device),label.to(device)

    batch_size = label.size(0)

    pred = model(batch)

    loss = loss_fn(pred,label)
    losses.update(loss.item(),batch_size)
    
    loss.backward()
    
    optimizer.step()
    optimizer.zero_grad()

    handler.logger('loss : '+losses.avg)
    score = metrics.accuracy(label.detach().cpu().numpy(),pred.detach().cpu().numpy())
  
  return losses.avg,score
