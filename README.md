# SRE Practice Skills

[![Install via skills.sh](https://img.shields.io/badge/skills.sh-install-green)](https://skills.sh/paulip114/sre-practice-skills)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/paulip114/sre-practice-skills)](https://github.com/paulip114/sre-practice-skills/issues)
[![GitHub stars](https://img.shields.io/github/stars/paulip114/sre-practice-skills?style=social)](https://github.com/paulip114/sre-practice-skills/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/paulip114/sre-practice-skills?style=social)](https://github.com/paulip114/sre-practice-skills/network/members)


**Give your AI agent an SRE playbook.** Eight agent skills that teach Claude Code (and other Agent Skills–compatible agents) to set SLOs, write burn-rate alerts, run incidents, review postmortems, and more — the way Google's SRE books describe.

```bash
npx skills add paulip114/sre-practice-skills
```

[English](#english) | [中文](#中文)

---

## English

### Why

Google's two free SRE books are some of the most practical writing on running production systems, but an agent doesn't know when or how to apply them. These skills turn the books' practices into step-by-step procedures, checklists and templates that the agent loads automatically when your request matches:

- *Site Reliability Engineering* (2016) — https://sre.google/sre-book/table-of-contents/
- *The Site Reliability Workbook* (2018) — https://sre.google/workbook/table-of-contents/

> **Unofficial project.** This is not affiliated with or endorsed by Google. The skills are
> original procedures and checklists written in our own words; they do not reproduce the
> books' text. Each skill links to the chapters it draws on, so read those for depth.
> The books are © Google, published by O'Reilly Media, and licensed under
> [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/).

### Install

With the [skills CLI](https://skills.sh) (recommended):
```bash
# All 8 skills
npx skills add paulip114/sre-practice-skills

# One skill, for Claude Code only
npx skills add paulip114/sre-practice-skills --skill sre-postmortem -a claude-code

# Install globally (all projects)
npx skills add paulip114/sre-practice-skills -g
```

Or copy the folders manually:
```bash
git clone https://github.com/paulip114/sre-practice-skills
mkdir -p ~/.claude/skills && cp -r sre-practice-skills/sre-* ~/.claude/skills/
```

The skills use the standard `SKILL.md` format, so they also work in other agents that support Agent Skills.

### Usage

Claude loads a skill automatically when your request matches its description. You can also name one directly:

```text
Use sre-slos-and-error-budgets to propose SLOs for our checkout API.
Use sre-postmortem to review this incident write-up.
Use sre-monitoring-and-alerting to turn a 99.9% SLO into Prometheus alerts.
```

### Example

**Prompt**

```text
Use sre-slos-and-error-budgets to propose starter SLOs for our checkout API.
Last 4 weeks: 3.2M requests, 99.62% non-5xx, p90 latency 380 ms, p99 1.1 s.
```

**What the skill guides the agent to produce** (abridged, illustrative)

| SLI | Measured at | Starter SLO | Allowed bad events / 4 weeks |
|---|---|---|---|
| Availability (non-5xx / all) | Load balancer | 99.6% | ~12,800 |
| Latency | Load balancer | 90% of requests < 400 ms | ~320,000 |
| Latency (tail) | Load balancer | 99% of requests < 1.2 s | ~32,000 |

Plus: the rationale (targets derived from observed performance, rounded to manageable values), known blind spots (load-balancer metrics miss requests that never reach it), a 4-week rolling window, a filled-in SLO document, sign-off steps for product, dev and ops, and a pointer to an error budget policy and burn-rate alerts.

**Burn-rate calculator** (real output)

```console
$ python3 sre-monitoring-and-alerting/scripts/burn_rate.py --slo 99.9 --period-days 30
SLO 99.9% over 30 days -> error budget 0.1%
A 100% outage exhausts the budget in 43.2m

severity  budget    long   short    burn   threshold
page          2%    1.0h    5.0m    14.4       1.44%
page          5%    6.0h   30.0m       6        0.6%
ticket       10%    3.0d    6.0h       1        0.1%
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

### Contributing

Issues and pull requests are welcome — new examples, fixes, and translations especially. Please keep contributions in your own words: do not paste text, tables or code from the books.

If these skills help you, a ⭐ helps others find them.

### License

[Apache License 2.0](LICENSE). This applies only to the original content in this repository and does not relicense any part of Google's books.

---

## 中文

### 為什麼做這個

Google 免費公開的兩本 SRE 書籍，是談正式環境維運最實用的資料之一，但 AI agent 並不知道何時、如何運用這些做法。這些 skills 把書中的實務做法整理成步驟、檢查清單與範本，當你的需求符合時，agent 會自動載入：

- 《Site Reliability Engineering》（2016）— https://sre.google/sre-book/table-of-contents/
- 《The Site Reliability Workbook》（2018）— https://sre.google/workbook/table-of-contents/

> **非官方專案。** 本專案與 Google 無關，也未經 Google 認可。這些 skills 是以我們自己的文字
> 重新撰寫的操作步驟與檢查清單，並未摘錄原書文字。每個 skill 都附有對應章節的連結，
> 想深入了解請閱讀原書。原書 © Google，由 O'Reilly Media 出版，以
> [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) 授權。

### 安裝

使用 [skills CLI](https://skills.sh)（推薦）：
```bash
# 安裝全部 8 個 skills
npx skills add paulip114/sre-practice-skills

# 只安裝一個 skill 到 Claude Code
npx skills add paulip114/sre-practice-skills --skill sre-postmortem -a claude-code

# 全域安裝（所有專案）
npx skills add paulip114/sre-practice-skills -g
```

或手動複製資料夾：
```bash
git clone https://github.com/paulip114/sre-practice-skills
mkdir -p ~/.claude/skills && cp -r sre-practice-skills/sre-* ~/.claude/skills/
```

這些 skills 採用標準的 `SKILL.md` 格式，其他支援 Agent Skills 的 agent 也能使用。

### 使用方式

當你的需求符合某個 skill 的描述時，Claude 會自動載入它。你也可以直接指定：

```text
用 sre-slos-and-error-budgets 幫我們的結帳 API 訂 SLO。
用 sre-postmortem 檢查這份事件報告。
用 sre-monitoring-and-alerting 把 99.9% 的 SLO 轉成 Prometheus 告警。
```

### 範例

**提示詞**

```text
用 sre-slos-and-error-budgets 幫我們的結帳 API 提出初始 SLO。
過去 4 週：320 萬個請求，99.62% 非 5xx，p90 延遲 380 ms，p99 1.1 秒。
```

**skill 引導 agent 產出的內容**（節錄，僅供示意）

| SLI | 量測位置 | 初始 SLO | 每 4 週可容許的錯誤數 |
|---|---|---|---|
| 可用性（非 5xx / 全部） | 負載平衡器 | 99.6% | 約 12,800 |
| 延遲 | 負載平衡器 | 90% 的請求 < 400 ms | 約 320,000 |
| 延遲（長尾） | 負載平衡器 | 99% 的請求 < 1.2 秒 | 約 32,000 |

另外還包括：目標的依據（由實際表現推算，取整數方便管理）、量測盲點（負載平衡器的指標看不到沒有抵達它的請求）、4 週滾動視窗、填好的 SLO 文件、產品／開發／維運三方的確認步驟，以及錯誤預算政策和燒錄率告警的下一步建議。

**燒錄率計算器**（實際輸出）

```console
$ python3 sre-monitoring-and-alerting/scripts/burn_rate.py --slo 99.9 --period-days 30
SLO 99.9% over 30 days -> error budget 0.1%
A 100% outage exhausts the budget in 43.2m

severity  budget    long   short    burn   threshold
page          2%    1.0h    5.0m    14.4       1.44%
page          5%    6.0h   30.0m       6        0.6%
ticket       10%    3.0d    6.0h       1        0.1%
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

### 參與貢獻

歡迎提出 issue 和 pull request，特別是新的範例、修正和翻譯。請用自己的文字撰寫，不要貼上原書的文字、表格或程式碼。

如果這些 skills 對你有幫助，給個 ⭐ 能讓更多人找到它。

### 授權

[Apache License 2.0](LICENSE)。此授權只適用於本 repo 中的原創內容，不會重新授權 Google 原書的任何部分。
