### README: Generating Transaction Code List from Payload.json

#### Introduction

This guide explains how to use the `Payload.json` file to generate a list of transaction codes for a given resort or company. The transaction codes are generated based on specific groups, subgroups, categories, and identifiers defined in the payload. The output is typically a set of SQL scripts to insert the generated transaction codes into a database.

#### Payload Structure

The `Payload.json` file is structured to include various data elements necessary for generating transaction codes. Below is a breakdown of the key sections:

1. **Resort**: Identifies the resort or company for which the transaction codes are being generated.

2. **Options**:

   - **Groups**: Defines the major categories (groups) of transactions, each with a unique code and description.
   - **Identifiers**: Specific identifiers used to differentiate transactions within the same group.
   - **Categories**: Further classification of transactions within groups, with options for itemization and tax settings.

3. **Sequences**: Details how transaction codes are to be generated, specifying the order and structure of groups and categories.

#### Example Structure

```json
{
  "Resort": "DEMO",
  "options": {
    "groups": [...],
    "identifiers": [...],
    "categories": [...]
  },
  "sequences": [...]
}
```

#### Full Option List

Each transaction code model generated will utilize the following options:

```json
{
  "trx_code": null,
  "description": null,
  "tc_subgroup": null,
  "tc_group": null,
  "tc_transaction_type": null,
  "trx_code_type": null,
  "tax_code_no": null,
  "tax_inclusive_yn": null,
  "result_included_in_sum_array": null,
  "cc_type": null,
  "cc_code": null,
  "ind_cash": null,
  "is_manual_post_allowed": null,
  "ind_billing": null,
  "ind_ar": null,
  "ind_revenue_gp": null,
  "ind_deposit_yn": null,
  "inh_deposit_yn": null,
  "adj_trx_code": null
}
```

These options represent various attributes of a transaction code, such as its type, whether it is cash-based, whether it is included in revenue or billing, and tax-related settings.

#### Option Layout

```json
{
  "Resort": "DEMO",
  "options": {
    "groups": ["options":{ }, ...],
    "identifiers": [...],
    "categories": ["options":{ }, ...]
  },
  "sequences": [...]
}
```

#### Steps to Generate Transaction Codes

1. **Preparation**:

   - Ensure the `Payload.json` file is correctly formatted and includes all necessary groups, identifiers, categories, and sequences.

2. **Loading Data**:

   - Parse the `Payload.json` file to extract data into the application. This involves loading groups, identifiers, categories, and sequences into appropriate data structures.

3. **Generating Transaction Codes**:

   - Use the data to create transaction codes. This typically involves combining group codes, identifiers, and categories according to the rules defined in the sequences section.

4. **Exporting SQL Scripts**:

   - The generated transaction codes are then formatted into SQL insert statements. This can include additional options or settings from the full option list.

5. **Review and Execution**:
   - Review the generated SQL scripts for accuracy and completeness.
   - Execute the SQL scripts to insert the transaction codes into the database.

#### Example Usage

The following Python function provides a basic structure for generating transaction codes:

```python
def generate_transaction_codes(payload_path):
    with open(payload_path, 'r') as file:
        data = json.load(file)

    resort = data["resort"]
    groups = {group["code"]: group for group in data["options"]["groups"]}
    identifiers = {identifier["no"]: identifier for identifier in data["options"]["identifiers"]}
    categories = {category["code"]: category for category in data["options"]["categories"]}
    sequences = data["sequences"]

    # Further processing to generate transaction codes
    # ...
```

#### Conclusion

This README provides a high-level overview of the process and structures involved in generating transaction codes from a `Payload.json` file. It is essential to tailor the implementation details to the specific requirements and data structures of your application. Always validate the generated codes and SQL scripts to ensure they meet your operational and data integrity standards.

### README: Modifier Options in Payload.json

#### Introduction

This document provides detailed information on how to use the `Payload.json` file to generate transaction codes. Specifically, it outlines the hierarchy and options available at different levels: **Itemizers**, **Categories**, and **Groups**. These levels are used to customize and configure transaction codes for a resort or organization.

#### Hierarchical Structure

The `Payload.json` is organized hierarchically into Groups, Categories, and Itemizers, each level allowing for specific options that can modify the behavior and attributes of transaction codes.

1. **Groups**: The top-level classification, defining broad categories of transactions.
2. **Categories**: Nested within Groups, providing more specific classifications and attributes.
3. **Itemizers**: The most granular level, specifying particular items within a category.

### Options Overview

Below is a breakdown of the available options at each hierarchical level.

#### 1. Group Options

Groups are defined under the `groups` key in `Payload.json`. Each group can have the following options:

- **tc_transaction_type**: Defines the type of transaction (e.g., "C" for charge, "FC" for financial charge).
- **trx_code_type**: Specifies the code type (e.g., "L" for ledger, "F" for food).
- **tax_code_no**: Associates a specific tax code number with the group.
- **tax_inclusive_yn**: Indicates whether the transaction is tax inclusive ("Y" for yes, "N" for no).
- **result_included_in_sum_array**: Controls inclusion in sum arrays (e.g., "111").
- **ind_revenue_gp**: Indicates if the group is part of the revenue group ("Y" or "N").
- **include_in_deposit_rule_yn**: Specifies inclusion in deposit rules ("Y" or "N").

**Example**:

```json
{
  "code": "ACC",
  "description": "Accommodation",
  "seq": 10,
  "options": {
    "tc_transaction_type": "C",
    "trx_code_type": "L",
    "tax_inclusive_yn": "N",
    "result_included_in_sum_array": "111",
    "ind_revenue_gp": "Y",
    "include_in_deposit_rule_yn": "Y"
  }
}
```

#### 2. Category Options

Categories are defined under the `categories` key and provide specific attributes for transaction codes within a group. Options include:

- **is_manual_post_allowed**: Determines if manual posting is allowed ("Y" or "N").
- **ind_revenue_gp**: Indicates revenue group inclusion ("Y" or "N").
- **percentage**: Specifies the percentage value for calculations (if applicable).
- **percentage_base_code**: Defines the base code for percentage calculations.
- **calculation_sequence**: The sequence order for applying calculations.
- **tax_code_no**: Specifies a tax code number (used in tax-related categories).

**Example**:

```json
{
  "code": "RV",
  "description": "Revenue",
  "seq": 0,
  "options": {
    "is_manual_post_allowed": "N",
    "ind_revenue_gp": "Y"
  },
  "itemized": true
}
```

#### 3. Itemizer Options

Itemizers are the most detailed level, specifying individual items within a category. They are defined under `itemizers` and can include:

- **ccType**: Credit card type (e.g., "M" for MasterCard).
- **ccCode**: Code associated with the credit card type.
- **isPaid**: Indicates if the itemizer is paid ("Y" or "N").

**Example**:

```json
{
  "itemizer": 1,
  "description": "Visa Card",
  "options": { "ccType": "M", "ccCode": "VA" }
}
```

### Usage Instructions

To generate transaction codes using the `Payload.json`:

1. **Load Data**: Parse the `Payload.json` file to extract groups, categories, and itemizers.
2. **Apply Options**: Use the extracted options to modify the attributes and behavior of transaction codes at each level.
3. **Generate Codes**: Create transaction codes using the hierarchical data, ensuring that options are correctly applied to reflect the desired configurations.
4. **Export**: Output the generated transaction codes into SQL scripts or other formats for use in your database or system.

### Conclusion

The hierarchical structure and options provided in the `Payload.json` file offer a flexible and detailed method for configuring transaction codes. By understanding and utilizing these options, you can tailor transaction behavior and attributes to meet specific business requirements.
