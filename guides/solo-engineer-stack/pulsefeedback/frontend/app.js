const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

$$(".tab").forEach((btn) => {
  btn.addEventListener("click", () => {
    $$(".tab").forEach((b) => b.classList.remove("active"));
    $$(".panel").forEach((p) => p.classList.remove("active"));
    btn.classList.add("active");
    $(`#${btn.dataset.tab}`).classList.add("active");
    if (btn.dataset.tab === "dashboard") loadFeedback();
    if (btn.dataset.tab === "analytics") loadEvents();
    if (btn.dataset.tab === "stack") loadStack();
  });
});

async function api(path, opts = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || res.statusText);
  return data;
}

$("#feedback-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  const payload = {
    title: fd.get("title"),
    body: fd.get("body"),
    email: fd.get("email") || null,
  };
  try {
    const out = await api("/api/feedback", { method: "POST", body: JSON.stringify(payload) });
    await api("/api/events", {
      method: "POST",
      body: JSON.stringify({ event: "feedback_submitted", properties: { id: out.id } }),
    });
    $("#submit-result").textContent = JSON.stringify(out, null, 2);
    e.target.reset();
  } catch (err) {
    $("#submit-result").textContent = err.message;
  }
});

async function loadFeedback() {
  const list = $("#feedback-list");
  list.innerHTML = "<p>Loading…</p>";
  try {
    const items = await api("/api/feedback");
    if (!items.length) {
      list.innerHTML = "<p>No feedback yet — submit one in the first tab.</p>";
      return;
    }
    list.innerHTML = items
      .map(
        (f) => `
      <article class="card" data-id="${f.id}">
        <h3>${escapeHtml(f.title)}</h3>
        <div class="meta">#${f.id} · ${f.status} · ${f.created_at}</div>
        <p>${escapeHtml(f.body)}</p>
        <div class="status-row">
          ${["new", "triaged", "done"]
            .map(
              (s) =>
                `<button class="status-btn ${f.status === s ? "current" : ""}" data-status="${s}">${s}</button>`
            )
            .join("")}
        </div>
      </article>`
      )
      .join("");

    list.querySelectorAll(".status-btn").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const card = btn.closest(".card");
        const id = card.dataset.id;
        await api(`/api/feedback/${id}`, {
          method: "PATCH",
          body: JSON.stringify({ status: btn.dataset.status }),
        });
        loadFeedback();
      });
    });
  } catch (err) {
    list.innerHTML = `<p>${err.message}</p>`;
  }
}

async function loadEvents() {
  const tbody = $("#events-table tbody");
  tbody.innerHTML = "";
  const events = await api("/api/events");
  events.forEach((ev) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${ev.created_at}</td><td>${escapeHtml(ev.event)}</td><td><code>${escapeHtml(JSON.stringify(ev.properties))}</code></td>`;
    tbody.appendChild(tr);
  });
}

$("#refresh-events").addEventListener("click", loadEvents);

$("#csat-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  const payload = {
    score: Number(fd.get("score")),
    comment: fd.get("comment") || null,
  };
  try {
    const out = await api("/api/webhooks/csat", { method: "POST", body: JSON.stringify(payload) });
    $("#csat-result").textContent =
      JSON.stringify(out, null, 2) +
      (out.loop_triggered
        ? "\n\n→ Check artifacts/11-csat-loop/new-task.json (Deca-Loop back to Task Master)"
        : "");
  } catch (err) {
    $("#csat-result").textContent = err.message;
  }
});

async function loadStack() {
  const grid = $("#stack-grid");
  const tools = await api("/api/stack");
  grid.innerHTML = tools
    .map(
      (t) => `
    <div class="stack-card ${t.live ? "live" : ""}">
      <h3><span class="dot"></span> ${t.id}. ${escapeHtml(t.name)}</h3>
      <p><strong>${escapeHtml(t.role)}</strong></p>
      <p>${escapeHtml(t.artifact)}</p>
      ${t.demo_url ? `<a href="${t.demo_url}" target="_blank" rel="noopener">Open →</a>` : ""}
    </div>`
    )
    .join("");
}

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

loadStack();
