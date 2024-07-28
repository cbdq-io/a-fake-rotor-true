# Routing Rules

These examples are taken from the tests ran as part of the system tests.

## Messages

### Message 1

```json
{
    "company_name": "John Smith & Associates",
    "family_name": "Smith",
    "given_name": "John"
}
```

### Message 2

```json
{
    "company_name": "John Smith & Associates",
    "country": "WTF",
    "family_name": "Smith",
    "given_name": "John",
    "vat_number": "WTF"
}
```

### Message 3

```json
{
    "company_name": "John Smith & Associates",
    "family_name": "Smith",
    "given_name": "John",
    "vat_number": "GB999 9999 73"
}
```

### Message 4

```json
{
    "company_name": "John Smith & Associates",
    "country": "GB",
    "family_name": "Smith",
    "given_name": "John"
}
```

### Message 5

```json
{
    "company_name": "Seána Murphy & Associates",
    "family_name": "Murphy",
    "given_name": "Seána",
    "vat_number": "IE1234567FA"
}
```

### Message 6

```json
{
    "company_name": "Seána Murphy & Associates",
    "country": "IE",
    "family_name": "Murphy",
    "given_name": "Seána"
}
```

## Rules

Rules are configured as JSON, the format of which must match the schema
provided in `rule-schema.json`.  The fields are:

- destination_topic: Where the message is to be routed to when the rule
  is matched.
- jmespath: A [JMESPath](https://jmespath.org/) expression to query an
  element within the JSON contained in the message.
- regexp: A
  [regular expression](https://en.wikipedia.org/wiki/Regular_expression)
  that will me used to match against the data returned from `jmespath`.
- source_topic: Were the message is to be sourced from to match this
  rule.

Rules are normally provided as minified JSON, for clarity in these examples,
we're showing them as beutified JSON.

### KAFKA_ROUTER_RULE_COUNTRY_IE_VAT_NUMBER

Checks if the VAT number has a prefix of "IE".

```json
```

### KAFKA_ROUTER_RULE_COUNTRY_IS_GB

```json
```

### KAFKA_ROUTER_RULE_COUNTRY_IS_IE

```json
```

### KAFKA_ROUTER_RULE_COUNTRY_UK_VAT_NUMBER

```json
```

