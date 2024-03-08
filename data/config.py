from datetime import datetime


class StaticConfig:
    #
    LOG_TYPES = [
        {"name": "Virus/Malware", "value": "officescan_virus"},
        {"name": "Spyware/Grayware", "value": "spyware"},
        {"name": "Predictive Machine Learning", "value": "Predictive_Machine_Learning"},
        {"name": "Intrusion Prevention", "value": "intrusion_prevention"},
    ]

    # Regex patterns
    TIMESTAMP_REGEX_PATTERNS = {"valid_month_day": r"^\d+m \d+d$"}

    REGEX_PATTERNS = {
        "officescan_virus": {
            "date_pattern": r"rt=(.*?GMT\+00:00)\s",
            "malware_name_pattern": r"\|[^|]+\|[^|]+\|[^|]+\|AV:[^|]+\|([^|]+)\|",
            "detections_pattern": r"cnt=(\d+)\s",
            "action_pattern": r"act=(.*?)\scn1Label=",
            "endpoint_ip_pattern": r"dst=(.*?)(?=\s\w+=|$)",
            "domain_pattern": r"deviceNtDomain=(.*?)(?=\s\w+=|$)",
            "host_pattern": r"dhost=(.*?)(?=\s\w+=|$)",
            "user_pattern": r"duser=(.*?)\sact=",
            "system_os_pattern": r"TMCMdevicePlatform=(.*?)(?=\s\w+=|$)",
            "filename_pattern": r"fname=(.*?)(?=\s\w+=|$)",
            "filepath_pattern": r"filePath=(.*?)(?=\s\w+=|$)",
        },
        "spyware": {
            "date_pattern": r"rt=(.*?GMT\+00:00)\s",
            "spyware_name_pattern": r"cs1=(.*?)\scs2Label=",
            "detections_pattern": r"cnt=(\d+)\s",
            "action_pattern": r"cs5=(.*?)\scs6Label=",
            "endpoint_ip_pattern": r"dst=(.*?)(?=\s\w+=|$)",
            "domain_pattern": r"deviceNtDomain=(.*?)(?=\s\w+=|$)",
            "host_pattern": r"dhost=(.*?)(?=\s\w+=|$)",
            "user_pattern": r"duser=(.*?)\scn2Label=",
            "system_os_pattern": r"TMCMdevicePlatform=(.*?)(?=\s\w+=|$)",
            "filename_pattern": r"fname=.*\\([^\\]+?)(?=\sfilePath=)",
            "filepath_pattern": r"filePath=(.*?)(?=\s\w+=|$)",
        },
        "Predictive_Machine_Learning": {
            "date_pattern": r"rt=(.*?GMT\+00:00)\s",
            "unidentified_malware_name_pattern": r"\|[^|]+\|[^|]+\|[^|]+\|PML:[^|]+\|([^|]+)\|",
            "detections_pattern": None,
            "action_pattern": r"PML:(.*?)\|",
            "endpoint_ip_pattern": r"dst=(.*?)(?=\s\w+=|$)",
            "domain_pattern": r"deviceNtDomain=(.*?)(?=\s\w+=|$)",
            "host_pattern": r"dhost=(.*?)(?=\s\w+=|$)",
            "user_pattern": r"duser=(.*?)\sapp=",
            "system_os_pattern": r"TMCMdevicePlatform=(.*?)(?=\s\w+=|$)",
            "filename_pattern": r"fname=(.*?)(?=\s\w+=|$)",
            "filepath_pattern": r"filePath=(.*?)(?=\s\w+=|$)",
        },
        "intrusion_prevention": {
            "date_pattern": r"rt=(.*?GMT\+00:00)\s",
            "attack_name_pattern": r"cs1=(.*?)\scnt=",
            "detections_pattern": None,
            "action_pattern": r"act=(.*?)\sdeviceDirection=",
            "attack_source_ip_pattern": r"src=(.*?)\sTMCMLogDetectedIP=",
            "attack_source_port_pattern": r"spt=(.*?)\sdmac=",
            "endpoint_ip_pattern": r"dst=(.*?)\ssmac=",
            "endpoint_port_pattern": r"dpt=(.*?)\scn2Label=",
            "domain_pattern": r"deviceNtDomain=(.*?)\sdntdom=",
            "host_pattern": r"TMCMLogDetectedHost=(.*?)\sdst=",
            "system_os_pattern": r"TMCMdevicePlatform=(.*?)\sdeviceNtDomain=",
        },
    }

    DATE_FORMATS = {
        "default_date_format": "%b %d %Y %H:%M:%S GMT%z",
        "brazil_date_format": "%d/%m/%Y %H:%M:%S",
    }

    CSV_FIELDS = {
        "officescan_virus": [
            "Date",
            "Virus/Malware",
            "Detections",
            "Action",
            "Destination IP",
            "Domain",
            "Host",
            "User",
            "OS",
            "File name",
            "File path",
        ],
        "spyware": [
            "Date",
            "Spyware/Grayware",
            "Detections",
            "Action",
            "Destination IP",
            "Domain",
            "Host",
            "User",
            "OS",
            "File name",
            "File path",
        ],
        "Predictive_Machine_Learning": [
            "Date",
            "Unidentified Malware Name",
            "Detections",
            "Action",
            "Destination IP",
            "Domain",
            "Host",
            "User",
            "OS",
            "File name",
            "File path",
        ],
        "intrusion_prevention": [
            "Date",
            "Attack Name",
            "Detections",
            "Action",
            "Attack Source IP",
            "Attack Source Port",
            "Destination IP",
            "Destination Port",
            "Domain",
            "Host",
            "User",
            "OS",
            "File name",
            "File path",
        ],
    }

    DEBUG = False


class DynamicConfig:
    clients = []
    selected_client = None
    selected_timestamp = None
    selected_old_date = None
    selected_logtype = None
    selected_logtype_regex_patterns = None
    log_list = []
    csv_filename = None
