# ThreatStream Automater

ThreatStream Automater is a threat intelligence aggregation and automation tool that ingests security news from multiple sources, extracts actionable intelligence, and delivers curated insights directly to collaboration platforms such as Microsoft Teams and Slack.

#### Developed by: Andre Alix

## Overview

This project automates the process of collecting, filtering, and distributing threat intelligence to reduce manual monitoring effort and improve visibility into emerging vulnerabilities and threats.

It is designed to support Application Security (AppSec) teams by surfacing relevant intelligence such as CVEs, exploits, and indicators of compromise (IOCs).

## Features

- **RSS Feed Aggregation**
  - Ingests threat intelligence from multiple RSS-based sources
  - Easily extensible framework for adding new feeds

- **Automated Web Scraping**
  - Uses Selenium to extract structured data from unstructured web pages
  - Custom scraping logic per source

- **Threat Intelligence Extraction**
  - Identifies and extracts:
    - CVEs
    - Key tags
    - Relevant security indicators

- **Customizable Filtering**
  - Keyword-based filtering to remove noise
  - Prioritizes high-risk vulnerabilities and relevant threats

- **Standardized Output**
  - Formats intelligence into a consistent structure
  - Optimized for analyst review

- **Collaboration Integration**
  - Sends curated threat intelligence directly to:
    - Microsoft Teams
    - Slack

## Architecture

![Tech Architecture Diagram](https://imgur.com/a/4QPra3Y)

## Use Cases

- Monitor emerging vulnerabilities affecting dependencies
- Track new CVEs and exploit trends
- Support AppSec vulnerability management workflows
- Provide actionable intelligence to SOC / threat intel teams
- Reduce manual effort in threat monitoring

## Tech Stack

- **Language:** Python  
- **Automation/Scraping:** Selenium  
- **Data Sources:** RSS Feeds  
- **Integrations:** Microsoft Teams, Slack  

## Setup

```bash

  python -m venv .venv

  .venv\Scripts\activate

  pip install -r requirements.txt

```
