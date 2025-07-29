# FUNCOES AUXILIARES.

from apps.customers.models import Customer

def get_customer_by_document(document):
    """
    Retorna o primeiro cliente com o documento informado.

    Args:
        document (str): Documento (CPF ou CNPJ) do cliente.

    Returns:
        Customer or None: Instância de Customer se encontrado, senão None.
    """
    return Customer.objects.filter(document=document).first()