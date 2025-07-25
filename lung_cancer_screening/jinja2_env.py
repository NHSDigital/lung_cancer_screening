from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse
from jinja2 import ChoiceLoader, Environment, PackageLoader


def environment(**options):

    env = Environment(**options, extensions=["jinja2.ext.do"])
    if env.loader:
        env.loader = ChoiceLoader(
            [
                env.loader,
                PackageLoader(
                    "nhsuk_frontend_jinja",
                    package_path="templates/components"
                ),
                PackageLoader(
                    "nhsuk_frontend_jinja",
                    package_path="templates/macros"
                ),
                PackageLoader("nhsuk_frontend_jinja"),
            ]
        )

    env.globals.update(
        {"static": static, "url": reverse, "STATIC_URL": settings.STATIC_URL}
    )

    return env
