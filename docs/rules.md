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

### Message 7

```
Hello, world!
```


### Message 8

```json
{
    "company_name": "Seána Murphy & Associates",
    "country": "FR",
    "family_name": "Murphy",
    "given_name": "Seána"
}
```

## Rules

Rules are configured as JSON, the format of which must match the schema
provided in `rule-schema.json`.  The fields are:

- destination_topic: Where the message is to be routed to when the rule
  is matched.  If this is blank ("") then messages that match the rule
  will be considered valid, not be produced onto the DLQ, but will be
  dropped.  The consumer will be committed.
- header: The name of a header to match against.  If provided, header_regexp
  header_regexp is required.
- header_regexp:  The regular expression to match against the value
  in the header.  If provided, header is required.
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
{
    "destination_topic": "IE.output",
    "jmespath": "vat_number",
    "regexp": "^IE",
    "source_topic": "input"
}
```

### KAFKA_ROUTER_RULE_COUNTRY_IS_GB

```json
{
    "destination_topic": "GB.output",
    "jmespath": "country",
    "regexp": "^GB$",
    "source_topic": "input"
}
```

### KAFKA_ROUTER_RULE_COUNTRY_IS_IE

```json
{
    "destination_topic": "IE.output",
    "jmespath": "country",
    "regexp": "^IE$",
    "source_topic": "input"
}
```

### KAFKA_ROUTER_RULE_COUNTRY_UK_VAT_NUMBER

```json
{
    "destination_topic": "GB.output",
    "jmespath": "vat_number",
    "regexp": "^GB",
    "source_topic": "input"
}
```

### KAFKA_ROUTER_RULE_COUNTRY_IS_FR

```json
{
    "destination_topic": "",
    "jmespath": "country",
    "regexp": "^FR$",
    "source_topic": "input.json"
}
```

## Outcomes

In these examples, the DLQ topic has been set to `input.dlq`.

| Message # | Destination Topic | Description                                                                                            |
| --------- | ----------------- | ------------------------------------------------------------------------------------------------------ |
| 1         | input.dlq         | No country code or VAT number provided.                                                                |
| 2         | input.dlq         | Country and VAT number provided, but neither match GB or IE.                                           |
| 3         | GB.output         | The VAT number has a prefix of GB.                                                                     |
| 4         | GB.output         | The country code is GB.                                                                                |
| 5         | IE.output         | The VAT/CBL number has a prefix of IE.                                                                 |
| 6         | IE.output         | The country code is IE.                                                                                |
| 7         | input.dlq         | Unable to parse JSON.                                                                                  |
| 8         | ""                | A rule matched the topic, so not a DLQ matter, but drop the message as the destination topic is blank. |
