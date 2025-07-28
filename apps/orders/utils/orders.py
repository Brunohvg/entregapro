from apps.customers.models import Customer, Address


# FUNCOES AUXILIARES.
def get_customer_by_document(document):
    """
    Retorna o primeiro cliente com o documento informado.

    Args:
        document (str): Documento (CPF ou CNPJ) do cliente.

    Returns:
        Customer or None: Instância de Customer se encontrado, senão None.
    """
    return Customer.objects.filter(document=document).first()


def handle_existing_customer(customer, form_order, form_address):
    """
    Atualiza ou cria endereço e cria um novo pedido para um cliente existente.

    Args:
        customer (Customer): Instância do cliente.
        form_order (OrderForm): Formulário com os dados do pedido.
        form_address (AddressForm): Formulário com os dados do endereço.

    Returns:
        bool: True se tudo foi salvo com sucesso, False se os formulários forem inválidos.
    """
    if not (form_order.is_valid() and form_address.is_valid()):
        return False

    address = Address.objects.filter(customer=customer).first()
    if address:
        # Atualiza endereço existente
        for field, value in form_address.cleaned_data.items():
            setattr(address, field, value)
        address.save()
    else:
        # Cria novo endereço se não tiver
        address = form_address.save(commit=False)
        address.customer = customer
        address.save()

    order = form_order.save(commit=False)
    order.customer = customer
    order.save()
    return True


def handle_new_customer(form_customer, form_address, form_order):
    if not (
        form_customer.is_valid() and form_address.is_valid() and form_order.is_valid()
    ):
        return False

    customer = form_customer.save()

    address = form_address.save(commit=False)
    address.customer = customer
    address.save()

    order = form_order.save(commit=False)
    order.customer = customer
    order.save()

    return True
