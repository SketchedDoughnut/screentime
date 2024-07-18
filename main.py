import time
import os

epoch_seconds = time.time()
epoch_minutes = epoch_seconds / 60
epoch_hours = epoch_minutes / 60
epoch_days = epoch_hours / 24
epoch_months = epoch_days / 31
epoch_years = epoch_months / 12

print(epoch_seconds)
print(epoch_minutes)
print(epoch_hours)
print(epoch_days)
print(epoch_months)
print(epoch_years)