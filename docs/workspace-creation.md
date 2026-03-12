# Azure Databricks Cost-Optimized Setup Guide

This guide details how to set up a workspace for PySpark learning while avoiding the ~€30/month fixed NAT Gateway cost.

## 1. Network Setup (VNet Creation)
Create your Virtual Network FIRST to enable "VNet Injection".
*   **Region:** Select a Serverless-ready region (e.g., East US 2, West US 2, West Europe).
*   **Address Space:** `10.1.0.0/16`.
*   **Subnets:** Create two empty subnets:
    *   `public-subnet` (e.g., `10.1.1.0/24`)
    *   `private-subnet` (e.g., `10.1.2.0/24`)
*   **Service Endpoints:** Enable `Microsoft.Storage` and `Microsoft.KeyVault` on BOTH subnets.

## 2. Workspace Deployment Settings
When creating the Azure Databricks resource, use these specific Networking tab settings:
*   **Tier:** Premium.
*   **Deploy in your own VNet:** Yes.
*   **VNet Selection:** Choose the VNet/Subnets created in Step 1.
*   **Secure Cluster Connectivity (No Public IP):** NO. 
    *   *Crucial: Setting this to "Yes" forces the creation of a NAT Gateway.*

## 3. Compute Configuration (PySpark Exploration)
To keep running costs minimal:
*   **Single-Node Cluster:** Use "Single Node" mode with a budget VM (e.g., `Standard_DS3_v2`).
*   **Auto-Termination:** Set to 20 minutes to prevent accidental idle charges.
*   **Serverless:** Use Serverless SQL/Notebooks for quick tasks—there is zero idle fee and no NAT Gateway charge for you.

## 4. Storage & VS Code Integration
*   **Access:** Use the `abfss://` protocol in PySpark. Ensure you have the **Storage Blob Data Contributor** role on your storage account.
*   **DABs:** Update your `databricks.yml` and `.databrickscfg` with your new **Host URL** and **Cluster ID**.
*   **Firewall:** In ADLS Gen2 Networking, allow access from the two subnets you created in Step 1.
*   **Local vs Platform Dev:** Local VS Code development is fine; data access still happens from Databricks compute in your VNet through the configured service endpoints.

## 5. Cost Protection
*   **Budget Alert:** Set an Azure Budget alert for $5 to receive an email if spending exceeds your expectations.
*   **Managed RG Check:** Confirm the `databricks-rg-...` resource group does NOT contain a NAT Gateway.
*   **Quick Validation:** Run a small notebook read/write against ADLS (`abfss://`) to confirm subnet endpoint + firewall rules are working.
