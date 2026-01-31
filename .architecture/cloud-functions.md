# Cloud Functions Architecture

This document defines the GCP Cloud Functions that power the C-suite AI agents.

---

## Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ENTRY POINTS                                 │
├─────────────────────────────────────────────────────────────────────┤
│  Telegram Bot  │  Signal Bot  │  GitHub Webhook  │  Scheduled Jobs  │
└───────┬────────┴──────┬───────┴────────┬─────────┴────────┬─────────┘
        │               │                │                  │
        └───────────────┴────────────────┴──────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │   MESSAGE ROUTER      │
                    │   (Cloud Function)    │
                    └───────────┬───────────┘
                                │
                    ┌───────────▼───────────┐
                    │     Pub/Sub Topics    │
                    └───────────┬───────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │           │           │           │           │
   ┌────▼────┐ ┌────▼────┐ ┌────▼────┐ ┌────▼────┐ ┌────▼────┐
   │   CEO   │ │   CFO   │ │   CMO   │ │   COO   │ │   ...   │
   │ Function│ │ Function│ │ Function│ │ Function│ │ Function│
   └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
        │           │           │           │           │
        └───────────┴───────────┴───────────┴───────────┘
                                │
                    ┌───────────▼───────────┐
                    │       BigQuery        │
                    │  (Shared Data Layer)  │
                    └───────────────────────┘
```

---

## Function Inventory

| Function | Trigger | Purpose |
|----------|---------|---------|
| `router` | Pub/Sub: messages | Route messages to agents |
| `ceo-agent` | Pub/Sub: ceo-tasks | Execute CEO commands |
| `cfo-agent` | Pub/Sub: cfo-tasks | Execute CFO commands |
| `cmo-agent` | Pub/Sub: cmo-tasks | Execute CMO commands |
| `coo-agent` | Pub/Sub: coo-tasks | Execute COO commands |
| `cio-agent` | Pub/Sub: cio-tasks | Execute CIO commands |
| `clo-agent` | Pub/Sub: clo-tasks | Execute CLO commands |
| `cpo-agent` | Pub/Sub: cpo-tasks | Execute CPO commands |
| `cto-agent` | Pub/Sub: cto-tasks | Execute CTO commands |
| `telegram-webhook` | HTTP | Receive Telegram messages |
| `greenlight-handler` | Pub/Sub: greenlights | Process approvals |
| `escalation-handler` | Pub/Sub: escalations | Route RED PHONE |
| `daily-summary` | Scheduler | Generate daily reports |
| `kpi-snapshot` | Scheduler | Capture daily KPIs |

---

## Base Agent Function

All agent functions share this structure:

```python
"""
Base agent Cloud Function template.
"""
import json
import base64
from datetime import datetime
from google.cloud import bigquery, secretmanager, pubsub_v1

# Initialize clients
bq_client = bigquery.Client()
secrets_client = secretmanager.SecretManagerServiceClient()
publisher = pubsub_v1.PublisherClient()


def get_secret(secret_name: str, project_id: str) -> str:
    """Retrieve secret from Secret Manager."""
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = secrets_client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


def log_conversation(data: dict):
    """Log conversation to BigQuery."""
    table_id = f"{data['project_id']}.{data['dataset']}.conversations"
    errors = bq_client.insert_rows_json(table_id, [data])
    if errors:
        raise Exception(f"BigQuery insert error: {errors}")


def log_thinking(data: dict):
    """Log thinking to BigQuery."""
    table_id = f"{data['project_id']}.{data['dataset']}.thinking_logs"
    errors = bq_client.insert_rows_json(table_id, [data])
    if errors:
        raise Exception(f"BigQuery insert error: {errors}")


def send_message(to: str, message: dict, topic: str):
    """Publish message to Pub/Sub."""
    message['timestamp'] = datetime.utcnow().isoformat()
    data = json.dumps(message).encode('utf-8')
    publisher.publish(topic, data)


def call_llm(prompt: str, config: dict) -> dict:
    """
    Call LLM and return response with metadata.
    
    Returns:
        {
            "content": str,
            "model": str,
            "provider": str,
            "input_tokens": int,
            "output_tokens": int,
            "cost": float,
            "thinking": list
        }
    """
    provider = config.get('provider', 'anthropic')
    model = config.get('model', 'claude-3.5-sonnet')
    
    # Provider-specific implementation
    if provider == 'anthropic':
        return call_anthropic(prompt, model, config)
    elif provider == 'openai':
        return call_openai(prompt, model, config)
    elif provider == 'google':
        return call_google(prompt, model, config)
    elif provider == 'openrouter':
        return call_openrouter(prompt, model, config)
    else:
        raise ValueError(f"Unknown provider: {provider}")


def call_anthropic(prompt: str, model: str, config: dict) -> dict:
    """Call Anthropic API."""
    import anthropic
    
    api_key = get_secret('anthropic-api-key', config['project_id'])
    client = anthropic.Anthropic(api_key=api_key)
    
    # Enable extended thinking if available
    response = client.messages.create(
        model=model,
        max_tokens=config.get('max_tokens', 4096),
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Calculate cost
    pricing = {
        "claude-3.5-sonnet": {"input": 3.00, "output": 15.00},
        "claude-3-opus": {"input": 15.00, "output": 75.00},
        "claude-3-haiku": {"input": 0.25, "output": 1.25}
    }
    model_pricing = pricing.get(model, {"input": 3.00, "output": 15.00})
    input_cost = (response.usage.input_tokens / 1_000_000) * model_pricing["input"]
    output_cost = (response.usage.output_tokens / 1_000_000) * model_pricing["output"]
    
    return {
        "content": response.content[0].text,
        "model": model,
        "provider": "anthropic",
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "cost": input_cost + output_cost,
        "thinking": []  # Extract if using extended thinking
    }


def agent_handler(event, context, agent_config: dict):
    """
    Generic agent handler.
    
    Args:
        event: Pub/Sub event
        context: Cloud Function context
        agent_config: Position-specific configuration
    """
    # Parse message
    message_data = json.loads(base64.b64decode(event['data']))
    
    conversation_id = message_data.get('conversation_id', str(uuid.uuid4()))
    business_id = message_data['business_id']
    command = message_data.get('command', 'default')
    
    start_time = datetime.utcnow()
    
    try:
        # Load context from GitHub/memory
        context_docs = load_agent_context(agent_config['position'], business_id)
        
        # Build prompt
        prompt = build_prompt(
            command=command,
            input_data=message_data.get('input', {}),
            context=context_docs,
            agent_config=agent_config
        )
        
        # Call LLM
        llm_response = call_llm(prompt, {
            'provider': agent_config.get('provider', 'anthropic'),
            'model': agent_config.get('model', 'claude-3.5-sonnet'),
            'project_id': agent_config['project_id'],
            'max_tokens': agent_config.get('max_tokens', 4096)
        })
        
        end_time = datetime.utcnow()
        
        # Log conversation
        log_conversation({
            'conversation_id': conversation_id,
            'business_id': business_id,
            'agent_position': agent_config['position'],
            'command': command,
            'model_provider': llm_response['provider'],
            'model_name': llm_response['model'],
            'started_at': start_time.isoformat(),
            'completed_at': end_time.isoformat(),
            'duration_seconds': (end_time - start_time).total_seconds(),
            'input_tokens': llm_response['input_tokens'],
            'output_tokens': llm_response['output_tokens'],
            'total_tokens': llm_response['input_tokens'] + llm_response['output_tokens'],
            'total_cost': llm_response['cost'],
            'status': 'success',
            'project_id': agent_config['project_id'],
            'dataset': agent_config['dataset']
        })
        
        # Log thinking
        for i, thought in enumerate(llm_response.get('thinking', [])):
            log_thinking({
                'log_id': f"{conversation_id}-{i}",
                'conversation_id': conversation_id,
                'business_id': business_id,
                'agent_position': agent_config['position'],
                'step_number': i,
                'thinking_type': thought.get('type', 'analysis'),
                'content': thought.get('content', ''),
                'confidence_score': thought.get('confidence', 0.8),
                'project_id': agent_config['project_id'],
                'dataset': agent_config['dataset']
            })
        
        # Process response and send any outgoing messages
        process_agent_response(
            response=llm_response['content'],
            agent_config=agent_config,
            conversation_id=conversation_id,
            business_id=business_id
        )
        
        return {'status': 'success', 'conversation_id': conversation_id}
        
    except Exception as e:
        # Log error
        log_conversation({
            'conversation_id': conversation_id,
            'business_id': business_id,
            'agent_position': agent_config['position'],
            'command': command,
            'status': 'error',
            'error_message': str(e),
            'project_id': agent_config['project_id'],
            'dataset': agent_config['dataset']
        })
        raise
```

---

## Agent-Specific Functions

### CEO Agent

```python
# functions/ceo-agent/main.py

from base_agent import agent_handler

CEO_CONFIG = {
    'position': 'CEO',
    'model': 'claude-3.5-sonnet',
    'provider': 'anthropic',
    'max_tokens': 8192,
    'commands': ['vision', 'plan', 'propagate', 'inquire', 'report'],
    'can_task_agents': ['CFO', 'CMO', 'COO', 'CIO', 'CLO', 'CPO'],
    'gates': ['CTO']  # CEO must greenlight CTO
}

def main(event, context):
    """CEO agent Cloud Function entry point."""
    return agent_handler(event, context, CEO_CONFIG)
```

### CFO Agent

```python
# functions/cfo-agent/main.py

from base_agent import agent_handler

CFO_CONFIG = {
    'position': 'CFO',
    'model': 'claude-3.5-sonnet',
    'provider': 'anthropic',
    'max_tokens': 8192,
    'commands': ['budget', 'forecast', 'analyze', 'compliance'],
    'escalation_direct_to_human': True,  # RED PHONE
}

def main(event, context):
    """CFO agent Cloud Function entry point."""
    return agent_handler(event, context, CFO_CONFIG)
```

---

## Telegram Webhook

```python
# functions/telegram-webhook/main.py

import os
import json
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()

def main(request):
    """Handle incoming Telegram messages."""
    update = request.get_json()
    
    if 'message' not in update:
        return {'ok': True}
    
    message = update['message']
    chat_id = message['chat']['id']
    text = message.get('text', '')
    
    # Check for GREENLIGHT/HALT commands
    if 'GREENLIGHT' in text.upper():
        return handle_greenlight(text, chat_id)
    elif 'HALT' in text.upper():
        return handle_halt(chat_id)
    
    # Route to CEO
    topic = os.environ.get('CEO_TOPIC')
    
    data = json.dumps({
        'business_id': get_business_for_chat(chat_id),
        'from': 'human',
        'command': 'vision',
        'input': {'message': text},
        'chat_id': chat_id
    }).encode('utf-8')
    
    publisher.publish(topic, data)
    
    return {'ok': True}


def handle_greenlight(text: str, chat_id: str):
    """Process GREENLIGHT command."""
    # Parse greenlight type
    import re
    match = re.search(r'GREENLIGHT:\s*(\w+)', text.upper())
    
    if match:
        greenlight_type = match.group(1)
        # Publish to greenlights topic
        topic = os.environ.get('GREENLIGHT_TOPIC')
        data = json.dumps({
            'business_id': get_business_for_chat(chat_id),
            'type': greenlight_type,
            'from': 'human',
            'chat_id': chat_id
        }).encode('utf-8')
        publisher.publish(topic, data)
        
    return {'ok': True}


def handle_halt(chat_id: str):
    """Process HALT command - stop all agents."""
    # Publish halt to all agent topics
    # ... implementation
    return {'ok': True}
```

---

## Deployment

### Terraform

```hcl
# terraform/main.tf

provider "google" {
  project = var.project_id
  region  = var.region
}

# Pub/Sub Topics
resource "google_pubsub_topic" "agent_topics" {
  for_each = toset([
    "ceo-tasks", "cfo-tasks", "cmo-tasks", "coo-tasks",
    "cio-tasks", "clo-tasks", "cpo-tasks", "cto-tasks",
    "messages", "greenlights", "escalations"
  ])
  
  name = "${var.business_id}-${each.key}"
}

# BigQuery Dataset
resource "google_bigquery_dataset" "agent_data" {
  dataset_id = "${replace(var.business_id, "-", "_")}_agents"
  location   = var.region
}

# Cloud Functions
resource "google_cloudfunctions2_function" "ceo_agent" {
  name     = "${var.business_id}-ceo-agent"
  location = var.region
  
  build_config {
    runtime     = "python311"
    entry_point = "main"
    source {
      storage_source {
        bucket = google_storage_bucket.functions.name
        object = google_storage_bucket_object.ceo_agent.name
      }
    }
  }
  
  service_config {
    max_instance_count = 10
    timeout_seconds    = 540
    
    environment_variables = {
      PROJECT_ID  = var.project_id
      BUSINESS_ID = var.business_id
      DATASET     = google_bigquery_dataset.agent_data.dataset_id
    }
    
    secret_environment_variables {
      key        = "ANTHROPIC_API_KEY"
      project_id = var.project_id
      secret     = "anthropic-api-key"
      version    = "latest"
    }
  }
  
  event_trigger {
    trigger_region = var.region
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic   = google_pubsub_topic.agent_topics["ceo-tasks"].id
  }
}

# Similar for other agents...
```

---

## Environment Configuration

```yaml
# config/prod.yaml
project_id: your-gcp-project
region: us-central1
business_id: nano-banana

agents:
  ceo:
    model: claude-3.5-sonnet
    provider: anthropic
    max_tokens: 8192
  cfo:
    model: claude-3.5-sonnet
    provider: anthropic
    max_tokens: 8192
  cmo:
    model: claude-3.5-sonnet
    provider: anthropic
    max_tokens: 8192
    # CMO may need special config for content generation
  coo:
    model: claude-3.5-sonnet
    provider: anthropic
    max_tokens: 4096
  cio:
    model: claude-3.5-sonnet
    provider: anthropic
    max_tokens: 4096
  clo:
    model: claude-3-opus  # More careful for legal
    provider: anthropic
    max_tokens: 8192
  cpo:
    model: claude-3.5-sonnet
    provider: anthropic
    max_tokens: 4096
  cto:
    model: claude-3.5-sonnet
    provider: anthropic
    max_tokens: 8192

budgets:
  daily_token_limit: 1000000
  daily_cost_limit: 50.00  # USD
  alert_threshold: 0.80    # Alert at 80% of limits
```
