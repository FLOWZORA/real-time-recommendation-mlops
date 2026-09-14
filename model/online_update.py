import torch
from torch.optim import Adam
import mlflow

_optimizer = None
_loss_fn = torch.nn.BCEWithLogitsLoss()

def init_online_learning(model):
    global _optimizer
    _optimizer = Adam(model.user.parameters(), lr=1e-3)
    print("[OK] Online learning optimizer initialized")


def online_update(model, user_features, item_features, label: float):
    global _optimizer
    if _optimizer is None:
        init_online_learning(model)

    model.train()

    score = model(user_features, item_features).view(-1)
    target = torch.tensor([float(label)], dtype=torch.float32).view(-1)

    loss = _loss_fn(score, target)

    _optimizer.zero_grad()
    loss.backward()
    _optimizer.step()

    # Log online loss to MLflow if active run exists
    try:
        if mlflow.active_run():
            mlflow.log_metric("online_loss", loss.item())
    except Exception:
        pass

    return loss.item()

