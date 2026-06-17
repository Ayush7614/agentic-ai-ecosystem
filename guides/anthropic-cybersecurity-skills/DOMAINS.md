# Security domains catalog

All **26 domains** in [Anthropic Cybersecurity Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) with skill counts and typical agent use cases.

---

## Domain index

| # | Domain | Skills | When to load |
|---|--------|--------|--------------|
| 1 | Cloud Security | 60 | AWS/Azure/GCP incidents, CSPM, cloud forensics |
| 2 | Threat Hunting | 55 | Proactive hypothesis-driven hunts, LOTL |
| 3 | Threat Intelligence | 50 | STIX/TAXII, MISP, actor profiling |
| 4 | Web Application Security | 42 | OWASP testing, SQLi/XSS/SSRF |
| 5 | Network Security | 40 | IDS/IPS, segmentation, PCAP analysis |
| 6 | Malware Analysis | 39 | Static/dynamic analysis, sandboxing |
| 7 | Digital Forensics | 37 | Disk/memory imaging, timelines |
| 8 | Security Operations | 36 | SIEM rules, log parsing, alert logic |
| 9 | Identity & Access Management | 35 | IAM, PAM, Okta, SailPoint, zero trust ID |
| 10 | SOC Operations | 33 | Playbooks, escalation, metrics, tabletops |
| 11 | Container Security | 30 | K8s RBAC, Falco, image scan, container DFIR |
| 12 | OT/ICS Security | 28 | Modbus, DNP3, IEC 62443, SCADA |
| 13 | API Security | 28 | REST/GraphQL, OWASP API Top 10 |
| 14 | Vulnerability Management | 25 | Scanning, CVSS prioritization, patching |
| 15 | Incident Response | 25 | Containment, ransomware, breach comms |
| 16 | Red Teaming | 24 | Full-scope adversary simulation |
| 17 | Penetration Testing | 23 | Network, web, cloud, mobile, wireless |
| 18 | Endpoint Security | 17 | EDR tuning, fileless malware, persistence |
| 19 | DevSecOps | 17 | CI/CD security, Terraform/IaC audit |
| 20 | Phishing Defense | 16 | DMARC, BEC, phishing IR |
| 21 | Cryptography | 14 | TLS audit, CT logs, key lifecycle |
| 22 | Zero Trust Architecture | 13 | BeyondCorp, microsegmentation, CISA ZT |
| 23 | Mobile Security | 12 | Android/iOS RE, mobile pentest, MDM |
| 24 | Ransomware Defense | 7 | Precursors, response, recovery |
| 25 | Compliance & Governance | 5 | CIS, SOC 2, regulatory mapping |
| 26 | Deception Technology | 2 | Honeytokens, canaries |

**Total:** 754 skills (counts from upstream README; may grow on `main`).

---

## Domain deep notes

### Cloud Security (60)

Multi-provider coverage: identity federation misconfigs, public storage, Lambda/Function abuse, K8s in cloud control planes. Combine with **Incident Response** for breach scoping.

**Example prompts:**

- "Audit S3 bucket policies using cloud security skills"  
- "Correlate CloudTrail and Entra sign-ins for stolen keys"  

### Threat Hunting (55)

Hypothesis → data → validation. Emphasis on living-off-the-land (LOTL) and behavioral analytics rather than IOC-only sweeps.

**Pair with:** Security Operations (data sources), Threat Intelligence (context).

### Threat Intelligence (50)

Operational TI: feed integration, STIX/TAXII, MISP workflows, actor TTP profiling — not just reading reports.

### Web Application Security (42)

OWASP Top 10 aligned testing workflows. Agent gets ordered test steps and verification — not just payload lists.

### Network Security (40)

Firewall rule review, VLAN design, IDS tuning, full PCAP analysis pipelines.

### Malware Analysis (39)

Static (strings, PE/ELF), dynamic (sandbox), RE entry points. Escalate to **Digital Forensics** for host-wide context.

### Digital Forensics (37)

Disk imaging, memory (Volatility3), timeline tools (Plaso, etc.), chain of custody checks in Prerequisites.

### Security Operations (36)

Day-to-day SOC: parser creation, correlation rules, alert triage decision trees.

### Identity & Access Management (35)

Policy review, privileged access, SSO/Okta hardening, entitlement audits.

### SOC Operations (33)

People and process: runbooks, shift handoff, KPIs, tabletop exercises — complements Security Operations tooling skills.

### Container Security (30)

Image vulnerability scan interpretation, K8s RBAC audit, runtime (Falco), container escape forensics.

### OT/ICS Security (28)

Safety-aware testing: Modbus/DNP3, historian protection, IEC 62443 zones. **Always** confirm authorized OT test windows.

### API Security (28)

GraphQL introspection abuse, REST authZ flaws, rate limit and mass assignment patterns.

### Vulnerability Management (25)

Scan → prioritize → patch → verify loops with CVSS contextualization.

### Incident Response (25)

Containment before eradication, evidence preservation, ransomware-specific branches.

### Red Teaming & Penetration Testing (24 + 23)

**Authorized engagements only.** AD attacks, phishing simulation, external/internal pentest methodologies. State scope in every prompt.

### Endpoint Security (17)

EDR query languages, fileless detection, persistence mechanism hunts.

### DevSecOps (17)

Pipeline secret scanning, SAST/DAST integration, signed commits, IaC policy checks.

### Phishing Defense (16)

Email authentication (SPF/DKIM/DMARC), BEC patterns, user reporting workflows.

### Cryptography (14)

Certificate validation, weak cipher detection, key rotation procedures.

### Zero Trust Architecture (13)

Maturity assessment, microsegmentation design, identity-centric access.

### Mobile Security (12)

APK/IPA analysis, mobile API testing, MDM compliance forensics.

### Ransomware Defense (7)

Precursor detection (VSS deletion, shadow copy abuse), recovery validation.

### Compliance & Governance (5) — needs contributors

CIS benchmark workflows, SOC 2 control mapping. High-value contribution area.

### Deception Technology (2) — needs contributors

Honeytokens, canary credentials, deception deployment.

---

## Subset installs by team

| Team | Suggested domains |
|------|-------------------|
| SOC L1/L2 | SOC Operations, Security Operations, Incident Response |
| Threat hunt team | Threat Hunting, Threat Intelligence, Endpoint Security |
| Cloud security | Cloud Security, Container Security, IAM |
| AppSec | Web Application Security, API Security, DevSecOps |
| DFIR | Digital Forensics, Malware Analysis, Incident Response |
| Red team | Red Teaming, Penetration Testing (scoped) |
| OT | OT/ICS Security only + IR liaison |
| GRC | Compliance & Governance, Zero Trust, FRAMEWORKS.md |

Clone full repo or symlink only matching `skills/*` directories.

---

## Discovering skills by domain

After clone:

```bash
SKILLS=~/.cybersec-skills/Anthropic-Cybersecurity-Skills/skills
grep -l "subdomain: digital-forensics" "$SKILLS"/*/SKILL.md 2>/dev/null | head
grep -l "tags:.*threat-hunting" "$SKILLS"/*/SKILL.md 2>/dev/null | head
```

Agents should prefer frontmatter `subdomain` and `tags` over filename guessing.

---

Back to [Tutorial](https://ayush7614.github.io/agentic-ai-ecosystem/guides/anthropic-cybersecurity-skills/tutorial/) · [Frameworks](https://ayush7614.github.io/agentic-ai-ecosystem/guides/anthropic-cybersecurity-skills/frameworks/)
