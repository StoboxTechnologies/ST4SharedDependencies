from stobox_dependencies.clients.company import CompanyHTTPClient
from stobox_dependencies.clients.payment import PaymentHTTPClient
from stobox_dependencies.clients.user import UserHTTPClient
from stobox_dependencies.settings.conf import settings

payment_client = PaymentHTTPClient(settings.PAYMENT_SERVICE_URL)
user_client = UserHTTPClient(settings.USER_MANAGER_URL)
company_client = CompanyHTTPClient(settings.COMPANY_MANAGER_URL)
