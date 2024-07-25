## README

#### Introduction

This guide explains how to use the `opera.py` module to generate a list of transaction codes import scripts for a given resort. This script outputs transaction code groups, subgroups, transaction codes. The output is typically a set of SQL scripts to insert the generated transaction codes into opera database.

The Following script generate transaction code based on Transaction code template defined in [Transaction Code Standard](/docs/docs/Transaction%20Code%20Standard.md) although this can be customized

#### Get Started

```python

import json
from src.opera import generate_tc_script

# Load the JSON payload from a sample payload file
with open("payload.json", 'r') as file:
    data = json.load(file)

# passthe payload data to the opera.generate_tc_script
generate_tc_script(data, "demo/trx_code.json")

```

### Payload Structure

The `Payload` file is structured to include various data elements necessary for generating transaction codes. Below is a breakdown of the key sections:

```json
{
  "Resort": "",
  "setup": {
    "groups": [...],
    "identifiers": [...],
    "categories": [...]
  },
  "sequences": [...]
}
```

#### 1. **Root Level**

- `**resort**`: The name or identifier of the resort or company. This is a string that uniquely identifies the entity for which the transaction codes are being generated.

  ```json
  "resort": "DEMO"
  ```

- **setup**: Contains the primary configuration details, including groups, identifiers, and categories.

#### 2. **Setup Section**

- `**groups**`: A list of transaction groups, each defined by a unique code and a set of options.

  - **code**: Unique identifier for the group.
  - **description**: Descriptive name of the group.
  - **seq**: Sequence number, used for ordering.
  - **options**: Key-value pairs defining specific attributes of the group and depended subgroups and transaction codes. (hierarchy lvl 1)

  ```json
  {
    "code": "ACC",
    "description": "Accommodation",
    "seq": 10,
    "options": {...}
  }
  ```

  > [!NOTE]
  > Sequence No define is the order by for the transaction group

- `**identifiers**`: A list of identifiers used to specify different aspects or types of transactions within groups.

  - **no**: Numeric identifier.
  - **seq**: Sequence number for ordering.
  - **name**: Name of the identifier which will be used for transaction code descriptions
  - **code**: Code representing the identifier.

  ```json
  {
    "no": 1,
    "seq": 1,
    "name": "Breakfast",
    "code": "BF"
  }
  ```

- `**categories**`: Detailed classifications within each group, including their specific options.

  - **code**: Unique code for the category.
  - **description**: Descriptive name of the category.
  - **abbr**: Abbreviation used for the category.
  - **seq**: Sequence number.
  - **defaultGroup**: (Optional) Default group code associated with the category.
  - **options**: Key-value pairs defining specific attributes of the depended transaction codes. (hierarchy lvl 2)

  ```json
  {
    "code": "RV",
    "description": "Revenue",
    "abbr": "",
    "seq": 0,
    "options": {...}
  }
  ```

#### 3. **Sequences Section**

- **sequences**: Defines how transaction codes are generated, including group associations and itemizers.

  - **sequence**: Numeric sequence for ordering.
  - **name**: Name of the sequence.
  - **prefix**: Boolean indicating if a prefix is used.
  - **group**: The associated group code.
  - **identifiers**: Identifiers associated with the sequence.
  - **categories**:
    - **code**: Categories linked with the sequence
    - **role**: specifying their role (e.g., "generate", "multiply", "others").
      - **generate**: a single transaction code will be created and attached to mutliplier type as generate.
      - **multiply**: itemizers will be mutliplied by this category.
      - **others**: a single transaction code will be created for this category.
  - **itemizers**: Specific items within the category, including their descriptions and options.
    - **itemizer**: Itemizer number which will be reflexted as the last two digit of the transcansaction code,
    - **description**: Itemizer description which will be reflexted on transcansaction code description,
    - **options**: Key-value pairs defining specific attributes of the depended transaction codes. (hierarchy lvl 3)

  ```json
  {
    "sequence": 10,
    "name": "Accommodation",
    "prefix": true,
    "group": "ACC",
    "identifiers": [0],
    "categories": [
      { "code": "SC", "role": "generate" },
      { "code": "TX", "role": "generate" },
      { "code": "RV", "role": "multiply" }
    ],
    "itemizers": [
      { "itemizer": 0, "description": "Revenue", "options":{...} },
      { "itemizer": 1, "description": "Room Upgrade", "options":{...} }
    ]
  }
  ```

  > [!IMPORTANT]
  > generate need to be define first before any thing else, and also in order of the generate eg: SVC first than GST

#### Full Option List

Each transaction code model generated will utilize the following options:

```json
{
  "trx_code_type": "FC",
  "tax_code_no": null,
  "tax_inclusive_yn": "N",
  "result_included_in_sum_array": null,
  "cc_type": null,
  "cc_code": null,
  "ind_cash": "N",
  "is_manual_post_allowed": "N",
  "trx_code_display": null,
  "ind_billing": "N",
  "ind_ar": "N",
  "ind_revenue_gp": "N",
  "ind_deposit_yn": "N",
  "inh_deposit_yn": "N",
  "include_in_deposit_rule_yn": "N",
  "adj_trx_code": null
}
```

> Options are defined based on the hierarchy where lvl 1 is weakers and lvl 3 is strongest

These options represent various attributes of a transaction code, such as its type, whether it is cash-based, whether it is included in revenue or billing, and tax-related settings. the option name is same as the transaction code table colomn name so its pretty much the same.
