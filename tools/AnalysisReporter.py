from CredentialManagement import CredentialManagement
from pyexcel_ods import get_data
import json

data = get_data("expenses.ods")

print(json.dumps(data))
