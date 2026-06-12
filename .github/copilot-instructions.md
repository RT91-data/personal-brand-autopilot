# GitHub Copilot instructions

<!-- github-copilot-toolbox:mcp-skills-awareness-begin -->

### MCP & Skills awareness (GitHub Copilot Toolbox)

_Last synced: 2026-06-12T04:17:00.823Z._

- **Full report:** `.github/copilot-toolbox-mcp-skills-awareness.md` in this workspace (auto-overwritten on each scan). Use it as ground truth for configured servers and skill folders.
- **MCP:** For **live tools**, use **Copilot Chat → Agent** and **trust/start** the right servers in the MCP UI.
- **When the user’s task matches a server** (e.g. “open this Confluence page” and a **Confluence** / **Atlassian** MCP is listed), **prefer that server id** and plan on Agent + MCP for actions—not only file search.
- **Skills:** Folders below contain `SKILL.md`; attach or cite paths in chat when relevant.

#### Workspace MCP

- `c:\AIlearning\personal-brand-autopilot\.vscode\mcp.json` _(workspace: personal-brand-autopilot)_ — _file missing_

_No active workspace servers in mcp.json._

#### User MCP

- `C:\Users\User\AppData\Roaming\Code\User\mcp.json` — _file missing_

_No active user-scoped servers in mcp.json._

#### Project skills

_None found (or no workspace open)._

#### User skills

- **airunway-aks-setup** — `C:\Users\User\.agents\skills\airunway-aks-setup` — Set up AI Runway on AKS — from bare cluster to running model. Covers cluster verification, controller install, GPU assessment, provider setup, and first deployment. WHEN: \"setup AI Runway\", \"onboard AKS cluster\", \"i

- **appinsights-instrumentation** — `C:\Users\User\.agents\skills\appinsights-instrumentation` — Guidance for instrumenting webapps with Azure Application Insights. Provides telemetry patterns, SDK setup, and configuration references. WHEN: how to instrument app, App Insights SDK, telemetry patterns, what is App Ins

- **azure-ai** — `C:\Users\User\.agents\skills\azure-ai` — Use for Azure AI: Search, Speech, OpenAI, Document Intelligence. Helps with search, vector/hybrid search, speech-to-text, text-to-speech, transcription, OCR. WHEN: AI Search, query search, vector search, hybrid search, s

- **azure-aigateway** — `C:\Users\User\.agents\skills\azure-aigateway` — Configure Azure API Management as an AI Gateway for AI models, MCP tools, and agents. WHEN: semantic caching, token limit, content safety, load balancing, AI model governance, MCP rate limiting, jailbreak detection, add 

- **azure-cloud-migrate** — `C:\Users\User\.agents\skills\azure-cloud-migrate` — Assess and migrate cross-cloud workloads to Azure with reports and code conversion. Supports Lambda→Functions, Beanstalk/Heroku/App Engine→App Service, Fargate/Kubernetes/Cloud Run/Spring Boot→Container Apps. WHEN: migra

- **azure-compliance** — `C:\Users\User\.agents\skills\azure-compliance` — Run Azure compliance and security audits with azqr plus Key Vault expiration checks. Covers best-practice assessment, resource review, policy/compliance validation, and security posture checks. WHEN: compliance scan, sec

- **azure-compute** — `C:\Users\User\.agents\skills\azure-compute` — Azure VM and VMSS router for recommendations, pricing, autoscale, orchestration, connectivity troubleshooting, capacity reservations, and Essential Machine Management. WHEN: Azure VM, VMSS, scale set, recommend, compare,

- **azure-cost** — `C:\Users\User\.agents\skills\azure-cost` — Azure cost management: query costs, forecast spending, optimize to reduce waste. WHEN: \"Azure costs\", \"Azure bill\", \"cost breakdown\", \"how much am I spending\", \"forecast spending\", \"optimize costs\", \"reduce 

- **azure-deploy** — `C:\Users\User\.agents\skills\azure-deploy` — Execute Azure deployments for ALREADY-PREPARED applications that have existing .azure/deployment-plan.md and infrastructure files. DO NOT use this skill when the user asks to CREATE a new application — use azure-prepare 

- **azure-diagnostics** — `C:\Users\User\.agents\skills\azure-diagnostics` — Debug Azure production issues on Azure using AppLens, Azure Monitor, resource health, and safe triage. WHEN: debug production issues, troubleshoot app service, app service high CPU, app service deployment failure, troubl

- **azure-enterprise-infra-planner** — `C:\Users\User\.agents\skills\azure-enterprise-infra-planner` — Architect and provision enterprise Azure infrastructure from workload descriptions. For cloud architects and platform engineers planning networking, identity, security, compliance, and multi-resource topologies with WAF 

- **azure-hosted-copilot-sdk** — `C:\Users\User\.agents\skills\azure-hosted-copilot-sdk` — Build, deploy, and modify GitHub Copilot SDK apps on Azure. MANDATORY when codebase contains @github/copilot-sdk or CopilotClient in package.json. PREFER OVER azure-prepare when copilot-sdk markers detected. WHEN: copilo

- **azure-kubernetes** — `C:\Users\User\.agents\skills\azure-kubernetes` — Plan, create, and configure production-ready Azure Kubernetes Service (AKS) clusters. Covers Day-0 checklist, SKU selection (Automatic vs Standard), networking options (private API server, Azure CNI Overlay, egress confi

- **azure-kusto** — `C:\Users\User\.agents\skills\azure-kusto` — Query and analyze data in Azure Data Explorer (Kusto/ADX) using KQL for log analytics, telemetry, and time series analysis. WHEN: KQL queries, Kusto database queries, Azure Data Explorer, ADX clusters, log analytics, tim

- **azure-messaging** — `C:\Users\User\.agents\skills\azure-messaging` — Troubleshoot and resolve issues with Azure Messaging SDKs for Event Hubs and Service Bus. Covers connection failures, authentication errors, message processing issues, and SDK configuration problems. WHEN: event hub SDK 

- **azure-prepare** — `C:\Users\User\.agents\skills\azure-prepare` — Prepare Azure apps for deployment (infra Bicep/Terraform, azure.yaml, Dockerfiles). Use for create/modernize or create+deploy; not cross-cloud migration (use azure-cloud-migrate). DO NOT USE FOR: copilot-sdk apps (use az

- **azure-quotas** — `C:\Users\User\.agents\skills\azure-quotas` — Check/manage Azure quotas and usage across providers. For deployment planning, capacity validation, region selection. WHEN: \"check quotas\", \"service limits\", \"current usage\", \"request quota increase\", \"quota exc

- **azure-rbac** — `C:\Users\User\.agents\skills\azure-rbac` — Helps users find the right Azure RBAC role for an identity with least privilege access, then generate CLI commands and Bicep code to assign it. Also provides guidance on permissions required to grant roles. WHEN: bicep f

- **azure-reliability** — `C:\Users\User\.agents\skills\azure-reliability` — Assess and improve the reliability posture of PaaS Applications (Azure Functions and Azure App Service). Scans deployed resources for zone redundancy, ZRS storage, health probes, and multi-region failover. Presents a fea

- **azure-resource-lookup** — `C:\Users\User\.agents\skills\azure-resource-lookup` — List, find, and show Azure resources across subscriptions or resource groups. Handles prompts like \"list the websites in my subscription\", \"list my web apps\", \"show my app services\", \"list virtual machines\", \"li

- **azure-resource-visualizer** — `C:\Users\User\.agents\skills\azure-resource-visualizer` — Analyze Azure resource groups and generate detailed Mermaid architecture diagrams showing the relationships between individual resources. WHEN: create architecture diagram, visualize Azure resources, show resource relati

- **azure-storage** — `C:\Users\User\.agents\skills\azure-storage` — Azure Storage Services including Blob Storage, File Shares, Queue Storage, Table Storage, and Data Lake. Answers questions about storage access tiers (hot, cool, cold, archive), when to use each tier, and tier comparison

- **azure-upgrade** — `C:\Users\User\.agents\skills\azure-upgrade` — Assess and upgrade Azure workloads between plans, tiers, or SKUs, or modernize Azure SDK dependencies in source code. WHEN: upgrade Consumption to Flex Consumption, upgrade Azure Functions plan, change hosting plan, func

- **azure-validate** — `C:\Users\User\.agents\skills\azure-validate` — Pre-deployment validation for Azure readiness. Run deep checks on configuration, infrastructure (Bicep or Terraform), RBAC role assignments, managed identity permissions, and prerequisites before deploying. WHEN: validat

- **entra-agent-id** — `C:\Users\User\.agents\skills\entra-agent-id` — Provision Microsoft Entra Agent Identity Blueprints, BlueprintPrincipals, and per-instance Agent Identities via Microsoft Graph, and configure OAuth 2.0 token exchange (fmi_path, OBO, cross-tenant) including the Microsof

- **entra-app-registration** — `C:\Users\User\.agents\skills\entra-app-registration` — Guides Microsoft Entra ID app registration, OAuth 2.0 authentication, and MSAL integration. USE FOR: create app registration, register Azure AD app, configure OAuth, set up authentication, add API permissions, generate s

- **microsoft-foundry** — `C:\Users\User\.agents\skills\microsoft-foundry` — Deploy, evaluate, fine-tune, and manage Foundry agents end-to-end: Docker build, ACR push, hosted/prompt agent create, batch eval, continuous eval, prompt optimizer, Agent Optimizer scaffold, agent.yaml, dataset curation

<!-- github-copilot-toolbox:mcp-skills-awareness-end -->
