"""Robust JSON extraction utility for parsing AI agent responses."""
import json
import re
from typing import Dict, Any, Optional, List, Union
import yaml


def extract_json_from_text(
    text: str,
    fallback_to_text: bool = True,
    allow_multiple: bool = False
) -> Union[Dict[str, Any], List[Dict[str, Any]], str]:
    """
    Extract JSON from text using multiple strategies.
    
    This function tries various methods to extract valid JSON from text that might:
    - Be wrapped in markdown code blocks (```json ... ```)
    - Have extra text before/after the JSON
    - Be escaped as a string
    - Be in YAML format
    - Have trailing commas or other minor issues
    
    Args:
        text: The text to extract JSON from
        fallback_to_text: If True, return the original text if JSON extraction fails
        allow_multiple: If True, return a list of all JSON objects found
        
    Returns:
        Extracted JSON as dict/list, or original text if extraction fails and fallback_to_text is True
    """
    if not text or not isinstance(text, str):
        if fallback_to_text:
            return text if isinstance(text, str) else {}
        return {}
    
    text = text.strip()
    if not text:
        return {} if not fallback_to_text else text
    
    found_objects = []
    
    # Strategy 1: Extract from markdown code blocks (```json ... ```)
    json_block_pattern = r'```(?:json)?\s*\n?(.*?)```'
    matches = re.findall(json_block_pattern, text, re.DOTALL | re.IGNORECASE)
    for match in matches:
        json_str = match.strip()
        result = _try_parse_json(json_str)
        if result is not None:
            if not allow_multiple:
                return result
            found_objects.append(result)
    
    # Strategy 2: Extract from generic code blocks (``` ... ```)
    if not found_objects:
        code_block_pattern = r'```[^\n]*\n?(.*?)```'
        matches = re.findall(code_block_pattern, text, re.DOTALL)
        for match in matches:
            json_str = match.strip()
            # Skip if it's clearly not JSON (e.g., Python code, YAML without JSON structure)
            if not _looks_like_json(json_str):
                continue
            result = _try_parse_json(json_str)
            if result is not None:
                if not allow_multiple:
                    return result
                found_objects.append(result)
    
    # Strategy 3: Find JSON object boundaries in plain text
    if not found_objects:
        # Look for JSON object patterns: { ... }
        json_object_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_object_pattern, text, re.DOTALL)
        for match in matches:
            result = _try_parse_json(match)
            if result is not None:
                if not allow_multiple:
                    return result
                found_objects.append(result)
    
    # Strategy 4: Try parsing the entire text as JSON
    if not found_objects:
        result = _try_parse_json(text)
        if result is not None:
            if not allow_multiple:
                return result
            found_objects.append(result)
    
    # Strategy 5: Try to extract JSON from YAML format
    if not found_objects:
        # Check if it looks like YAML
        if 'openapi:' in text.lower() or text.strip().startswith('---'):
            try:
                yaml_data = yaml.safe_load(text)
                if isinstance(yaml_data, dict):
                    if not allow_multiple:
                        return yaml_data
                    found_objects.append(yaml_data)
            except (yaml.YAMLError, Exception):
                pass
    
    # Strategy 6: Try to find JSON in escaped string format
    if not found_objects:
        # Look for escaped JSON strings like "{\"key\": \"value\"}"
        escaped_json_pattern = r'"[^"]*\{[^"]*\}[^"]*"'
        matches = re.findall(escaped_json_pattern, text)
        for match in matches:
            try:
                # Unescape the string
                unescaped = json.loads(match)
                if isinstance(unescaped, str):
                    result = _try_parse_json(unescaped)
                    if result is not None:
                        if not allow_multiple:
                            return result
                        found_objects.append(result)
            except (json.JSONDecodeError, Exception):
                pass
    
    # Strategy 7: Try to fix common JSON issues and parse
    if not found_objects:
        # Remove trailing commas
        fixed_text = re.sub(r',(\s*[}\]])', r'\1', text)
        result = _try_parse_json(fixed_text)
        if result is not None:
            if not allow_multiple:
                return result
            found_objects.append(result)
    
    # Strategy 8: Extract JSON from text with extra content
    if not found_objects:
        # Find the first { and last } in the text
        first_brace = text.find('{')
        last_brace = text.rfind('}')
        if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
            json_candidate = text[first_brace:last_brace + 1]
            result = _try_parse_json(json_candidate)
            if result is not None:
                if not allow_multiple:
                    return result
                found_objects.append(result)
    
    # Return results
    if found_objects:
        if allow_multiple:
            return found_objects
        return found_objects[0]
    
    # Fallback: return original text or empty dict
    if fallback_to_text:
        return text
    return {}


def _try_parse_json(text: str) -> Optional[Dict[str, Any]]:
    """
    Try to parse text as JSON with error handling.
    
    Args:
        text: Text to parse
        
    Returns:
        Parsed JSON dict or None if parsing fails
    """
    if not text or not isinstance(text, str):
        return None
    
    text = text.strip()
    if not text:
        return None
    
    # Remove BOM if present
    if text.startswith('\ufeff'):
        text = text[1:]
    
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
        elif isinstance(parsed, list) and len(parsed) > 0 and isinstance(parsed[0], dict):
            # If it's a list of objects, return the first one
            return parsed[0]
    except json.JSONDecodeError:
        pass
    
    return None


def _looks_like_json(text: str) -> bool:
    """
    Check if text looks like it might be JSON.
    
    Args:
        text: Text to check
        
    Returns:
        True if text looks like JSON
    """
    if not text:
        return False
    
    text = text.strip()
    
    # Must start with { or [
    if not (text.startswith('{') or text.startswith('[')):
        return False
    
    # Must have matching braces/brackets
    open_braces = text.count('{')
    close_braces = text.count('}')
    open_brackets = text.count('[')
    close_brackets = text.count(']')
    
    if open_braces != close_braces or open_brackets != close_brackets:
        return False
    
    # Should have some JSON-like structure
    if ':' not in text and '"' not in text:
        return False
    
    return True


def extract_yaml_from_text(text: str) -> Optional[Dict[str, Any]]:
    """
    Extract YAML from text and convert to dict.
    
    Args:
        text: Text that might contain YAML
        
    Returns:
        Parsed YAML as dict or None
    """
    if not text:
        return None
    
    try:
        # Try to extract YAML from code blocks
        yaml_block_pattern = r'```(?:yaml|yml)?\s*\n?(.*?)```'
        matches = re.findall(yaml_block_pattern, text, re.DOTALL | re.IGNORECASE)
        for match in matches:
            try:
                yaml_data = yaml.safe_load(match.strip())
                if isinstance(yaml_data, dict):
                    return yaml_data
            except (yaml.YAMLError, Exception):
                continue
        
        # Try parsing the entire text as YAML
        yaml_data = yaml.safe_load(text)
        if isinstance(yaml_data, dict):
            return yaml_data
    except (yaml.YAMLError, Exception):
        pass
    
    return None
