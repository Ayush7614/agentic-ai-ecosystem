# Framework mappings reference

How **Anthropic Cybersecurity Skills** maps each skill to five industry frameworks — and how to use those mappings in investigations, compliance, and AI governance.

Upstream: [mukul975/Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills)

---

## Overview

| Framework | Version | Repo scope | Primary use |
|-----------|---------|------------|-------------|
| MITRE ATT&CK | v19.1 | 15 tactics · 286 techniques | TTP labeling, detection engineering |
| NIST CSF 2.0 | 2.0 | 6 functions · 22 categories | Security program alignment |
| MITRE ATLAS | v5.4 | 16 tactics · 84 techniques | ML/AI adversarial threats |
| MITRE D3FEND | v1.3 | 7 categories · 267 techniques | Defensive countermeasures |
| NIST AI RMF | 1.0 | 4 functions · 72 subcategories | AI agent risk management |

**754/754 skills** include ATT&CK mappings. ATLAS, D3FEND, AI RMF, and NIST CSF appear in YAML frontmatter where applicable.

---

## Where mappings live

| Location | Contents |
|----------|----------|
| `SKILL.md` frontmatter | `nist_csf`, `atlas_techniques`, `d3fend_techniques`, `nist_ai_rmf` |
| `references/standards.md` | ATT&CK technique IDs, extended framework notes |
| GitHub Releases | ATT&CK Navigator JSON layers |

---

## Example crosswalk

**Skill:** `analyzing-network-traffic-of-malware`

| Framework | ID / category | Meaning |
|-----------|---------------|---------|
| MITRE ATT&CK | T1071 | Application Layer Protocol (C2) |
| NIST CSF 2.0 | DE.CM | Continuous monitoring — detection |
| MITRE ATLAS | AML.T0047 | ML attack technique (where ML pipeline involved) |
| MITRE D3FEND | D3-NTA | Network traffic analysis countermeasure |
| NIST AI RMF | MEASURE-2.6 | AI system measurement & monitoring |

Use this row in IR reports: one finding → five audit-friendly references.

---

## MITRE ATT&CK v19.1

Validated with `mitreattack-python`. **Zero revoked or deprecated IDs.**

### v19.1 structural change

**Defense Evasion** split into:

- **Stealth** (TA0005) — hide activity  
- **Defense Impairment** (TA0112) — disable or weaken defenses  

When upgrading from older ATT&CK versions, remap detections that referenced generic Defense Evasion.

### Tactic skill counts

| Tactic | ID | Skills |
|--------|-----|--------|
| Reconnaissance | TA0043 | 103 |
| Resource Development | TA0042 | 22 |
| Initial Access | TA0001 | 467 |
| Execution | TA0002 | 350 |
| Persistence | TA0003 | 444 |
| Privilege Escalation | TA0004 | 464 |
| Stealth | TA0005 | 442 |
| Defense Impairment | TA0112 | 92 |
| Credential Access | TA0006 | 202 |
| Discovery | TA0007 | 237 |
| Lateral Movement | TA0008 | 68 |
| Collection | TA0009 | 172 |
| Command and Control | TA0011 | 123 |
| Exfiltration | TA0010 | 82 |
| Impact | TA0040 | 50 |

### Using Navigator layers

1. Download layer from [Releases](https://github.com/mukul975/Anthropic-Cybersecurity-Skills/releases)  
2. Import at [mitre-attack.github.io/attack-navigator](https://mitre-attack.github.io/attack-navigator/)  
3. Filter by skill coverage heatmap for gap analysis  

---

## NIST CSF 2.0

Six functions: **Govern, Identify, Protect, Detect, Respond, Recover**.

| Function | Example skill activities |
|----------|-------------------------|
| Govern (GV) | Compliance skills, policy review |
| Identify (ID) | Asset discovery, risk assessment |
| Protect (PR) | Hardening, IAM, zero trust |
| Detect (DE) | SIEM, threat hunting, NTA |
| Respond (RS) | Incident response, containment |
| Recover (RC) | Ransomware recovery, backup validation |

Frontmatter uses categories like `DE.CM-01`, `RS.AN-03`.

---

## MITRE ATLAS

For incidents touching **training data, model serving, or ML pipelines**:

- Poisoning, evasion, extraction, inversion  
- Supply chain of models and datasets  

Frontmatter: `atlas_techniques: [AML.Txxxx]`

Pair ATLAS with ATT&CK when attackers combine traditional IT intrusion with model abuse.

---

## MITRE D3FEND

Maps skills to **defensive techniques** — what blue team controls apply:

| D3FEND category | Examples |
|-----------------|----------|
| Detect | D3-NTA, D3-MA (memory analysis) |
| Harden | Configuration hardening countermeasures |
| Isolate | Network isolation patterns |
| Deceive | Overlap with deception technology skills |
| Evict | Remediation and eradication |

Use D3FEND IDs in remediation tickets: finding (ATT&CK) → fix (D3FEND).

---

## NIST AI RMF

Four functions: **Govern, Map, Measure, Manage**.

Relevant when **AI agents** execute these skills:

| Concern | RMF angle |
|---------|-----------|
| Agent runs offensive skill without scope | GOVERN — policies, human approval |
| Skill library in production SOC | MAP — context of use, stakeholders |
| Logging which skills fired | MEASURE — monitoring, metrics |
| Kill switch / rollback | MANAGE — response to agent errors |

Frontmatter: `nist_ai_rmf: [MEASURE-2.6, ...]`

---

## Reporting template

```markdown
## Finding summary
<one paragraph>

## Framework mapping
| Framework | Reference |
|-----------|-----------|
| ATT&CK | Txxxx — <technique name> |
| NIST CSF | DE.CM-01 |
| D3FEND | D3-NTA |
| ATLAS | (if applicable) |
| AI RMF | (if agent-executed) |

## Skill used
`<skill-name>` v<x.y> — Verification: <pass/fail criteria>
```

---

## Further reading

- [MITRE ATT&CK](https://attack.mitre.org/)  
- [NIST CSF 2.0](https://www.nist.gov/cyberframework)  
- [MITRE ATLAS](https://atlas.mitre.org/)  
- [MITRE D3FEND](https://d3fend.mitre.org/)  
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)  
- [agentskills.io](https://agentskills.io)  

Back to [Tutorial](https://ayush7614.github.io/agentic-ai-ecosystem/guides/anthropic-cybersecurity-skills/tutorial/) · [Domains](https://ayush7614.github.io/agentic-ai-ecosystem/guides/anthropic-cybersecurity-skills/domains/)
