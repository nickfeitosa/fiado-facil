from sqlalchemy.orm import Session

from . import models, schemas


def get_client_balance(db: Session, client_id: int) -> float:
    client = (
        db.query(models.Client)
        .filter(models.Client.id == client_id)
        .first()
    )

    if not client:
        return 0.0

    return round(sum(p.value for p in client.purchases), 2)


def list_clients(db: Session):
    clients = (
        db.query(models.Client)
        .order_by(models.Client.name.asc())
        .all()
    )

    result = []

    for client in clients:
        balance = round(
            sum(p.value for p in client.purchases),
            2
        )

        result.append({
            "id": client.id,
            "name": client.name,
            "phone": client.phone,
            "created_at": client.created_at,
            "balance": balance
        })

    return result


def create_client(
    db: Session,
    payload: schemas.ClientCreate
):
    client = models.Client(
        name=payload.name.strip(),
        phone=payload.phone.strip()
    )

    db.add(client)
    db.commit()
    db.refresh(client)

    return client


def list_purchases(db: Session):
    purchases = (
        db.query(models.Purchase)
        .order_by(models.Purchase.created_at.desc())
        .all()
    )

    return [
        {
            "id": p.id,
            "client_id": p.client_id,
            "product": p.product,
            "value": p.value,
            "purchase_date": p.purchase_date,
            "created_at": p.created_at,
            "client_name": p.client.name
        }
        for p in purchases
    ]


def create_purchase(
    db: Session,
    payload: schemas.PurchaseCreate
):
    client = (
        db.query(models.Client)
        .filter(models.Client.id == payload.client_id)
        .first()
    )

    if not client:
        return None

    purchase = models.Purchase(
        client_id=payload.client_id,
        product=payload.product.strip(),
        value=round(payload.value, 2),
        purchase_date=payload.purchase_date
    )

    db.add(purchase)
    db.commit()
    db.refresh(purchase)

    current_balance = get_client_balance(
        db,
        payload.client_id
    )

    receipt_text = (
        f"Olá {client.name}\n"
        f"Sua compra foi registrada:\n"
        f"Produto: {purchase.product}\n"
        f"Valor: R$ {purchase.value:.2f}\n"
        f"Saldo atual: R$ {current_balance:.2f}\n"
        f"Obrigado pela confiança."
    )

    return {
        "purchase": {
            "id": purchase.id,
            "client_id": purchase.client_id,
            "product": purchase.product,
            "value": purchase.value,
            "purchase_date": purchase.purchase_date,
            "created_at": purchase.created_at,
            "client_name": client.name
        },
        "current_balance": current_balance,
        "receipt_text": receipt_text
    }


def get_dashboard(db: Session):
    clients = db.query(models.Client).all()
    purchases = db.query(models.Purchase).all()

    total_clients = len(clients)
    total_purchases = len(purchases)

    total_open_amount = round(
        sum(p.value for p in purchases),
        2
    )

    overdue_clients = 0

    for client in clients:
        balance = sum(
            p.value
            for p in client.purchases
        )

        if balance > 0:
            overdue_clients += 1

    return {
        "total_clients": total_clients,
        "total_purchases": total_purchases,
        "total_open_amount": total_open_amount,
        "overdue_clients": overdue_clients
    }