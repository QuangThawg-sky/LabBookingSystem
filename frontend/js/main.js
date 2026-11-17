const API_BASE = "";

let accessToken = localStorage.getItem("access_token");
let currentUser = null;

let rooms = [];
let equipment = [];

let equipmentPage = 0;
const PAGE_SIZE = 10;

let notificationTimer = null;

const $ = (id) => document.getElementById(id);

function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    })[char]);
}

async function apiRequest(path, options = {}) {
    const headers = {
        ...(options.headers || {})
    };

    if (accessToken) {
        headers.Authorization = `Bearer ${accessToken}`;
    }

    if (options.body && typeof options.body !== "string") {
        headers["Content-Type"] = "application/json";
        options.body = JSON.stringify(options.body);
    }

    const response = await fetch(`${API_BASE}${path}`, {
        ...options,
        headers
    });

    if (response.status === 401 && path !== "/auth/login") {
        logout(false);
        throw new Error("Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.");
    }

    if (response.status === 204) {
        return null;
    }

    const data = await response.json().catch(() => null);

    if (!response.ok) {
        const message = data?.detail;
        throw new Error(
            typeof message === "string"
                ? message
                : JSON.stringify(message || `HTTP ${response.status}`)
        );
    }

    return data;
}

function showNotification(message, isError = false) {
    const element = $("notification");

    element.textContent = message;
    element.classList.remove("hidden", "error");

    if (isError) {
        element.classList.add("error");
    }

    clearTimeout(notificationTimer);

    notificationTimer = setTimeout(() => {
        element.classList.add("hidden");
    }, 4000);
}

function showLogin() {
    $("loginPage").classList.remove("hidden");
    $("appPage").classList.add("hidden");
}

function showApplication() {
    $("loginPage").classList.add("hidden");
    $("appPage").classList.remove("hidden");
}

function logout(showMessage = true) {
    accessToken = null;
    currentUser = null;

    localStorage.removeItem("access_token");

    showLogin();

    if (showMessage) {
        $("loginError").textContent = "Bạn đã đăng xuất.";
    }
}

function setUserInformation() {
    const name = currentUser.full_name || currentUser.email || "Người dùng";
    const role = currentUser.role || "student";

    const roleNames = {
        staff: "Nhân viên",
        lecturer: "Giảng viên",
        student: "Sinh viên"
    };

    $("sidebarName").textContent = name;
    $("topbarName").textContent = name;
    $("welcomeName").textContent = name;
    $("sidebarRole").textContent = roleNames[role] || role;

    document.querySelectorAll(".admin-only").forEach(button => {
        button.classList.toggle("hidden", role !== "staff");
    });
}

async function login(event) {
    event.preventDefault();

    $("loginError").textContent = "";

    const email = $("email").value.trim();
    const password = $("password").value;

    try {
        const data = await apiRequest("/auth/login", {
            method: "POST",
            body: { email, password }
        });

        accessToken = data.access_token;
        localStorage.setItem("access_token", accessToken);

        await loadCurrentUser();

        showApplication();
        await loadDashboard();

        showNotification("Đăng nhập thành công.");
    } catch (error) {
        $("loginError").textContent = error.message;
    }
}

async function loadCurrentUser() {
    currentUser = await apiRequest("/auth/me");
    setUserInformation();
}

function showPage(page) {
    const pages = {
        dashboard: "dashboardPage",
        rooms: "roomsPage",
        equipment: "equipmentPage"
    };

    if (!pages[page]) return;

    Object.values(pages).forEach(id => {
        $(id).classList.add("hidden");
    });

    $(pages[page]).classList.remove("hidden");

    document.querySelectorAll(".nav-item").forEach(button => {
        button.classList.toggle("active", button.dataset.page === page);
    });

    const titles = {
        dashboard: "Tổng quan",
        rooms: "Phòng thực hành",
        equipment: "Thiết bị"
    };

    $("pageTitle").textContent = titles[page];

    if (page === "rooms") {
        loadRooms();
    }

    if (page === "equipment") {
        loadEquipment();
    }

    if (page === "dashboard") {
        loadDashboard();
    }
}

function statusLabel(status) {
    const labels = {
        available: "Sẵn sàng",
        in_use: "Đang sử dụng",
        maintenance: "Bảo trì",
        damaged: "Hư hỏng"
    };

    return labels[status] || status;
}

function renderRoomRows(items, targetId) {
    const target = $(targetId);

    if (!items.length) {
        target.innerHTML = `
            <tr><td colspan="${targetId === "roomTable" ? 6 : 4}"
                class="empty-cell">Không có phòng nào.</td></tr>`;
        return;
    }

    target.innerHTML = items.map(room => `
        <tr>
            ${targetId === "roomTable" ? `<td>${room.id}</td>` : ""}
            <td><strong>${escapeHTML(room.name)}</strong></td>
            <td>${escapeHTML(room.location)}</td>
            <td>${room.capacity}</td>
            ${targetId === "roomTable"
                ? `<td>${escapeHTML(room.description || "—")}</td>`
                : ""}
            <td>
                <span class="status ${room.is_active ? "" : "inactive"}">
                    ${room.is_active ? "Hoạt động" : "Ngừng hoạt động"}
                </span>
            </td>
        </tr>
    `).join("");
}

async function loadRooms() {
    try {
        const data = await apiRequest("/rooms/");
        rooms = Array.isArray(data) ? data : data.items || [];

        renderRoomRows(rooms, "roomTable");
        renderRoomRows(rooms.slice(0, 5), "dashboardRoomTable");

        $("roomCount").textContent = rooms.length;
    } catch (error) {
        showNotification("Không tải được danh sách phòng: " + error.message, true);
    }
}

function renderEquipment() {
    const target = $("equipmentTable");

    if (!equipment.length) {
        target.innerHTML = `
            <tr><td colspan="5" class="empty-cell">Không tìm thấy thiết bị.</td></tr>`;

        $("pageInfo").textContent = "Không có dữ liệu";
        $("previousPage").disabled = true;
        $("nextPage").disabled = true;
        return;
    }

    const totalPages = Math.ceil(equipment.length / PAGE_SIZE);

    equipmentPage = Math.min(equipmentPage, totalPages - 1);

    const start = equipmentPage * PAGE_SIZE;
    const items = equipment.slice(start, start + PAGE_SIZE);

    target.innerHTML = items.map(item => `
        <tr>
            <td>${item.id}</td>
            <td><strong>${escapeHTML(item.name)}</strong></td>
            <td>${escapeHTML(item.asset_code)}</td>
            <td>${escapeHTML(item.description || "—")}</td>
            <td>
                <span class="status ${escapeHTML(item.status)}">
                    ${escapeHTML(statusLabel(item.status))}
                </span>
            </td>
        </tr>
    `).join("");

    $("pageInfo").textContent =
        `Trang ${equipmentPage + 1} / ${totalPages}`;

    $("previousPage").disabled = equipmentPage === 0;
    $("nextPage").disabled = equipmentPage >= totalPages - 1;
}

async function loadEquipment() {
    const search = $("equipmentSearch").value.trim();
    const status = $("equipmentStatus").value;

    const params = new URLSearchParams({
        skip: "0",
        limit: "500"
    });

    if (search) params.set("search", search);
    if (status) params.set("status", status);

    try {
        const data = await apiRequest(`/equipment/?${params.toString()}`);

        equipment = Array.isArray(data) ? data : data.items || [];

        equipmentPage = 0;
        renderEquipment();

        $("equipmentCount").textContent = equipment.length;
        $("availableCount").textContent =
            equipment.filter(item => item.status === "available").length;
    } catch (error) {
        showNotification("Không tải được thiết bị: " + error.message, true);
    }
}

async function loadDashboard() {
    await Promise.all([
        loadRooms(),
        loadEquipment()
    ]);
}

function openModal(id) {
    $(id).classList.remove("hidden");
}

function closeModal(id) {
    $(id).classList.add("hidden");
}

async function createRoom(event) {
    event.preventDefault();

    if (currentUser?.role !== "staff") {
        showNotification("Bạn không có quyền thêm phòng.", true);
        return;
    }

    const body = {
        name: $("roomName").value.trim(),
        location: $("roomLocation").value.trim(),
        capacity: Number($("roomCapacity").value),
        description: $("roomDescription").value.trim(),
        is_active: true
    };

    try {
        await apiRequest("/rooms/", {
            method: "POST",
            body
        });

        closeModal("roomModal");
        $("roomForm").reset();

        await loadRooms();
        showNotification("Thêm phòng thành công.");
    } catch (error) {
        showNotification("Không thêm được phòng: " + error.message, true);
    }
}

async function createEquipment(event) {
    event.preventDefault();

    if (currentUser?.role !== "staff") {
        showNotification("Bạn không có quyền thêm thiết bị.", true);
        return;
    }

    const body = {
        name: $("equipmentName").value.trim(),
        asset_code: $("assetCode").value.trim(),
        description: $("equipmentDescription").value.trim(),
        status: $("newEquipmentStatus").value
    };

    try {
        await apiRequest("/equipment/", {
            method: "POST",
            body
        });

        closeModal("equipmentModal");
        $("equipmentForm").reset();

        await loadEquipment();
        showNotification("Thêm thiết bị thành công.");
    } catch (error) {
        showNotification("Không thêm được thiết bị: " + error.message, true);
    }
}

function debounce(callback, delay = 350) {
    let timer;

    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => callback(...args), delay);
    };
}

function initializeEvents() {
    $("loginForm").addEventListener("submit", login);

    $("logoutButton").addEventListener("click", () => logout());

    document.querySelectorAll(".nav-item").forEach(button => {
        button.addEventListener("click", () => showPage(button.dataset.page));
    });

    document.querySelectorAll("[data-goto]").forEach(button => {
        button.addEventListener("click", () => showPage(button.dataset.goto));
    });

    $("addRoomButton").addEventListener("click", () => openModal("roomModal"));
    $("addEquipmentButton").addEventListener("click", () => openModal("equipmentModal"));

    $("roomForm").addEventListener("submit", createRoom);
    $("equipmentForm").addEventListener("submit", createEquipment);

    document.querySelectorAll("[data-close]").forEach(button => {
        button.addEventListener("click", () => closeModal(button.dataset.close));
    });

    document.querySelectorAll(".modal").forEach(modal => {
        modal.addEventListener("click", event => {
            if (event.target === modal) {
                closeModal(modal.id);
            }
        });
    });

    $("equipmentSearch").addEventListener(
        "input",
        debounce(() => {
            equipmentPage = 0;
            loadEquipment();
        })
    );

    $("equipmentStatus").addEventListener("change", () => {
        equipmentPage = 0;
        loadEquipment();
    });

    $("previousPage").addEventListener("click", () => {
        if (equipmentPage > 0) {
            equipmentPage--;
            renderEquipment();
        }
    });

    $("nextPage").addEventListener("click", () => {
        if ((equipmentPage + 1) * PAGE_SIZE < equipment.length) {
            equipmentPage++;
            renderEquipment();
        }
    });
}

async function initialize() {
    initializeEvents();

    if (!accessToken) {
        showLogin();
        return;
    }

    try {
        await loadCurrentUser();
        showApplication();
        await loadDashboard();
    } catch (error) {
        logout(false);
    }
}

document.addEventListener("DOMContentLoaded", initialize);