import json
from jsonschema import validate
import re
import ast

OBJECT_SCHEMA = {
  "type": "object",
  "properties": {
    "$schema": {
      "type": "string"
    },
    "meta": {
      "type": "object",
      "properties": {
        "uri": {
          "type": "string"
        },
        "request_id": {
          "type": "string"
        },
        "id": {
          "type": "string"
        },
        "dt": {
          "type": "string"
        },
        "domain": {
          "type": "string"
        },
        "stream": {
          "type": "string"
        },
        "topic": {
          "type": "string"
        },
        "partition": {
          "type": "integer"
        },
        "offset": {
          "type": "integer"
        }
      }
    },
    "type": {
      "type": "string",
      #"enum": ["log"]
    },
    "namespace": {
      "type": "integer"
    },
    "title": {
      "type": "string"
    },
    "title_url": {
      "type": "string"
    },
    "comment": {
      "type": "string",
      #"enum": [""]  
    },
    "timestamp": {
      "type": "integer"
    },
    "user": {
      "type": "string"
    },
    "bot": {
      "type": "boolean"
    },
    "log_id": {
      "type": "integer"
    },
    "log_type": {
      "type": "string",
      #"enum": ["abusefilter"]
    },
    "log_action": {
      "type": "string",
      #"enum": ["hit"]
    },
    "log_action_comment": {
      "type": "string"
    },
    "server_url": {
      "type": "string"
    },
    "server_name": {
      "type": "string"
    },
    "server_script_path": {
      "type": "string"
    },
    "wiki": {
      "type": "string"
    },
    "parsedcomment": {
      "type": "string"
    }
  },
  "required": []
}

def validate_data(json_data, schema=OBJECT_SCHEMA):
    # Validate the data against the schema
    error = ""
    try:
        validate(instance=json_data, schema=schema)
    except Exception as e:
        error = str(e)
    
    result = True if error == "" else False
    return {
        "result": result,
        "error": error
    }
