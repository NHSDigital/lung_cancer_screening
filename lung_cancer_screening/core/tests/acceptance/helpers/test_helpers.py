def check_labels(page, answers):
    if answers is None:
        return

    if isinstance(answers, str):
        page.get_by_label(answers, exact=True).check()
        return

    if isinstance(answers, list, tuple):
        for answer in answers:
            page.get_by_label(answer, exact=True).check()
        return

    raise TypeError("answers must be a string, list, or tuple")

