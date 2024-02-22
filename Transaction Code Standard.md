# Universal Resorts Opera PMS Transaction Code Standardization

`PROPOSAL-01`

## Overview

This document outlines the new standardized transaction code configuration for Opera Property Management System (PMS) to be adopted across all Universal Resorts properties. The system is composed of three fundamental components:

- **Transaction Group Codes**: Alpha-numeric codes signifying broad categories such as accommodation or food and beverage services.
- **Transaction Subgroups**: More granular categorizations within the primary transaction groups.
- **Transaction Codes Setup**: Detailed code configurations that capture specific transaction information like outlet number, meal plan, and itemizers.

The standardization initiative aims to enhance clarity, efficiency, and consistency in our PMS operations.

## Transaction Group Codes

### Alpha Codes: `AAA`

A three-letter alpha code is utilized for each transaction category, offering both intuitive identification and scalability.

#### Sequencing and Numbering:

- `10` = Accommodation
- `20` = Food and Beverage
- `30` = MOD
- `40` = (Unassigned)
- `50` = Other / Transportation
- `60` = (Unassigned)
- `70` = Service Charge
- `80` = Tax
- `90` = Payment

### Example Codes:

- `ACC` for Accommodation
- `FNB` for Food & Beverate Revenue
- `DIV` for Dive Center
- `RET` for Retail
- `TRF` for Transportation

#### Optional Improvement:

Separate the Food and Beverage category into distinct groups to facilitate easier user selection and analysis.

- `FFD` for Food Revenue
- `FBV` for Beverage Revenue

> [!IMPORTANT]
> PKG Group code is removed to create a more stream line catogoriztion.

---

## Transaction Subgroups

### Numeric & Alpha Codes: `00AA`

The subgroups should ideally reflect the sequence number or range of the transaction code, along with a distinguishing character for the relevant outlet or category.

#### Subgroup Options:

- `RV` = Revenue Codes
- `NR` = Non-Revenue
- `RB` = Rebate Codes (Optional)
- `DC` = Discounts (Optional)
- `SC` = Service
- `GT` = Green Tax
- `TX` = Tax
- `TP` = Tips
- `CA` = Cash
- `CL` = City Ledger
- `CC` = Credit Card

### Examples:

- `10RV` for Accommodation Revenue
- `10RB` for Accommodation Rebate
- `20RV` for The Restaurant Revenue
- `20RB` for The Restaurant Rebate
- `90CA` for Payment Cash
- `90CL` for Payment Direct Payment
- `91CC` for Payment Credit Card

#### Optional Improvement:

Introduction of customized grouping codes for different revenue streams:

- `RM` for Room Revenue
- `FD` for Food Revenue
- `FB` for Beverage Revenue
- `OR` for Other Revenue
- `NR` for Non-Revenue (Optional)

This method allows tailored grouping of revenue codes beyond the built-in categories, potentially omitting the need for `RB` codes.

## Transaction Codes Setup

### Detailed 5-Digit Codes: `00000`

Each five-digit code provides a precise picture of the transaction details, organized systematically to prevent overlaps and ensure clarity.

1. Group Classification
2. Outlet Number
3. Serving Period
4. Itemizer Number
5. Detailed Classification (such as Rebate, Discount, Service Charge, GST, Tips)

### Examples:

- `21101` for The Restaurant Breakfast Food
- `21121` for The Restaurant Breakfast Food Rebate or The Restaurant Breakfast Food [R]
- `21141` for The Restaurant Breakfast Food Discount or The Restaurant Breakfast Food [D]
- `21170` for The Restaurant Breakfast Service Charge
- `21180` for The Restaurant Breakfast GST

The above structure and examples offer a glimpse into our evolved transaction coding process, creating a refined and scalable model for all our property management operations.

---

This document is intended for immediate implementation across all Universal Resorts properties. Training sessions and additional resources will be provided to ensure a smooth transition to the new system. Any questions or suggestions for further refinement are welcome and should be directed to the PMS System Coordinator.

Prepared by: [Mohamed Shaif Hassan]  
Position: [Product Manager]  
Date: [22nd February 2024]

For further assistance, please contact [Contact Information].
