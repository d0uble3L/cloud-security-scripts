import os
import json
import importlib
import configparser
import logging
from getpass import getpass
import csv
from jinja2 import Template

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='cloud_analysis.log',
                    filemode='a')
logger = logging.getLogger(__name__)

def setup_aws_credentials():
    print("\n--- Setting up AWS credentials ---")
    aws_access_key_id = input("Enter your AWS Access Key ID: ")
    aws_secret_access_key = getpass("Enter your AWS Secret Access Key: ")
    aws_region = input("Enter your default AWS region (e.g., us-west-2): ")

    config = configparser.ConfigParser()
    config['default'] = {
        'aws_access_key_id': aws_access_key_id,
        'aws_secret_access_key': aws_secret_access_key,
        'region': aws_region
    }

    os.makedirs(os.path.expanduser("~/.aws"), exist_ok=True)
    with open(os.path.expanduser("~/.aws/credentials"), 'w') as configfile:
        config.write(configfile)

    print("AWS credentials have been saved to ~/.aws/credentials")
    logger.info("AWS credentials have been saved to ~/.aws/credentials")

def setup_azure_credentials():
    print("\n--- Setting up Azure credentials ---")
    tenant_id = input("Enter your Azure Tenant ID: ")
    client_id = input("Enter your Azure Client ID: ")
    client_secret = getpass("Enter your Azure Client Secret: ")
    subscription_id = input("Enter your Azure Subscription ID: ")
    azure_region = input("Enter your default Azure region (e.g., eastus): ")

    azure_config = {
        'tenant_id': tenant_id,
        'client_id': client_id,
        'client_secret': client_secret,
        'subscription_id': subscription_id,
        'region': azure_region
    }

    with open('azure_config.json', 'w') as f:
        json.dump(azure_config, f)

    print("Azure credentials have been saved to azure_config.json")
    logger.info("Azure credentials have been saved to azure_config.json")

def get_available_scripts(directory):
    scripts = []
    if os.path.exists(directory):
        for file in os.listdir(directory):
            if file.endswith(".py") and file != "__init__.py":
                scripts.append(file[:-3])  # Remove .py extension
    return scripts

def run_analysis(env, scripts):
    results = []
    for script in scripts:
        print(f"\nRunning {script} for {env}...")
        logger.info(f"Running {script} for {env}...")
        try:
            module = importlib.import_module(f"{env}-scripts.{script}")
            if hasattr(module, 'main'):
                script_results = module.main()
                results.append({"script": script, "results": script_results})
            else:
                logger.warning(f"{script} does not have a main() function.")
        except Exception as e:
            error_message = f"Error running {script}: {str(e)}"
            print(error_message)
            logger.error(error_message)
            results.append({"script": script, "error": error_message})
    return results

def save_results_to_csv(results, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Script', 'Result'])
        for result in results:
            script = result['script']
            if 'error' in result:
                writer.writerow([script, f"Error: {result['error']}"])
            else:
                for item in result['results']:
                    if item.lower().startswith('warning'):
                        writer.writerow([script, f"WARNING: {item}"])
                    else:
                        writer.writerow([script, item])

def save_results_to_html(results, filename):
    template = Template("""
    <html>
    <head>
        <title>Cloud Security Analysis Results</title>
        <style>
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid black; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .warning { color: red; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>Cloud Security Analysis Results</h1>
        {% for result in results %}
            <h2>{{ result.script }}</h2>
            {% if 'error' in result %}
                <p style="color: red;">Error: {{ result.error }}</p>
            {% else %}
                <table>
                    <tr><th>Result</th></tr>
                    {% for item in result.results %}
                        <tr>
                            <td {% if item.lower().startswith('warning') %}class="warning"{% endif %}>
                                {{ item }}
                            </td>
                        </tr>
                    {% endfor %}
                </table>
            {% endif %}
        {% endfor %}
    </body>
    </html>
    """)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(template.render(results=results))

def setup_aws_region():
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~/.aws/credentials'))
    
    if 'default' not in config or 'region' not in config['default']:
        print("\nAWS region not found in credentials file.")
        region = input("Enter your default AWS region (e.g., us-west-2): ")
        
        if 'default' not in config:
            config['default'] = {}
        config['default']['region'] = region
        
        with open(os.path.expanduser('~/.aws/credentials'), 'w') as configfile:
            config.write(configfile)
        
        print(f"AWS region {region} has been added to ~/.aws/credentials")
        logger.info(f"AWS region {region} has been added to ~/.aws/credentials")

def main():
    print("Welcome to the Cloud Security Scripts analyzer!")
    logger.info("Starting Cloud Security Scripts analyzer")

    # Select environment
    print("\nSelect environment(s) to analyze:")
    print("1. AWS")
    print("2. Azure")
    print("3. Both")
    env_choice = input("Enter your choice (1/2/3): ")

    # Setup credentials if needed
    if env_choice in ['1', '3']:
        if not os.path.exists(os.path.expanduser("~/.aws/credentials")):
            setup_aws_credentials()
        else:
            print("\nAWS credentials already exist.")
        setup_aws_region()  # Add this line

    if env_choice in ['2', '3']:
        if not os.path.exists("azure_config.json"):
            setup_azure_credentials()
        else:
            print("\nAzure credentials already exist.")

    # Get available scripts
    aws_scripts = get_available_scripts("aws-scripts")
    azure_scripts = get_available_scripts("azure-scripts")

    # Select scripts to run
    aws_selected = []
    azure_selected = []

    if env_choice in ['1', '3']:
        if aws_scripts:
            print("\nAvailable AWS scripts:")
            for i, script in enumerate(aws_scripts, 1):
                print(f"{i}. {script}")
            aws_input = input("Enter the numbers of the AWS scripts to run (comma-separated): ")
            aws_selected = [aws_scripts[int(i)-1] for i in aws_input.split(',') if i.strip()]
            print(f"Selected AWS scripts: {', '.join(aws_selected)}")
        else:
            print("\nNo AWS scripts found in the 'aws-scripts' directory.")

    if env_choice in ['2', '3']:
        if azure_scripts:
            print("\nAvailable Azure scripts:")
            for i, script in enumerate(azure_scripts, 1):
                print(f"{i}. {script}")
            azure_input = input("Enter the numbers of the Azure scripts to run (comma-separated): ")
            azure_selected = [azure_scripts[int(i)-1] for i in azure_input.split(',') if i.strip()]
            print(f"Selected Azure scripts: {', '.join(azure_selected)}")
        else:
            print("\nNo Azure scripts found in the 'azure-scripts' directory.")

    # Run selected scripts
    all_results = []
    if env_choice in ['1', '3'] and aws_selected:
        print("\n--- Running AWS Analysis ---")
        all_results.extend(run_analysis('aws', aws_selected))
    if env_choice in ['2', '3'] and azure_selected:
        print("\n--- Running Azure Analysis ---")
        all_results.extend(run_analysis('azure', azure_selected))

    # Ask for output format
    output_format = input("Choose output format (csv/html/both): ").lower()
    if output_format in ['csv', 'both']:
        save_results_to_csv(all_results, 'cloud_security_analysis.csv')
        print("Results saved to cloud_security_analysis.csv")
    if output_format in ['html', 'both']:
        save_results_to_html(all_results, 'cloud_security_analysis.html')
        print("Results saved to cloud_security_analysis.html")

    print("\nAnalysis complete!")
    logger.info("Analysis complete!")

if __name__ == "__main__":
    main()