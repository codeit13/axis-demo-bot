"""Robust JSON extraction utility for parsing AI agent responses."""
import json
import re
from typing import Dict, Any, Optional, List, Union
import yaml


def extract_json_from_text(
    text: str,
    fallback_to_text: bool = True,
    allow_multiple: bool = False,
    preferred_keys: Optional[List[str]] = None
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
        preferred_keys: List of keys that should be present in the JSON (helps select the right object)
        
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
    
    # Strategy 1: Extract from markdown code blocks (```json ... ``` or ```yaml ... ```)
    # Note: Sometimes YAML is wrapped in ```json blocks, so we need to check both
    json_block_pattern = r'```(?:json|yaml|yml)?\s*\n?(.*?)```'
    matches = re.findall(json_block_pattern, text, re.DOTALL | re.IGNORECASE)
    for match in matches:
        content_str = match.strip()
        
        # First try as JSON
        result = _try_parse_json(content_str)
        if result is not None:
            # If preferred_keys are specified, check if this object has them
            if preferred_keys and _has_preferred_keys(result, preferred_keys):
                if not allow_multiple:
                    return result
                found_objects.insert(0, result)  # Insert at beginning (higher priority)
            else:
                if not allow_multiple and not preferred_keys:
                    return result
                found_objects.append(result)
        else:
            # If JSON parsing failed, try as YAML (common for OpenAPI specs)
            # Check if it looks like YAML (starts with key: or has YAML-like structure)
            if _looks_like_yaml(content_str):
                try:
                    yaml_data = yaml.safe_load(content_str)
                    if isinstance(yaml_data, dict):
                        result = yaml_data
                        if preferred_keys and _has_preferred_keys(result, preferred_keys):
                            if not allow_multiple:
                                return result
                            found_objects.insert(0, result)
                        else:
                            if not allow_multiple and not preferred_keys:
                                return result
                            found_objects.append(result)
                except (yaml.YAMLError, Exception):
                    pass
    
    # Strategy 2: Extract from generic code blocks (``` ... ```)
    # Also handle YAML that might be in code blocks
    if not found_objects:
        code_block_pattern = r'```[^\n]*\n?(.*?)```'
        matches = re.findall(code_block_pattern, text, re.DOTALL)
        for match in matches:
            content_str = match.strip()
            
            # Try JSON first
            if _looks_like_json(content_str):
                result = _try_parse_json(content_str)
                if result is not None:
                    if not allow_multiple:
                        return result
                    found_objects.append(result)
                    continue
            
            # If JSON parsing failed or doesn't look like JSON, try YAML
            if _looks_like_yaml(content_str):
                try:
                    yaml_data = yaml.safe_load(content_str)
                    if isinstance(yaml_data, dict):
                        result = yaml_data
                        if preferred_keys and _has_preferred_keys(result, preferred_keys):
                            if not allow_multiple:
                                return result
                            found_objects.insert(0, result)
                        else:
                            if not allow_multiple and not preferred_keys:
                                return result
                            found_objects.append(result)
                except (yaml.YAMLError, Exception):
                    pass
    
    # Strategy 3: Find JSON object boundaries in plain text (prefer larger/complete objects)
    if not found_objects:
        # Look for JSON object patterns: { ... }
        # Use a more sophisticated approach to find complete JSON objects
        json_objects = []
        brace_count = 0
        start_pos = -1
        
        for i, char in enumerate(text):
            if char == '{':
                if brace_count == 0:
                    start_pos = i
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0 and start_pos != -1:
                    json_candidate = text[start_pos:i+1]
                    result = _try_parse_json(json_candidate)
                    if result is not None:
                        json_objects.append((len(json_candidate), result))
                    start_pos = -1
        
        # Sort by length (prefer larger objects) and try them
        json_objects.sort(key=lambda x: x[0], reverse=True)
        for _, result in json_objects:
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
    
    # Return results - prefer objects with preferred_keys
    if found_objects:
        if allow_multiple:
            return found_objects
        
        # If preferred_keys specified, find the best match
        if preferred_keys:
            for obj in found_objects:
                if _has_preferred_keys(obj, preferred_keys):
                    return obj
        
        # Return the first (or most preferred) object
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


def _has_preferred_keys(obj: Dict[str, Any], preferred_keys: List[str]) -> bool:
    """
    Check if object has any of the preferred keys.
    
    Args:
        obj: Dictionary to check
        preferred_keys: List of keys to look for
        
    Returns:
        True if object has at least one preferred key
    """
    if not isinstance(obj, dict) or not preferred_keys:
        return False
    return any(key in obj for key in preferred_keys)


def _looks_like_yaml(text: str) -> bool:
    """
    Check if text looks like YAML.
    
    Args:
        text: Text to check
        
    Returns:
        True if text looks like YAML
    """
    if not text:
        return False
    
    text = text.strip()
    
    # YAML indicators:
    # - Starts with key: value pattern
    # - Has openapi: or info: at the start
    # - Has --- at the start
    # - Has indentation-based structure (lines starting with spaces followed by key:)
    if text.startswith('---'):
        return True
    
    if 'openapi:' in text.lower()[:100]:  # Check first 100 chars
        return True
    
    # Check for YAML key: value pattern (not JSON "key": value)
    yaml_pattern = r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*:\s*'
    lines = text.split('\n')[:5]  # Check first 5 lines
    yaml_lines = sum(1 for line in lines if re.match(yaml_pattern, line))
    if yaml_lines >= 2:  # At least 2 lines look like YAML
        return True
    
    return False


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
