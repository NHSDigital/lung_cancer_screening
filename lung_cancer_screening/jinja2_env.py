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

    return env
