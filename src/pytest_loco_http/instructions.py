"""URL-related DSL instructions for pytest-loco HTTP plugin.

This module provides the `urljoin` instruction, which composes a URL
at runtime by joining a base URL stored in the execution context with
a postfix path defined in YAML.
"""

from typing import TYPE_CHECKING
from urllib.parse import urljoin

import yaml

from pytest_loco.builtins.lookups import VariableLookup
from pytest_loco.errors import DSLRuntimeError, DSLSchemaError
from pytest_loco.extensions import Instruction

if TYPE_CHECKING:
    from pytest_loco.schema import YAMLLoader, YAMLNode
    from pytest_loco.values import Deferred, RuntimeValue, Value


def urljoin_constructor(loader: 'YAMLLoader', node: 'YAMLNode') -> 'Deferred[RuntimeValue]':
    """Create a deferred URL join resolver from YAML node.

    Parses a scalar value and returns a resolver function that
    performs URL composition at runtime.

    Args:
        loader: YAML loader instance.
        node: YAML scalar node containing instruction arguments.

    Returns:
        A resolver that joins the resolved base URL
        with the provided postfix and returns the resulting URL as string.

    Raises:
        DSLSchemaError: If the YAML node cannot be parsed or does not
            match the expected format.
    """
    try:
        path, postfix = loader.construct_scalar(node).split(' ', 1)
        lookup = VariableLookup(path)

    except yaml.MarkedYAMLError as base:
        raise DSLSchemaError.from_yaml_error(base) from base

    except Exception as base:
        raise DSLSchemaError.from_yaml_node('Invalid variable', node) from base

    def resolver(context: dict[str, 'Value']) -> 'RuntimeValue':
        """Wrapper for join path to value."""
        value = lookup(context)
        if not value:
            return None

        try:
            return urljoin(value, postfix)
        except Exception as base:
            raise DSLRuntimeError.from_yaml_node('bad urljoin arguments', node) from base

    return resolver


urljoin_ = Instruction(
    constructor=urljoin_constructor,
    name='urljoin',
)
