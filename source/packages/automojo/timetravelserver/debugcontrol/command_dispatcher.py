import json
import socket
from typing import Any, Dict, Optional


class CommandError(Exception):
    """Raised when a remote command returns an error status."""
    pass


class CommandTimeoutError(Exception):
    """Raised when a command times out."""
    pass


class CommandDispatcher:
    def __init__(self, credential_token: str, timeout_seconds: float = 10.0):
        self.credential_token = credential_token
        self.timeout_seconds = timeout_seconds

    def dispatch(self, remote_address: str, command: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send a command and return the response dict."""
        if params is None:
            params = {}

        try:
            host, port_str = remote_address.split(":")
            port = int(port_str)
        except ValueError:
            raise ValueError(f"Invalid remote address format: {remote_address}. Expected 'host:port'.")

        request = {
            "command": command,
            "params": params,
            "token": self.credential_token,
        }

        request_json = json.dumps(request) + "\n"

        try:
            with socket.create_connection((host, port), timeout=self.timeout_seconds) as sock:
                # Wrap socket in makefile for line-based I/O
                with sock.makefile("rw", encoding="utf-8") as f:
                    # Write request
                    f.write(request_json)
                    f.flush()

                    # Read response
                    response_json = f.readline()

                    if not response_json:
                        raise CommandError("Connection closed without response.")

                    try:
                        response = json.loads(response_json)
                    except json.JSONDecodeError as e:
                        raise CommandError(f"Invalid JSON response: {e}")

                    if response.get("status") == "error":
                        raise CommandError(response.get("message", "Unknown remote error"))

                    if response.get("status") != "ok":
                        raise CommandError(f"Unexpected response status: {response.get('status')}")

                    return response.get("data", {})

        except socket.timeout:
            raise CommandTimeoutError(f"Command '{command}' to {remote_address} timed out.")
        except ConnectionRefusedError:
            raise ConnectionError(f"Connection to {remote_address} refused.")
        except Exception as e:
            if isinstance(e, (CommandError, CommandTimeoutError, ConnectionError, ValueError)):
                raise e
            raise CommandError(f"Error during command dispatch: {e}")

    def close(self) -> None:
        """Close any pooled connections."""
        # Currently no connection pooling is implemented.
        pass
