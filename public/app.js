const API = "/api";

const clientForm = document.getElementById("clientForm");
const purchaseForm = document.getElementById("purchaseForm");

const clientSelect = document.getElementById("clientSelect");
const receipt = document.getElementById("receipt");
const clientsTableBody =
    document.getElementById(
        "clientsTableBody"
    );
const purchasesTableBody =
    document.getElementById(
        "purchasesTableBody"
    );
const totalClients = document.getElementById("totalClients");
const totalPurchases = document.getElementById("totalPurchases");
const totalOpenAmount = document.getElementById("totalOpenAmount");
const overdueClients = document.getElementById("overdueClients");

async function loadDashboard() {
    const response = await fetch(`${API}/dashboard`);
    const data = await response.json();

    totalClients.textContent = data.total_clients;
    totalPurchases.textContent = data.total_purchases;
    totalOpenAmount.textContent =
        `R$ ${data.total_open_amount.toFixed(2)}`;
    overdueClients.textContent = data.overdue_clients;
}

async function loadClients() {

    const response =
        await fetch(`${API}/clients`);

    const clients =
        await response.json();

    clientSelect.innerHTML = "";

    clientsTableBody.innerHTML = "";

    clients.forEach(client => {

        const option =
            document.createElement("option");

        option.value = client.id;

        option.textContent =
            `${client.name} - Saldo R$ ${client.balance.toFixed(2)}`;

        clientSelect.appendChild(option);

        const row =
            document.createElement("tr");

        row.innerHTML = `
            <td>${client.name}</td>
            <td>${client.phone}</td>
            <td>R$ ${client.balance.toFixed(2)}</td>
        `;

        clientsTableBody.appendChild(row);

    });

}
async function loadPurchases() {

    const response =
        await fetch(`${API}/purchases`);

    const purchases =
        await response.json();

    purchasesTableBody.innerHTML = "";

    purchases.forEach(purchase => {

        const row =
            document.createElement("tr");

        row.innerHTML = `
            <td>${purchase.client_name}</td>
            <td>${purchase.product}</td>
            <td>R$ ${purchase.value.toFixed(2)}</td>
            <td>${purchase.purchase_date}</td>
        `;

        purchasesTableBody.appendChild(row);

    });

}

clientForm.addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();

        const payload = {
            name: document.getElementById("name").value,
            phone: document.getElementById("phone").value
        };

        const response = await fetch(
            `${API}/clients`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            }
        );

        if (response.ok) {

            alert("Cliente cadastrado!");

            clientForm.reset();

            await loadClients();
            await loadDashboard();

        }

    }
);

purchaseForm.addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();

        const payload = {

            client_id: parseInt(
                clientSelect.value
            ),

            product:
                document.getElementById(
                    "product"
                ).value,

            value: parseFloat(
                document.getElementById(
                    "value"
                ).value
            ),

            purchase_date:
                document.getElementById(
                    "purchaseDate"
                ).value
        };

        const response = await fetch(
            `${API}/purchases`,
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json"
                },
                body: JSON.stringify(payload)
            }
        );

        const data = await response.json();

        if (response.ok) {

        receipt.value =
            data.receipt_text;

        purchaseForm.reset();

        await loadClients();
        await loadDashboard();
        await loadPurchases();

    alert("Compra registrada!");

}

    }
);

document
    .getElementById(
        "copyReceipt"
    )
    .addEventListener(
        "click",
        async () => {

            await navigator
                .clipboard
                .writeText(
                    receipt.value
                );

            alert(
                "Comprovante copiado!"
            );

        }
    );

async function init() {

    const today =
        new Date()
            .toISOString()
            .split("T")[0];

    document
        .getElementById(
            "purchaseDate"
        ).value = today;

    await loadDashboard();
    await loadClients();
    await loadPurchases();

}

init();