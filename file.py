
with open("query.sql","w") as file:
    file.write("SET DEFINE OFF;\n")
    for tc_group in TC_GROUPS.values():
        query = f"Insert into TC$_GROUPS (RESORT,IND_REVENUE_GP,TC_GROUP,DESCRIPTION,TC_TRANSACTION_TYPE,CLASS_1_MANDATORY_YN,CLASS_2_MANDATORY_YN,INSERT_USER,INSERT_DATE,UPDATE_USER,UPDATE_DATE,ORDER_BY) values ('{RESORT}','{tc_group["isRevenue"]}','{tc_group["code"]}','{tc_group["description"]}','{tc_group["type"]}','N','N',2,SYSDATE,2,SYSDATE,{tc_group["seq"]});\n"
        file.write(query)


    for tc_subgroup in TC_SUBGROUPS:
        query = f"Insert into TC$_SUBGROUPS (RESORT,TC_GROUP,TC_SUBGROUP,DESCRIPTION,TC_TRANSACTION_TYPE,CLASS_1_MANDATORY_YN,CLASS_2_MANDATORY_YN,RESULT_INCLUDED_IN_SUM_ARRAY,INSERT_USER,INSERT_DATE,UPDATE_USER,UPDATE_DATE,IND_REVENUE_GP,TAX_YN,SUB_GP_TYPE,INTERNAL_YN,ORDER_BY,GP_POINTS_REDEMPTION_YN,FREQUENT_FLYER_YN) values ('{RESORT}','{tc_subgroup["group"]}','{tc_subgroup["code"]}','{tc_subgroup["description"]}','{tc_subgroup["type"]}',null,null,null,2,SYSDATE,2,SYSDATE,null,'N',null,null,{tc_subgroup["seq"]},'N','N');\n"
        file.write(query)

    for tc_code in TC_CODES:
        query = f"""Insert into TRX$_CODES (RESORT,TC_GROUP,TC_SUBGROUP,TRX_CODE,TCL_CODE_DFLT_CL1,TCL_CODE_DFLT_CL2,CLASS_1_MANDATORY_YN,CLASS_2_MANDATORY_YN,DESCRIPTION,TC_TRANSACTION_TYPE,IS_MANUAL_POST_ALLOWED,RESULT_INCLUDED_IN_SUM_ARRAY,INSERT_USER,INSERT_DATE,UPDATE_USER,UPDATE_DATE,CC_TYPE,COMMISSION,CC_CODE,CURRENCY,IND_BILLING,IND_AR,IND_REVENUE_GP,ADJ_TRX_CODE,IND_CASH,ARRANGE_CODE,EXPENSE_FOLIO,GROUP_FOLIO,DEFERRED_YN,IND_DEPOSIT_YN,REV_GP_ID,REV_BUCKET_ID,AR_NAME_ID,TRX_CODE_TYPE,FREQUENT_FLYER_YN,TAX_INCLUSIVE_YN,CRS_TAX_DESC,TAX_CODE_NO,EXPORT_BUCKET,INH_SALES_YN,INH_PAY_YN,INH_DEPOSIT_YN,FISCAL_TRX_CODE_TYPE,COMP_YN,DEFAULT_PRICE,INACTIVE_DATE,PAYMENT_TAX_INVOICE_YN,INTERNAL_YN,FISCAL_PAYMENT_YN,COMP_NIGHTS_YN,ROTATION_REV_YN,OWNER_REV_YN,CHECK_NO_MANDATORY_YN,DED_OWNER_REV_YN,NON_TAXABLE_YN,COMP_PAYMENT_YN,MIN_AMT,MAX_AMT,TRX_SERVICE_TYPE,DAILY_PLAN_FOLIO,TRX_CODE_DISPLAY,INCLUDE_IN_DEPOSIT_RULE_YN,INCLUDE_IN_8300_YN,MANUAL_POST_COVERS_YN,ROUND_FACTOR_YN,DEPOSIT_POSTING_ONLY_YN,TRX_TAX_TYPE_CODE,DEPOSIT_TYPE,GP_POINTS_REDEMPTION_YN,EXTERNAL_PAYMENT_CODE) values ('{RESORT}','{tc_code["group"]}','{tc_code["subGroup"]}','{tc_code["code"]}',null,null,null,null,'{tc_code["description"]}','{tc_code["trxType"]}','{tc_code["isManual"]}',null,2,SYSDATE,2,SYSDATE,null,0,null,null,'{tc_code["isCash"]}','{tc_code["isAr"]}','{tc_code["isRevenue"]}',null,'{tc_code["isPaid"]}',null,null,null,'N','{tc_code["isDeposit"]}',null,null,null,'{tc_code["type"]}','N','N',null,'{tc_code["tc_code_no"]}',null,'N','N','N',null,'N',null,null,'N',null,'N','N',null,null,'N',null,'N','N',null,null,null,null,null,'N',null,null,'N',null,null,null,'N',null);\n"""
        file.write(query)

        if tc_code["generates"]:
            for gen in tc_code["generates"]:
                query = f"Insert into TRX_CLASS_RELATIONSHIPS (ID,RESORT,TC_GROUP,TC_SUBGROUP,TRX_CODE,TC_GROUP_GENERATOR,TC_SUBGROUP_GENERATOR,TRX_CODE_GENERATOR,TCL_CODE_GENERATOR,TCR_TYPE,AMOUNT,PERCENTAGE,PERCENTAGE_BASE_CODE,UDF_FUNCTION,CALCULATION_SEQUENCE,AMOUNT_FROM_SCHEDULE_YN,CURRENCY,RESULT_INCLUDED_IN_SUM_ARRAY,GENERATED_PRINTED_ON_FOLIO_YN,NAME_TAX_TYPE,UDF_INVERSE,STOP_DAYS,ADJUSTMENT_TYPE,USE_TAX_BRACKET_YN,INSERT_USER,INSERT_DATE,UPDATE_USER,UPDATE_DATE) values (TRX_CLASS_RELATIONSHIP_ID.nextval,'{RESORT}','{gen["group"]}','{gen["subGroup"]}','{gen["code"]}','{tc_code["group"]}','{tc_code["subGroup"]}','{tc_code["code"]}',null,'A',null,{gen["percent"]},{gen["base"]},null,{gen["no"]},'N',null,'{gen["addTo"]}',null,null,null,null,'N','N',2,SYSDATE,2,SYSDATE);\n"
                file.write(query)

    file.write("/")