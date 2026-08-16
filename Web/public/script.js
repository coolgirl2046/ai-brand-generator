// AI 브랜드 아이덴티티 생성기 - 프론트엔드 로직

const form = document.getElementById("brief-form");
const errorEl = document.getElementById("form-error");
const submitBtn = document.getElementById("submit-btn");
const submitBtnLabel = submitBtn.querySelector(".submit-btn-label");
const resultSection = document.getElementById("result-section");

function showError(message) {
  errorEl.textContent = message;
  errorEl.hidden = false;
}

function clearError() {
  errorEl.hidden = true;
  errorEl.textContent = "";
}

function getRequiredFields() {
  return [
    { el: document.getElementById("industry"), label: "업종" },
    { el: document.getElementById("target"), label: "타겟" },
    { el: document.getElementById("keywords"), label: "키워드" },
  ];
}

function validateForm() {
  const missing = [];
  for (const field of getRequiredFields()) {
    field.el.classList.add("touched");
    if (!field.el.value.trim()) {
      missing.push(field.label);
    }
  }
  if (missing.length > 0) {
    showError(`필수 항목을 입력해주세요: ${missing.join(", ")}`);
    return false;
  }
  clearError();
  return true;
}

function splitCommaList(value) {
  return value
    .split(",")
    .map((s) => s.trim())
    .filter((s) => s.length > 0);
}

function buildBriefPayload() {
  return {
    industry: document.getElementById("industry").value.trim(),
    target: document.getElementById("target").value.trim(),
    keywords: splitCommaList(document.getElementById("keywords").value),
    tone: document.getElementById("tone").value.trim(),
    competitors: splitCommaList(document.getElementById("competitors").value),
    notes: document.getElementById("notes").value.trim(),
  };
}

function setLoading(isLoading) {
  submitBtn.disabled = isLoading;
  submitBtn.classList.toggle("is-loading", isLoading);
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str ?? "";
  return div.innerHTML;
}

function renderResult(data) {
  const parts = [];

  parts.push(`<div class="result-index">SPEC / 02 · 생성 결과</div>`);

  parts.push(`<section class="result-block"><h2 class="result-title">브랜드 네이밍</h2>`);
  if (data.names && data.names.length > 0) {
    parts.push(`<div class="name-list">`);
    for (const item of data.names) {
      const suffix = item.name_en ? ` <span class="name-en">(${escapeHtml(item.name_en)})</span>` : "";
      parts.push(`
        <div class="name-card">
          <p class="name-kr">${escapeHtml(item.name)}${suffix}</p>
          <p class="name-meaning">${escapeHtml(item.meaning)}</p>
        </div>
      `);
    }
    parts.push(`</div>`);
  } else {
    parts.push(`<p class="result-empty">네이밍 생성에 실패했습니다.</p>`);
  }
  parts.push(`</section>`);

  parts.push(`<section class="result-block"><h2 class="result-title">슬로건</h2>`);
  if (data.slogans && data.slogans.length > 0) {
    parts.push(`<ul class="slogan-list">`);
    for (const s of data.slogans) {
      parts.push(`<li>"${escapeHtml(s)}"</li>`);
    }
    parts.push(`</ul>`);
  } else {
    parts.push(`<p class="result-empty">슬로건 생성에 실패했습니다.</p>`);
  }
  parts.push(`</section>`);

  parts.push(`<section class="result-block"><h2 class="result-title">브랜드 스토리</h2>`);
  if (data.story) {
    parts.push(`<blockquote class="story-block">${escapeHtml(data.story)}</blockquote>`);
  } else {
    parts.push(`<p class="result-empty">스토리 생성에 실패했습니다.</p>`);
  }
  parts.push(`</section>`);

  parts.push(`<section class="result-block"><h2 class="result-title">컬러 팔레트</h2>`);
  if (data.colors && data.colors.main) {
    parts.push(`<div class="swatch-row">`);
    parts.push(`
      <div class="swatch-chip">
        <div class="swatch-color" style="background:${escapeHtml(data.colors.main)}"></div>
        <p class="swatch-label">MAIN</p>
        <p class="swatch-hex">${escapeHtml(data.colors.main)}</p>
      </div>
    `);
    for (const sub of data.colors.subs || []) {
      parts.push(`
        <div class="swatch-chip">
          <div class="swatch-color" style="background:${escapeHtml(sub)}"></div>
          <p class="swatch-label">SUB</p>
          <p class="swatch-hex">${escapeHtml(sub)}</p>
        </div>
      `);
    }
    parts.push(`</div>`);
    if (data.palette_image_base64) {
      parts.push(`<img class="palette-image" src="data:image/png;base64,${data.palette_image_base64}" alt="컬러 팔레트 시각화">`);
    }
  } else {
    parts.push(`<p class="result-empty">컬러 팔레트 생성에 실패했습니다.</p>`);
  }
  parts.push(`</section>`);

  parts.push(`<section class="result-block"><h2 class="result-title">로고 시안</h2>`);
  if (data.logos_base64 && data.logos_base64.length > 0) {
    parts.push(`<div class="logo-grid">`);
    data.logos_base64.forEach((b64, i) => {
      parts.push(`
        <div class="logo-card">
          <img src="data:image/png;base64,${b64}" alt="로고 시안 ${i + 1}">
          <p class="logo-caption">시안 ${i + 1}</p>
        </div>
      `);
    });
    parts.push(`</div>`);
  } else {
    parts.push(`<p class="result-empty">로고 시안 생성에 실패했습니다.</p>`);
  }
  parts.push(`</section>`);

  if (data.competitor_differentiators && data.competitor_differentiators.length > 0) {
    parts.push(`<section class="result-block"><h2 class="result-title">경쟁사 차별화 포인트 <span class="bonus-tag">보너스</span></h2>`);
    parts.push(`<ul class="diff-list">`);
    for (const d of data.competitor_differentiators) {
      parts.push(`<li>${escapeHtml(d)}</li>`);
    }
    parts.push(`</ul></section>`);
  }

  if (data.markdown_report) {
    parts.push(`
      <div class="download-row">
        <button type="button" id="download-md-btn" class="download-btn">Markdown 리포트 다운로드</button>
      </div>
    `);
  }

  resultSection.innerHTML = parts.join("\n");
  resultSection.hidden = false;

  if (data.markdown_report) {
    document.getElementById("download-md-btn").addEventListener("click", () => {
      const blob = new Blob([data.markdown_report], { type: "text/markdown;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "brand_result.md";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    });
  }

  resultSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

async function submitBrief(brief) {
  const response = await fetch("/api/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(brief),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || `요청 실패 (HTTP ${response.status})`);
  }

  return data;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!validateForm()) {
    return;
  }

  const brief = buildBriefPayload();

  setLoading(true);
  resultSection.hidden = true;

  try {
    const data = await submitBrief(brief);
    renderResult(data);
  } catch (err) {
    showError(err.message || "생성 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.");
  } finally {
    setLoading(false);
  }
});