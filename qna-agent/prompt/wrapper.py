from jinja2 import Environment, FileSystemLoader, select_autoescape

template_dir = "./prompt/templates"


class PromptWrapper:
    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def assemble(self, template_name, params):
        if not template_name.endswith('txt'):
            template_name += ".txt"
        try:
            template = self.env.get_template(template_name)
        except Exception as e:
            raise FileNotFoundError

        try:
            result = template.render(params)
        except Exception as e:
            raise FileNotFoundError

        return result
