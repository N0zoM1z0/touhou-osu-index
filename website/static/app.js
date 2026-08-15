const PAGE_SIZE = 60;
const state = { accepted: [], review: [], mode: "all", query: "", candidates: false, shown: PAGE_SIZE };

const results = document.querySelector("#results");
const count = document.querySelector("#result-count");
const empty = document.querySelector("#empty");
const more = document.querySelector("#more");
const search = document.querySelector("#search");
const candidateToggle = document.querySelector("#candidates");
const modeButtons = [...document.querySelectorAll("[data-mode]")];

function displayMode(mode) {
  return { osu: "osu!", taiko: "taiko", catch: "catch", mania: "mania" }[mode] || mode;
}

function searchable(entry) {
  return [entry.beatmapset_id, entry.artist, entry.title, entry.creator, entry.source,
    entry.status, entry.touhou_kind, ...entry.origin_games, ...entry.original_themes]
    .join(" ").toLocaleLowerCase();
}

function filtered() {
  const source = state.candidates
    ? [...state.accepted, ...state.review.filter((entry) => entry.confidence === "candidate")]
    : state.accepted;
  return source
    .filter((entry) => state.mode === "all" || entry.modes.includes(state.mode))
    .filter((entry) => !state.query || searchable(entry).includes(state.query))
    .sort((a, b) => a.artist.localeCompare(b.artist) || a.title.localeCompare(b.title) || a.beatmapset_id - b.beatmapset_id);
}

function escapeHtml(value) {
  const element = document.createElement("span");
  element.textContent = value;
  return element.innerHTML;
}

function card(entry) {
  const title = entry.title || `Beatmapset #${entry.beatmapset_id}`;
  const artist = entry.artist || "Metadata pending reconciliation";
  const modes = entry.modes.length
    ? entry.modes.map((mode) => `<span>${escapeHtml(displayMode(mode))}</span>`).join("")
    : "<span>mode pending</span>";
  return `<article class="card">
    <a href="https://osu.ppy.sh/beatmapsets/${entry.beatmapset_id}" target="_blank" rel="noopener noreferrer">
      <div class="cover"><img loading="lazy" alt="" src="https://assets.ppy.sh/beatmaps/${entry.beatmapset_id}/covers/list.jpg"><b>${escapeHtml(entry.confidence)}</b></div>
      <div class="card-copy">
        <p class="artist">${escapeHtml(artist)}</p>
        <h3>${escapeHtml(title)}</h3>
        <p class="meta">mapped by ${escapeHtml(entry.creator || "unknown")} · ${escapeHtml(entry.status)}</p>
        <div class="modes">${modes}</div>
        <p class="source">${escapeHtml(entry.source || entry.evidence[0])}</p>
      </div>
    </a>
  </article>`;
}

function render() {
  const matches = filtered();
  const visible = matches.slice(0, state.shown);
  results.innerHTML = visible.map(card).join("");
  count.value = `${matches.length.toLocaleString()} beatmapset${matches.length === 1 ? "" : "s"}`;
  empty.hidden = matches.length !== 0;
  more.hidden = visible.length >= matches.length;
}

function resetAndRender() {
  state.shown = PAGE_SIZE;
  render();
}

search.addEventListener("input", () => {
  state.query = search.value.trim().toLocaleLowerCase();
  resetAndRender();
});

candidateToggle.addEventListener("change", () => {
  state.candidates = candidateToggle.checked;
  resetAndRender();
});

for (const button of modeButtons) {
  button.addEventListener("click", () => {
    state.mode = button.dataset.mode;
    for (const option of modeButtons) {
      const active = option === button;
      option.classList.toggle("active", active);
      option.setAttribute("aria-pressed", String(active));
    }
    resetAndRender();
  });
}

more.addEventListener("click", () => {
  state.shown += PAGE_SIZE;
  render();
});

Promise.all([
  fetch("catalog.json").then((response) => response.json()),
  fetch("review.json").then((response) => response.json()),
]).then(([catalog, review]) => {
  state.accepted = catalog.entries;
  state.review = review.entries;
  render();
}).catch((error) => {
  count.value = "Catalog failed to load";
  empty.textContent = error.message;
  empty.hidden = false;
});
