from awsforyou import recommender, report_generator


def aws_foryou(python_call, module_name):
    """
    Wrapper function
    :param python_call: string that calls a python function
    :param module_name: python module in which function resides
    :return: None
    """

    df = recommender.create_dataframe(python_call, module_name)
    report_generator.generate_report(df)
    return None
