---
title: Enumeration
layout: docs
---

In this session we will be looking on how to do enumeration in an AD environment. This Domain enumeration phase will be conducted 100% via Powershell.

For Domain enumeration, we do have so far, 4 ways to accomplish this task.

# The Active Directory PowerShell module.

Based on [Microsoft](https://learn.microsoft.com/en-us/powershell/module/activedirectory/?view=windowsserver2022-ps), the Active Directory module for Windows PowerShell is a PowerShell module that consolidates a group of cmdlets. You can use these cmdlets to manage your Active Directory domains, Active Directory Lightweight Directory Services (AD LDS) configuration sets, and Active Directory Database Mounting Tool instances in a single, self-contained package.

# BloodHound

BloodHound uses graph theory to reveal the hidden and often unintended relationships within an Active Directory or Azure environment. Attackers can use BloodHound to easily identify highly complex attack paths that would otherwise be impossible to quickly identify. Defenders can use BloodHound to identify and eliminate those same attack paths. Both blue and red teams can use BloodHound to easily gain a deeper understanding of privilege relationships in an Active Directory or Azure environment.

# PowerView(PowerShell)

PowerView is a PowerShell tool to gain network situational awareness on Windows domains. It contains a set of pure-PowerShell replacements for various windows "net *" commands, which utilize PowerShell AD hooks and underlying Win32 API functions to perform useful Windows domain functionality.

[https://github.com/PowerShellMafia/PowerSploit/blob/dev/Recon/PowerView.ps1](https://github.com/PowerShellMafia/PowerSploit/blob/dev/Recon/PowerView.ps1)

# SharpView

SharpView is a .NET port of one of our favorite tools `PowerView`. `SharpView` offers the ability to use any of the PowerView functions and arguments in a .NET assembly. 
If you’re familiar with PowerView, SharpView will be easy to pick up. 
I like to say that SharpView is PowerView with Steroids 😄.

[https://github.com/tevora-threat/SharpView](https://github.com/tevora-threat/SharpView)

*Enough is Enough…* After all this reading, let’s now see how everything works by practicing enumeration in Active Directory. We will focused this enumeration using PowerView Module.

Well, Assuming that we already have access to a valid user in an Active Domain environment, we won’t be doing Recon’s like enumerating the network or trying to compromise a user.
Notice once again that from this phase we already have a valid user and we will carry on from here.

# PowerShell Detection Bypass

Previously we discussed a little bit about 4 PowerShell Detection mechanisms, now we will discuss few ways to bypass these mechanisms and try to be stealthy while doing our domain enumeration phase.

### Invisi-Shell

Using [Invisi-Shell](https://github.com/OmerYa/Invisi-Shell) is a .bat script that will hide your powershell script in plain sight! Invisi-Shell bypasses all of Powershell security features (ScriptBlock logging, Module logging, Transcription, AMSI) by hooking .Net assemblies. 
The hook is performed via CLR Profiler API.

It’s always good that we do run Invisi-Shell via cmd before we start doing our enumeration and right after script execution, Powershell will be executed. This script should be executed depending on the type of privilege we do have on the machine.

If we are just a simple low level privileged user, then we should run*RunWithRegistetyNonAdmin.ba***t**.

If we are a high level privileged user like Administrator for example, then we should run *RunWithPathAsAdmin.bat***.**

*RunWithRegistetyNonAdmin.ba*`t`

As you can see the output after Invisi-Shell execution, we don’t need to worry about Powershell Detections anymore and PowerShell is called right after.

Now we can import the PowerView modules. For this importing mechanism we do have 2 ways to import modules.

First option is using a dot sourcing mechanism.

`. .\PowerView.ps1`

Second option is using Import-Module.

`Import-Module PowerView.ps1`

# PowerView

PowerView is a PowerShell script used in security testing to discover and exploit vulnerabilities in Windows Active Directory environments. It helps with tasks like finding Active Directory objects (users, groups, computers), analyzing Group Policy Objects, identifying privileged accounts, exploring trust relationships, detecting ACL misconfigurations, and mapping out the Active Directory topology. This tool is popular among penetration testers and red team operators for simulating attacks and assessing security weaknesses. It should be used responsibly and with proper authorization in controlled environments.

Let’s start by importing PowerView.ps1 Modules then using it to enumerate users, computers, Domain Administrators and Enterprise Administrators as well.

`Import-Module .\PowerView.ps1`

We can use the module Get-DomainUser to Enumerate Domain Users when using PowerView.
`Get-DomainUser`

The Command Above will get all the domain users. Note this can really be painful when we are dealing with an AD, because we may have millions of users accounts.
It’s always good if we use filters to bring us only the real relevant information in the output. we can use the `select-object` (or its alias `select`) cmdlet.
Let’s imagine we want to bring only the property `samaccountname`, which will brings us only account usernames.

`Get-DomainUSer | select -ExpandProperty samaccountname `

After filtering to bring us only `samaccountname`, we can see that we have all the AD usernames on our output.

### Domain Computers

Now, to enumerate member computers in the domain we can use Get-DomainComputer module.

`Get-DomainComputer`

Above command helps us to request all the computers we have in the domain.
We can filter this as well by using the same we did when enumerating users.

`Get-DomainComputer | select -ExpandProperty dnshostname`

The screenshot above shows us all the computers that we do have in the account so far by bringing us all the computer names.

### Domain Groups

Our next move will be checking all the domain groups and find out all the domain groups we have in this domain. We can use the following command.
`Get-DomainGroup`

Once we issue the command, we get all the groups available in this domain including all its properties.

We can as well once again filter it and bring group names only.

`Get-DomainGroup | select -ExpandProperty name`

Then We can get information of one specific group instead of bringing all the groups information by specifying the group identity.

`Get-DomainGroup -Identity "Domain admins"`

### Domain Admin Members

Another good thing to check when enumerating users inside a domain, is to check what users are member of `Domain Admins` group.

`Get-DomainGroupMember -Identity "Domain Admins"`

The command issued above will bring us all the domain accounts belonging to the `Domain Admins` group plus other properties.
The other thing we can do as well is to filter by MemberName property, this way we will get only all the domain accounts belonging to `Domain Admins` groups.

`Get-DomainGroupMember -Identity "Domain Admins" | select -ExpandProperty MemberName`

We can see above that we do have only users **svcadmin** and **Adminisrator** as part of `Domain Admins` group.

### Enterprise Admins

Another option is to enumerate Enterprise admins group members.

`Get-DomainGroupMember -Identity "Enterprise Admins"`

If this is not a root domain, the above command will return nothing. We need to query the root domain as `Enterprise Admins` group is present only in the root of a forest.

`Get-DomainGroupMember -Identity "Enterprise Admins" -Domain moneycorp.local`

We can see above that, only **Administrator** is part of `Enterprise Admins` group.

# Active Directory module (ADModule)

ADModule is a Microsoft signed DLL for the ActiveDirectory PowerShell module. Just a backup for the Microsoft's ActiveDirectory PowerShell module from Server 2016 with RSAT and module installed. 
Also there are many benefits like very low chances of detection by AV, very wide coverage by cmdlets, good filters for cmdlets, signed by Microsoft etc. 
The most useful one, however, is that this module works flawlessly from PowerShell's Constrained Language Mode.

To be able to list all the cmdlets in the module, import the module as well. Remember to import the DLL first. [https://github.com/samratashok/ADModule](https://github.com/samratashok/ADModule)

`Import-Module C:\ADModule\Microsoft.ActiveDirectory.Management.dll`

`Import-Module C\ADModule\ActiveDirectory\ActiveDirectory.psd1`

After importing ADModule, we can start by enumerating users.

### Enumerate Users

`Get-ADUser -Filter *`

We can list specific properties. Let's list `samaccountname` and description for the users. 
Note that we are listing all the properties first using the **-Properties** parameter.

`Get-ADUser -Filter * -properties * | select SamAccountName,Description`

### Enumerate computers

The Following command will show us all the computers we do have on the Domain, including its properties.
`Get-ADComputer -Filter *`

By using some filters we can bring only the properties we want to, for example on the command below, we will only bring all properties but using select to specify only want we want, in our case, the properties **DNSHostName** and its **Description**.

`Get-ADComputer -Filter * -properties *  | select DNSHostName,Discription `

### Domain Groups

ADModule can also identify all the Domain groups and its properties using the following command.

`Get-ADGroup -Filter *`

We can also filter this by bringing us only the domain group names instead of all its properties.

For the following query, we will be filtering the query to bring us only the property **Name** and its **Description**.

`Get-ADGroup -Filter * -properties * | select Name,Description`

### Domain Group Members

Let’s say that we already know all the groups we have in the domain, but now we want to know what users are part of a specific group, like Domain Admins group for example.

Below we can see all user’s that are member of a specific groups, in this case `Domain Admins` Group Members.

`Get-ADGroupMember -Indentity "Domain Admins"`

We can also filter it by bringing us only the `SamAccountName` property for all the **Domain Admins** group.

`Get-ADGroupMember -Identity "Domain Admins" | select SamAccountName,Description `

### Enterprise Domains Group Members

The following command will only work if we are in a root domain in this case in parent domain, otherwise it won’t work at all, then Its better if we specify the domain itself to see what users are part of `Enterprise Domains` group.

`Get-ADGroupMember -Identify "Enterprise Domains" -Server moneycorp.local`

Enumerating Organization Units (OUs) and Group Policy Objects (GPOs) during a penetration test provides several key benefits for assessing and exploiting Active Directory environments effectively:

### Benefits of Enumerating OUs:

1. Understanding Organizational Structure:
  - OUs reveal how Active Directory objects (users, computers, groups) are organized within the domain, aiding in understanding the network's layout and hierarchy.

- OUs reveal how Active Directory objects (users, computers, groups) are organized within the domain, aiding in understanding the network's layout and hierarchy.

2. Targeted Reconnaissance:
  - Identifying OUs helps focus reconnaissance efforts on specific areas of interest, such as privileged user groups, sensitive departments, or critical systems.

- Identifying OUs helps focus reconnaissance efforts on specific areas of interest, such as privileged user groups, sensitive departments, or critical systems.

3. User and Group Enumeration:
  - OUs often contain users and groups with specific permissions and roles. Enumerating OUs facilitates gathering information about these entities for potential privilege escalation or lateral movement.

- OUs often contain users and groups with specific permissions and roles. Enumerating OUs facilitates gathering information about these entities for potential privilege escalation or lateral movement.

4. Mapping Attack Surfaces:
  - Knowing the distribution of objects across OUs assists in mapping potential attack paths and identifying high-value targets for exploitation.

- Knowing the distribution of objects across OUs assists in mapping potential attack paths and identifying high-value targets for exploitation.

### Benefits of Enumerating GPOs:

1. Policy Assessment:
  - GPO enumeration provides insight into the configuration settings applied across the domain, including security policies, restrictions, and administrative controls.

- GPO enumeration provides insight into the configuration settings applied across the domain, including security policies, restrictions, and administrative controls.

2. Identifying Security Weaknesses:
  - Analyzing GPOs helps identify misconfigurations, loopholes, or insecure settings that could be exploited to gain unauthorized access or escalate privileges.

- Analyzing GPOs helps identify misconfigurations, loopholes, or insecure settings that could be exploited to gain unauthorized access or escalate privileges.

3. Audit and Compliance:
  - Enumerating GPOs aids in assessing compliance with organizational standards, industry regulations, and best practices related to IT security and governance.

- Enumerating GPOs aids in assessing compliance with organizational standards, industry regulations, and best practices related to IT security and governance.

4. Exploitation Opportunities:
  - Certain GPO settings, such as startup scripts, software deployment configurations, or registry modifications, can be leveraged for executing malicious actions during an attack.

- Certain GPO settings, such as startup scripts, software deployment configurations, or registry modifications, can be leveraged for executing malicious actions during an attack.

### Overall Pentesting Benefits:

- Risk Assessment: Enumerating OUs and GPOs provides valuable insights into the security posture of Active Directory, allowing pentesters to assess risks and prioritize attack vectors.

- Lateral Movement and Privilege Escalation: Knowledge of OUs and GPOs assists in identifying potential paths for lateral movement across the network and discovering opportunities for escalating privileges.

- Detailed Reconnaissance: OUs and GPOs offer detailed reconnaissance data that helps pentesters understand the target environment, plan attack strategies, and simulate real-world attack scenarios.

In summary, enumerating OUs and GPOs during a penetration test enhances the effectiveness of reconnaissance, risk assessment, and exploitation activities within Active Directory environments, leading to more comprehensive security assessments and actionable findings for improving overall security posture.

For the practical demonstration, several types of OUs and GPOs enumerations will showed here and We will be using PowerView.
Let’s start by importing PowerView modules.
`Import-Module .\PowerView.ps1`

### OUs(Organization Units) Enumeration

Let’s start by querying all Organization Units in the target domain with the following Command

`Get-DomainOU`

Above we can see all Organization Units configured in this Domain, containing all the properties as well.
But we can also make the same request and filter to bring only the properties that import the most to us. 
For example we will use the property name to bring us only the `name` of all OUs in this domain, this way we see OU names only.

`Get-DomainOU | select -ExpandProperty name`

Above we can see that we do have 4 Organization Units configured for the target domain.

As it’s known, inside a Organization Unit we do have some computers assigned to it. Let’s use OU `StudentMachines` as an example and find out, what Computers are assigned to this OU.

`(Get-DomainOU -Identity StudentMachines).DistinguishedName | %{Get-DomainComputer -SearchBase $_} | select name `

We can see that we were able to find out all the computers that are assigned to the `StudentMachines` OU.

### GPOs(Group Policy Objects) Enumeration

We will focus now on GPO enumeration, also using PowerView modules.

`Get-DomainGPO`

Access privileges for resources in Active Directory Domain Services are usually granted through the use of an Access Control Entry (ACE). Access Control Entries describe the allowed and denied permissions for a principal (e.g. user, computer account) in Active Directory against a securable object (user, group, computer, container, organizational unit (OU), GPO and so on).

Enumerating Access Control Lists (ACLs) during an Active Directory penetration test offers several benefits and can be instrumental in identifying security weaknesses and potential attack paths. Here are the benefits along with a use case illustrating the importance of ACL enumeration:

### Benefits of ACL Enumeration:

1. Identifying Security Misconfigurations:
  - ACL enumeration helps identify misconfigured permissions on critical Active Directory objects (e.g., OUs, user accounts, group memberships), which can lead to unauthorized access or privilege escalation.

- ACL enumeration helps identify misconfigured permissions on critical Active Directory objects (e.g., OUs, user accounts, group memberships), which can lead to unauthorized access or privilege escalation.

2. Understanding Access Controls:
  - By examining ACLs, pentesters gain insights into who has permissions to perform specific actions (e.g., read, write, modify) on directory objects, aiding in understanding the overall access control model.

- By examining ACLs, pentesters gain insights into who has permissions to perform specific actions (e.g., read, write, modify) on directory objects, aiding in understanding the overall access control model.

3. Mapping Attack Surfaces:
  - ACL enumeration allows for mapping out potential attack paths by identifying objects accessible to certain user accounts or groups, facilitating targeted exploitation strategies.

- ACL enumeration allows for mapping out potential attack paths by identifying objects accessible to certain user accounts or groups, facilitating targeted exploitation strategies.

4. Detection of Overly Permissive Settings:
  - Discovering overly permissive ACLs (e.g., Everyone group with unnecessary permissions) helps highlight security risks and areas requiring remediation.

- Discovering overly permissive ACLs (e.g., Everyone group with unnecessary permissions) helps highlight security risks and areas requiring remediation.

### Use Case: ACL Enumeration in Active Directory Pentesting

**Scenario**:
During a penetration test of an Active Directory environment, the pentester is tasked with assessing the security posture of a domain controller and identifying potential avenues for privilege escalation.

**Steps**:

1. Enumerate Directory Objects:
  - Use PowerShell scripts or built-in tools to enumerate key Active Directory objects (e.g., OUs, user accounts, groups).

- Use PowerShell scripts or built-in tools to enumerate key Active Directory objects (e.g., OUs, user accounts, groups).

2. Retrieve ACL Information:
  - For each directory object, retrieve and analyze the Access Control Lists (ACLs) to identify who has permissions and what actions (e.g., read, write, modify) are allowed.

- For each directory object, retrieve and analyze the Access Control Lists (ACLs) to identify who has permissions and what actions (e.g., read, write, modify) are allowed.

3. Identify Misconfigured Permissions:
  - Look for objects with overly permissive ACLs (e.g., Everyone or Authenticated Users with unnecessary write permissions) that could be exploited by an attacker.

- Look for objects with overly permissive ACLs (e.g., Everyone or Authenticated Users with unnecessary write permissions) that could be exploited by an attacker.

4. Assess Privilege Escalation Opportunities:
  - Focus on objects accessible to low-privileged accounts (e.g., standard users) and analyze if there are paths to escalate privileges by modifying permissions or exploiting misconfigurations.

- Focus on objects accessible to low-privileged accounts (e.g., standard users) and analyze if there are paths to escalate privileges by modifying permissions or exploiting misconfigurations.

5. Document Findings and Recommendations:
  - Document identified ACL vulnerabilities, along with recommendations for remediation (e.g., tightening permissions, removing unnecessary access), to assist the organization in improving its security posture.

- Document identified ACL vulnerabilities, along with recommendations for remediation (e.g., tightening permissions, removing unnecessary access), to assist the organization in improving its security posture.

**Benefits**:

- Risk Mitigation: ACL enumeration helps uncover security risks related to permissions and access controls, allowing organizations to proactively mitigate vulnerabilities.

- Targeted Exploitation: Detailed ACL analysis enables pentesters to target specific objects and permissions during exploitation, simulating real-world attack scenarios.

- Comprehensive Security Assessment: By focusing on ACL enumeration, pentesters gain a holistic view of the Active Directory security landscape, identifying areas for improvement and enhancing overall security awareness.

In summary, ACL enumeration is a critical aspect of Active Directory pentesting, offering valuable insights into security misconfigurations, access control issues, and opportunities for privilege escalation. Properly conducted ACL assessment contributes to a thorough security assessment and helps organizations enhance their defensive capabilities. 
If an object's (called **objectA**) DACL features an ACE stating that another object (called **objectB**) has a specific right (e.g. `GenericAll`) over it (i.e. over **objectA**), attackers need to be in control of **objectB** to take control of **objectA**.

There are 2 types of ACLs in Active Directory

**Discretionary Access Control List (DACL)**:
 This type of ACL defines the access rights assigned to an entity over an object. It specifies the access that is explicitly allowed by the Access Control Entries (ACEs) in the DACL. If an object has a DACL, the 
system allows access based on the permissions granted in the DACL. If the DACL has ACEs that allow access to specific users or groups, access is implicitly.

**System Access Control List (SACL)**:
This type of ACL generates audit reports that detail which entity attempted to gain access to an object, whether access was granted or denied, and the type of access provided. The SACL is crucial for auditing and monitoring access attempts within the Active Directory environment.

For this ACL enumeration, PowerView will be used. Once PowerView modules has been imported, Let’s start the enumeration.

To enumerate ACLs, we can use `Get-DomainObjectACL`.

Let’s enumerate the Access Control List for the `Domain Admins` group.

`Get-DomainObjectACL -Identity "Domain Admins" -ResolveGUIDs -Verbose `

Enumerating domains, forests, and trusts during a penetration test provides several key benefits for assessing and understanding the Active Directory (AD) environment thoroughly. Here are the benefits of each enumeration:

### Domain Enumeration:

1. Understanding Domain Structure:
  - Domain enumeration reveals the structure of the AD domain, including domain controllers, domain member systems, and domain-specific resources. This helps in mapping out the attack surface.

- Domain enumeration reveals the structure of the AD domain, including domain controllers, domain member systems, and domain-specific resources. This helps in mapping out the attack surface.

2. Identifying Domain Admins and Critical Groups:
  - Discovering domain administrator accounts and other privileged groups within the domain is crucial for identifying high-value targets during penetration testing.

- Discovering domain administrator accounts and other privileged groups within the domain is crucial for identifying high-value targets during penetration testing.

3. User and Group Enumeration:
  - Enumerating domain users and groups helps in identifying potential attack vectors, such as privileged user accounts or misconfigured group memberships.

- Enumerating domain users and groups helps in identifying potential attack vectors, such as privileged user accounts or misconfigured group memberships.

4. Mapping Trust Relationships:
  - Understanding which domains are trusted by the current domain (incoming trusts) and which domains the current domain trusts (outgoing trusts) aids in lateral movement and privilege escalation.

- Understanding which domains are trusted by the current domain (incoming trusts) and which domains the current domain trusts (outgoing trusts) aids in lateral movement and privilege escalation.

### Forest Enumeration:

1. Assessing Forest Topology:
  - Enumerating forests provides insights into the overall structure of multiple domains and trust relationships within the AD environment.

- Enumerating forests provides insights into the overall structure of multiple domains and trust relationships within the AD environment.

2. Identifying Trust Relationships Between Forests:
  - Discovering trust relationships between different forests helps in understanding inter-forest communication paths, which is critical for lateral movement and reconnaissance.

- Discovering trust relationships between different forests helps in understanding inter-forest communication paths, which is critical for lateral movement and reconnaissance.

3. Analyzing Global Catalog Servers:
  - Enumerating global catalog servers in a forest provides information about replicated directory data and facilitates targeted attacks against specific domains.

- Enumerating global catalog servers in a forest provides information about replicated directory data and facilitates targeted attacks against specific domains.

### Trusts Enumeration:

1. Mapping Trust Relationships:
  - Enumerating trusts reveals the relationships and communication paths established between domains and forests, aiding in identifying potential paths for privilege escalation or lateral movement.

- Enumerating trusts reveals the relationships and communication paths established between domains and forests, aiding in identifying potential paths for privilege escalation or lateral movement.

2. Identifying External Trusts:
  - Discovering external trusts (trusts with domains outside the organization's forest) helps in assessing potential security risks associated with external entities accessing internal resources.

- Discovering external trusts (trusts with domains outside the organization's forest) helps in assessing potential security risks associated with external entities accessing internal resources.

3. Assessing Trust Authentication Levels:
  - Understanding the authentication settings and levels (e.g., selective authentication, forest-wide authentication) associated with trusts assists in evaluating security boundaries and attack vectors.

- Understanding the authentication settings and levels (e.g., selective authentication, forest-wide authentication) associated with trusts assists in evaluating security boundaries and attack vectors.

Let’s start by enumerating all the domains in a forest and for that we will use PowerView modules. If PowerView module has been imported, then we can carry on with our enumeration.

### Domains Enumeration

The following command will enumerate all the domains we have in this current forest.

`Get-ForestDomain -Verbose`

As we can see above, all the domains in the current forest are listed to us. For a better and cleaning view, we can simply filter it and get the property name.

The following command brings us the name of all 3 Domains we do have in this forest. Keep in mind that the command below will only show us domains within forest, no external domains will be shown here.

`Get-ForestDomain | select -ExpandProperty Name`

The above command brings us the name of all 3 Domains we do have in this forest.

**moneycorp.local**
**dollarcorp.moneycorp.local**
**us.dollarcorp.moneycorp.local**

Now we can also enumerate and map all the Trusts domain **dollarcorp.moneycorp.local** contains.
`Get-DomainTrust`

We can see above that we are checking all the trusts that we do have in the current domain(`dollarcorp.moneycorp.local`). Above it’s possible to see that we do have 1 type of trust and 2 types of Attributions, which are:

### Trusts

`UPLEVEL (0x00000002)` - A trusted Windows domain that is running Active Directory.This is output as **WINDOWS_ACTIVE_DIRECTORY** in PowerView for those not as familiar with the terminology.

### Attributions

`WITHIN_FOREST (0x00000020)` — the trusted domain is within the same forest, meaning a parent->child or cross-link relationship

`QUARANTINED_DOMAIN (0x00000004)` — SID filtering is enabled (more on this later). Output as **FILTER_SIDS** with PowerView for simplicity.

There are several types of trusts, some of which have various offensive implications, covered in a bit:

- Parent/Child — Part of the same forest — a child domain retains an implicit two-way transitive trust with its parent. This is probably the most common type of trust that you’ll encounter.

- Cross-link (shortcut)— aka a “shortcut trust” between child domains to improve referral times. Normally referrals in a complex forest have to filter up to the forest root and then back down to the target domain, so for a geographically spread out scenario, cross-links can make sense to cut down on authentication times. (used to speed up authentication).

- External (inter-forest)— an implicitly non-transitive trust created between disparate domains. “External trusts provide access to resources in a domain outside of the forest that is not already joined by a forest trust.” External trusts enforce SID filtering.

- Tree-root (intra-Forest)— an implicit two-way transitive trust between the forest root domain and the new tree root you’re adding. I haven’t encountered tree-root trusts too often, but from the Microsoft documentation, they’re created when you when you create a new domain tree in a forest. These are intra-forest trusts, and they preserve two-way transitivity while allowing the tree to have a separate domain name (instead of child.parent.com).

- Forest — a transitive trust between one forest root domain and another forest root domain. Forest trusts also enforce SID filtering.

- MIT — a trust with a non-Windows RFC4120-compliant Kerberos domain.

[TrustType](https://msdn.microsoft.com/en-us/library/cc223771.aspx):

- DOWNLEVEL (0x00000001) — A trusted Windows domain that IS NOT running Active Directory. This is output as WINDOWS_NON_ACTIVE_DIRECTORY in PowerView for those not as familiar with the terminology.

- UPLEVEL (0x00000002) — A trusted Windows domain that is running Active Directory.This is output as WINDOWS_ACTIVE_DIRECTORY in PowerView for those not as familiar with the terminology.

- MIT (0x00000003) — a trusted domain that is running a non-Windows (*nix), RFC4120-compliant Kerberos distribution. This is labeled as MIT due to, well, MIT publishing RFC4120.

[TrustAttributes](https://msdn.microsoft.com/en-us/library/cc223779.aspx):

- NON_TRANSITIVE (0x00000001) — The trust cannot be used transitively. That is, if DomainA trusts DomainB and DomainB trusts DomainC, then DomainA does not automatically trust DomainC. Also, if a trust is non-transitive, thenyou will not be able to query any Active Directory information from trusts up the chain from the non-transitive point. External trusts are implicitly non-transitive.

- UPLEVEL_ONLY (0x00000002) — only Windows 2000 operating system and newer clients can use the trust.

- QUARANTINED_DOMAIN (0x00000004) — SID filtering is enabled (more on this later). Output as FILTER_SIDS with PowerView for simplicity.

- FOREST_TRANSITIVE (0x00000008) — cross-forest trust between the root of two domain forests running at least domain functional level 2003 or above.

- CROSS_ORGANIZATION (0x00000010) — the trust is to a domain or forest that is not part of the organization, which adds the OTHER_ORGANIZATION SID. This is a bit of a weird one. According to this post it means that the selective authentication security protection is enabled. For more information, check out this MSDN doc.

- WITHIN_FOREST (0x00000020) — the trusted domain is within the same forest, meaning a parent->child or cross-link relationship

- TREAT_AS_EXTERNAL (0x00000040) — the trust is to be treated as external for trust boundary purposes. According to the documentation, “If this bit is set, then a cross-forest trust to a domain is to be treated as an external trust for the purposes of SID Filtering. Cross-forest trusts are more stringently filtered than external trusts. This attribute relaxes those cross-forest trusts to be equivalent to external trusts.” This sounds enticing, and I’m not 100% sure on the security implications of this statement ¯\_(ツ)_/¯ but I will update this post if anything new surfaces.

- USES_RC4_ENCRYPTION (0x00000080) — if the TrustType is MIT, specifies that the trust that supports RC4 keys.

- USES_AES_KEYS (0x00000100) — not listed in the linked Microsoft documentation, but according to some documentation I’ve been able to find online, it specifies that AES keys are used to encrypt KRB TGTs.

- CROSS_ORGANIZATION_NO_TGT_DELEGATION (0x00000200) — “If this bit is set, tickets granted under this trust MUST NOT be trusted for delegation.” This is described more in [MS-KILE] 3.3.5.7.5 (Cross-Domain Trust and Referrals.)

- PIM_TRUST (0x00000400) — “If this bit and the TATE (treat as external) bit are set, then a cross-forest trust to a domain is to be treated as Privileged Identity Management trust for the purposes of SID Filtering.” According to [MS-PAC] 4.1.2.2 (SID Filtering and Claims Transformation), “A domain can be externally managed by a domain that is outside the forest. The trusting domain allows SIDs that are local to its forest to come over a PrivilegedIdentityManagement trust.”

Trusts can be one-way or two-way. A bidirectional (two-way) trust is actually just two one-way trusts. A one-way trust means users and computers in a *trusted domain* can potentially access resources in another *trusting domain*. A one-way trust is in one direction only, hence the name. Users and computers in the *trusting* domain can not access resources in the *trusted* domain. 
Microsoft has a nice diagram to visualize this:

**One-Way Trust**

A one-way trust is a unidirectional authentication path created between two domains (trust flows in one direction, and access flows in the other). 
This means that in a one-way trust between a trusted domain and a trusting domain, users or computers in the trusted domain can access resources in the trusting domain. However, users in the trusting  domain cannot access resources in the trusted domain. Some one-way trusts can be either nontransitive or transitive, depending on the type of trust being created.

**Two-Way Trust**

A two-way trust can be thought of as a combination of two, opposite-facing one-way trusts, so that, the trusting and trusted domains both trust each other (trust and access flow in both directions). This means that authentication requests can be passed between the two domains in both directions. Some two-way relationships can be either nontransitive or transitive depending on the type of trust being created. All domain trusts in an Active Directory forest are two-way, transitive trusts. When a new child domain is created, a two-way, transitive trust is automatically created between the new child domain and the parent domain.

**Trust Transitivity**

Transitivity determines whether a trust can be extended beyond the two domains between which it was formed. A transitive trust extends trust relationships to other domains; a nontransitive trust does not extend trust relationships to other domains. Each time you create a new domain in a forest, a two-way, transitive trust relationship is automatically created between the new domain and its parent domain. If child domains are added to the new domain, the trust path flows upward through the domain hierarchy, extending the initial trust path created between the new domain and its parent.

Transitive trust relationships thus flow upward through a domain tree as it is formed, creating transitive trusts between all domains in the domain tree. A domain tree can therefore be defined as a hierarchical structure of one or more domains, connected by transitive, bidirectional trusts, that forms a contiguous namespace. Multiple domain trees can belong to a single forest.

Authentication requests follow these extended trust paths, so accounts from any domain in the forest can be authenticated by any other domain in the forest. Consequently, with a single logon process, 
accounts with the proper permissions can access resources in any domain in the forest.

With a **none-transitive** trust, the flow is restricted to the two domains in the trust relationship and does not extend to any other domains in the forest. A nontransitive trust can be either a two-way trust or a one-way trust.

What we care about is the *direction of access*, not the *direction of the trust*. With a one-way trust where **A -trusts-> B**, if the trust is enumerated from A, the trust is marked as *outbound*, while if the same trust is enumerated from B the trust is marked as *inbound*, while the potential access is from **B** to **A**.

The next command is used to identify external trusts in `dollarcorp.moneycorp.local` instead of all the  trusts. As we can see below, the external trust for **dollarcorp** is `eurocorp.local`**.**

`Get-DomainTrust | ?{$_.TrustAttributes -eq "FILTER_SIDS"}`

Since the above is a Bi-Directional trust, we can extract information from the `eurocorp.local` forest. We either need bi-directional trust or one-way trust from eurocorp.local to dollarcorp.moneycorp.local to be able to use the below command and enumerate eurocorp.local trusts.

`Get-ForestDomain -Forest eurocorp.local | %{Get-DomainTrust -Domain $_.Name}`

Notice the error above. It occurred because PowerView attempted to list trusts even for `eu.eurocorp.local`. Because external trust is non-transitive it was not possible!

Let’s say now I want to list only the external trusts in the `moneycorp.local`**(our root forest)…** **(which is our is our parent domain)**. 
Meaning, the command below will allow us to get the external trusts from the root forest of our domain, in our case we are in `dollarcorp.moneycorp.local` (which is a child domain from **moneycorp.local**)and with this command we can get only the external trusts instead of all the domains at the same time.

`Get-ForestDomain | {Get-DomainTrust -Domain $_.Name} | ?{$_Trust_Attributes -eq "FILTER_SIDS"}`