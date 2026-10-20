# SRE Practice Skills for Claude Code

[English](#english) | [中文](#中文)

---

## English

Eight agent skills that teach Claude Code how to apply Site Reliability Engineering practices: SLOs, alerting, incident response, postmortems, on-call, releases, capacity and data reliability.

The skills are based on the ideas in Google's two free SRE books:

- *Site Reliability Engineering* (2016) — https://sre.google/sre-book/table-of-contents/
- *The Site Reliability Workbook* (2018) — https://sre.google/workbook/table-of-contents/

> **Unofficial project.** This is not affiliated with or endorsed by Google. The skills are
> original procedures and checklists written in our own words; they do not reproduce the
> books' text. Each skill links to the chapters it draws on, so read those for depth.
> The books are © Google, published by O'Reilly Media, and licensed under
> [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/).

### Install

Copy the `sre-*` folders into a Claude Code skills directory.

For one project:
```bash
mkdir -p .claude/skills && cp -r sre-* .claude/skills/
```

For all your projects:
```bash
mkdir -p ~/.claude/skills && cp -r sre-* ~/.claude/skills/
```

The skills use the standard `SKILL.md` format, so they also work in other agents that support Agent Skills.

### Usage

Claude loads a skill automatically when your request matches its description. You can also name one directly:

```text
Use sre-slos-and-error-budgets to propose SLOs for our checkout API.
Use sre-postmortem to review this incident write-up.
Use sre-monitoring-and-alerting to turn a 99.9% SLO into Prometheus alerts.
```

### Skills

| Skill | What it covers |
|---|---|
| `sre-slos-and-error-budgets` | Choosing SLIs, setting SLO targets, SLO documents, error budget policies, budget-based prioritization |
| `sre-monitoring-and-alerting` | Golden signals, dashboards, alert hygiene, multiwindow multi-burn-rate SLO alerts |
| `sre-incident-response` | Declaring incidents, incident command roles, the live incident document, mitigation, drills, systematic troubleshooting |
| `sre-postmortem` | Blameless postmortems, action items, review checklist, postmortem culture |
| `sre-on-call-and-toil` | On-call rotation design, page load, interrupts, onboarding, team overload, toil, safe automation, adopting SRE |
| `sre-release-and-launch` | Release engineering, canary analysis, configuration design, reliability testing, launch checklists, production readiness reviews |
| `sre-capacity-and-system-design` | Capacity math, load balancing, overload, cascading failures, simplicity, distributed consensus |
| `sre-data-reliability` | Data pipelines, scheduled jobs, backups and restores, data integrity |

### Included templates and tools

| Path | Contents |
|---|---|
| `sre-slos-and-error-budgets/references/` | SLI menu by component type, SLO document template, error budget policy template |
| `sre-monitoring-and-alerting/references/prometheus-rules.md` | Prometheus recording and alerting rules |
| `sre-monitoring-and-alerting/scripts/burn_rate.py` | Burn-rate and alert-threshold calculator (Python standard library only) |
| `sre-incident-response/references/` | Live incident state document template |
| `sre-postmortem/references/` | Postmortem template |
| `sre-release-and-launch/references/` | Launch checklist, production best-practices audit list |
| `sre-capacity-and-system-design/references/` | Back-of-envelope estimation cheatsheet |

Example:
```bash
python3 sre-monitoring-and-alerting/scripts/burn_rate.py --slo 99.9 --period-days 30
```

### Contributing

Issues and pull requests are welcome. Please keep contributions in your own words: do not paste text, tables or code from the books.

### License

- Documentation (`SKILL.md` files, templates, references): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- Code (`scripts/`): [MIT](https://opensource.org/licenses/MIT)

These licenses apply only to the original content in this repository. They do not relicense any part of Google's books.

---

## 中文

八個 agent skills，讓 Claude Code 懂得運用網站可靠性工程（SRE）的實務做法，涵蓋 SLO、告警、事件應變、事後檢討、值班、發布、容量規劃與資料可靠性。

內容依據 Google 免費公開的兩本 SRE 書籍中的觀念整理：

- 《Site Reliability Engineering》（2016）— https://sre.google/sre-book/table-of-contents/
- 《The Site Reliability Workbook》（2018）— https://sre.google/workbook/table-of-contents/

> **非官方專案。** 本專案與 Google 無關，也未經 Google 認可。這些 skills 是以我們自己的文字
> 重新撰寫的操作步驟與檢查清單，並未摘錄原書文字。每個 skill 都附有對應章節的連結，
> 想深入了解請閱讀原書。原書 © Google，由 O'Reilly Media 出版，以
> [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) 授權。

### 安裝

把 `sre-*` 資料夾複製到 Claude Code 的 skills 目錄。

只用在單一專案：
```bash
mkdir -p .claude/skills && cp -r sre-* .claude/skills/
```

用在所有專案：
```bash
mkdir -p ~/.claude/skills && cp -r sre-* ~/.claude/skills/
```

這些 skills 採用標準的 `SKILL.md` 格式，其他支援 Agent Skills 的 agent 也能使用。

### 使用方式

當你的需求符合某個 skill 的描述時，Claude 會自動載入它。你也可以直接指定：

```text
用 sre-slos-and-error-budgets 幫我們的結帳 API 訂 SLO。
用 sre-postmortem 檢查這份事件報告。
用 sre-monitoring-and-alerting 把 99.9% 的 SLO 轉成 Prometheus 告警。
```

### Skills 一覽

| Skill | 涵蓋內容 |
|---|---|
| `sre-slos-and-error-budgets` | 選擇 SLI、設定 SLO 目標、SLO 文件、錯誤預算政策、依錯誤預算排定優先順序 |
| `sre-monitoring-and-alerting` | 黃金四信號、儀表板、告警整理、多視窗多燒錄率 SLO 告警 |
| `sre-incident-response` | 宣告事件、事件指揮角色、即時事件文件、緩解措施、演練、系統化除錯 |
| `sre-postmortem` | 無責事後檢討、行動項目、審查清單、事後檢討文化 |
| `sre-on-call-and-toil` | 值班輪班設計、告警負擔、干擾處理、新人培訓、團隊過載、瑣事（toil）、安全自動化、導入 SRE |
| `sre-release-and-launch` | 發布工程、金絲雀分析、組態設計、可靠性測試、上線檢查清單、上線就緒審查（PRR） |
| `sre-capacity-and-system-design` | 容量估算、負載平衡、過載處理、連鎖故障、簡潔設計、分散式共識 |
| `sre-data-reliability` | 資料管線、排程工作、備份與還原、資料完整性 |

### 附帶的範本與工具

| 路徑 | 內容 |
|---|---|
| `sre-slos-and-error-budgets/references/` | 依元件類型分類的 SLI 清單、SLO 文件範本、錯誤預算政策範本 |
| `sre-monitoring-and-alerting/references/prometheus-rules.md` | Prometheus 記錄規則與告警規則 |
| `sre-monitoring-and-alerting/scripts/burn_rate.py` | 燒錄率與告警門檻計算器（只用 Python 標準函式庫） |
| `sre-incident-response/references/` | 即時事件狀態文件範本 |
| `sre-postmortem/references/` | 事後檢討範本 |
| `sre-release-and-launch/references/` | 上線檢查清單、正式環境最佳實務稽核清單 |
| `sre-capacity-and-system-design/references/` | 粗略估算速查表 |

範例：
```bash
python3 sre-monitoring-and-alerting/scripts/burn_rate.py --slo 99.9 --period-days 30
```

### 參與貢獻

歡迎提出 issue 和 pull request。請用自己的文字撰寫，不要貼上原書的文字、表格或程式碼。

### 授權

- 文件（`SKILL.md`、範本、參考資料）：[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- 程式碼（`scripts/`）：[MIT](https://opensource.org/licenses/MIT)

以上授權只適用於本 repo 中的原創內容，不會重新授權 Google 原書的任何部分。
