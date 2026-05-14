# Security & Privacy Policy for froglet

## Data Residency
- All data stays on your local machine (**if** you only use **local** LLMs)
- No cloud sync (unless you enable it)
- No telemetry

## Threat Model
This tool assumes:
- ✅ You trust your computer/OS
- ✅ You're running legitimate software
- ❌ NOT protected against malware on your machine
- ❌ NOT protected against physical theft without encryption

## Best Practices
1. Use disk encryption (BitLocker, FileVault, LUKS)
2. Keep your LLM client updated
3. Use local LLMs for sensitive data
4. Review Cline permissions regularly
5. Backup wiki regularly (encrypted)

## Data Sensitivity Policy

### ✅ Safe for froglet (Local Storage)
- Public company information
- Published research
- General knowledge base content
- Non-sensitive meeting notes

### ⚠️ Requires Additional Controls
- **Public**: Data with no confidentiality requirement
  - Control: Standard local file permissions

- **Confidential**: Internal company data
  - Control: Disk encryption (BitLocker, FileVault) + access controls

- **Restricted/HIPAA**: Patient records, health data, SSNs
  - Control: Full disk encryption + separate encrypted partition + audit logging
  - Recommendation: DO NOT store in this tool; use compliant systems instead

- **PCI-DSS**: Credit card data
  - Recommendation: NEVER store locally; use compliant payment processors
