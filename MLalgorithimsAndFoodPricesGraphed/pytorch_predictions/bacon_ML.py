import pandas as pd
import torch
import torch.nn as nn

df = pd.read_csv("/home/ivgo5040/CSCI-4502-Data-Mining-Project/MLalgorithimsAndFoodPricesGraphed/bacon_avg.csv")
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
data = df[months].astype(float)
class MonthModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(1, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )
    def forward(self, x):
        return self.net(x)
    
years = torch.arange(len(df)).float().view(-1,1) 
year_2025 = torch.tensor([[10.0]])                

models = {}
predictions_2025 = {}

for month in months:
    y = torch.tensor(data[month].values, dtype=torch.float32).view(-1,1)

    # Mask out missing values (NaN)
    mask = ~torch.isnan(y.squeeze())
    X_train = years[mask]
    y_train = y[mask]

    # Build + train model
    model = MonthModel()
    opt = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_fn = nn.MSELoss()

    for step in range(2000):
        pred = model(X_train)
        loss = loss_fn(pred, y_train)
        opt.zero_grad()
        loss.backward()
        opt.step()

    models[month] = model

    # Predict missing 2025 month
    pred_2025 = model(year_2025).item()
    predictions_2025[month] = pred_2025

print("\nPredictions for missing 2025 months:")
for m in months:
    print(f"{m}: {predictions_2025[m]:.4f}")
