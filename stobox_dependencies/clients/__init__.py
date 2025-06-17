from stobox_dependencies.clients.company import CompanyHTTPClient
from stobox_dependencies.clients.payment import PaymentHTTPClient
from stobox_dependencies.clients.user import UserHTTPClient

payment_client = PaymentHTTPClient()
user_client = UserHTTPClient()
company_client = CompanyHTTPClient()
