import re
from apps.customers.models import Customer, Address

def get_customer_by_document(document):
    """Busca cliente pelo documento, retorna ou None."""
    clean_doc = re.sub(r'\D', '', document)
    return Customer.objects.filter(document=clean_doc).first()

def get_customer_by_id(customer_id):
    """Busca cliente pelo ID, retorna ou None."""
    return Customer.objects.filter(pk=customer_id).first()

def get_address_by_customer(customer_id):
    """Busca endereço pelo ID do cliente, retorna ou None."""
    return Address.objects.filter(customer_id=customer_id).first()
