from datetime import date
from db_functions import create_vulnerability, create_user

def add_real_cve_vulnerabilities():
    vulnerabilities = [
        {
            "score": 9.8,
            "location": "Web Server A",
            "status": "Open",
            "discovery_date": date(2023, 12, 10),
            "category": "Injection",
            "description": "SQL Injection in login endpoint due to improper input sanitization.",
            "cve": "CVE-2022-23521"  # Django vulnerability: SQL injection via Trunc() and Extract() functions.
        },
        {
            "score": 8.2,
            "location": "API Gateway",
            "status": "Open",
            "discovery_date": date(2024, 1, 5),
            "category": "Injection",
            "description": "SQL Injection in query parameter handling in an API endpoint.",
            "cve": "CVE-2023-34362"  # MOVEit Transfer SQL injection vulnerability.
        },
        {
            "score": 9.1,
            "location": "E-commerce Application",
            "status": "Resolved",
            "discovery_date": date(2023, 8, 15),
            "category": "Injection",
            "description": "SQL Injection vulnerability in product catalog search feature.",
            "cve": "CVE-2022-23305"  # Apache Log4j vulnerability (deserialization leading to SQL injection).
        },
        {
            "score": 7.4,
            "location": "CMS Backend",
            "status": "Open",
            "discovery_date": date(2023, 10, 30),
            "category": "Injection",
            "description": "Reflected XSS and SQL Injection vulnerability in CMS admin panel.",
            "cve": "CVE-2021-36749"  # WordPress SQL injection in specific plugins.
        },
        {
            "score": 9.0,
            "location": "Database Server",
            "status": "Resolved",
            "discovery_date": date(2024, 3, 5),
            "category": "Injection",
            "description": "Union-based SQL Injection in reporting module due to unsafe query construction.",
            "cve": "CVE-2020-13945"  # Apache Superset SQL Injection vulnerability.
        },
        {
            "score": 8.7,
            "location": "Mobile App Backend",
            "status": "Open",
            "discovery_date": date(2023, 9, 18),
            "category": "Injection",
            "description": "Blind SQL Injection vulnerability in user authentication mechanism.",
            "cve": "CVE-2020-9484"  # Apache Tomcat SQL injection in certain configurations.
        },
        {
            "score": 7.2,
            "location": "Internal API",
            "status": "Resolved",
            "discovery_date": date(2023, 11, 20),
            "category": "Injection",
            "description": "Error-based SQL Injection in parameterized API calls.",
            "cve": "CVE-2019-11043"  # PHP-FPM vulnerability leading to SQL injection.
        },
        {
            "score": 8.5,
            "location": "Payment Gateway",
            "status": "Open",
            "discovery_date": date(2024, 4, 25),
            "category": "Injection",
            "description": "SQL Injection in transaction history retrieval function.",
            "cve": "CVE-2018-6574"  # Vulnerability in Go's `text/template` package allowing injection.
        },
        {
            "score": 6.8,
            "location": "Intranet Portal",
            "status": "Resolved",
            "discovery_date": date(2024, 6, 18),
            "category": "Injection",
            "description": "SQL Injection in employee profile update API.",
            "cve": "CVE-2022-26134"  # Atlassian Confluence Server injection vulnerability.
        },
        {
            "score": 9.2,
            "location": "Legacy Web App",
            "status": "Open",
            "discovery_date": date(2024, 2, 12),
            "category": "Injection",
            "description": "SQL Injection in legacy web forms using unsafe string concatenation.",
            "cve": "CVE-2021-45046"  # Apache Log4j additional SQL injection.
        }
    ]

    for vuln in vulnerabilities:

        create_vulnerability(
            score=vuln["score"],
            location=vuln["location"],
            status=vuln["status"],
            discovery_date=vuln["discovery_date"],
            category=vuln["category"]
        )
        print(f"Added vulnerability: {vuln['description']} (CVE: {vuln['cve']})")
