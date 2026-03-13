# GOAD - Game of Active Directory

<p align="center">
  <img src="https://img.shields.io/badge/Status-All%2012%20Parts%20Complete-00bfff?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Difficulty-Intermediate-yellow?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Type-Hands--On-blue?style=for-the-badge" />
</p>

---

A comprehensive guide to attacking and defending Active Directory environments. Based on the [GOAD](https://github.com/Orange-Cyberdefense/GOAD) lab by Orange Cyberdefense.

---

## Overview

| Phase | Topic | Description |
|:----:|-------|-------------|
| 1 | [Reconnaissance](./game-of-active-directory/part-1-reconnaissance/README.md) | Network scanning, enum4linux, Kerberos setup |
| 2 | [Finding Users](./game-of-active-directory/part-2-finding-users/README.md) | Kerbrute, AS-REP Roasting, Kerberoasting |
| 3 | [Authenticated Enumeration](./game-of-active-directory/part-3-authenticated-enumeration/README.md) | LDAP, BloodHound, GPP, Shares |
| 4 | [NTLM Relaying](./game-of-active-directory/part-4-ntlm-relaying/README.md) | Responder, LLMNR, SMB Relay, Coercion |
| 5 | [ADCS](./game-of-active-directory/part-5-adcs/README.md) | ESC1-ESC16, Certificate attacks |
| 6 | [MSSQL](./game-of-active-directory/part-6-mssql/README.md) | Database enumeration and exploitation |
| 7 | [Privilege Escalation](./game-of-active-directory/part-7-privilege-escalation/README.md) | RBCD, SeImpersonate, AMSI bypass |
| 8 | [Lateral Movement](./game-of-active-directory/part-8-lateral-move/README.md) | Pivoting, secretsdump, WMI, PSRemoting |
| 9 | [Delegations](./game-of-active-directory/part-9-delegations/README.md) | Unconstrained, Constrained, RBCD |
| 10 | [ACL Abuse](./game-of-active-directory/part-10-acl/README.md) | GenericWrite, AddMember, DCSync |
| 11 | [Trusts](./game-of-active-directory/part-11-trusts/README.md) | Cross-domain, Forest, SID Filtering |
| 12 | [Having Fun](./game-of-active-directory/part-12-having-fun/README.md) | Persistence, Golden Ticket, DSRM |

---

## Quick Navigation

### Attack Phases
- **Initial Access**: Parts 1-3
- **Credential Theft**: Parts 4-6
- **Privilege Escalation**: Parts 7-10
- **Domain Domination**: Parts 11-12

### Tools Covered
- NetExec, Impacket, BloodHound, Responder
- Certipy, mitm6, ntlmrelayx, Kerbrute
- PowerView, lsassy, DonPAPI, SecretsDump

---

## Lab Environment

- **Domain**: `sevenkingdoms.local` / `essos.local`
- **OS**: Windows Server 2019/2022
- **Attacker**: Kali Linux

---

<p align="center">
  <sub>Part of Mr Stark Study Notes</sub>
</p>
