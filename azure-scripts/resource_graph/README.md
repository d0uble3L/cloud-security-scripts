# Azure Resource Graph Query Script

This project contains a Python script that authenticates to Azure using a service principal and runs a query against the Azure Resource Graph. The query retrieves information about Azure resources such as their name, type, and location.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Script](#running-the-script)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before running the script, ensure you have the following:

- Python 3.6 or higher installed
- The following Python libraries:
  - `azure-identity`
  - `azure-mgmt-resourcegraph`
- An Azure service principal with the necessary permissions to query Azure Resource Graph
- The following Azure credentials:
  - Tenant ID
  - Client ID
  - Client Secret
  - Subscription ID

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/d0uble3L/cloud-security-scripts.git
   cd azure-resource-graph-script
